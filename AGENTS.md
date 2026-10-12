# obsidian-360 — working instructions

- Read `docs/STATE.md`, then `docs/EXPERIMENTS.md`, before any hardware interaction.
- Communicate with the user in French. Write repository documentation, comments, reports, and contribution material in English. Distinguish direct measurements, source analysis, hypotheses, and unverified results.
- Check the console's live state before presenting a historical observation as current.
- An mmap read of flash window `0000:01:08.0/resource1` froze the console. Do not rerun the archived probe or a variant until its technical cause has been explained and resolved; prefer documented XeLL acquisition or a hardware reader.
- Archived installation scripts erase disks. They document completed work and are not instructions to replay.
- Do not erase or flash NAND experimentally: a validated independent boot chain and a hardware-appropriate, restorable raw backup are missing.
- Do not touch eFuses, thermal protection, or power settings during inventory collection.
- Keep SSH keys, CPU/DVD keys, keyvaults, firmware dumps, and private working addresses out of Git; `.local/` and `private/` are ignored.
- The repository is public. Before committing a capture (`ip link`, `dmesg`, `lsblk`, network or USB listings), replace the console's MAC address, disk and USB serial numbers, LAN addresses and local host names with placeholders (`REDACTED_MAC_ADDRESS`, `REDACTED_DISK_SERIAL`, `REDACTED_USB_SERIAL`, `XBOX_LINUX_IP`).
- Boot Linux through Rock Band Blitz with Ethernet disconnected; reconnect only after Linux starts. Stock firmware and temporary patches are still required.
- On the operator's Mac, reach the console through the wired interface (`en0`); VPN routes not bound to that interface previously produced misleading results.
- Prefer targeted reads and existing drivers. Even a read-only MMIO access can hang hardware.
- After every experiment, update STATE and EXPERIMENTS with evidence and limitations. Never describe inventory or a documentary synthesis as complete reverse engineering.
- The GitHub repository (https://github.com/ludovic111/obsidian-360) is public. Work on `main`; do branch work in a worktree under `.claude/worktrees/<name>` and merge it back into `main`. Push to `main` as fast-forwards only: never force-push, and never delete tags or history on GitHub. Keys, keyvaults, firmware/NAND dumps, game binaries and personal identifiers never enter Git. The public export process in `docs/PUBLICATION.md` is historical.
- While the user is away overnight, do not intentionally reboot or perform irreversible operations; record physical actions in `docs/BLOCKED.md` and continue independent work.
