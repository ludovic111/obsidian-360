# Off-console analysis bench

`check-memory-bounds.py` uses Python 3 and a Clang with AddressSanitizer. External sources are fetched locally into `.local/upstream/` and identified by `evidence/2026-10-01/deep-audit/sources.json`. Do not silently replace the pinned commits with the latest branches.

The copies `.local/analysis-source/xenos.c` and `snd-xenon.c` come from the files newly added in `patch-6.18-xenon0.30.diff`. `prepare-research-sources.py` verifies the commits and hashes before extracting them. The hash of `xenos.c` is also recorded in the test results.

Run from the repository root:

```sh
python3 tools/prepare-research-sources.py

python3 research/tests/check-memory-bounds.py \
  --xenos .local/analysis-source/xenos.c \
  --xell .local/upstream/xell-reloaded/source/lv2/httpd/httpd_flash.c

python3 tools/analyze-video.py \
  --ana evidence/2026-10-01/ana-720p.bin \
  --gpu evidence/2026-10-01/gpu-display-registers.json \
  --tables .local/upstream/libxenon/libxenon/drivers/xenos/xenos_videomodesdata.h
```

The first program checks four resolutions with the initial and then the rounded allocation, and the XeLL HTTP handler before/after the buffer fix. It fails if an expected overflow is not detected or if a corrected case fails. Compilation uses `-O0` to prevent elimination of graphics writes whose result is never displayed. Overflow attempts happen only inside the bench's local processes.

The second program only reads files; it programs no register. It checks the length of the capture and of the tables, then reports the differences without treating the comparison as hardware validation.

Live collection, after reading STATE and EXPERIMENTS:

```sh
./tools/ssh-xbox 'python3 -' < tools/collect-runtime.py
```

This collection uses `/proc`, standard sysfs attributes and status commands. It reads no PCI BAR, no `/dev/mem`, no NAND and no eFuses; it records no IP address or key. The outputs remain snapshots and errors are kept.

## SMC cache and compilation

`check-smc-cache.py --original SOURCE_PATH --candidate CORRECTED_PATH` compiles the real table and lookup function in a local ASan process. The known identifiers and all 256 possible values are tested in both variants. No device is opened. The experiment's paths and SHA-256 values are described in `docs/SMC-AUDIT-2026-10-01.md` and `smc-audit/cache-bounds.json`.

`tools/build-kernel.py --source SOURCE_PATH --output BUILD_PATH --jobs 4` compiles an already prepared tree, with its `.config`, in the local LLVM 16 image. It downloads, installs and boots nothing on the Xbox. Keep the log and follow the existing process before any resumption; see `docs/SESSION-RECOVERY.md`. A successful `vmlinux` does not validate the modules, the loader or physical operation.

## LED lifecycle

```sh
python3 research/tests/check-led-lifecycle.py --source CORRECTED_LED_PATH --output REPORT_PATH.json
```

The real C file is compiled with ASan/UBSan and resource/FIFO models. The 21 cases include nine allocation failures, eight LED registration failures, driver/device creation errors, probe deferral, and success with removal. The bench's headers and main are next to the script. No physical concurrency is verified; see `docs/LED-AUDIT-2026-10-01.md`.

`tools/check-kernel-artifacts.py` checks the format and version of the modules in `modules.order`, as well as six sections between the kernel and its image. The report is published only if these checks pass; it does not prove a boot.

## Video traces

`tools/trace-video-modes.py` runs the real libxenon f1/f2 C functions on the Mac under ASan/UBSan and replaces GPU accesses with a bounded trace. The standard/Corona tables are walked, then the final values are compared with an older capture. The LUT wait is simulated; there is no validation of clocks, ANA or physical video output. Command and limits in `docs/VIDEO-MODE-TRACE-2026-10-01.md`.

## Publication and executables

`python3 research/tests/check-public-audit.py` uses a temporary Git repository with dummy data. It checks unaudited content, a modified hash, a dummy token pattern, and persistence of the pattern in an older commit after the current file is cleaned. It accesses no real key.

The Rust parser and the nine tests of its CLI are described in `game-analysis/xex-inspect/README.md`. The synthetic samples are built during the tests; no commercial XEX file is needed.

## Audio: models of real functions

- `check-audio-buffers.py`: 16,369 sizes, descriptors and the old cache loop. The loop removed after 0011 represents zero candidate cases, not a validation of the real cache. JSON output on stdout.
- `check-audio-lifecycle.py`: thirteen original scenarios and twenty candidate scenarios after 0011/0012, resource accounting and error injection.
- `check-smc-post.py`: nineteen SMC scenarios with extracted functions and iopoll macros.
- `check-audio-pcm.py`: fifteen scenarios after 0012; memory areas, constraints, sizes, addresses, sequential close and rejection of the low-resolution timer.
- `check-audio-poll.py`: one earlier scenario reproduces two defects; fifteen candidate scenarios check progress, stop, and a controlled pthread interleaving during release.
- `check-audio-submission.py`: reproduces 96 cases of non-idempotent publication, an expected signed overflow in the ALSA helpers, and a partial-block case under a protocol hypothesis. It does not validate a fix.

Recipes and limits in `docs/AUDIO-PCM-DMA.md`, `docs/AUDIO-STREAM-POLLING.md` and `docs/AUDIO-SUBMISSION-AUDIT.md`. ASan/UBSan replace neither hardware tests nor general concurrency proofs. `check-kernel-artifacts.py --kernel-only` validates the kernel/modules without requiring a boot image.

`check-audio-queue.py` tests the original component in `research/audio/` with a reference content queue, 512 sizes and two interleaved streams. It compares synthetic frames and the final silence, not registers or real DMA memory. See `research/audio/README.md`.

## ALSA adapter (E60)

`check-audio-adapter.py --source CANDIDATE --kernel LINUX_SOURCE --output REPORT` extracts the callbacks of patch 0013, the real application rollback and the ALSA mmap guards. Fifteen scenarios, including the 512 sizes and a controlled concurrent close. Registers and DMA completions are simulated; a stalled last block must produce an error, not a success. See `docs/AUDIO-ALSA-ADAPTER.md`.

## Descriptors and audio register lead (E62)

`check-audio-descriptors.py` compares the prepare functions before/after 0014 over 512 sizes and 16,384 entries per variant. It compiles the real SiS register definitions and runs the LibXenon functions on simulated words. Agreement between sources demonstrates neither the Xbox protocol nor the end of sound output. Recipe and limits: `docs/AUDIO-REGISTER-HYPOTHESIS.md`.


## Audio stop and ALSA lifetime (E65/E66)

`check-audio-stop.py` tests the filter and the footprint of the single write on ordinary memory, without hardware. `check-audio-free-contract.py --kernel SOURCE --output REPORT` extracts three ALSA functions to compare the error returns with buffer release and detachment. The real behavior of the analog channel and the limits are in `docs/AUDIO-STOP-EXPERIMENT.md`. The tests do not run the hardware tool.


## Analog protocol and clocks (E67–E70)

`check-audio-protocol-step.py` checks the selector, the preconditions and the footprint of the ACK/reset writes on ordinary memory. It does not launch the hardware operations. `check-clock-analysis.py` tests the timing bounds with a known rate and invalid captures. `tools/measure-clock-drift.py --analyze CAPTURE --output NEW_REPORT` reproduces the analysis without SSH access; without --analyze, it only performs standard reads on the console. See `docs/AUDIO-ACK-RESET.md` and `docs/TIMEBASE-CALIBRATION.md`.
