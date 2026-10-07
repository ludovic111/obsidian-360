# Audio driver: compilation and buffer geometry — E51

October 2, 2026 analysis of `sound/pci/snd-xenon.c`, linux-custom `a293dd19311668900eb1eeb2f6cb01dcac54f330`. Driver SHA-256: `4289271b03404f6079b590f696e44625d07c59017f099295833390d38f89a0ac`. No sound-device access or new module installation occurred. The working obsidian4 kernel kept sound disabled.

## Original compilation

A separate output directory reused obsidian4 configuration with SOUND, SND, and SND_XENON enabled as modules and SND_PCI enabled. Source and previous build were unchanged. The known LLVM 16 image ran without Docker networking, limited to two CPUs and 2 GiB.

`olddefconfig` succeeded; `sound/pci/snd-xenon.o` failed with eight errors and one warning. Missing APIs were `from_timer`, `pci_alloc_consistent`, `pci_free_consistent`, `snd_printk`, and `del_timer_sync`. The warning concerned a missing prototype for the driver's private SMC transport. This confirms E17 through an actual build, without producing a usable audio object. Logs, configuration, and method: `evidence/2026-10-02/audio-buffers/`.

## Cache loop

The function subtracts 128 from a signed integer while it is nonzero. A positive size not divisible by 128 crosses zero without reaching it and keeps advancing the address; eventual signed overflow makes C behavior undefined. This does not prove a real console hang: that driver is disabled on this machine.

The harness retains the actual C loop, replaces only two PowerPC instructions with hooks, and aborts at the first traversal beyond the expected cache-line span. Five of eight sizes trigger that guard: 64, 68, 132, 192, and 65,532 bytes. Sizes 128, 256, and 65,536 terminate normally. This is a bounded logical demonstration, not PowerPC cache execution or a DMA-coherence measurement.

A 64 KiB ALSA preallocation does not avoid the problem: `snd_pcm_lib_malloc_pages` in `sound/core/pcm_memory.c` assigns the requested size to `runtime->dma_bytes` even when reusing a larger allocation.

## Descriptors

The driver creates 32 upward-rounded segments, then subtracts all excess from the last. For 68 bytes it chooses three bytes per segment, excess 28, and last encoded length `3 - 1 - 28 = -26`, producing `0xffffffe6`. Earlier segments already exceed the buffer before the descriptor list ends.

The harness executes actual hw_params/prepare functions with mocked allocation, locking, and MMIO. Across **16,369** four-byte-aligned sizes from 64 through 65,536, **98** geometries exceed the buffer under the code's length-minus-one interpretation. Another **12,273** geometries split four-byte stereo frames across descriptors. That second property alone is not a demonstrated hardware failure: mid-frame descriptor crossing support is unverified. The union is **12,301** sizes.

## Partial correction 0008

The cache loop now stops at nonpositive size. hw_params rejects values outside 128–65,536 or not divisible by 128; prepare repeats the check before hardware operations and requires DMA/ALSA size agreement. Each accepted size gives 32 equal segments containing whole frames.

The same tests accept **512** sizes, reject **15,857** before allocation/mapping, and produce no out-of-buffer segment. The independent DMA/ALSA mismatch test passes. Eight cache-loop tests stay within the expected span. ASan/UBSan report no error in the modeled harness.

This is an initial defensive restriction. ALSA negotiation must advertise it, the complete port needs testing, and descriptor format must be confirmed on hardware. Enumerating sizes does not prove every one is negotiable in real ALSA or that an application will choose an accepted size.

## Activation blockers identified at this checkpoint

- Timer initialized without an initial arm; only its callback contains mod_timer. Period notifications/calculation need review.
- Private SMC transport bypasses the existing core lock and waits indefinitely. Adopting shared transport also requires addressing its own unbounded waits.
- Unchecked DMA allocation under lock, masked DMA handle later freed, and ioremap of a DMA address violate or obscure memory ownership contracts.
- Cleanup can precede timer_setup; creation failure can free a null object; ALSA registration failure can double-free. Fault injection is needed.
- IRQ handler always claims handled, while enable/disable operations are empty. DMA stop and callback synchronization remain unvalidated.

Fixing compilation alone does not make loading appropriate. E51 validates no HDMI support, audio playback, latency, or stability.

## Reproduction without hardware

Apply patch 0008 to a copy of the original:

```sh
python3 research/tests/check-audio-buffers.py --original ORIGINAL/snd-xenon.c --candidate CANDIDATE/snd-xenon.c
```

The harness requires Clang and ASan/UBSan runtimes, creates temporary files, and contacts no hardware. For the original build, mount source read-only at /src and a new output at /build in the documented LLVM 16 image, copy configuration, then run:

```sh
/src/scripts/config --file /build/.config -m SOUND -m SND -e SND_PCI -m SND_XENON
make -C /src O=/build ARCH=powerpc LLVM=1 LOCALVERSION=-audio-audit olddefconfig
make -C /src O=/build ARCH=powerpc LLVM=1 LOCALVERSION=-audio-audit -j2 sound/pci/snd-xenon.o
```

This original build is expected to fail with the retained diagnostics. It is not an installation procedure.
