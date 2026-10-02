# Bounded SMC post for audio — E54

Patch 0010 adds a separate `xenon_smc_post` path, used by the audio candidate after 0008/0009. It targets linux-custom's SMC core after the cache/export fixes already included in obsidian4. No Xbox command was sent and no image installed in this experiment.

## Contract and scope

The call is restricted to process context and takes a readable 16-byte kernel buffer. The first byte's high bit must be set, matching the no-reply convention already used by `_xenon_smc_wait`. This does not validate the meaning of every possible message; the only new client is audio initialization `8d 01 01`.

The function accepts a budget of 1–1,000 microseconds, copies bytes into four aligned words, and immediately tries two locks: a probe/remove lifecycle mutex, then the existing FIFO lock with interrupt-state preservation. Contention returns `-EBUSY` without waiting or reading a register. Missing transport returns `-ENODEV`.

Under the FIFO lock, `readl_poll_timeout_atomic` checks readiness with a nominal one-microsecond delay per attempt. The harness uses the actual `include/linux/iopoll.h` macros, not a rewritten loop. For permanently busy modeled hardware, a 1,000 budget gives 1,001 reads and 1,000 delay calls before `-ETIMEDOUT`. A budget of one gives two reads and one delay. The final read can still succeed, as specified by the kernel macro.

This is not a strict real-time bound: operation cost adds to nominal delays, and software polling cannot interrupt an MMIO transaction that never returns. Existing senders/waiters remain unchanged and may still wait without a bound. E54 does not resolve every possible SMC/kernel hang.

Only after readiness succeeds does the exact write sequence occur: open FIFO with 4, send four words with `writesl`, close with 0. Failure/contention performs no write. Tested paths restore acquired locks and interrupt state.

## Probe/remove protection

The new mutex excludes `xenon_smc_post` during initialization/removal. A second probe is rejected if transport already exists. Mapping/IRQ errors are propagated, the mapped pointer is cleared during cleanup, and successful PCI enable is balanced even if region reservation fails.

PCI interrupts are masked before initialization and enabled after handler acquisition. Removal masks them, frees the handler before unmapping, and clears callbacks/pointers. This mutex protects the new path; old functions do not take it, so their concurrent access remains a separate audit. Sequential tests do not prove their safety under concurrent unbind. Do not trigger a real unbind to test that hypothesis.

The audio candidate also masks its PCI interrupt immediately after enabling the function and propagates post errors before programming channels. Contention does not trigger an unbounded retry or hidden automatic recovery.

## Tests and builds

Nineteen ASan/UBSan scenarios cover four probe failures, pre-probe call, double probe, null buffer, reply-requiring message, zero/excessive budgets, contention on both locks, immediate/late/final-read readiness, two timeouts, minimum-budget final-read success, and restoration of initially disabled interrupts. The test message is deliberately unaligned; the transmitted copy must be aligned and byte-identical. A post-remove call is rejected without another read.

Locks, IRQs, and MMIO are mocked; physical delays and SMP interleavings are not measured. Host errno numbers may differ from Linux, so C assertions use symbolic names. The first harness attempt failed on an upstream unused-parameter warning; that tooling failure is preserved, then corrected by matching the kernel's warning option.

The audio resource harness now passes eighteen scenarios, including SMC contention/timeout propagation. Thirteen original comparison cases and buffer regression retain their expected outcomes.

| Variant | Audio patches | Verified result |
|---|---|---|
| `6.18.11-xenon-audio-lifecycle` | 0008/0009 | Kernel and 70 modules, no warnings |
| `6.18.11-xenon-audio-post` | 0008/0009/0010 | Kernel and 70 modules, no warnings; xenon_smc_post GPL export present |

All 70 modules have ELF64 big-endian PowerPC headers and matching release vermagic. Kernel/module/source hashes and logs are retained. The second build uses an independent copy of the first output with three candidate sources mounted read-only; obsidian4 remains intact.

Evidence: `evidence/2026-10-02/audio-lifecycle/full-build.*` and `evidence/2026-10-02/smc-post/`. No XeLL packaging, initramfs, load, or boot was performed for these variants. Descriptor format, DMA addresses, PCM handling, notifications, and HDMI remained unvalidated at this checkpoint.

## Reproduce without hardware

Apply 0008, 0009, then 0010 to working sources:

```sh
python3 research/tests/check-smc-post.py --source CANDIDATE/drivers/xenon/smc-core.c --iopoll SOURCE/include/linux/iopoll.h --output smc-post.json
python3 research/tests/check-audio-lifecycle.py --original ORIGINAL/sound/pci/snd-xenon.c --candidate CANDIDATE/sound/pci/snd-xenon.c --output audio-lifecycle.json
```

Build with E53's configuration and LLVM 16 image, `LOCALVERSION=-audio-post`, and targets `vmlinux modules`. Applied patches must reproduce the source hashes in `full-build.json` before treating these results as applicable.
