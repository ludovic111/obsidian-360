# Patches and validation status

Patches 0001–0007 are analysis results. The six Linux patches (all except 0002) were compiled together into the obsidian4 candidate, with its modules and its boot image. Its files are staged on the console and on the USB drive for an optional trial; its boot was then confirmed in E38 and its return after a trial of the stock system in E52. XeLL has not been rebuilt. The working system remains the default entry.

- `0001-xenos-pad-tiled-framebuffer.patch`: allocation size rounded up to 32 × 32 macro-tiles. Base: `xenos.c` added by the Linux 6.18-xenon0.30 patch, commit `498bbe1910f707ceba0535276d75a3e6ad0b7df4` of the Free60Project/linux-kernel-xbox360 repository.
- `0002-xell-allocate-physical-page.patch`: buffer sized for the 528 bytes of the raw NAND page. Base: Free60Project/xell-reloaded, commit `a36ed6b7dae940e47e472a20fd14b0616ddc8cef`.
- `0003-xenon-preserve-ipi-target-mask.patch`: fixes the mask/shift order in the IPI callback. Base: techflashYT/linux-custom, commit `a293dd19311668900eb1eeb2f6cb01dcac54f330`. 256 combinations tested per variant with simulated MMIO; the ordinary SMP path calls another function.
- `0004-xenon-bound-smc-reply-cache.patch`: bounds the SMC cache lookup to its thirteen entries. Same linux-custom base; four ASan cases check the original and the candidate, with no messages sent to the hardware.
- `0005-xenon-led-lifecycle.patch`: single init/exit, managed resources, checked allocation errors, sending without a reply and under lock. Same linux-custom base; 21 off-console ASan/UBSan cases.
- `0006-xenon-export-smc-ready.patch`: GPL export of the SMC core readiness, needed by the LED driver built as a module. Applies after 0004; the core is built by PPC_XENON, independently of the XENON_SMC character interface.
- `0007-xenon-isolate-boot-image-recipe.patch`: excludes the Xenon image from the competing generic recipe and removes a copy to a local path specific to the upstream developer. The obsidian4 build no longer produces these warnings.

The ten cases of the first AddressSanitizer bench pass: the three expected errors are reproduced in the original sources; the corrected variants and the non-overflow controls terminate normally. The hardware interfaces are simulated. The graphics driver was then compiled into the complete candidate vmlinux with LLVM 16; XeLL is not compiled as a complete PowerPC loader. The evidence for the latest candidate is in `evidence/2026-10-01/kernel-build-obsidian4/`. The LED and competing-recipe warnings are resolved.

Before promotion to the default system: validate boot, desktop, peripherals and return to the previous system. The initramfs and the optional set are prepared; see `docs/BOOT-PREFLIGHT-2026-10-01.md`. The LLVM candidate does not reproduce the installed GCC build bit for bit. The HTTP defect validates neither SFCX statuses, nor ECC, nor bad blocks.

Do not apply these diffs to the evidence archives. No NAND flash is required for the planned graphics test.

## Audio: compiled candidates, not enabled

`0008-xenon-audio-buffer-geometry.patch` targets the same snd-xenon.c (GPL-2.0-or-later). It bounds sizes to multiples of 128 bytes and prevents the cache loop from continuing for a negative size. Tests of the extracted C on the host: 16,369 sizes, 512 accepted by the candidate, no out-of-buffer geometry among them. This diff is not a usable driver: API porting, lifecycle, SMC transport, DMA and ALSA notifications remain to be resolved. See `docs/AUDIO-BUFFER-AUDIT.md`.

`0009-xenon-audio-resource-lifecycle.patch` applies after 0008: single ALSA owner, error paths, DMA/timer API, shared SMC transport, removal of the fake IRQ handler. PowerPC object compiled and sixteen resource scenarios validated in the model; still not enableable. See `docs/AUDIO-LIFECYCLE-AUDIT.md`.

`0010-xenon-bounded-smc-post.patch` adds a send API that does not wait for the lock, with a polling budget, and uses it in the audio driver. Nineteen SMC scenarios and eighteen resource scenarios pass. The 0008/0009 and then 0008/0009/0010 variants compile the kernel + 70 modules without warnings. Nothing loaded; old SMC paths still unbounded. See `docs/SMC-BOUNDED-POST.md`.

`0011-xenon-audio-coherent-pcm.patch` switches to ALSA-managed buffers and their existing CPU address, removes the private remapping/cache handling, and adds constraints and defensive checks. Twenty resource scenarios, twelve callback scenarios and the geometry regression pass; kernel and 70 modules compiled. Timer and protocol remain incomplete; nothing loaded. See `docs/AUDIO-PCM-DMA.md`.

`0012-xenon-audio-stream-polling.patch` adds per-stream tracking and synchronization before release; 15 tracking scenarios, 20 resource scenarios and 15 PCM scenarios pass off hardware. High-resolution configuration enabled, final kernel and 70 modules verified without warnings, not enabled. See `docs/AUDIO-STREAM-POLLING.md`.
