# Current state — October 2, 2026

This is the current summary, not a claim that every historical measurement still holds. [EXPERIMENTS](EXPERIMENTS.md) and [JOURNAL](JOURNAL.md) retain the chronological record. The newest successful system check was received at **13:54:16 UTC on the host**. Console wall-clock timestamps differ and must not be treated as synchronized UTC.

## Running system and clock correction — E73

The user booted the optional **obsidian_clock** entry and reconnected Ethernet. SSH identifies **6.18.11-xenon-obsidian-clock**, internal `/dev/sda1` ext4 root, 65 corresponding module files, Xorg and IceWM, a **1280 × 720** framebuffer, and no listed failed systemd units. The targeted kernel-log search found no NETDEV WATCHDOG, kernel panic, BUG, or Oops match. It is not a claim that the entire boot log contains no warnings.

The kernel command line contains `xenon_tb_hz=49875000`; the boot log explicitly reports 49,875,000 Hz software conversion versus 50,000,000 Hz from firmware. `/proc/cpuinfo` agrees with the active conversion. The user separately confirms that the desktop responds to controller or keyboard input; the exact input device was not specified in that answer.

| Measurement | Before, E69 / obsidian4 | After, E73 / obsidian-clock |
|---|---|---|
| Capture | Seven SSH samples, approximately 60 s | Seven SSH samples, approximately 60 s |
| Raw-clock relative error | −2,531.254 to −2,481.332 ppm | −28.155 to +14.432 ppm |
| Comparison source | Mac monotonic clock | Same Mac monotonic clock |
| Active conversion | 50,000,000 Hz | 49,875,000 Hz |
| Interpretation | About 0.25% slow | Error interval includes zero at this measurement resolution |

The conservative absolute-error bound improves by at least **88.13 times** between these windows. This is a measured cadence improvement, not proof of an exactly calibrated oscillator or long-term stability. Civil time is still approximately **243.026 seconds behind** the Mac. Neither NTP nor the wall clock was changed during the experiment.

The collector was corrected to use the kernel's active conversion when inferring timebase frequency. The firmware device tree remains at 50 MHz after the override; using that unchanged field would mislabel the post-patch frequency. Thirteen analysis tests cover the override, legacy captures, missing/invalid conversion, malformed timing, and incomplete transport.

Evidence: `evidence/2026-10-02/timebase-first-boot/`. Details: [first boot](TIMEBASE-FIRST-BOOT.md), [calibration](TIMEBASE-CALIBRATION.md).

## Boot files and recovery — E38, E52, E70–E73

- **obsidian_clock**: new kernel and initramfs on USB, 65 modules in a separate internal directory, now booted once successfully.
- **obsidian4**: earlier confirmed working kernel retained unchanged.
- **linux_hdd**: remains the menu default. Its continued presence is not a fresh rollback boot test.
- Existing live USB recovery files retained with verified hashes.
- Previous menu backed up before the optional entry was added.
- No NAND, eFuse, oscillator/PLL, power, or thermal configuration changed.

E71 built a **16,171,806-byte** initramfs, extracted and matched its **43 modules**, checked six essential ELF32 PowerPC binaries, and verified the USB contents after a read-only remount. The optional menu entry is 168 bytes and includes the existing root parameter plus the explicit frequency option. See [boot preparation](TIMEBASE-BOOT.md).

Boot still depends on the authenticated Xbox system, Rock Band Blitz, temporary patches, XeLL, and USB. Keep Ethernet unplugged during the exploit/loader path and reconnect after Linux. No standalone power-button-to-Linux path or restorable NAND backup has been validated.

## Audio — host candidate and hardware evidence are separate

The current clock kernel **does not include the experimental audio driver**. PCI configuration on the latest boot still identifies `1414:580c`, no bound audio driver, status `0x0288`, and no advertised capability list. That header matches E64. No audio BAR registers were read after the reboot, so the earlier analog STOP/ACK state must not be described as current.

### Candidate implementation

- E53–E56: driver API/resource cleanup, coherent PCM buffers, bounded new SMC post path, and high-resolution per-stream polling were implemented and compiled off-console.
- E57–E60: submission defects were analyzed; an original queue and ALSA ack/drain/reset adapter were tested with source-extracted callbacks. The queue model covered 54,008 operations and 24,544,033 frames in E59.
- E62: descriptor lengths changed to literal byte counts, supported by LibXenon history and SiS driver analysis. The audio-bytes kernel and 70 modules were verified, not deployed.
- E63: control changes no longer echo W1C status bits; polling keeps IRQ enables off. Tests cover 4,096 modeled transitions, 15 adapter cases, 20 resource cases, and 16,384 descriptors. The SiS register relationship remains a hypothesis beyond what hardware experiments establish.

### Pre-reboot hardware observations

