# Optical drive investigation

## Initial observation: 1 October 2026

At console time 21:29:44 UTC, sysfs and the kernel log identify `/dev/sr0` as **PLDS DG-16D2S**, SCSI revision `0251`, ATAPI identification `02510C`. The kernel device state is `running`. The optical drive occupies ATA1; the internal Hitachi disk occupies ATA2. The user reported that the tray opens but no discs are read.

Identification establishes communication with the drive electronics. It does not establish head movement, spindle operation, laser focus, or sector readability. This initial collection issued no eject, reset, write, or disc-read commands.

## Why Linux reports no DVD capability

`/proc/sys/dev/cdrom/info` reports speed 1 and `Can read DVD: 0`; the boot log says `scsi-1 drive`. In the exact kernel source, `drivers/scsi/sr.c:get_capabilities`, lines 838–852 at `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330`, this fallback follows a failed capabilities-page `0x2a` request or invalid lengths. It selects speed 1 and masks several capabilities, including DVD.

**This is neither a measured speed nor proof that the hardware cannot read DVDs.** The retained evidence does not distinguish which fallback condition occurred. Initial capture: `evidence/2026-10-01/boot-preflight/optical-inventory.json`.

Use standard driver requests and known-good media to compare detection, user-observed rotation, and precise sense errors. Media condition, optics, mechanics, firmware, and transport remain distinct hypotheses. Do not adjust the laser or flash firmware speculatively. Sector readability and game execution require separate validation.

## E44: readable audio CD, 2 October

The user inserted a music CD; prior readability on another device was not confirmed. Under `6.18.11-xenon-obsidian4`, `CDROM_DRIVE_STATUS` returned 4 (`CDS_DISC_OK`), and `CDROMREADTOCHDR` reported tracks 1–20. TOC entries were all audio, with lead-out at LBA 263934.

The original `tools/inspect-audio-cd.py` uses standard read-only CDROM ioctls. After reading the TOC, it read one 2,352-byte sector at each of LBA 150, 123793, and 249235. All reads succeeded with nonzero data. A repeated read at LBA 150 produced the same hash. Measured monotonic call durations were 0.091–0.207 seconds; this was not a throughput benchmark. Mac and console wall clocks differed and are recorded separately.

**Direct measurement:** the CD read path worked for these samples, disproving an absolute inability to read any medium at that time. This does not validate the entire CD, DVD reading, Xbox authentication or execution, or system audio output. No adjustment, flashing, reboot, or hardware repair occurred; kernel audio remained disabled.

Reproduction with an audio CD inserted:

```sh
timeout -k 2 45 python3 tools/inspect-audio-cd.py
```

The tool accepts only optical `/dev/sr0`, limits reads to four sectors, and stores/publishes no audio payload. A process timeout cannot guarantee immediate interruption of blocked kernel I/O. ABI references are `include/uapi/linux/cdrom.h`, `drivers/scsi/sr_ioctl.c`, and `drivers/cdrom/cdrom.c` at the kernel revision recorded in `optical-cd/method.json`.

## E45: Just Cause 2 not detected

After the CD was replaced with the Xbox 360 game Just Cause 2, CDROM status became 1 (`CDS_NO_DISC`). A standard LBA 0 read failed with EIO; no game data was recovered. A data-free `TEST UNIT READY` returned SCSI status 2, host_status 0, driver_status 8, and fixed sense `02/3a/00`: NOT READY / MEDIUM NOT PRESENT. The pinned kernel labels this in `drivers/scsi/sense_codes.h:461`.

The previous sysfs capacity still described the audio CD; **it is not the game's capacity**. Kernel read-ahead also means a 2,048-byte pread does not imply exactly one sector requested from the drive.

Measured conclusion: partial CD readability and an undetected game DVD in this trial. Disc condition, DVD detection/focus, other optical or mechanical components, and firmware remain possible causes. Neither a definite laser fault nor an authentication failure was established. No firmware changed. A known-good video DVD is a useful next comparison.

```sh
timeout -k 2 15 python3 tools/optical-ready.py
```

Five offline sense-decoding tests are in `research/tests/check-optical-sense.py`.

## PAL/NTSC region hypothesis

The user reported PAL markings on the Just Cause 2 box and other Xbox 360 game boxes. These are user observations of packaging, not extracted disc regions or a measured console region. The archived [Microsoft KB909819](https://ftp.zx.net.nz/pub/archive/ftp.microsoft.com/MISC/KB/en-us/909/819.HTM) includes region matching among troubleshooting checks; it does not establish an incompatibility here.

The [official T10 ASC/ASCQ table](https://www.t10.org/lists/asc-num.txt) defines `3a/00` as medium not present, not an explicit region error. **Inference:** readable CD samples and an absent game DVD point more directly toward medium recognition than a launch-region restriction. Region compatibility remains unmeasured, and the precise fault is unknown. Packaging alone does not justify a region change or NAND access.

The user bought the console and games together second-hand and does not know whether these games ever worked on this console. That history does not establish compatibility.

## E48: Big Order video DVD

The user replaced Just Cause 2 with a Big Order anime DVD. Two TEST UNIT READY requests approximately 59 Mac-clock seconds apart returned the same `02/3a/00`, with host_status 0. No video content or additional sectors were read. Prior readability elsewhere was not confirmed. The user heard brief rotation followed by stopping, similar to the game; repeated clicking was not confirmed. This is an auditory observation, not a spindle-speed measurement.

The comparison now comprises readable audio-CD samples and two undetected DVDs, one game and one video. An explanation specific to Just Cause 2 fits this evidence less well. T10 distinguishes `6f/04` (DVD region mismatch) from `3a/00` (medium absent), but that does not guarantee perfect firmware reporting, identify a failed component, or reveal the Xbox region. Before physical intervention, verify the DVD elsewhere and compare stock-dashboard behavior. Evidence: `evidence/2026-10-02/optical-video/`.

## E50: reported stock-dashboard result

The requested check was a clean Linux shutdown, power-on, and observation of the stock disc tile without launching Rock Band Blitz. In that context, the user reported that nothing was detected. No screenshot or exact dashboard message was captured. A Linux-only cause becomes less likely, but the report does not identify the failed component or prove compatible regions. No repair is claimed. Evidence: `evidence/2026-10-02/stock-dvd/observation.json`.
