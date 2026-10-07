# Observed architecture

Measurements describe this particular console. Recheck current state before a new experiment; a PCI database family label does not identify every board or chip revision.

| Block | Evidence on this console | Status and limitation |
|---|---|---|
| Xenon CPU | PVR `00710500`, six logical processors, reported 3,200 MHz | Core frequency not electrically measured |
| Timebase | Firmware DT 50 MHz; kernel conversion 49.875 MHz after E73 | Relative clock measurement supports the correction; no calibrated oscillator instrument |
| RAM | 469,568 KiB usable; 480 MiB exposed as System RAM | Not every reservation has been attributed |
| Xenos GPU | PCI `1414:5831`, revision `11`, Jasper family according to PCI database | Motherboard revision still needs visual confirmation |
| Display | 1280 × 720, 32-bit framebuffer, Xorg modesetting | Inherited video mode; 1080p and acceleration not validated |
| SMC | PCI `1414:580d`, consistent version/AV replies | Firmware not completely analyzed |
| Storage | SATA controllers `5802/5803`, 120 GB Hitachi drive, SanDisk USB | Persistent Linux root works |
| Optical drive | PLDS DG-16D2S identification; tray works by user report; audio CD TOC and samples read | Owned game/DVD not detected; mechanism, laser, firmware and media causes not isolated |
| USB | Two OHCI and two EHCI controllers | Changing ports restored keyboard operation; root cause not established |
| Controller | Receiver `045e:0291`, xpad, js0 and input events | Desktop responsiveness confirmed after E73; every gesture not independently tested |
| Network | PCI `580a`, Xenon-adapted sis190 | A TX watchdog was observed earlier; root cause remains unresolved |
| Audio | PCI `580c` and XMA `5801` | Experimental driver absent from the current kernel; no playback validated |
| NAND | PCI `580b`; existing driver only identifies the controller | No MTD access; direct flash-window reading hung the console |

## Current boot dependency

Authenticated Xbox system → Rock Band Blitz → BadUpdate → FreeMyXe/XeLL → USB kernel/initramfs → internal Linux root → desktop.

BadUpdate runs after authenticated startup. Erasing the Xbox system would remove this working entry path without disabling early boot verification. No new persistent exploit has been discovered. Documented RGH approaches require a compatible hardware intervention; ABadAvatar may reduce interaction while retaining a dependency on the Xbox system. None of those alternatives is validated as this console's independent Linux boot chain.

## Display path

GPU register dimensions `0x500` and `0x2d0` match 1280 × 720. The installed driver's branch also fixes its mode at 1280 × 720; the initially studied Free60 patch instead reads those dimensions from registers. [Binary identification](BINARY-AUDIT-2026-10-01.md) distinguishes the two sources.

The driver copies pixels into the hardware's expected tiled layout. The corrected allocation rounds up to complete 32 × 32 macro-tiles. Merely changing desktop dimensions does not program HDMI/ANA/HANA clocks and timings. Historical 1080p register captures are not a validated recipe for this console.

## Memory ownership and audio

ALSA buffer ownership, DMA addresses, CPU mappings, descriptor lifetime, and hardware completion are separate contracts. E66 demonstrates that callback errors do not prevent managed buffers from being detached or freed. E72 demonstrates that a generic PCI wait may return success without reading a non-PCIe endpoint. Neither a software flag nor an MMIO readback alone establishes that hardware has finished all memory accesses.

See the subsystem reports, [research map](RESEARCH-MAP.md), and [initial report](INITIAL-REPORT.txt) for the detailed evidence and open questions.
