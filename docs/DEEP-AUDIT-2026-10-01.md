# Deep audit — October 1, 2026

This checkpoint combines live Linux observations, source analysis, and C tests on the Mac. It is not complete silicon reverse engineering. Two memory-bounds defects were reproduced in reference code, with candidate patches retained and no Xbox kernel/loader modification during these experiments. Subsequent binary identification and deployment are separate evidence.

## Evidence scope

- Direct observations: `evidence/2026-10-01/deep-audit/runtime.json`, `kernel-provenance.txt`.
- Reproducible analysis: `video-analysis.json`, `tiling-bounds.json`, `memory-bounds.json` in that directory.
- Source identities and hashes: `deep-audit/sources.json`.
- Examined Linux patch: `patch-6.18-xenon0.30.diff`, SHA-256 `d5d79cd502f859311dd2f2b834b57a489fead1e8e622deb55c6a70f79df604ad`.
- Installed package: linux-xenon 6.18.11-1. Version identity alone did not prove instruction identity. At this stage no rebuild/disassembly had established that match; E20–E24 later correct the exact source attribution.

## F01 — Framebuffer allocation too small for tiling

Confirmed in reference code and reproduced on the Mac. The driver allocates width×height×cpp, while xenos_blit places pixels in 32×32 macro-tiles. Heights not divisible by 32 can write past the allocation.

| Dimensions | Original bytes | Maximum addressed end, exclusive | Proposed allocation |
|---|---:|---:|---:|
| 640 × 480 | 1,228,800 | 1,228,800 | 1,228,800 |
| 1280 × 720 | 3,686,400 | 3,766,272 | 3,768,320 |
| 1920 × 1080 | 8,294,400 | 8,354,816 | 8,355,840 |
| 1280 × 768 | 3,932,160 | 3,932,160 | 3,932,160 |

The actual xenos_blit C function is extracted and built under ASan. Original 720p/1080p allocations trigger heap-buffer-overflow; tile-rounded allocation passes all four. Exhaustive index calculation provides an independent check.

Live corroboration: the boot log reported `Using 1280x720 (384000) fb`; 0x384000 is exactly 3,686,400. This supports relevance to the installation without proving actual accesses or replacing binary verification. `deep-audit/final-console-check.txt` recorded console access after 22 minutes, active desktop, and no failed units.

Patch: `0001-xenos-pad-tiled-framebuffer.patch`. Tests use Mac allocations, not PowerPC DMA. All four widths are multiples of 32. DRM lifecycle, damage rectangles, cache, allocation failures, and every format still need testing. The fix programs no HDMI timing, enables no 1080p, and does not explain E10.