- E64: three targeted register snapshots, after fixing the 64 KiB page/BAR offset calculation. Initial analog index/control `0x00008000` / `0x1d08001c`; digital `0x00009616` / `0x1d08001c`. PCI command allowed memory and bus mastering although no Linux driver was attached.
- E65: one analog STOP write changed control first to `0x0008001d`, later `0x0000001d`; index became zero and the digital channel remained unchanged. This supports the interpreted halted indicator without proving outstanding DMA completion or FIFO drain.
- E67: separate writes 4, 8, and 16 produced `0x1d → 0x19 → 0x11 → 0x01`, demonstrating W1C behavior for those analog status bits while stopped.
- E68: a reset request read back `0x01`, compatible with self-clearing but also insufficient to distinguish a fully effective reset from an ignored command, because observed state was already unchanged.

### Remaining lifetime and protocol blockers

E66 executes real ALSA functions: callback errors do not retain managed buffers. Of 144 tested combinations, 24 detachments and 12 dynamic frees occur after a callback error. Preallocated buffers can instead remain available for reuse; both lifetime paths require coherent hardware state.

E72 executes seven real PCI functions: the generic pending-transaction wait returns success without a read for a non-PCIe endpoint. A simulated failed MASTER-clear write can leave hardware enabled while the software flag is false. This is not a hardware fault observed on Xbox; it invalidates relying on those helper results alone as a DMA completion proof.

No audio START, valid playback, final-descriptor completion, full FIFO drain, or complete reset semantics are established. A future driver needs real buffer retention/isolation on failed stop, bounded ownership transitions, and a recovery strategy. See [PCI isolation](AUDIO-PCI-ISOLATION.md), [STOP contract](AUDIO-STOP-EXPERIMENT.md), and [ACK/reset](AUDIO-ACK-RESET.md).

## Desktop, display, and input

obsidian4's padded framebuffer allocation was confirmed at boot: 1280 × 736 × 4 bytes rather than the unpadded 1280 × 720 allocation. The clock candidate retains that correction. The display remains 720p; changing Xorg dimensions alone cannot program HDMI/ANA/HANA timings.

E46 recovered an X server stall without restarting Linux. E47 reproduced the IceWM resize/XGrabServer interaction under Xvfb. OpaqueMove/OpaqueResize configuration was installed and survived a later boot. Current desktop responsiveness is now user-confirmed, but repeated physical resize and all controller mappings are not separately validated.

The launcher, virtual keyboard, and input engine have host tests. The shutdown authorization check used the real graphical process, but a successful desktop shutdown still needs its own observed test. A past “failed request” message is not evidence that poweroff now works.

## Optical drive and game analysis

The PLDS DG-16D2S answers identification commands. A music CD exposed 20 tracks, and selected raw audio sectors were acquired. Just Cause 2 and the Big Order DVD returned media-absent responses under Linux; the user also reported no detection in the stock dashboard and brief spin-up followed by stopping.

The health of the DVD media on another player, console region, laser/mechanical fault, firmware pairing, and full game-authentication behavior are unresolved. A PAL marking alone does not explain the observed absence of both game and video DVD detection. The drive is not repaired.

The Rust XEX2 inspector works on synthetic structural fixtures. No legitimate game executable has yet been acquired for deeper analysis, and no proprietary game assets or binaries are published. See [optical investigation](OPTICAL-DRIVE.md) and [XEX2](XEX2-INSPECTION.md).

## Other constraints and open work

- Earlier TX watchdog and USB keyboard symptoms are real observations with unresolved causes; do not combine them into a definitive hardware diagnosis.
- The first IPI mask defect was reproduced and patched, but its callback is not the ordinary SMP IPI path in this branch.
- The SMC cache bound and LED lifecycle fixes are in the booted base. The new bounded SMC post API is part of the separate audio work; historical SMC paths still contain unbounded behavior.
- Package installation previously encountered a missing pacman keyring. Do not disable signature verification; investigate before installing new packages.
- Direct flash BAR1 reading hung the console. Never rerun the archived probe without resolving the mechanism. XeLL HTTP page-size analysis alone does not validate a raw NAND backup, ECC, or bad-block handling.
- Motherboard revision, NAND geometry, independent recovery, 1080p, GPU acceleration, reliable audio, and owned-game analysis remain unfinished.

## Repository and publication

The GitHub repository is private. On 2026-10-07 the full English research history, including E72 and E73, was merged into `main`; the earlier public-export history (last export commit `47b0a02d8820d009aa6cde4741a925b6e6018cae`, 452 files, covering E71) is the merge's first parent. `research/bootstrap` remains on GitHub, fully merged. New work goes on `main`, with branch work in worktrees. The controlled public export is historical; see [PUBLICATION](PUBLICATION.md) for the history and the dated audit receipts.
