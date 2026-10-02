# Initial obsidian4 performance baseline — E39

Direct measurements at console time 21:50:15 UTC on 1 October, after SSH identity verification: `6.18.11-xenon-obsidian4`, internal ext4 root. No settings changed and no packages were installed. Desktop and SSH remained active during collection.

| Measurement | Value and scope |
|---|---|
| systemd boot completion | 34.129 s: 16.133 s classified as kernel + 17.996 s userspace |
| Graphical target | 34.125268 s from monotonic origin, confirmed by systemd property |
| First /init | 3.157328 s in dmesg |
| ext4 root mount | 14.262733 s in dmesg |
| Exposed total memory | 469,568 KiB = 458.5625 MiB |
| Available memory before collection | 121,344 KiB = 118.5 MiB |
| Swap used before collection | 27,520 KiB; zswap enabled |
| Kernel page size | 65,536 bytes |
| Exposed CPU topology | Six logical CPUs; SMT siblings 0–1, 2–3, 4–5; package_id −1 means unspecified |
| SHA-256, three samples | Median 22.553 MiB/s; range 22.551–22.557 |
| Python bytearray copy, three samples | Median 136.225 MiB/s useful data; range 122.407–136.265 |

The systemd interval excludes the dashboard, game, and XeLL; `graphical.target` does not measure the first visible desktop. The approximately 11.105 seconds between /init and root mount cover multiple stages and cannot all be attributed to udev. The cpuinfo value of 3.2 GHz is not a measurement of instantaneous frequency.

Proportional resident memory (PSS) was 22,625 KiB for Xorg, 21,303 KiB for IceWM, 2,141 KiB for icewm-session, and 22,440 KiB for pre-existing Python PID 436. Collector PID 708 added 13,396 KiB; this is not permanent desktop overhead. Xorg also had 10,304 KiB in swap. Samples were sequential, not atomic; shared RSS values must not be naively summed.

## Method and limitations

`tools/collect-baseline.py --workloads` reads proc/sysfs and systemd properties. Hashing uses installed `_hashlib` (OpenSSL 3.6.3), an 8 MiB buffer, and four passes per sample. Its SHA-256 result was independently recomputed on the Mac. The copy workload includes Python and allocation overhead and does not represent raw RAM bandwidth. No affinity, frequency change, or sustained stress was applied.

The four hwmon readings changed from 55.484 / 49.542 / 53.285 / 28.082 °C to 55.507 / 49.503 / 53.238 / 28.054 °C. These describe only this short run, not sustained thermal stability. No systemd units were failed afterward.

`systemd-analyze blame` and `critical-chain` each timed out after 12 seconds; failures are retained. `tools/collect-boot-detail.py` subsequently obtained target timestamps, not a complete critical chain. Its first run failed because `/proc/slabinfo` was absent; that interface is now optional. `CONFIG_SLUB_DEBUG` is disabled, and the pinned `mm/slab_common.c` gates slabinfo creation on that option. No kernel rebuild was requested for this collection.

Evidence in `evidence/2026-10-01/performance-baseline/` includes the initial report, targeted follow-up, tool hashes, and intermediate failure. From the Mac:

```sh
./tools/ssh-xbox 'python3 - --workloads' < tools/collect-baseline.py
./tools/ssh-xbox 'python3 -' < tools/collect-boot-detail.py
```

Later E69 identified a console timebase conversion error; these historical durations retain their original clock basis. No speculative retroactive correction has been applied. E73 separately measures the corrected clock; see `docs/TIMEBASE-FIRST-BOOT.md`.

Future comparisons should isolate initramfs waiting, unreclaimable kernel memory, launcher overhead, and framebuffer blitting. E39 alone demonstrates no before/after performance gain.
