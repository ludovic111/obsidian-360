# Experiment ledger

Each row records its own checkpoint. Later experiments may supersede its status; consult [STATE](STATE.md) for the current system. Host-model success is distinct from hardware validation, and console timestamps may differ from host UTC.

## Initial installation, inventory, and fault analysis

| ID | Action | Result and evidence | Follow-up or limit |
|---|---|---|---|
| E01 | Rock Band Blitz exploit and XeLL from USB | Linux startup observed, then SSH verified | Preserve this recovery path |
| E02 | User-authorized installation on the 120 GB Hitachi drive | `/dev/sda1` ext4 root and 2 GiB swap verified after actual boot | Never replay partitioning |
| E03 | System update and desktop installation | pacman service completed with `Result=success` | SSH required a local restart |
| E04 | Xorg fbdev attempt | `no screens found` | Replaced with modesetting; original Xorg permissions restored |
| E05 | Xorg modesetting with software rendering | Verified 1280 × 720 capture | 1080p support missing |
| E06 | XTest and virtual-keyboard clicks | Terminal received `xbox360`, then `123` and Enter | Physical controller use not yet confirmed |
| E07 | XRandR request for 1920 × 1080 on None-1 | `cannot find mode 1920x1080` | Video programming needs implementation and validation |
| E08 | PCI/USB/configuration/dmesg inventory | Twelve PCI functions; evidence copied to Mac | Dated snapshot, not continuous telemetry |
| E09 | SMC status, hwmon, ANA and targeted video-register reads | Consistent replies, temperatures, 1,024 ANA bytes and 15 GPU registers | Retrieval verified in E11 |
| E10 | PROT_READ mmap of flash-controller BAR1 | SSH/ping lost; user confirmed frozen image; no validated dump | Probe blocked; cause unknown; no erase/program command sent |
| E11 | User restart and SSH reconnection | Internal ext4 root, IceWM/launcher active; SMC/ANA/GPU files retrieved with matching hashes | E10 recovered, cause unresolved |
| E12 | Controller diagnostic after reboot | js0 present, device_open=true, 4,557 events | Visible interaction still needed |
| E13 | Live inventory through standard kernel interfaces | SSH, root, desktop, temperature and network checked; `deep-audit/runtime.json` | No raw MMIO/NAND access |
| E14 | Offline GPU decoding and ANA/LibXenon comparison | HDMI 720p horizontal parameters agree; 109/121 non-sentinel ANA entries identical | Vertical total/clock not measured; six differences explained by constant writes |
| E15 | Actual xenos_blit C function under host ASan | Heap overruns reproduced at 720p/1080p; rounded allocation passes four dimensions | Candidate patch only at this checkpoint; no full build/deployment |
| E16 | Actual XeLL HTTP handler with mocked SFCX | 512/528-byte stack overrun reproduced; correction transmits two intact pages | Status/ECC unresolved; no real NAND acquisition |
| E17 | Audio driver and Linux 6.18 header review | Missing legacy APIs; DMA/SMC/IRQ risks identified | Port/build required before activation |
| E18 | Kernel provenance and pacman observation | linux-xenon 6.18.11-1; missing public-keyring warning | Binary not yet disassembled; diagnose keyring before installation |
| E19 | Final live graphics-log check | Reported allocation 0x384000 = 3,686,400 bytes at 720p; desktop active after 22 minutes | Supports F01's size finding, not proof of corruption or E10 cause |
| E20 | Acquire vmlinux/System.map and compare ELF | Local/remote hashes match; six sections match boot image, including .text | Identifies disk code, not live memory |
| E21 | Find exact package recipe; disassemble nine functions | linux-custom identified; fixed 720p and allocation calculation confirmed | Corrects earlier attribution to Free60 patch |
| E22 | DMA, PCI, and IRQ-routing analysis | 64 KiB pages; software GPU remapping; devices routed to CPU0 | Exact allocation path not instrumented on console |
| E23 | Actual IPI callback with mocked MMIO | Original loses 252/256 masks; candidate correct for 256/256; defect also in binary | Ordinary SMP path uses another function; live impact unestablished |
| E24 | Repair analysis toolchain | Old PowerPC64-tool incompatibilities worked around; multiarchitecture environment built; complete audit succeeds | Failed tools are not evidence; kernel build still pending then |

## Off-console kernel work

