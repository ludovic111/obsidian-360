# Original PCM queue — software component, E59

`pcm_queue.c` and `pcm_queue.h` are original MIT-licensed components intended to replace historical audio submission logic. They are not a driver. E60 integrates them into the unactivated `snd-xenon` candidate through patch 0013; see `docs/AUDIO-ALSA-ADAPTER.md`. This component performs no hardware access, allocation, audio copy, barrier, or locking.

It tracks committed data, publishable blocks, the incomplete tail, physical consumption, and logical consumption separately. Buffers range from 128 to 65,536 bytes in 128-byte increments, with 32 equal blocks and four-byte frames. Each instance represents one stream and requires its caller's lock.

## API and plans

| Function | Software effect |
|---|---|
| `obs_audio_queue_init` | Initialize an empty queue with zero positions |
| `obs_audio_queue_push` | Accept frames already copied into the buffer; announce only newly complete blocks |
| `obs_audio_queue_drain` | Close further submission and plan final-block silence if required |
| `obs_audio_queue_consume` | Record physical block consumption after the adapter has verified completion |
| `obs_audio_forward_delta` | Compute bounded frame-counter progress, including wrap, rejecting backwards/out-of-capacity jumps |

A plan contains a publish flag, last-block index, and optional zero-fill range. A non-publishing plan must not write an index. A full buffer still generates publication when the final circular index equals its earlier value.

An incomplete tail remains committed but unpublished. Drain plans zero-fill for its remainder and then makes the last block publishable. The adapter must **perform that fill, then the DMA barrier, before publishing**; this component does neither. No committed sample lies in the zero-fill range, which remains inside the allocation.

Padding counts toward physical bytes consumed but not logical bytes returned to ALSA. At maximum buffer size it can add 2,044 bytes, approximately 10.646 ms at the expected 192,000 bytes/s. This is a calculated bound, not measured latency.

Errors leave state and output arguments unchanged. Push after drain is rejected; a new stream needs reinitialization. Repeated drain is idempotent. Callers must supply valid, distinct, nonconcurrent objects; invariant checks cannot protect arbitrary invalid pointers.

`obs_audio_forward_delta` handles 64-bit boundaries without multiplying the complete counter. Only the bounded delta, at most 16,384 frames, may later be converted to bytes. ALSA reset and live-stream rebasing belong to the adapter and are not guessed by this function.

## Tests and compilation

From the repository root:

```sh
python3 research/tests/check-audio-queue.py --output queue-validation.json
clang --analyze -std=c11 -Wall -Wextra -Werror research/audio/pcm_queue.c
clang --target=powerpc64-linux-gnu -ffreestanding -std=c11 -O2 -Wall -Wextra -Werror -c research/audio/pcm_queue.c -o pcm_queue.o
```

The cross-compile used LLVM 16 in the project build environment. Host tests use Clang, ASan, and UBSan. LeakSanitizer is disabled on this unsupported Mac platform; its initial refusal is retained as a tooling failure before any cases ran.

The harness generates numbered frames, keeps an independent content queue, and compares consumed content including final zeros. It covers all 512 sizes, full buffers, a single final sample, unchanged state after rejection, and 44,800 deterministic fill/consume steps across two interleaved queues. The recorded run compared **54,008 operations and 24,544,033 logical frames**. Occupied slots cannot be republished before consumption in this model.

A minimal link module was also built against `6.18.11-xenon-audio-poll` headers/configuration. It contains these sources and a file declaring only `MODULE_LICENSE("Dual MIT/GPL")` and a description. It has no hardware init or PCI driver. All five functions, ELF64 big-endian PowerPC format, and vermagic were verified. No module was loaded.

```make
obj-m += obsidian_pcm_queue.o
obsidian_pcm_queue-y := pcm_queue.o build_check.o
```

Build with `make -C SOURCE O=BUILD M=MODULE ARCH=powerpc LLVM=1 LOCALVERSION=-audio-poll modules`. Kernel files were mounted read-only in the recorded check. This validates `__KERNEL__` compilation/linkage, not ALSA integration.

## Hardware integration prerequisites

The model assumes ordered block consumption and last-valid-block publication. It establishes no register bits, length encoding, actual completion, or absence of DMA prefetch. The driver must translate verified hardware progress into consumption and must not infer an empty queue from an unchanged modulo position.

The adapter must connect `.ack`, START, DRAIN, `.pointer`, polling, and ALSA resets; propagate errors/rollback; and preserve fill/barrier/publication order. E60 replaces pointer-driven publication with an offline-tested adapter. Final-block completion remains unresolved, preventing hardware validation of drain and sound output.

Evidence: `evidence/2026-10-02/audio-queue/`. E59 performed no Xbox interaction; its last preceding hardware snapshot was E56, not a statement of current hardware state. E60 renamed parameter `current` to `position` to avoid a kernel macro collision; the algorithm was unchanged and the full harness reran.
