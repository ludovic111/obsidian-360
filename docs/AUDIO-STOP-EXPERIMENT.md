# Targeted analog STOP — E65

## Question and limits before execution

E64 found apparent RUN and stable values without a Linux audio driver. Candidate 0015 clears RUN but checks neither halted state nor transaction completion before buffer reuse. The Intel reference waits for halted after STOP; intel8x0 even contains an unbounded wait that must not be copied onto Xbox. The SiS register resemblance remains a hypothesis.

Original probe `research/audio/stop_analog_once.c` permits exactly one write: **0x00080000 to analog +0x08**, after checking PCI identity, a 64-byte BAR, no bound driver, and both controls exactly 0x1d08001c. It clears RUN/IRQ without writing ones to presumed W1C bits, preserving the middle field. No START, reset, descriptor replacement, SMC command, PCI reconfiguration, or flash access occurs.

Before writing, it prints and flushes its observation. It then reads both controls and indices: six reads total on the accepted path. No polling or automatic retry. Digital is unwritten and serves as comparison. Changed preconditions cause refusal before writing. No automatic return to RUN is permitted: restarting an old DMA address would be unjustified. A separate read-only follow-up may run after the process returns.

A lost connection or freeze requires manual recovery through known obsidian4, Ethernet disconnected during Rock Band Blitz/XeLL. Software timeouts do not protect against a stalled bus transaction. No intentional reboot, firmware change, or boot-file change occurs in this experiment.

## Off-console verification

The harness executes the actual C gate/write against ordinary memory. Only the exact initial state passes; 64 single-bit changes are rejected without changing output, and only four bytes at +0x08 change. ASan/UBSan pass. The page calculation reuses E64's corrected logic and checks offset 0x1600. No-argument launch returns 2 before any hardware access.

The static ELF32 big-endian PowerPC binary builds without diagnostics in the audio-observer image. Disassembly shows one MMIO-sequence stw at +8, little-endian conversion, preceding hwsync, and following eieio. Transfer must preserve its hash before execution.

Two tooling failures are retained: an unused harness counter and an extraction that searched for sync while objdump printed hwsync. Corrected results are separate; neither failure involved hardware execution.

References: pinned `sound/pci/intel8x0.c` and [Intel ICH4 section 14.2.7](https://www.intel.com/content/dam/www/public/us/en/documents/datasheets/82801db-io-controller-hub-4-datasheet.pdf). The Intel reference does not identify Xbox silicon or prove its effects.

## Hardware result

At **12:47:31 console UTC on October 2**, the probe exited zero under obsidian4. Writing 0x00080000 gave immediate analog control **0x0008001d** and index **0x00000000**. Digital remained **0x1d08001c / 0x00009616**. One write, six reads, no automatic restart.

At 12:48:41 console UTC, read-only follow-up showed analog **0x0000001d**, index zero, digital unchanged. The middle field therefore changed from 8 to 0 between observations; precise timing and role were not measured. Four further reads, no writes. SSH responded, framebuffer was 1280 × 720, and no failed systemd units were listed. Visual responsiveness was not checked.

Under the studied layout, RUN cleared, DCH changed 0→1, and status bits 2–4 stayed set despite zeros being written. This supports separation of control/status and an analog halted indication. It does not establish W1C behavior, complete reset, absence of outstanding transactions, FIFO drain, or digital behavior. Analog index bit 15 disappeared; its exact meaning remained open.

Analog was left stopped; no inherited RUN was restored. The next experiment had to update preconditions and distinguish acknowledgement/reset. Never blindly rerun the original STOP tool once its initial state has changed. The later E73 reboot also supersedes this state.

## ALSA lifetime contract — E66

Source review found a further constraint: returning an error from hw_free does not prevent ALSA from calling snd_pcm_lib_free_pages, and the sync_stop return value is ignored. Three actual functions from pcm_native.c/pcm_memory.c run under ASan/UBSan across **144** callback/error/state/buffer combinations. **24** cases detach memory after a callback error, including **12** actual dynamic frees. This tests the software contract, not an ALSA bug or an observed Xbox error.

Preallocated buffers differ: they detach from runtime but remain available for reuse; only dynamic allocations are freed by that function. The candidate reserves 64 KiB per stream, so not every scenario physically frees its buffer. Reuse still requires a coherent hardware state.

Adding polling followed by `return -ETIMEDOUT` alone does not solve lifetime. Before integration, establish per-channel stop, bounded reset before descriptor replacement, and actual retention/isolation on failure. Clearing PCI MASTER alone is not a measured completion guarantee. Earlier models assumed instantaneous STOP and do not cover this issue.

```sh
python3 research/tests/check-audio-stop.py
python3 research/tests/check-audio-free-contract.py \
  --kernel .local/kernel-build/source/linux-custom-a293dd19311668900eb1eeb2f6cb01dcac54f330 \
  --output .local/audio-free-contract.json
```

These reproduction commands are off-console. Cross-compilation and the hardware-probe hash are documented in `evidence/2026-10-02/audio-stop/build.json`; executing the physical probe is not part of these tests.
