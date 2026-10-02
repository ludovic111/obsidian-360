# Measured Xenon clock and opt-in correction — E69/E70

E69 measured the original drift; E70 built an independent candidate. E71 subsequently staged it and E73 booted it successfully. This document preserves the original reasoning; [first-boot results](TIMEBASE-FIRST-BOOT.md) describe the later measured improvement.

## Direct measurement

Console and Mac timestamps in the audio experiments differed by approximately 44 seconds. Seven exchanges in one persistent SSH session over about 60 seconds bracketed each remote reading with two Mac monotonic timestamps. Measured round trips were 1.37–1.94 ms. No date, frequency, NTP, or hardware setting was changed.

The console reported `timebase` as its clocksource and **50,000,000 Hz** in all three live device-tree `timebase-frequency` properties. During 60.0354–60.0384 Mac seconds, the console's CLOCK_MONOTONIC_RAW advanced 59.8864 seconds. The bounded ratio was 0.9974687–0.9975187: approximately **−0.25%**, corresponding to roughly nine seconds lost per hour if that rate persisted. Monotonic and civil clocks showed similar rates during the same minute.

Using the Mac as reference, the effective timebase compatible with the exchange bounds was **49,873,437–49,875,933 Hz**. This is neither an electrical oscillator measurement nor an absolute calibration of the Mac. **49,875,000 Hz** lies inside the interval and exactly matches the formula in [pinned LibXenon](https://github.com/Free60Project/libxenon/blob/a333adef440f28b436a667be0a4f014afce6349d/libxenon/drivers/ppc/timebase.h). The local file matched the GitHub API content hash; an initial raw web fetch failed without usable data.

A later timedatectl check reported CanNTP=yes, NTP=yes, and NTPSynchronized=yes. Those flags do not negate the measured offset or raw-clock drift and do not themselves verify time accuracy. No NTP setting was changed.

At the final sample, console-minus-Mac civil time was between −44.2806 and −44.2789 seconds. Historical captures retain their original timestamps: do not retroactively adjust every observation using one measured offset. Identify the clock's host and use uptime/monotonic counters for correlation. Historical performance durations may also be affected; exact corrections require the relevant kernel and boot context.

Evidence: `evidence/2026-10-02/clock-calibration/`. The short collector smoke test validates the new tool; its two-second duration does not replace the primary 60-second measurement. The initial seven host tests check known synthetic rates and reject incomplete or misordered captures. E73 expands these to thirteen cases for active-conversion handling.

## Software path

The Xenon platform uses `generic_calibrate_decr`, which reads device-tree timebase frequency. The examined Linux and XeLL DTS sources contain 50 MHz. The built `zImage.xenon` is an ELF conversion of the kernel; its recipe does not automatically embed the adjacent DTS. Editing that file alone would therefore not demonstrate a correction to the actual boot.

Initial `loops_per_jiffy=50000000` is a temporary delay estimate, separate from `ppc_tb_freq`. It must not be changed as though it were the clock-conversion setting.

The later read-only confirmation found `/proc/cpuinfo` timebase=50000000 and no higher-priority `ibm,extended-timebase-frequency` properties. Evidence: `clock-calibration/effective-timebase.json`.

## Candidate built in E70

Independent patch **0016** adds the early option `xenon_tb_hz=49875000`. Without an option, firmware calibration remains unchanged. `xenon_tb_hz=50000000` allows an explicit nominal-value comparison; other values are rejected. Parsing occurs before `time_init`. Xenon first calls `generic_calibrate_decr`, then replaces `ppc_tb_freq` and logs both firmware and selected values.

The option changes software tick conversion only. It does not program PLLs, voltage, or an oscillator. It is opt-in because one console's measurement does not characterize every board revision. Separately reported CPU frequency is not recalibrated by this patch.

A separate Linux build volume seeded from the proven obsidian4 objects/configuration produced **6.18.11-xenon-obsidian-clock**, its XeLL image, and **65 modules**. All three build targets finished with status zero and no warnings. Checks covered ELF formats, six payload sections, every module's vermagic, the option and calibration symbols, and exact reconstruction from the patch. Experimental audio patches are not included.

At E70 completion the candidate was only built. E71 later created its initramfs and optional USB entry; E73 then measured the running correction. These stages are distinct and must not be collapsed into a claim that the build itself demonstrated improved cadence.

## Reproduction

Read standard clock interfaces over the existing private SSH configuration:

```sh
python3 tools/measure-clock-drift.py --samples 7 --interval 10 \
  --output .local/clock-observation-new.json
```

Analyze an existing capture without console access:

```sh
python3 tools/measure-clock-drift.py \
  --analyze evidence/2026-10-02/clock-calibration/samples.json \
  --output .local/clock-analysis-new.json
python3 research/tests/check-clock-analysis.py
```

Use new output paths to preserve evidence. Exact commands, source hashes, and reconstruction results are in `timebase-build/build.json`, `timebase-build/reconstruction.json`, and `clock-calibration/sources.json` under the dated evidence directory.

The current collector records active `/proc/cpuinfo` timebase separately from the firmware DT; this matters after an override. Preserve obsidian4 and linux_hdd as recovery choices, and check `/proc/cmdline`, the calibration log, and active frequency on every new test boot.
