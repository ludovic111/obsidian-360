# Clock-correction boot preparation — E71

Kernel `6.18.11-xenon-obsidian-clock` was prepared separately on the internal disk and USB drive. It retains obsidian4 with optional patch 0016, excluding experimental audio changes. `xenon_tb_hz=49875000` changes tick conversion, not oscillator or voltage programming. See [calibration](TIMEBASE-CALIBRATION.md) for the baseline and limits.

This report covers staging. The subsequent successful boot and measurement are documented separately in [E73](TIMEBASE-FIRST-BOOT.md).

## Build and inspection

Before preparation, SSH responded under obsidian4, with internal ext4 root, a separate ARCH vfat USB partition, and no listed failed units. The 65 candidate modules and kernel image were packaged from E70 after individual hash comparisons. The received archive matched its hash and was extracted into a new work directory without replacing active modules.

`depmod -e -E` and `mkinitcpio --nopost` succeeded without image-build errors or warnings. Configuration used base, udev, modconf, block, filesystems, keyboard, and fsck hooks, with zstd level 1. The image analysis command initially emitted a `tput` display diagnostic because TERM was absent; generation still succeeded, and later inspections used TERM=dumb.

The initramfs is **16,171,806 bytes**, below the studied LibXenon 32 MiB limit. SHA-256: `0f2bea5579d397127a75b9daa27aa724a24deb2d2be3984749de64c16e937eef`. Extraction contains only the expected module-version directory and **43 modules**, each hash-matched to E70. Six essential programs are ELF32 big-endian PowerPC, with resolved paths confined to the extracted image. `/init` and the udev hook are present.

Kernel image SHA-256: `85b39fd069950625ad6e6cb8f5c17c71aa2755c7d325d3459cf848b69fa241cb`. Hashes and exact commands are in `evidence/2026-10-02/timebase-boot/`.

## Staged layout

- Modules: new `/usr/lib/modules/6.18.11-xenon-obsidian-clock` directory; all 65 hashes rechecked.
- USB: `obsidian-clock/kernel` and `obsidian-clock/initrd`.
- Menu: new **obsidian_clock** entry, 168 bytes, reusing obsidian4's root parameter and adding the 49,875,000 Hz conversion option.
- Previous menu: `Recovery/kboot-before-obsidian-clock.conf`.
- Default: **linux_hdd unchanged**; obsidian4 and existing recovery entries retained. Eight pre-existing boot/recovery files match their pre-copy hashes.

A second read after unmounting and remounting read-only confirmed the new files, fallback files, and menu. The Mac copy of the initramfs also matched. SSH still reported obsidian4 and no failed units at the end of staging.

The menu was changed only after verifying both new boot files and the installed modules. Its temporary file was synchronized and renamed, followed by filesystem synchronization and unmount. This reduces incomplete-copy exposure; it does not guarantee recovery from every physical storage failure. Exact procedures are archived as text under `research/archive/` for audit, not automatic replay.

## Physical boot procedure

1. Shut down normally and disconnect Ethernet.
2. Start Rock Band Blitz, choose USB if requested, and explicitly select **obsidian_clock** in XeLL.
3. Reconnect Ethernet only after the Linux desktop appears.
4. Verify the release, command line, calibration message, root and services through SSH; repeat the seven-sample, 60-second E69 measurement.

If the candidate stalls, physically restart into **obsidian4**, which previously reached the desktop. linux_hdd and live recovery are also retained, but their presence is not a new boot-validation result. Staging scripts issue no reboot and change no firmware, NAND, or eFuses.

At E71 completion only the files were ready. E73 subsequently confirmed boot, desktop responsiveness, and improved cadence. Preserve console-issued report timestamps as recorded and interpret them alongside host timestamps because E69 established a clock discrepancy.
