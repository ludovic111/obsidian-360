# Desktop resize freeze and recovery — 2 October 2026

## Direct observations and user report

After more than nine hours, Linux still answered SSH and no systemd unit was failed. That did not prove desktop responsiveness: controller state had not changed since the previous day. XRandR timed out, Xorg waited in epoll, and IceWM in poll. The user corrected an initial responsiveness report and said the image had frozen during controller-driven window resizing.

## Recovery

The launcher did not exit on SIGTERM; forcibly stopping it did not restore XRandR. IceWM's documented restart SIGHUP was also insufficient. Killing only the window manager caused icewm-session to start a replacement. XRandR then responded at 1280 × 720 while Xorg and Linux remained running. Linux was not rebooted. Old synthetic button states were released before relaunching the controller bridge, which reopened the controller and updated its status file.

## Source analysis and configuration fix

Installed preferences were `OpaqueMove=0` and `OpaqueResize=0`. In [IceWM 4.0.0 movesize.cc](https://github.com/ice-wm/icewm/blob/4.0.0/src/movesize.cc), `startMoveSize` selects the outline paths for these settings. `outlineResize` holds `XGrabServer` while waiting for events. Other clients, including the controller bridge's XTest connection, can therefore block while the window manager waits for their events. The observations and recovery fit this mechanism; the original process stack was not captured and the freeze was not deliberately reproduced on the console.

The installed fix uses `OpaqueMove=1` and `OpaqueResize=1`, avoiding those outline branches. Reusable configuration: `desktop/icewm-controller.conf`. The previous console configuration is saved as `~/.icewm/preferences.before-resize-fix-20261002`. More redraws during movement are a possible cost; no speed improvement is claimed. No kernel, GPU, or firmware change was made.

The [IceWM manual](https://ice-wm.org/man/icewm.html) documents SIGHUP, and the [icewm-session manual](https://ice-wm.org/man/icewm-session.html) documents restart after a crash. Evidence and limitations are in `evidence/2026-10-02/desktop-recovery/`. A physical resize test remained pending. Periodic status-file writes may be optimized separately, but measurements from the frozen launcher are not a valid performance baseline.

## E47: isolated reproduction

IceWM 4.0.0 was rebuilt from `5ebafddba37de22fc115d6cde43cb01cfc9ef263` on aarch64 and tested in two disposable Xvfb servers. The real repository launcher and its X11/XTest class supplied synthetic input. `_NET_WM_MOVERESIZE` initiated bottom-right resizing, followed by relative motion and button release. E47 accessed no Xbox hardware.

| Setting | Controller request after release | Independent X11 client | Final dimensions |
|---|---|---|---|
| OpaqueResize=0 | Timed out after 3 s | Timed out after 1 s | Could not query |
| OpaqueResize=1 | Responded | Responded | 1180 × 600, reduced from 1240 × 640 |

The blocking mechanism was reproduced off-console, and the configuration avoided it in this scenario. An earlier assumed-border-coordinate attempt caused no resize and correctly failed despite responsive processes; it is retained in `first-attempt.json`. The final test requires both dimensions to decrease and an independent client to respond.

This is not PowerPC emulation or validation of Xenos, the physical joystick, or every window action. Xvfb uses Xorg 21.1.7 versus console Xorg 21.1.24. Upstream compilation retained optional-feature warnings and two GCC diagnostics in network-applet string handling; fallback-theme font warnings are also retained. No warning-free upstream build is claimed. The console configuration disables the network applet. Detailed reproduction: `docs/DESKTOP-TESTING.md`.

The later E73 user confirmation establishes general desktop responsiveness after the clock-kernel boot, not completion of the specific physical resize test.
