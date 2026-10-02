# OBSIDIAN-360

**Understand the hardware. Preserve the evidence. Build a useful Linux system.**

OBSIDIAN-360 is an ongoing hardware and systems research project for one Xbox 360. It combines console measurements, source and binary analysis, original tooling, kernel changes, a controller-oriented desktop, and documented recovery procedures. The repository is written in English.

## Verified status — October 2, 2026

| Area | Established result | Important limit |
|---|---|---|
| Persistent Linux | ArchPOWER boots from the internal 120 GB drive, with ext4 root and 2 GiB swap | Startup still requires the stock Xbox chain, Rock Band Blitz, XeLL, and USB boot files |
| Current kernel | `6.18.11-xenon-obsidian-clock` booted and was identified over SSH | One confirmed boot of this version; no default-menu promotion |
| Clock calibration | Raw-clock drift improved from −2,531…−2,481 ppm to −28…+14 ppm relative to the Mac over approximately 60 seconds | This measures cadence, not absolute time accuracy; the civil clock remains about 243 seconds behind |
| Desktop | Xorg and IceWM active at 1280 × 720; user confirms the desktop responds after the new boot | No 1080p or hardware-accelerated desktop validated |
| Framebuffer | obsidian4's padded tiled allocation is active; the new clock kernel retains it | Long-duration graphics stress and all modes remain untested |
| Input | Controller receiver, xpad events, desktop launcher, and virtual keyboard have been investigated | A responsive desktop does not validate every controller gesture or repeated resize |
| Optical drive | Audio CD TOC and selected audio sectors read successfully | Just Cause 2 and Big Order DVD detection failed; the drive is not repaired |
| Audio | Candidate driver builds and host tests; analog STOP and individual status acknowledgements observed before the latest reboot | No working playback, no experimental audio driver loaded, and no proven DMA release protocol |
| Game analysis | Original Rust XEX2 structural inspector, synthetic fixtures, bounded parsing | No decryption, execution, proprietary asset distribution, or successful owned-game acquisition |
| Firmware | Boot-chain and NAND-controller research, preserved evidence of a failed flash-window read | No validated restorable raw NAND backup or independent Linux boot |

The project has **not** completed reverse engineering of the console. PCI signatures are not a complete motherboard identification; passing tests are not hardware guarantees. [Current state](docs/STATE.md) identifies the latest evidence, superseded observations, and remaining uncertainty.

## Latest measured result

The firmware advertises a 50 MHz timebase. A bounded SSH clock comparison and LibXenon source analysis supported 49.875 MHz on this console. Patch 0016 adds an explicit `xenon_tb_hz` override to the kernel's software conversion, without programming an oscillator, PLL, power setting, or thermal control.

The separately staged **obsidian_clock** entry has now booted. The kernel log and `/proc/cpuinfo` confirm 49,875,000 Hz; seven timestamp exchanges show an error interval containing zero. The conservative absolute-error bound improved by more than 88 times between the two measured windows. This is not a claim of zero physical oscillator error or long-term clock stability.

Read [calibration analysis](docs/TIMEBASE-CALIBRATION.md), [boot preparation](docs/TIMEBASE-BOOT.md), and [first-boot results](docs/TIMEBASE-FIRST-BOOT.md). Raw samples, runtime checks, and comparison hashes are in `evidence/2026-10-02/timebase-first-boot/`.

## Research guide

| Topic | Documentation |
|---|---|
| Status and priorities | [STATE](docs/STATE.md), [NEXT](docs/NEXT.md), [physical actions](docs/BLOCKED.md) |
| Objective and evidence standards | [Full objective](docs/OBJECTIVE.md), [research map](docs/RESEARCH-MAP.md), [working instructions](AGENTS.md) |
| Hardware and boot | [Architecture](docs/ARCHITECTURE.md), [build and recovery](docs/BUILD-AND-RECOVERY.md), [obsidian4 boot](docs/BOOT-PREFLIGHT-2026-10-01.md) |
| Experiment history | [Experiment ledger](docs/EXPERIMENTS.md), [research journal](docs/JOURNAL.md), [sources](docs/SOURCES.md) |
| Kernel and binaries | [Deep audit](docs/DEEP-AUDIT-2026-10-01.md), [binary audit](docs/BINARY-AUDIT-2026-10-01.md), [kernel artifacts](docs/KERNEL-CANDIDATE-2026-10-01.md) |
| SMC, LED, and SMP | [SMC audit](docs/SMC-AUDIT-2026-10-01.md), [bounded SMC post](docs/SMC-BOUNDED-POST.md), [LED lifecycle](docs/LED-AUDIT-2026-10-01.md) |
| Video and desktop | [Mode tracing](docs/VIDEO-MODE-TRACE-2026-10-01.md), [resize recovery](docs/DESKTOP-RESIZE-RECOVERY.md), [Xvfb regression](docs/DESKTOP-TESTING.md) |
| Performance | [Initial baseline](docs/PERFORMANCE-BASELINE-2026-10-01.md), [timebase calibration](docs/TIMEBASE-CALIBRATION.md) |
| Optical and games | [Drive investigation](docs/OPTICAL-DRIVE.md), [XEX2 analysis](docs/XEX2-INSPECTION.md), [Rust inspector](game-analysis/xex-inspect/README.md) |
| Audio buffers and submission | [DMA/PCM](docs/AUDIO-PCM-DMA.md), [stream polling](docs/AUDIO-STREAM-POLLING.md), [submission audit](docs/AUDIO-SUBMISSION-AUDIT.md), [ALSA adapter](docs/AUDIO-ALSA-ADAPTER.md) |
| Audio protocol and memory lifetime | [Register hypothesis](docs/AUDIO-REGISTER-HYPOTHESIS.md), [STOP](docs/AUDIO-STOP-EXPERIMENT.md), [ACK/reset](docs/AUDIO-ACK-RESET.md), [PCI isolation limits](docs/AUDIO-PCI-ISOLATION.md) |
| Original code and verification | [PCM queue](research/audio/README.md), [patch index](research/patches/README.md), [host tests](research/tests/README.md) |

## Repository layout

- `docs/`: technical analysis, results, chronology, recovery limits, and next steps.
- `evidence/`: dated observations and SHA-256 lists. A historical capture is not a live-state assertion.
- `desktop/`: Python controller-oriented launcher and desktop configuration.
- `tools/`: local SSH wrapper, collectors, artifact verifiers, and publication checks.
- `research/`: original research components, candidate patches, host tests, and source provenance.
- `game-analysis/`: original software-format inspection tools.
- `research/archive/`: historical installation/staging procedures stored as text, excluded from the public export.
- `research/blocked/`: the probe that hung the console, retained for analysis, not execution.
- `.local/` and `private/`: ignored local material, access configuration, private captures, and non-redistributable files.

## Local checks

```sh
./tools/ssh-xbox 'uptime'
python3 desktop/xbox_desktop.py --self-test
```

SSH requires the operator's existing private configuration and key outside Git. It does not discover unrelated machines and keeps host-key verification. The desktop self-test does not simulate physical controller use. Refer to the [test guide](research/tests/README.md) for source-dependent C/ALSA/PCI tests and the [build guide](docs/BUILD-AND-RECOVERY.md) for kernel prerequisites.

No universal installer is provided. Boot files, firmware, games, disc images, console secrets, and third-party binaries are not bundled. Public snapshots pass content/history checks described in [PUBLICATION](docs/PUBLICATION.md); licensing and attribution are detailed in [THIRD_PARTY](THIRD_PARTY.md).
