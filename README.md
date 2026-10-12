# obsidian-360

Evidence-based Xbox 360 hardware research, Linux modernization and reproducible diagnostic tools.

**Status:** experimental research, in development. No releases. Latest recorded experiment: E73, October 2, 2026.

> **Legal notice.** Not affiliated with or endorsed by Microsoft. Xbox and Xbox 360 are trademarks of Microsoft. No Microsoft code, firmware, keys or games are included or distributed; use only on hardware you own.

## What it is

obsidian-360 is a research log and toolkit built around one retail Xbox 360 (Xenon) running Linux. It records what was measured on the console, what was learned from source and binary analysis, and what remains unknown, and it keeps the tools, kernel patches and tests needed to reproduce each result.

It is written for people who already run Linux on an Xbox 360, or who study its hardware: kernel and driver developers, Free60 / LibXenon contributors and hardware researchers. It is not an installer and not an end-user distribution.

Every claim distinguishes direct measurements, source analysis, hypotheses and unverified results, and points to dated evidence in `evidence/`.

## Verified status (October 2, 2026)

| Area | Established result | Important limit |
|---|---|---|
| Persistent Linux | ArchPOWER boots from the internal 120 GB drive, with ext4 root and 2 GiB swap | Startup still requires the stock Xbox chain, Rock Band Blitz, XeLL, and USB boot files |
| Current kernel | `6.18.11-xenon-obsidian-clock` booted and was identified over SSH | One confirmed boot of this version; no default-menu promotion |
| Clock calibration | Raw-clock drift improved from −2,531…−2,481 ppm to −28…+14 ppm relative to a reference host over approximately 60 seconds | This measures cadence, not absolute time accuracy; the civil clock remains about 243 seconds behind |
| Desktop | Xorg and IceWM active at 1280 × 720; the desktop responds after the new boot | No 1080p or hardware-accelerated desktop validated |
| Framebuffer | obsidian4's padded tiled allocation is active; the new clock kernel retains it | Long-duration graphics stress and all modes remain untested |
| Input | Controller receiver, xpad events, desktop launcher, and virtual keyboard have been investigated | A responsive desktop does not validate every controller gesture or repeated resize |
| Optical drive | Audio CD TOC and selected audio sectors read successfully | Two game DVDs are not detected; the drive is not repaired |
| Audio | Candidate driver builds and host tests; analog STOP and individual status acknowledgements observed before the latest reboot | No working playback, no experimental audio driver loaded, and no proven DMA release protocol |
| Game analysis | Original Rust XEX2 structural inspector, synthetic fixtures, bounded parsing | No decryption, execution or asset extraction; no real game file tested |
| Firmware | Boot-chain and NAND-controller research, preserved evidence of a failed flash-window read | No validated restorable raw NAND backup or independent Linux boot |

The project has **not** completed reverse engineering of the console. PCI signatures are not a complete motherboard identification, and passing host tests are not hardware guarantees. [Current state](docs/STATE.md) lists the latest evidence, superseded observations and remaining uncertainty.

### Latest result: timebase correction

The firmware advertises a 50 MHz timebase. A bounded clock comparison over SSH and LibXenon source analysis supported 49.875 MHz on this console. Patch 0016 adds an explicit `xenon_tb_hz` override to the kernel's software conversion, without programming an oscillator, PLL, power setting or thermal control.

The separately staged **obsidian_clock** boot entry has booted once. The kernel log and `/proc/cpuinfo` confirm 49,875,000 Hz, and seven timestamp exchanges show an error interval containing zero. This is not a claim of zero oscillator error or long-term stability. See [calibration analysis](docs/TIMEBASE-CALIBRATION.md), [boot preparation](docs/TIMEBASE-BOOT.md) and [first-boot results](docs/TIMEBASE-FIRST-BOOT.md).

## What is in the repository

| Path | Contents |
|---|---|
| `docs/` | Technical analysis, results, chronology, recovery limits and next steps |
| `evidence/` | Dated observations with SHA-256 lists. A historical capture is not a statement about the live state |
| `research/patches/` | Candidate Linux kernel patches (GPL-2.0) and one XeLL patch, with an [index](research/patches/README.md) |
| `research/tests/`, `research/audio/` | Host-side tests and original audio research code |
| `game-analysis/xex-inspect/` | Read-only XEX2 structural inspector in Rust, tested with synthetic samples |
| `desktop/` | Controller-oriented desktop launcher and X11 / IceWM configuration |
| `tools/` | SSH wrapper, collectors, artifact verifiers and the historical public-export tools |
| `research/archive/` | Historical installation and staging scripts, kept as text records. **They erase disks: do not run them** |
| `research/blocked/` | The probe that hung the console, kept for analysis only. **Do not run it** |

Boot files, firmware, games, disc images, console secrets and third-party binaries are not included.

## Getting started

There is no installer and no release. Clone the repository:

```sh
git clone https://github.com/ludovic111/obsidian-360.git
cd obsidian-360
```

Checks that run on any Linux or macOS host, without a console:

