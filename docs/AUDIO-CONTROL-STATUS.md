# Audio control and targeted observation — E63/E64

## Separating control and status in software

The audio word at +0x08 (+0x18 for digital) resembles the SiS SR/PIV/CR grouping described in AUDIO-REGISTER-HYPOTHESIS. If status bits 2–4 are write-one-to-clear, writing the observed word back during START/STOP loses events. At E63 this was a model assumption, not an Xbox measurement; E67 later tests W1C behavior while stopped.

Patch 0015 masks these bits and IRQ enables before changing RUN. Prepare keeps an explicit stopped-state acknowledgement. The historical middle field is preserved because its Xenon role is unvalidated. No final-audio-completion decoder or reset wait is added.

The harness extracts actual C functions: two channels, 32 prefetched values, 32 statuses, and two transitions, giving 4,096 cases per variant. Before: 3,584 transitions clear status and all retain interrupt enables. After: zero of either. Fifteen adapter scenarios, twenty resource cases, and 16,384 descriptors pass again, with no ASan/UBSan diagnostic. Evidence: `evidence/2026-10-02/audio-control/`.

The final module is ELF64 big-endian PowerPC with audio-bytes vermagic; E63 did not rebuild vmlinux. An initial isolated target failed modpost due to absent ALSA dependencies; the complete modules target succeeded without warnings. No module loaded.

## Observation preparation: no DMA start

Standard PCI capture identifies 1414:580c, 64-byte BAR0, no driver, and enable=0. PCI command 0x0006 allows memory decoding and bus mastering; it does not demonstrate an active transfer.

Original tool `research/audio/read_status_once.c` rejects wrong identity, attached driver, unexpected window, or disabled memory decoding. It opens resource0 read-only and reads only offsets +0x04/+0x08/+0x14/+0x18, already used by the driver. No register write, PCI enable, DMA allocation, or SMC command occurs. This audio window is distinct from E10's prohibited flash window, but even a read can hang the bus; a software timeout cannot guarantee interruption.

Pre-execution review found a defect in the first observer: sysfs maps the page containing the BAR, not the BAR's first byte. This kernel uses drivers/pci/mmap.c and shifts resource_start by PAGE_SHIFT. With 64 KiB pages, the observer must add **0x1600** to the mapping. The corrected geometry passes **31,744 positions and seven invalid inputs** under ASan/UBSan. The old binary never read registers. Final ELF32 PowerPC disassembly contains four aligned lwz, eight eieio, byte-order conversion, and no MMIO store in the examined sequence.

The ARM build environment lacked the cross-compiler; the legacy Docker builder still selected ARM despite --platform. An explicit amd64/debian base with an architecture assertion succeeded. Both failures are retained. The static binary transferred to /tmp matched its hash; launching without an argument returns usage before hardware access. No package was installed on the console.

Hardware reading and interpretation are recorded separately below. Compatible register bits alone do not prove acknowledgement effects, DMA progress, or sound output.

## Direct observations on October 2

Captures at 12:05:30.002727, 12:06:27.111764, and 12:06:27.219473 console UTC succeeded and matched. There were twelve aligned MMIO reads total and zero writes. The process and SSH returned after each observation under obsidian4; visual response was not checked.

| Channel | Index/residual word | Control/status word |
|---|---|---|
| Analog | 0x00008000 | 0x1d08001c |
| Digital | 0x00009616 | 0x1d08001c |

Hypothetical interpretation using SiS/LibXenon masks: current index equals last index (0 analog, 22 digital), residual zero, RUN=1, IRQ enables=0x1c, low status=0x1c, halted=0. This is not a simple stopped signature. Index bit 15 appears on both channels and remains unexplained here. Control exactly matches LibXenon's initialization constant; these reads cannot distinguish inherited state, partially latched fields, or hardware events.

Identical snapshots do not prove no DMA occurred between reads, and zero residual does not establish final sound output. Linux enable count and absence of a driver are therefore not quiescence proofs before reset or memory release. E63's W1C hypothesis was not proven by these words; no extra write was attempted in this experiment.

The next step was a reviewed bounded STOP/reset transition with confirmation before any active driver. Preserve the working boot and coordinate physical recovery. Do not turn this observer into an arbitrary register scan. E65–E68 contain subsequent targeted writes; E73's reboot supersedes their initial-state assumptions.
