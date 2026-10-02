# Building components and understanding the installation

This project documents one console and an existing installation. It does not yet provide a universal installer. A clone supports reading the research and building local components; it does not include games, binary payloads, firmware, secrets, or dumps needed to reproduce the original entry chain.

## obsidian4 base kernel

Prerequisites: Python 3, Docker with Linux containers, build storage, and the exact Linux source. The verified build uses `research/Dockerfile.kernel-build`, LLVM 16, and `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330`. Reference archive SHA-256: `b3e0b3a92523f334e594e07b57da58e459b4d21630ec1366aba48297da9282f0`. Do not substitute a current moving branch.

In a fresh copy of that source, apply Linux patches **0001, 0003, 0004, 0005, 0006, and 0007** from `research/patches/`, in order. Use `patch -p1 --dry-run` before applying each patch. Patch 0002 targets XeLL, not Linux. Keep source and output directories separate. Copy `evidence/2026-10-01/kernel-build-obsidian4/candidate.config` to the output directory's `.config`. This configuration comes from the studied console and is not a compatibility guarantee for other revisions.

```sh
docker build -t obsidian360-kernel:llvm16 -f research/Dockerfile.kernel-build .
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian4 --target vmlinux
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian4 --target modules
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian4 --target zImage.xenon
python3 tools/check-kernel-artifacts.py --build BUILD_DIR --output NEW_REPORT.json
```

Replace uppercase placeholders. Build targets sequentially; do not run concurrent builds against one output directory. The wrapper preserves logs and refuses to conceal an existing container. It resolves a local image identity at launch, but rebuilding the Dockerfile today does not guarantee identical packages or binaries. Versions, configuration, commands, and hashes of the verified build are in `evidence/2026-10-01/kernel-build-obsidian4/`.

This describes the components used successfully. A complete clean-room reproduction from a fresh clone has not yet been performed. [Host tests](../research/tests/README.md) list their required upstream sources. These build commands do not flash or reboot the console.

## Clock-correction variant

Apply **0016** to the obsidian4 base and use a distinct output directory and `LOCALVERSION=-obsidian-clock`. Audio patches 0008–0015 are not part of this variant. Build and verify vmlinux, modules, and zImage.xenon consistently with the same suffix. The boot entry supplies `xenon_tb_hz=49875000`; without that explicit option, the patch preserves firmware-derived conversion.

E70 verifies the image and 65 modules; E71 prepares the initramfs and optional entry; E73 verifies a hardware boot and a 60-second clock comparison. See [calibration](TIMEBASE-CALIBRATION.md), [boot preparation](TIMEBASE-BOOT.md), and [first boot](TIMEBASE-FIRST-BOOT.md). Building the files alone does not validate installation on another console.

## Existing persistent system

The verified installation uses ArchPOWER on internal ext4 with swap, a PPC64 kernel, and PPC32 applications. Unaccelerated Xorg modesetting starts through tty1 autologin/startx, with IceWM and the `desktop/` launcher. Those desktop files alone do not provision another console's packages, accounts, permissions, or disks.

Kernel modules are version-specific: `/usr/lib/modules/6.18.11-xenon-obsidian4` and `/usr/lib/modules/6.18.11-xenon-obsidian-clock`. USB directories `obsidian4/` and `obsidian-clock/` contain their respective kernels/initramfs. Match modules exactly to the kernel release. The documented mkinitcpio procedure uses a separate module root and `--nopost`, then verifies extracted contents; it does not overwrite `/boot` or the previous initramfs.

## Boot and recovery

The actual chain remains stock startup → Rock Band Blitz → XeLL → selected USB kernel → internal Linux root. Disconnect Ethernet before entering this path and reconnect after Linux appears. The menu default remains **linux_hdd**, with optional **obsidian4** and **obsidian_clock** entries and retained live recovery files.

If a candidate does not work, physically restart into a previously working entry. obsidian4 has a confirmed successful boot history. Retained files do not prove a fresh rollback test; report what was actually attempted and observed.

No software procedure currently restores a damaged NAND on this console. A suitable raw backup and independent hardware recovery method have not been validated. Do not replace NAND to experiment with direct boot. Historical partitioning scripts and the flash-window probe that froze the console remain local archives, never installation steps to replay.