| ID | Action | Result and evidence | Follow-up or limit |
|---|---|---|---|
| E25 | SMC-cache source test and installed disassembly | Array overrun confirmed; four expected ASan outcomes; corrected search across 256 IDs; `smc-audit/` | No hardware messages; concurrency/waits unresolved |
| E26 | Verified archive, LLVM 16, olddefconfig, vmlinux with three Linux patches | Exit zero, ELF64 big-endian PowerPC, `6.18.11-xenon-obsidian1`; `kernel-build/` | LED warning remains; modules/image/boot unvalidated |
| E27 | Diagnose Codex interruptions and follow existing build | Structured `cyber_policy` error across five turns; local process remained live and later succeeded | Platform controls cannot be changed by project scripts; see SESSION-RECOVERY |
| E28 | LED source/disassembly review and fault injection | 21 candidate ASan/UBSan cases pass; allocation/cleanup/init/exit/send corrected; `led-audit/` | No real SMP-order or visual LED validation |
| E29 | Compile LED as a PowerPC module | Original duplicate init/exit; first fix missing SMC symbol; GPL export resolves build without diagnostics | Intermediate failures retained; module not loaded |
| E30 | Build obsidian3 kernel, modules, XeLL image | Exit zero; 65 modules and six payload sections verified; `kernel-build-obsidian3/` | Two competing-recipe warnings; no initramfs/boot validation yet |

## Boot, desktop, optical drive, and tooling

| ID | Action | Result and evidence | Follow-up or limit |
|---|---|---|---|
| E31 | Check SSH, boot configuration, and read-only USB | Installed kernel live, internal root, no failed units; boot/recovery hashes retained | `boot-preflight/runtime.json`, `usb.json` |
| E32 | Clean image recipe and build obsidian4 | Three targets exit zero without warnings; 65 modules and six sections verified | `kernel-build-obsidian4/` |
| E33 | Generate initramfs using separately staged candidate modules | depmod/mkinitcpio/lsinitcpio exit zero; 43 extracted modules match; PPC executables checked | Matching Mac copy; no boot yet |
| E34 | Stage modules and optional USB entry | 65 modules, verified kernel/initrd, saved menu; linux_hdd default and prior files intact | `boot-preflight/staging-result.json`; archived procedure, not replayable installation |
| E35 | Identify drive through sysfs/proc/logs and inspect driver fallback | DG-16D2S; unusable capabilities page; user reports opening tray but no disc reading | Cause unknown; no disc read or mechanical command sent |
| E36 | First manual boot attempt, photo and user report | Stall after /init/udev/USB detection; no confirmed obsidian4 selection; unknown kernel; no SSH | Do not blame candidate; linux_hdd recovery requested; `first-boot-observation.json` |
| E37 | Execute real video f1/f2 functions with mocked MMIO | 26 entries, 1,846 traced writes, ASan/UBSan clean; 12/13 shared HDMI720 registers match older capture | No hardware programming/clock validation; `video-mode-trace/modes.json` |
| E38 | Explicit user selection of obsidian, then SSH validation | obsidian4, internal root, desktop, no failed units, udev settle zero; framebuffer 0x398000 | `obsidian4-first-boot/`; one proven boot, E36 cause and long-term stability unknown |
| E39 | CPU/memory/boot baseline through standard interfaces and short userspace tests | Graphical target ~34.1 s, 118.5 MiB available, median SHA-256 22.553 MiB/s; `performance-baseline/` | Two systemd requests timed out; targeted follow-up succeeded; absent slabinfo made optional; no settings changed |
| E40 | Audit public export/history, create GitHub repo, verify remote tree | 187 files, two MAC redactions, 17 exclusions; parentless f9da49e and matching tree | Private history not pushed; `publication/verification.json`; repeat audit per update |
| E41 | Cross-check XEX2 primary sources and implement bounded Rust parser | Ten tests, 10,000 mutations, nine CLI cases; no reads of instrumented opaque regions; `evidence/2026-10-02/xex-inspect` | No real game, decryption, authentication, execution, or console access |
| E42 | Automate public-file and reachable-history checks | Five synthetic cases, including a marker removed from current content but retained in history | Run before commit/push; pattern scanner is not exhaustive; game-analysis added to export |
| E43 | Live check after nine hours; observe launcher for twelve seconds | obsidian4, IceWM, no failed units; unchanged I/O counters and controller file | Long uptime, not load test; no measured write saving; launcher state needs diagnosis |
| E44 | User inserts music CD; standard CDROM ioctls and samples | Twenty tracks; three separated sectors read and first repeated with same SHA-256; `optical-cd/` | Partial CD readability only; no complete-disc/DVD/game/playback proof |
| E45 | User inserts Just Cause 2; standard check and bounded TEST UNIT READY | Status 1, EIO; CHECK CONDITION, sense 02/3a/00; `optical-game/` | Media not recognized; no definitive laser diagnosis |
| E46 | Diagnose resize freeze and recover graphics processes | Forced IceWM restart restores XRandR; OpaqueMove/Resize=1, launcher restarted without Linux reboot; `desktop-recovery/` | Consistent with source XGrabServer path; physical retest still required |
| E47 | Rebuild IceWM 4.0.0; compare XTest resizes under isolated Xvfb | Old mode blocks two clients; direct mode resizes 1240×640 → 1180×600 with responses; `desktop-resize-regression/` | Initial attempt without actual resize rejected; physical confirmation still needed |
| E48 | User replaces game with Big Order DVD; two readiness checks | Same sense 02/3a/00 in spaced observations; `optical-video/` | Two unrecognized DVDs versus readable CD; exact cause and independent media health unknown |
| E49 | Diagnose Shut Down rejection; request normal administrator shutdown | CanPowerOff=challenge, no inhibitor; systemctl poweroff timer accepted; `poweroff/request.json` | Physical shutdown not directly observed; graphical button not fixed by this test |
| E50 | User compares Big Order in stock dashboard | User reports no detection; `stock-dvd/observation.json` | Exclusively Linux cause less likely; exact dashboard wording and media health unknown |
| E51 | Compile original audio and execute real calculations with mocked interfaces | Build fails: eight errors/one warning; 98 out-of-buffer geometries, five excessive loops; partial patch 0008 passes; `audio-buffers/` | No sound; lifecycle/API/DMA/SMC/ALSA negotiation remain |
| E52 | Verify Linux return and real graphical-process permissions | obsidian4 live, XRandR responds, settings persist; pkcheck allows both shutdown actions for launcher PID; `return-linux/` | Corrects SSH-subject challenge interpretation; button not triggered while user absent |

