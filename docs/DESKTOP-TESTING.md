# Offline controller resize regression test

This test reproduces an X11 deadlock in a disposable Linux container. It does not access the Xbox, Mac input devices, or an existing display server. It runs the real `desktop/xbox_desktop.py` and its X11 input class; it does not emulate joydev packets.

## Build the environment

Requirements: running Docker, curl, and approximately 1 GB of free space. From the repository root:

```sh
mkdir -p .local/desktop-test-build .local/desktop-resize-tests
curl --fail --location \
  https://codeload.github.com/ice-wm/icewm/tar.gz/5ebafddba37de22fc115d6cde43cb01cfc9ef263 \
  --output .local/desktop-test-build/icewm-source.tar.gz
cp research/Dockerfile.desktop-test .local/desktop-test-build/Dockerfile
docker build -t obsidian360-desktop-test:icewm4 .local/desktop-test-build
```

The Dockerfile verifies the upstream archive SHA-256 before extraction and compilation. The build context contains only that archive and the Dockerfile. Do not use the whole repository as context: it contains Git-ignored private data. The test binary is aarch64 on this Mac and is not installed on the Xbox. The base digest, image identity, and package versions are recorded in `evidence/2026-10-02/desktop-resize-regression/environment.json`. APT packages are not pinned to a snapshot, so bit-for-bit rebuilds are not guaranteed.

## Run

```sh
docker run --rm --name obsidian-resize-regression \
  --network none --cpus 2 --memory 512m --pids-limit 128 \
  --mount "type=bind,source=$PWD/desktop,target=/workspace/desktop,readonly" \
  --mount "type=bind,source=$PWD/research/tests,target=/workspace/research/tests,readonly" \
  --mount "type=bind,source=$PWD/.local/desktop-resize-tests,target=/output" \
  obsidian360-desktop-test:icewm4 \
  python3 research/tests/check-desktop-resize.py --output /output/result.json
```

Each case creates its own Xvfb using `-displayfd`, IceWM, and launcher. Inherited DISPLAY is removed, X11 TCP is disabled, and no host X11 socket is mounted. Cleanup terminates only the created process groups. Forced cleanup is intentional because the old configuration is expected to hang.

The test sends the standard `_NET_WM_MOVERESIZE` message for bottom-right resizing. The real X11 class then moves by −60/−40 and releases the button. It waits for a synchronous response and queries geometry through an independent client. Both dimensions must actually decrease: process liveness or a response without resizing is insufficient.

Expected result: `passed: true`, old mode timed out, new mode responsive with a smaller window. Nonzero exit or incomplete output is a failure to investigate, not permission to claim validation.

## Evidence and limits

The first attempt assumed a border position, produced no resize, and failed. It is preserved in `first-attempt.json`; the corrected run is `validation.json`. Compiler diagnostics are in `build-diagnostics.log`, alongside retained theme/font logs. No warning-free build is claimed.

The mechanism is reproduced under Xvfb with IceWM 4.0.0. This does not validate Xenos, the PowerPC kernel, physical controller input, every window operation, or console redraw cost. It does not replace the requested manual console test.
