# obsidian4 preparation and first boot

## Initial console state

SSH was verified on October 1 at 21:21:44 UTC: `6.18.11-xenon`, `/dev/sda1` ext4 root, and no failed units. ARCH USB was mounted read-only for hashes and unmounted. Its working kernel, installed-root initramfs, and live recovery files were present.

The `/boot` initramfs and USB `linux-hdd` initramfs had different hashes. USB retained the older image used for successful startup; neither was synchronized to the other or replaced during preparation.

## Build and verification

Patch 0007 excludes zImage.xenon from the competing generic recipe and removes the upstream developer's local TFTP copy. **6.18.11-xenon-obsidian4** builds vmlinux, modules, and zImage.xenon without warnings. All 65 selected modules are verified, and six checked sections match between kernel and image. Evidence: `kernel-build-obsidian4/`.

Modules were transferred into `/var/tmp/obsidian4-preflight-20261001/root` after archive SHA-256 verification. `depmod -e -E` reported no symbol/version errors. `mkinitcpio 40` generated an image using a separate module root, exact suffix, and `--nopost`, without presets or writes to `/boot`.

The initramfs is **16,169,156 bytes**, SHA-256 `87c91934ead6d828fcaaf0bc5b6bfe78fc011c8a895b53441cdfb404f208e7b5`. Its 43 modules were extracted and individually matched to candidate modules. Checked essential executables are ELF32 big-endian PowerPC; resolved paths stay inside the extraction. The copy retrieved to the Mac has the same hash.

Xenon SATA, SCSI, block disk, ext4, OHCI/EHCI USB, sis190 networking, and zstd decompression are built into the kernel configuration. This does not replace a real boot test.

Studied LibXenon commit `a333adef440f28b436a667be0a4f014afce6349d`, `libxenon/drivers/elf/elf.c`, limits initrd size to 32 MiB; this candidate fits. The studied kboot parser limits an entry to 255 bytes; the prepared entry also fits. These source checks do not prove the complete binary identity of the running XeLL.

## Files actually staged

Post-copy verification at 21:29:51 UTC confirmed:

- Modules in `/usr/lib/modules/6.18.11-xenon-obsidian4`, without replacing the working release directory.
- USB `obsidian4/kernel` and `obsidian4/initrd` match candidate hashes.
- Previous menu saved as `Recovery/kboot-before-obsidian4.conf`.
- Optional **obsidian4** entry added; **default=linux_hdd retained**.
- Existing kernel, initramfs, and recovery hashes unchanged.
- USB synchronized and unmounted; no scripted reboot.

`boot-preflight/menu-plan.json` describes the intended menu and `staging-result.json` confirms installation. The former says `installed: false` because it predates copying; the later staging result is authoritative for the later state. The executed procedure is archived as `research/archive/stage-obsidian4.py.txt` for audit, not replay.

## User test and intermediate stall

The user reported starting the test: Ethernet disconnected, Rock Band Blitz, USB if requested, explicit obsidian4 selection in XeLL, Ethernet reconnected after Linux. The first SSH check timed out, which is compatible with a disconnected-network phase and proves neither freeze nor success.

Photo IMG_1372 shows `Run /init as init process`, systemd-udevd 259-2-arch, `Triggering uevents...`, then SanDisk and sdb1 detection. The last visible line is at 4.016710 seconds after boot. No kernel panic is visible. The user later confirmed a persistent stall and did not remember selecting an entry.

Because linux_hdd remained default, the photo cannot establish that the candidate ran. Local initramfs analysis shows the udev hook triggers events and calls `udevadm settle` before root resolution/mounting. That identifies a diagnostic point, but the photo does not distinguish a udev wait from a kernel hang and does not demonstrate disk failure.

Requested recovery was a physical shutdown, restart without Ethernet, explicit linux_hdd selection if the menu appeared, and Ethernet only after the desktop. No further remote modifications were sent during recovery. Evidence: `boot-preflight/first-boot-observation.json`; the photo is outside Git.

## Candidate boot confirmed — E38

The user subsequently found the XeLL menu, selected obsidian, and reported reaching the desktop. SSH identified **6.18.11-xenon-obsidian4**. The 21:45:47 UTC capture recorded 132 seconds uptime, internal ext4 root, no failed units, active Xorg/IceWM, 1280 × 720 XRandR output, active udev, and a queue settling within five seconds. No network watchdog or panic appeared in the collected warnings for that boot.

`Using 1280x720 (398000) fb` confirms execution of the corrected allocation path: 1280 × 736 × 4 = **3,768,320 bytes**, versus **3,686,400** historically. This validates activation of the change, not the absence of all graphics corruption. Early ioremap/rodata warnings remain; the log is not claimed warning-free.

Evidence: `evidence/2026-10-01/obsidian4-first-boot/{runtime,validation}.json`. Collection reads no BAR or NAND, sends no reboot, and changes no configuration. Menu default remains unchanged. The earlier stall's cause remains unknown; linux_hdd rollback was not tested in that sequence. At E38, visible controller use, repeated boot, and load stability still required validation. Later results, including the clock variant, are in [STATE](STATE.md).
