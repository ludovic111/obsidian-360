# obsidian-360 — working instructions

- Read `docs/STATE.md`, then `docs/EXPERIMENTS.md`, before any hardware interaction.
- Communicate with the user in French. Write repository documentation, comments, reports, and contribution material in English. Distinguish direct measurements, source analysis, hypotheses, and unverified results.
- Check the console's live state before presenting a historical observation as current.
- An mmap read of flash window `0000:01:08.0/resource1` froze the console. Do not rerun the archived probe or a variant until its technical cause has been explained and resolved; prefer documented XeLL acquisition or a hardware reader.
- Archived installation scripts erase disks. They document completed work and are not instructions to replay.
- Do not erase or flash NAND experimentally: a validated independent boot chain and a hardware-appropriate, restorable raw backup are missing.
- Do not touch eFuses, thermal protection, or power settings during inventory collection.
- Keep SSH keys, CPU/DVD keys, keyvaults, firmware dumps, and private working addresses out of Git; `.local/` and `private/` are ignored.
- Boot Linux through Rock Band Blitz with Ethernet disconnected; reconnect only after Linux starts. Stock firmware and temporary patches are still required.
- Access on this Mac uses `en0`; Tailscale routes not bound to this interface previously produced misleading results.
- Prefer targeted reads and existing drivers. Even a read-only MMIO access can hang hardware.
- After every experiment, update STATE and EXPERIMENTS with evidence and limitations. Never describe inventory or a documentary synthesis as complete reverse engineering.
- The GitHub repository (https://github.com/ludovic111/obsidian-360) is private. Work on `main`; do branch work in a worktree under `.claude/worktrees/<name>` (see `~/code/CLAUDE.md`) and merge it back into `main`. Push to `main` as fast-forwards only: never force-push, and never delete branches, tags or history on GitHub. `research/bootstrap` is fully merged into `main` and stays on GitHub as a record. Being private does not relax the content rules: keys, keyvaults, firmware/NAND dumps and game binaries never enter Git. The public export process in `docs/PUBLICATION.md` is historical.
- While the user is away overnight, do not intentionally reboot or perform irreversible operations; record physical actions in `docs/BLOCKED.md` and continue independent work.
