# Next work

## Immediate priorities

1. Done on 2026-10-07: the English research history, including E72's PCI contract result and E73's measured clock correction, is merged into `main` (the repository is public since 2026-10-12). Keep committing new results to `main`; see [PUBLICATION](PUBLICATION.md).
2. Extend the clock validation beyond one 60-second window under representative load. Keep host and console timestamps distinct. Diagnose the approximately 243-second civil-time offset separately; a corrected raw cadence does not set the date.
3. Design actual audio memory retention/isolation when STOP is not confirmed. E66 rules out relying on a callback error to retain ALSA buffers. E72 rules out treating the generic non-PCIe pending-transaction helper as a completion measurement. Cover samples, descriptors, mmap, reconfiguration, teardown, failed probe, and module reload.
4. Resolve audio final-descriptor completion, FIFO drain, address limits, reset semantics, interrupt ownership, and inherited channel state before playback. The new boot invalidates the old STOP/ACK preconditions; any hardware experiment needs a new initial-state check.
5. Continue the 1080p path through video timing/clock/ANA/HANA analysis and a recoverable USB loader experiment. Merely enlarging the desktop is insufficient.

## System stability and peripherals

- Keep **obsidian4**, **linux_hdd**, and live recovery available. E73 confirms one obsidian-clock boot and desktop responsiveness; repeat boot/rollback and load tests before changing the default.
- Verify physical resize and controller gestures after the E46/E47 X11 fix. General responsiveness is not a repeated-resize test.
- Optical: audio CD samples read; Just Cause 2 and Big Order return media absent. Compare the video DVD on another player. Console region and media health remain unconfirmed; no definitive laser diagnosis.
- Investigate TX watchdog and USB symptoms separately. Do not turn isolated observations into an unsupported common hardware diagnosis.
- Resolve the missing pacman keyring observation before further package installation. Keep signature verification enabled.
- Use E39 as a bounded initial performance reference, not a comprehensive benchmark. Evaluate Rust where a concrete component and the PowerPC target justify it.

## Lower-level research

- SMC: transaction serialization, interrupt propagation, timeouts, and IRQ contract. Do not issue unknown commands simply to reproduce a cache defect.
- SMP: validate the corrected IPI callback where it is actually used; the normal SMP path in this branch uses another function.
- NAND: identify the XeLL binary actually running, verify/fix its physical-page HTTP buffer and SFCX error handling, then establish matching raw acquisitions and ECC/bad-block checks. An HTTP response of the expected length is not a validated backup.
- Identify motherboard markings and NAND geometry visually when possible. Keep console-specific keys, keyvaults, and firmware dumps outside Git.
- Analyze this console's bootloader versions and functions after a legitimate acquisition. Structural understanding alone does not bypass their signatures.
- Direct Linux boot requires an applicable, validated independent method. Do not erase the Xbox system while the working path depends on it.
- Continue original game-format inspection tools with synthetic tests; use legitimately acquired inputs when available, without publishing copyrighted payloads.

## Evidence standard

The original objective remains broad: hardware, software, games, modernization, recovery, reproducibility, and publication. An inventory, source synthesis, or passing model is not complete reverse engineering. Electrical measurements, undocumented protocols, silicon behavior, and several physical validations remain beyond what SSH alone has established. See [OBJECTIVE](OBJECTIVE.md), [RESEARCH-MAP](RESEARCH-MAP.md), and [BLOCKED](BLOCKED.md).
