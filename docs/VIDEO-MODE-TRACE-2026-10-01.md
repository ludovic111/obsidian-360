# Video mode tracing — E37

Offline source analysis, with no new console access. The local libxenon revision is `a333adef440f28b436a667be0a4f014afce6349d`. Input files are `drivers/xenos/xenos.c`, `xenos.h`, `xenos_videomodesdata.h`, and `include/xetypes.h`; their hashes are recorded in the report.

## Method and results

`tools/trace-video-modes.py` extracts the unchanged `xenos_set_mode_f1` and `xenos_set_mode_f2` functions, includes the original tables, and compiles them on the Mac under ASan/UBSan. Writes become trace entries. The only expected read explicitly models LUT completion. An access limit and unexpected-access checks terminate invalid runs. This does not emulate the GPU, physical scheduling, or clocks.

Both families contain 13 modes, each producing 71 writes: **1,846 writes total**, with no compiler or sanitizer diagnostics. No entry has a width of 1920 pixels. Evidence: `evidence/2026-10-01/video-mode-trace/modes.json`.

For HDMI 720p, these functions write 13 of the 15 registers in the earlier capture. Twelve values match; the framebuffer address differs (`0x1e000000` in libxenon versus `0x04000000` under Linux). Linux programs this address from its DMA allocation, so the difference is compatible with Linux takeover, without reconstructing the exact sequence of events.

Registers `0x6024` and `0x652c` are outside the writes in these functions and receive no equality verdict. Standard and Corona families produce identical HDMI 720p f1/f2 results; these traces cannot identify the motherboard.

## Implications for 1080p

The code writes `total_height - 1` to `0x6010`, despite its `D1CRTC_H_SYNC_B` macro name, and zero to `0x6020`, named `D1CRTC_V_TOTAL`. Decoding from names alone would be misleading. The traced 720p totals are 1650 × 750. The vertical total is source-derived, not measured: the earlier capture omitted `0x6010`.

The installed Linux driver exposes a fixed 1280 × 720 DRM mode. Activation programs the framebuffer address and enable state, not a replacement HDMI/ANA sequence. Adding a DRM resolution or increasing allocation size alone does not configure the output signal.

Further work requires separate ANA/HANA and clock analysis, followed by a complete loader/driver mode with consistent tiling, pitch, and reserved memory. A fabricated 1920 × 1080 table based only on dimensions is not ready for deployment. E37 installed and tested no 1080p mode.

## Reproduction and limitations

```sh
python3 tools/trace-video-modes.py \
  --source-dir .local/upstream/libxenon/libxenon/drivers/xenos \
  --capture evidence/2026-10-01/gpu-display-registers.json \
  --output .local/video-trace-recheck.json
```

The first harness attempt lacked the xetypes header; it is now included and hashed. Parsing of mode names containing spaces was also corrected before producing the successful report. The published results come from the completed run. The source has not been proven identical to the XeLL binary actually booted.
