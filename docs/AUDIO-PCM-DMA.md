# ALSA-managed PCM buffers — E55

Patch 0011 follows 0008/0009/0010. It removes the second audio-sample mapping and gives allocation ownership to ALSA. Kernel **6.18.11-xenon-audio-pcm** and 70 modules build without warnings; they were not installed or booted. The driver remains incomplete.

## Source analysis

In linux-custom `a293dd19311668900eb1eeb2f6cb01dcac54f330`, SNDRV_DMA_TYPE_DEV uses dma_alloc_coherent (`sound/core/memalloc.c`), providing the CPU address through runtime->dma_area. A DMA address is not a CPU address to remap through ioremap. The historical remapping, auxiliary pointer, and private assembly cache-maintenance loop are removed.

`snd_pcm_set_managed_buffer_all` replaces preallocation alone, and both outputs propagate its errors. ALSA allocates before hw_params and detaches/frees after hw_free, as documented in `Documentation/sound/kernel-api/writing-an-alsa-driver.rst`. The driver no longer frees these pages in close. A preallocation may remain attached to the PCM until destruction: managed does not mean every hw_free returns physical pages.

Open advertises 128–65,536 bytes in steps of 128 and propagates constraint errors before register programming. hw_params retains a defensive check, which in this variant occurs after ALSA's managed allocation. `sound/core/pcm_memory.c` confirms runtime->dma_bytes becomes the requested size even when reusing a larger preallocation.

Prepare validates the CPU pointer, size agreement, and the entire DMA range against the historical 29-bit mask. Subtraction after checking the start avoids addition overflow. Samples are initialized through runtime->dma_area, and dma_wmb precedes descriptor publication/start. Platform DMA coherence is not proven by the host harness.

Hw_free writes STOP only to the owning channel and reads it back before ALSA can release the buffer. Geometry counters are invalidated; pointer avoids zero-size calculations, and START is rejected after freeing. This does not prove real DMA transactions have ended; hardware-stop semantics remain to be established. E66/E72 later show why callback errors and generic PCI helpers are insufficient lifetime guarantees.

## Off-console results

- Twenty resource scenarios pass under ASan/UBSan, including failures preparing either managed buffer; thirteen original comparison cases retain expected outcomes.
- Twelve actual-callback scenarios cover constraints, null pointer, inconsistent sizes, invalid/overflowing addresses, unknown owner, two simultaneously open streams, and ten successive prepares.
- The normal case checks buffer guards, barriers, single-channel stop before simulated free, START rejection afterward, and protected pointer behavior.
- Geometry regression examines 16,369 sizes: 512 accepted, 15,857 rejected, no out-of-buffer descriptor among accepted sizes. With the private cache function removed, zero cases execute that old function; this is not a PowerPC cache validation.
- Four diffs reconstruct the three compiled sources exactly. Kernel and 70 ELF64 big-endian PowerPC modules have matching vermagic and no build diagnostics.

ALSA/MMIO/locks are modeled. Sequential assertions do not prove actual negotiation, stop behavior, inter-CPU ordering, or absence of races. The harness frees memory immediately after hw_free to expose subsequent accesses; this represents a possible core free path, not every preallocation path.

`check-kernel-artifacts.py --kernel-only` verifies kernel/modules without a XeLL image. Its full mode was also rerun on unchanged obsidian4 artifacts: six matching payload sections and 65 valid modules.

## Limits at this checkpoint

The historical timer remained shared and initially unarmed. Period accounting, callback synchronization, and missing sync_stop still needed work. appl_ptr publication remained in pointer with historical arithmetic. Keeping these outside the diff provides a reviewable scope, not a ready driver.

Descriptor-length disagreement between Linux and LibXenon, a possible low-32-MiB address constraint, and analog/HDMI initialization were unresolved. No sound or performance improvement was measured; no initramfs or boot image for this variant was produced.

## Reproduction

In an independent obsidian4-prepared source copy, apply 0008 through 0011 in order. Retain original sources separately.

```sh
python3 research/tests/check-audio-lifecycle.py --original ORIGINAL/sound/pci/snd-xenon.c --candidate CANDIDATE/sound/pci/snd-xenon.c --output lifecycle.json
python3 research/tests/check-audio-buffers.py --original ORIGINAL/sound/pci/snd-xenon.c --candidate CANDIDATE/sound/pci/snd-xenon.c > buffers.json
python3 research/tests/check-audio-pcm.py --source CANDIDATE/sound/pci/snd-xenon.c --output pcm.json
make -C CANDIDATE O=BUILD ARCH=powerpc LLVM=1 LOCALVERSION=-audio-pcm -j2 vmlinux modules
python3 tools/check-kernel-artifacts.py --kernel-only --build BUILD --output artifacts.json
```

Use `evidence/2026-10-02/audio-pcm/kernel.config` and E53's LLVM 16 environment. The recorded build uses an independent copy of E54 output and three read-only candidate-file overlays on obsidian4 source. Source/diff hashes, image identity, logs, tests, and ELF metadata are in `audio-pcm/`.

## Separate live check — E56

After the user's return, SSH confirmed obsidian4, approximately 5,139 seconds uptime, no failed units, and 1280 × 720 framebuffer. Only standard interfaces were read. This did not measure visual responsiveness, load stability, or the new driver, which remained on the Mac. Exact timestamps are in `console-status.json`.