## Audio software and controlled register experiments

| ID | Action | Result and evidence | Follow-up or limit |
|---|---|---|---|
| E53 | Port audio resource ownership; inject failures into actual C | PPC object builds; twelve expected original defects reproduced; sixteen candidate cases pass; `audio-lifecycle/` | Full build tracked separately; protocol/PCM DMA/timer/concurrency unvalidated; not loaded |
| E54 | Add bounded SMC post and link complete audio variants | Nineteen SMC and eighteen resource cases; audio-lifecycle/audio-post plus 70 modules, no warnings; `smc-post/` | Not loaded; old SMC paths unbounded; protocol and PCM DMA remain |
| E55 | Move PCM to ALSA-managed DMA; test real callbacks | Twenty resource, twelve callback cases; 16,369-size regression; audio-pcm + 70 modules without warnings; `audio-pcm/` | No load; timer/concurrency/protocol remain |
| E56 | Read-only SSH check after user's return | obsidian4, 5,139.44 s uptime, no failed units, 1280×720; `audio-pcm/console-status.json` | Not visual, load, or audio validation |
| E57 | Reproduce unarmed timer/false notifications; add per-stream tracking and sync_stop | Fifteen tracking cases including controlled concurrent close, twenty resource and fifteen PCM cases; `audio-poll/` | High-resolution kernel + 70 modules verified without warnings; no load/hardware protocol proof |
| E58 | Execute real pointer/ALSA conversions; inspect ack contract and emulator | Ninety-six alternating-queue cases without new data, expected signed overflow, conditional partial publication; `audio-submission/` | Replacement must handle drain/reset; emulator insufficient for protocol validation |
| E59 | Implement original PCM queue with partial commitments, silent drain padding, bounded counter | 512 sizes, 54,008 operations, 24,544,033 compared frames; PPC link module; `audio-queue/` | No ALSA adapter/hardware access at this stage; DMA completion unresolved |
| E60 | Integrate queue, ack, drain/reset and tracking; test actual callbacks/ALSA rollback | Fifteen scenarios including 512 geometries and controlled concurrent close, twenty resource cases, queue regression; kernel + 70 modules without warnings; `audio-adapter/` | Final block completion undecoded; stagnation becomes XRUN; no load |
| E61 | Read-only SSH system check | obsidian4, 9,327.35 s uptime, no failed units, 720p; `audio-adapter/console-status.json` | Visual response/audio unverified |
| E62 | Inspect audio history/SiS registers; correct lengths | 16,384 descriptors per variant, fifteen callback and twenty resource cases; audio-bytes + 70 modules, Linux volume build without warnings; `audio-protocol/` | Hardware correspondence unmeasured; DMA completion differs from audio output; status/FIFO open |
| E63 | Separate control and acknowledgement under SiS model; compile module | 4,096 transitions per variant: 3,584 modeled losses before, zero after; fifteen callbacks, twenty resources, 16,384 descriptors; `audio-control/` | Hardware hypothesis not yet validated; module rebuilt against audio-bytes, not loaded |
| E64 | Audio PCI header then three targeted four-register reads | PCI command 0x0006, no driver; stable controls 0x1d08001c, indices 0x00008000 / 0x00009616; SSH remains; `audio-control/observer-*` | Twelve reads, zero writes; mapping fixed before execution and 31,744 cases tested; no stop/DMA/output proof |
| E65 | One guarded analog STOP write after tests/ELF32 validation | 0x1d08001c → 0x0008001d → 0x0000001d, index zero, digital unchanged, SSH responds; `audio-stop/` | Ten total reads, one write; supports halted indicator, not transaction/FIFO completion; left stopped before later reboot |
| E66 | Execute three real ALSA functions with callback errors | 144 ASan/UBSan cases; 24 detachments including twelve dynamic frees after errors; `audio-stop/free-contract.json` | Software contract, not ALSA bug; returning an error does not retain memory |
| E67 | Separately acknowledge three analog bits after 512 refusal tests | 0x1d → 0x19 → 0x11 → 0x01; digital unchanged; SSH responds; `audio-ack/ack-bit*.json` | Three writes, 24 reads; W1C observed while stopped, event meaning under playback unproved |
| E68 | Request reset from analog stopped state | Write 0x02000000, read 0x00000001; zero index, digital unchanged; `audio-ack/reset-stopped.json` | One write/eight reads; compatible with self-clear, but unchanged observation does not prove complete reset |