```sh
# Desktop launcher self-test (does not simulate physical controller use)
python3 desktop/xbox_desktop.py --self-test

# XEX2 inspector: tests and release build (Rust, no external dependencies)
cargo test --offline --manifest-path game-analysis/xex-inspect/Cargo.toml
cargo build --offline --release --manifest-path game-analysis/xex-inspect/Cargo.toml
```

With a console already running Linux, `tools/ssh-xbox` runs commands over SSH. It needs your own SSH configuration and key, outside Git; see `tools/ssh_config.example`.

```sh
./tools/ssh-xbox 'uptime'
```

Source-dependent C, ALSA and PCI tests need upstream kernel or LibXenon checkouts: see the [test guide](research/tests/README.md). Kernel prerequisites and recovery limits are in [build and recovery](docs/BUILD-AND-RECOVERY.md).

Reaching Linux on a retail console depends on third-party exploits and loaders that this project does not distribute. Read [STATE](docs/STATE.md) and [build and recovery](docs/BUILD-AND-RECOVERY.md) before touching hardware.

## Documentation

| Topic | Documentation |
|---|---|
| Status and priorities | [STATE](docs/STATE.md), [NEXT](docs/NEXT.md), [physical actions](docs/BLOCKED.md) |
| Objective and evidence standards | [Objective](docs/OBJECTIVE.md), [research map](docs/RESEARCH-MAP.md), [working instructions](AGENTS.md) |
| Hardware and boot | [Architecture](docs/ARCHITECTURE.md), [build and recovery](docs/BUILD-AND-RECOVERY.md), [obsidian4 boot](docs/BOOT-PREFLIGHT-2026-10-01.md) |
| Experiment history | [Experiment ledger](docs/EXPERIMENTS.md), [research journal](docs/JOURNAL.md), [sources](docs/SOURCES.md) |
| Kernel and binaries | [Deep audit](docs/DEEP-AUDIT-2026-10-01.md), [binary audit](docs/BINARY-AUDIT-2026-10-01.md), [kernel artifacts](docs/KERNEL-CANDIDATE-2026-10-01.md) |
| SMC, LED and SMP | [SMC audit](docs/SMC-AUDIT-2026-10-01.md), [bounded SMC post](docs/SMC-BOUNDED-POST.md), [LED lifecycle](docs/LED-AUDIT-2026-10-01.md) |
| Video and desktop | [Mode tracing](docs/VIDEO-MODE-TRACE-2026-10-01.md), [resize recovery](docs/DESKTOP-RESIZE-RECOVERY.md), [Xvfb regression](docs/DESKTOP-TESTING.md) |
| Performance | [Initial baseline](docs/PERFORMANCE-BASELINE-2026-10-01.md), [timebase calibration](docs/TIMEBASE-CALIBRATION.md) |
| Optical and games | [Drive investigation](docs/OPTICAL-DRIVE.md), [XEX2 analysis](docs/XEX2-INSPECTION.md), [Rust inspector](game-analysis/xex-inspect/README.md) |
| Audio buffers and submission | [DMA/PCM](docs/AUDIO-PCM-DMA.md), [stream polling](docs/AUDIO-STREAM-POLLING.md), [submission audit](docs/AUDIO-SUBMISSION-AUDIT.md), [ALSA adapter](docs/AUDIO-ALSA-ADAPTER.md) |
| Audio protocol and memory lifetime | [Register hypothesis](docs/AUDIO-REGISTER-HYPOTHESIS.md), [STOP](docs/AUDIO-STOP-EXPERIMENT.md), [ACK/reset](docs/AUDIO-ACK-RESET.md), [PCI isolation limits](docs/AUDIO-PCI-ISOLATION.md) |
| Original code and verification | [PCM queue](research/audio/README.md), [patch index](research/patches/README.md), [host tests](research/tests/README.md) |
| Repository history | [Publication history](docs/PUBLICATION.md), [licences and provenance](THIRD_PARTY.md) |

## Project status and roadmap

obsidian-360 is an active, experimental project with no release and no stability promise. Results apply to one console; nothing is validated across Xbox 360 revisions.

Known limits:

- Linux still boots through the stock system, a game-based exploit, XeLL and USB files. There is no independent boot path and no validated, restorable NAND backup.
- No audio playback, no 1080p mode and no GPU acceleration.
- The optical drive does not detect the game DVDs tested.
- The corrected clock kernel has booted once; repeat boot, rollback and load tests are pending.

Next steps, from [NEXT](docs/NEXT.md): longer clock validation under load, the audio memory-retention and descriptor-completion design needed before playback, the 1080p video timing path, and verified raw NAND acquisition.

## Contributing

Read [CONTRIBUTING](CONTRIBUTING.md), [STATE](docs/STATE.md) and [EXPERIMENTS](docs/EXPERIMENTS.md) first. Contributions are in English and must separate host simulation from console validation. Never attach keys, keyvaults, firmware or NAND dumps, game executables or assets to issues or commits.

## Licence

Original tools, tests and writing are released under the [MIT License](LICENSE). Kernel patches and kernel-derived material keep their GPL-2.0 terms, and other upstream material keeps its own licence: see [THIRD_PARTY.md](THIRD_PARTY.md) and `LICENSES/`.

## Author

Made by [Ludovic Marie](https://lu4ovic.com) ([GitHub](https://github.com/ludovic111)).
