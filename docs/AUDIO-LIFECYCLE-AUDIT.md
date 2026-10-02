# Audio resource lifecycle port — E53

Off-console work dated October 2, 2026. Patch `0009-xenon-audio-resource-lifecycle.patch` follows 0008 on linux-custom `a293dd19311668900eb1eeb2f6cb01dcac54f330`. No module was loaded or kernel installed. E52 was the latest hardware observation at this checkpoint; source work did not refresh live state.

## Reproduced defects

The harness extracts actual structures and allocation, PCM creation, initialization, probe, remove, and free functions. Kernel interfaces become a resource model; callbacks execute sequentially without real DMA, IRQ, SMC, or timers.

Thirteen original scenarios produce one successful normal lifecycle and twelve precisely recognized expected failures:

| Injection | Original result |
|---|---|
| Card creation returns ENOSPC | Driver incorrectly replaces it with ENOMEM |
| PCI enable, chip allocation, wrong BAR type, PCI reservation | Null-pointer access during free, caught by UBSan |
| IRQ request, PCM 0/1 creation, lowlevel registration | Cleanup of an uninitialized timer, caught by the model |
| Final card registration | Use-after-free after initial cleanup, caught by ASan |
| Synthetic DMA handle with high bits | Handle passed to free differs from allocator result |
| Remove with modeled active stream/timer | PCM freed before quiescence, caught by model |

The synthetic handle is not an address observed on Xbox. Active removal is model injection, not measured DMA traffic. Early failures do not establish every defect that they may mask.

The first harness failed to compile because its fake IRQ-handler signature was wrong and macOS deprecated sprintf. `harness-first-attempt.json` preserves that tooling failure. The corrected harness uses the proper prototype and suppresses only that host-library deprecation, retaining relevant Wall/Wextra/Werror checks.

## Candidate correction

The ALSA card becomes the sole owner of private state once lock/timer initialization completes. Acquisition flags track partial-failure cleanup. snd_card_free executes once; its private callback frees the object after PCM devices, matching `sound/core/init.c:snd_card_do_free`.

Remove and post-allocation failures first request both channels to stop, call timer_shutdown_sync, and clear PCI bus mastering. The model verifies this ordering before PCM destruction. Actual controller-stop effects still require hardware evidence; later E66/E72 further qualify memory-release guarantees.

Descriptor allocation uses checked dma_alloc_coherent outside the lock and preserves the exact handle for dma_free_coherent. The requested 29-bit mask follows historical masking but is not validated as the hardware limit. LibXenon comparison requires further review.

Private SMC mapping/transport is removed in favor of xenon_smc_ready and xenon_smc_message. This uses the shared lock but does not fix the core's indefinite ready wait. The old IRQ handler always claimed handled without recognizing/acknowledging a source; it is removed, and that PCI function's interrupt is disabled. Polling operation still needs implementation.

Timer API becomes timer_container_of. Obsolete snd_printk calls disappear with old error paths. Sixteen candidate scenarios cover normal/card/PCI/allocation/BAR/short BAR/DMA mask/reservation/mapping/DMA allocation/SMC unavailability or failure/two PCM/final registration/modeled active removal. Each ends with no owned resources and no ASan/UBSan finding. This does not cover SMP interleavings or all ALSA open/close orders.

E51 regression remains valid: 16,369 sizes, 512 accepted, no out-of-buffer geometry for accepted sizes, and eight cache-loop cases.

## Compilation

LLVM 16 builds the PowerPC `sound/pci/snd-xenon.o` without warnings using a fresh output directory and read-only replacement of the candidate file; obsidian4 remains intact. A subsequent full kernel/module build succeeds with 70 modules and no warnings; see `evidence/2026-10-02/audio-lifecycle/`. Distinguish a compiled object, a linked module, and a functioning driver.

## Protocol differences requiring resolution

The verified local reference is Free60Project/libxenon `a333adef440f28b436a667be0a4f014afce6349d`, `libxenon/drivers/xenon_sound/sound.c`, with no local changes. Comparison is preserved in `source-comparison.json`.

| Topic | Historical Linux | LibXenon | Consequence |
|---|---|---|---|
| Placement | 29-bit masking | Comment suggesting first 32 MiB; low-memory sections | Actual DMA address range unproven |
| 2,048-byte descriptor length | 0x800007ff | 0x80000800 | Length-minus-one versus literal bytes; not yet resolved in E53 |
| HDMI | SMC `8d 01 01` | DAC GPIO reset and eleven I2C writes through SMC, then that message | ALSA device existence does not prove HDMI audio |

Do not blindly copy initialization from another runtime: LibXenon assumes different placement and boot state. E51 geometry tests explicitly follow Linux's encoding, not proven hardware semantics. Later E62 examines the length discrepancy.

Kernel source also confirms SNDRV_DMA_TYPE_DEV already uses dma_alloc_coherent and dma_mmap_coherent in `sound/core/memalloc.c`. Re-ioremapping runtime->dma_addr and applying private cache instructions is not that API's contract. The next port should use runtime->dma_area, appropriate barriers, and PCM lifetime management that stops accesses before returning memory.

## Reproduction

Apply 0008 then 0009 to an original-driver copy:

```sh
python3 research/tests/check-audio-lifecycle.py --original ORIGINAL/snd-xenon.c --candidate CANDIDATE/snd-xenon.c --output validation.json
python3 research/tests/check-audio-buffers.py --original ORIGINAL/snd-xenon.c --candidate CANDIDATE/snd-xenon.c
```

The first harness requires its two neighboring scaffolding files and checks precise expected diagnostics, not merely nonzero exit. Success means original predicted failures reproduced and candidate model scenarios passed.

Use AUDIO-BUFFER-AUDIT's configuration/image, apply both patches to separate working source, and build the object or vmlinux/modules with LOCALVERSION=-audio-lifecycle. No XeLL packaging or installation is part of this experiment. The candidate remains unsuitable for activation until DMA, timer/notifications, concurrent close, SMC delay, and real protocol issues are resolved. No analog, S/PDIF, or HDMI playback is validated.