## Clock correction and subsequent validation

| ID | Action | Result and evidence | Follow-up or limit |
|---|---|---|---|
| E69 | Seven persistent-SSH clock samples and live device-tree read | About −0.25% over 60 s; advertised 50 MHz; compatible relative 49.8734–49.8759 MHz; `clock-calibration/` | Mac uncalibrated; no reconfiguration; console timestamps offset and old durations need context |
| E70 | Add optional timebase conversion and build independent kernel | obsidian-clock + image + 65 modules without warnings; ELF/sections/vermagic checked; `timebase-build/` | No install/initramfs/boot at this checkpoint |
| E71 | Prepare matching initramfs, modules, and optional USB entry | 16,171,806-byte image, 43 extracted modules match, 65 installed; obsidian_clock entry; linux_hdd/fallbacks preserved; remount verification; `timebase-boot/` | No scripted reboot; physical test requested; console timestamps not corrected |
| E72 | Execute seven real PCI functions under simulated access outcomes | 512 capability-start, sixteen MASTER-clear and six pending cases; failed write can coexist with success from non-PCIe wait; `audio-isolation/` | Host contract test, not DMA fence or observed write failure; later E73 header refresh matches historical capability absence |
| E73 | User boots obsidian_clock; SSH/runtime and seven-point clock comparison | Release/log/cpuinfo confirm 49.875 MHz; −28.155…+14.432 ppm versus −2,531…−2,481 before; user confirms responsive desktop; `timebase-first-boot/` | Two finite windows relative to Mac; civil clock ~243 s behind; no 1080p/audio/long-load claim; old MMIO state superseded by reboot |

## E10 incident analysis

Documentation describes a read-only flash window without ECC. That did not guarantee the chosen broad read would work on this hardware/kernel combination. The program opened `resource1` with O_RDONLY, mapped PROT_READ, and contained no erase/program command. The freeze is correlated with the read; its exact mechanism remains unknown.

The probe is retained as text in `research/blocked/` for examination. It is not an executable experiment to repeat. Prefer documented XeLL acquisition or a hardware interface with explicit result validation.

## Template for future experiments

- Precise question and hypothesis.
- Initial hardware/software state and recovery path.
- Exact action, access limits, and duration/volume bounds.
- Preserved evidence, hashes, and observed result.
- Uncertainty, system effects, and justified next step.
