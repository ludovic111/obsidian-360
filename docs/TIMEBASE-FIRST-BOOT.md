# Clock-correction kernel: first hardware validation — E73

## Result

`6.18.11-xenon-obsidian-clock` successfully booted through the existing Rock Band Blitz/USB/XeLL path. The user reconnected Ethernet and confirmed the desktop responds. SSH independently identifies the release, root filesystem, graphics processes, and active clock conversion.

The correction reduces the previously observed approximately 0.25% raw-clock slowdown to an interval consistent with the Mac's cadence over a 60-second measurement. It does **not** correct the civil-clock offset, prove long-term stability, enable 1080p, or activate audio.

## Boot evidence

The runtime capture received by the host at **2026-10-02T13:54:16.568999Z** records:

- Release `6.18.11-xenon-obsidian-clock`.
- Command-line `xenon_tb_hz=49875000` and the existing internal root UUID.
- `/proc/cpuinfo` timebase **49,875,000 Hz**.
- Kernel message: `Xenon: timebase conversion 49875000 Hz (firmware 50000000 Hz)`.
- `/dev/sda1` mounted as ext4 root, 65 module files for this release.
- Xorg and IceWM running, framebuffer **1280 × 720**.
- No failed systemd units listed and no match for the targeted watchdog/panic/BUG/Oops patterns.
- No audio driver attached. The 64-byte audio PCI header matches E64, with no capability list advertised.

The console reported its own wall time as 13:50:13.119028Z and uptime as 432.43 seconds. Those wall timestamps are intentionally retained rather than silently adjusted. The user's responsiveness report is separate subjective evidence; it does not identify which input device was used or constitute a resize stress test.

## Before/after measurement

Both captures use seven timestamp exchanges across one persistent SSH session, approximately ten seconds apart. Each console timestamp lies between a host send and receive observation. Endpoint brackets produce a range rather than treating a packet midpoint as exact.

| Quantity | E69, before | E73, after |
|---|---:|---:|
| Active conversion | 50,000,000 Hz | 49,875,000 Hz |
| Host elapsed bounds | 60.035369333–60.038374041 s | 60.032962875–60.035519584 s |
| Console raw elapsed | 59.886401660 s | 60.033829256 s |
| Relative raw rate | 0.9974687459–0.9975186682 | 0.9999718445–1.0000144318 |
| Raw error bounds | −2,531.254 to −2,481.332 ppm | −28.155 to +14.432 ppm |
| Final civil-time offset | Approximately −44.28 s | −243.026452 to −243.025018 s |

The after interval includes zero frequency error relative to the Mac. Comparing the smallest pre-patch absolute error against the largest post-patch bound gives a conservative improvement factor of **88.13**. This compares two finite windows, not a long-duration oscillator calibration. The Mac itself was not independently calibrated.

After-patch CLOCK_MONOTONIC and civil-clock rates agree with the raw rate within the observation bounds. The civil-time offset is separate: changing tick conversion does not set the date or undo an offset introduced before or during boot. No NTP or clock-setting operation was performed here.

## Collector correction required by the experiment

The firmware device-tree properties remain **50,000,000 Hz**. That value is an input to the original calibration, not the active conversion after patch 0016 overrides it. The initial collector inferred effective timebase from device-tree frequency; using that formula unchanged after the patch would produce a misleading approximately 50 MHz result.

The collector now reads the kernel's `/proc/cpuinfo` timebase and records both advertised and active frequencies. It uses the active conversion for effective-frequency inference. For legacy captures it explicitly labels the device-tree assumption; E69's active 50 MHz value was separately confirmed. Missing active conversion suppresses the derived frequency rather than inventing it. Thirteen tests cover this change and invalid/incomplete input.

## Artifacts and reproducibility

All public evidence is under `evidence/2026-10-02/timebase-first-boot/`:

- `samples.json`: complete seven-point capture, identity, transport completion, and analysis.
- `runtime.json`: kernel, calibration, root, graphics, services, and limited PCI check.
- `user-observation.json`: attributed desktop responsiveness report.
- `analysis-validation.json`: thirteen host-side analysis cases.
- `comparison.json`: before/after capture hashes, error bounds, reduction factor, collector hash, and limitations.

```sh
python3 tools/measure-clock-drift.py --samples 7 --interval 10 --output NEW_CAPTURE.json
python3 tools/measure-clock-drift.py --analyze NEW_CAPTURE.json --output NEW_ANALYSIS.json
python3 research/tests/check-clock-analysis.py
```

These commands do not reconfigure clocks or hardware. A fresh capture requires working private SSH configuration. Use new output paths to retain earlier evidence.

## Recovery and follow-up

The USB menu default remains **linux_hdd**; **obsidian4** and the existing recovery images were retained. The new entry remains optional. Successful startup once does not validate repeated boot, rollback, prolonged load, or every input gesture.

The reboot supersedes the pre-boot analog STOP/ACK register state from E65–E68. No audio BAR registers were read afterward, so no current analog/digital engine state is claimed. Future audio experiments must acquire their own initial state.

Next steps are longer clock measurements under representative load, civil-clock synchronization diagnosis, repeated boot and fallback checks, and continued audio/video work. No destructive firmware change is justified by this result.