Source: [pinned Free60 patch](https://github.com/Free60Project/linux-kernel-xbox360/blob/498bbe1910f707ceba0535276d75a3e6ad0b7df4/patch-6.18-xenon0.30.diff), xenos_enable/xenos_blit.

## F02 — XeLL HTTP NAND buffer too small

Confirmed for studied sources and reproduced with mocked hardware. response_flash_do_data allocates sfc.page_sz bytes, but raw sfcx_read_page writes sfc.page_sz_phys. LibXenon initializes them to **512 and 528**: metadata/ECC needs sixteen extra bytes.

The harness compiles the complete XeLL HTTP file with hardware/network dependencies mocked to preserve raw-page write size. ASan reports dynamic-stack-buffer-overflow. With 528 bytes, two pages transmit correctly: **1,056 checked bytes**.

Candidate: `0002-xell-allocate-physical-page.patch`. HTTP also ignores sfcx_read_page's returned status; LibXenon's STATUS_BUSY wait is unbounded. Two matching downloads would not establish a restorable acquisition without separate geometry, ECC, bad-block, and read-status checks.

No /FLASH request was sent in this session. The running XeLL binary was not identified by code identity. This HTTP issue does not explain Linux's mmap freeze. The patch remains outside the controlled public export pending its provenance review.

Sources: [HTTP handler](https://github.com/Free60Project/xell-reloaded/blob/a36ed6b7dae940e47e472a20fd14b0616ddc8cef/source/lv2/httpd/httpd_flash.c), [SFCX geometry/read](https://github.com/Free60Project/libxenon/blob/a333adef440f28b436a667be0a4f014afce6349d/libxenon/drivers/xenon_nand/xenon_sfcx.c).

## F03 — HDMI 720p correlation

Historical GPU captures decoded offline give width 1,280, height 720, pitch 1,280 pixels, horizontal total 1,650, and horizontal offset 259, matching LibXenon's HDMI 720p table.

Of 121 non-sentinel ANA entries (excluding ffffffff/deadbeef), **109** match. Twelve differ; six at 0x20–0x25 exactly match constants written separately by xenos_init_ana_new. Other differences remain unexplained, and shared zeros are weak identity evidence.

Register naming is misleading: LibXenon intentionally writes zero to D1CRTC_V_TOTAL at 0x6020 and total_height−1 to 0x6010 despite its D1CRTC_H_SYNC_B name. The capture lacks 0x6010, so vertical total is not measured. Neither 0x6020 nor DRM's declared 60 Hz provides an actual clock measurement. 0x6024 cannot simply be interpreted as generic Radeon timing either.

The Free60 patch constructs one fixed mode from existing register dimensions. Later package identification corrects this: the installed branch instead forces 1280×720; see [binary audit](BINARY-AUDIT-2026-10-01.md). Studied LibXenon tables expose thirteen modes and no 1920×1080. A successful 1080p path needs ANA/HANA clocks, GPU timings, memory layout, and mode startup; an XRandR modeline is insufficient.

Linux ana_read_reg decodes reply bytes without validating SMC status. ANA captures retain that limitation rather than being guaranteed reads of every physical register.

Sources: [LibXenon video](https://github.com/Free60Project/libxenon/blob/a333adef440f28b436a667be0a4f014afce6349d/libxenon/drivers/xenos/xenos.c), [mode tables](https://github.com/Free60Project/libxenon/blob/a333adef440f28b436a667be0a4f014afce6349d/libxenon/drivers/xenos/xenos_videomodesdata.h).

## F04 — Audio source exists, port incomplete

Measured configuration has PCI 1414:580c but CONFIG_SOUND disabled and no bound driver. Historical snd-xenon describes analog and digital stereo S16_LE 48 kHz PCM; HDMI output was not demonstrated.

Immediate activation would be premature. It uses pci_alloc_consistent, pci_free_consistent, from_timer, and del_timer_sync, absent from examined Linux v6.18 headers. Modern coherent DMA and timer_container_of/timer_delete/timer_shutdown APIs must be selected according to actual lifetime requirements.

Other source risks: private SMC access bypasses core serialization; unbounded readiness wait; unchecked DMA allocation; handle masked before free; IRQ handler always returns IRQ_HANDLED while PCM advances through a timer. HZ=300 cannot guarantee a requested 200-microsecond cadence.

No PowerPC audio build or playback occurred here. Installing a userspace mixer/ALSA alone would not resolve these issues. Later audio reports document actual porting and remaining protocol gaps.

Sources: historical snd-xenon.c; [Linux v6.18 timer API](https://github.com/torvalds/linux/blob/v6.18/include/linux/timer.h), [DMA API](https://github.com/torvalds/linux/blob/v6.18/include/linux/dma-mapping.h).

## F05 — Network, temperatures, and interrupts

One direct snapshot reports enp1s7 at **100 Mbit/s full duplex**, zero RX/TX errors, zero collisions, and 84 dropped RX packets. Drops alone do not prove physical failure. Queried logs contained no new watchdog, timeout, Oops, or BUG at that moment; this does not establish resolution of the historical TX watchdog or load stability.

Observed peripheral IRQs arrive on CPU0; IPI/timers also use other threads. hwmon readings, in the studied driver's order: CPU **55.121°C**, GPU **49.195°C**, eDRAM **52.925°C**, board **27.898°C**. No thermal setpoint changed.

The network patch contains a fixed fallback MAC and restricts Gigabit negotiation to SiS191. These source facts do not diagnose the transmit timeout.

## Remaining work at this checkpoint

| Subsystem | Established | Missing |
|---|---|---|
| CPU/RAM/interrupts | Inventory, Linux topology, IRQ route, configuration | Cache/performance/DMA-coherence measurements; no silicon analysis |
| GPU/HDMI | Correlated 720p, reproduced allocation defect | Candidate build then DMA validation, 1080p clocks/tables, 3D acceleration |
| Audio/XMA | PCI endpoints and historical driver analysis | Tested port, physical playback, XMA decoder |
| SATA/USB/controller | Mounted disk, bound drivers, input events | Prolonged validation, proprietary protocols |
| SMC/ANA/thermal | Status commands, captures, source | Remaining register meanings and robust exchanges |
| NAND/boot | Linux stub, SFCX source, reproduced XeLL defect | Freeze cause, actual geometry, controlled acquisition, ECC, console bootloaders |
| Ethernet | Active link, counters, identified driver | Watchdog cause and controlled load validation |

Independent Linux boot remains unfinished. No new persistent exploit is established, and no boot memory was erased or programmed.
