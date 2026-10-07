# Installed kernel, DMA, and interrupts

This is the E20–E24 checkpoint. Later builds and hardware boots are recorded separately; statements about unbuilt candidates below describe this historical stage.

## Evidence chain

Installed package: `linux-xenon 6.18.11-1`. ArchPOWER recipe commit `b166195754bd59ec1cbb4392dee6ae0f1ded87e4` selects **techflashYT/linux-custom**, commit `a293dd19311668900eb1eeb2f6cb01dcac54f330`, which is not exactly the initially examined Free60 patch.

Files were acquired once and local/remote hashes compared:

| Artifact | SHA-256 |
|---|---|
| Symbol-bearing vmlinux | `a51fb462247102de87b49f3047bb7b96dc8c8c40a5a488cc98ad8f2a919d95aa` |
| System.map | `6e67b74e4e568c03c18874ccb222905ab13b003d16cac3eb7b85c196363e0f90` |
| Boot vmlinuz | `a499ab2816bd5a94843442b0a8b89d18af4c1f98f4f264a83b0da5940c8bed66` |

The boot image has an ELF32 PowerPC header; vmlinux is ELF64 big-endian ABI v2. This does not mean the kernel executes as 32-bit: `.head.text`, `.text`, `.rodata`, `.init.text`, `.data`, and `.notes` match byte-for-byte. The local boot image matches `/boot/vmlinuz-linux-xenon`; examined System.map function addresses also match the /proc/kallsyms capture.

Evidence under `evidence/2026-10-01/binary-audit/`: `remote-provenance.txt`, `elf-comparison.json`, `source-provenance.json`, `session-check.json`, and disassemblies. Full binaries remain in ignored `.local/binaries/`. Recipe: [pinned PKGBUILD](https://github.com/kth5/archpower/blob/b166195754bd59ec1cbb4392dee6ae0f1ded87e4/kernels/powerpc/linux-xenon/PKGBUILD).

## Correcting the earlier video attribution

Free60's patch reads GPU dimensions. The package's actual branch instead constructs a constant **1280 × 720** mode in xenos_load without reading dimensions from registers. Disassembled xenos_pci_probe loads 720 and 1280 at `0xc0000000007465c0` and `0xc0000000007465c8` respectively.

The inventory's register reads remain valid hardware observations, but did not describe this binary's mode construction. Even a loader leaving GPU in 1080p would therefore require a matching kernel mode change and validated GPU/ANA/HANA programming. Source: [package-selected xenos.c](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/drivers/gpu/drm/tiny/xenos.c).

## Framebuffer allocation confirmed in binary

In xenos_enable, instructions at `0xc000000000746328` and `...632c` multiply width, height, and bytes/pixel; `...6338` passes the result to dma_alloc_attrs without tile rounding. Tiled copying is inlined into xenos_update.

This connects the host-ASan defect to the installed code. It still does not prove actual console corruption or E10 causality.

Page size is measured as **65,536 bytes**, consistent with CONFIG_PPC_64K_PAGES=y. dma_direct_alloc rounds to that granularity, also visible in disassembly. The DMA pool path uses a PAGE_SHIFT-granular gen_pool. Graphics requests allocation with zero GFP flags; the exact path depends in part on device DMA coherence.

| Dimensions | Driver request | 64 KiB rounding | Calculated maximum blit end | Beyond page-rounded size |
|---|---:|---:|---:|---:|
| 1280 × 720 | 3,686,400 | 3,735,552 | 3,766,272 | 30,720 |
| 1920 × 1080 | 8,294,400 | 8,323,072 | 8,354,816 | 31,744 |

These are conditional calculations for a page-rounded allocation, not measurements of live DMA allocation. Higher-order pages may reserve more. Allocator rounding never justifies writing beyond the requested driver size; the candidate explicitly rounds dimensions to macro-tiles.

Sources: [direct DMA](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/kernel/dma/direct.c), [DMA pool](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/kernel/dma/pool.c).

## IPI destination-mask defect

xenon_ipi_send_mask computes `(mask << 16) & 0x3f`, whose low six bits are necessarily zero. The binary confirms dest is not read and only priority is written. Candidate patch 0003 changes it to `(mask & 0x3f) << 16`, matching xenon_cause_IPI's encoding.

Actual C with mocked MMIO covers 64 masks and four priorities. The original loses destinations in **252 nonzero-mask cases**; the candidate satisfies all **256**. This does not validate electrical interrupt delivery.

The ordinary SMP path, smp_xenon_message_pass, calls the separate xenon_cause_IPI, which retains destinations. No session call to the faulty callback was established. Do not claim general SMP failure, network-watchdog explanation, or NAND-freeze causality.

Patch: `research/patches/0003-xenon-preserve-ipi-target-mask.patch`; test: `research/tests/check-ipi-mask.py`; result: `binary-audit/ipi-mask-test.json`. It was not deployed at this checkpoint, but later entered the booted obsidian4 base.

Sources: [interrupt.c](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/arch/powerpc/platforms/xenon/interrupt.c), [smp.c](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/arch/powerpc/platforms/xenon/smp.c).

## Software topology choices versus wiring

GPU appears as Linux `01:0f.0` because xenon_pci_ecam_map_bus maps it to bus 0, slot 2 for ECAM. The driver also forces Linux's first bus to 1 to work around incomplete bridge handling. Linux inventory is a remapped view, not raw physical topology.

Peripheral IRQs reach CPU0 because iic_unmask calls connect_pci_irq with CPU 0. The observed lack of distribution across six threads is consistent with that policy. No affinity or interrupt register was changed. Source: [Xenon PCI](https://github.com/techflashYT/linux-custom/blob/a293dd19311668900eb1eeb2f6cb01dcac54f330/arch/powerpc/platforms/xenon/pci.c).

## Analysis toolchain repair

Installed tools did not guarantee target support: Xcode LLVM lacked PowerPC, and the console's objdump rejected ELF64. This Mac used legacy Docker without buildx; the initially requested big-endian cross-GCC packages were unavailable for its ARM64 host.

The validated path uses Debian ARM64 with binutils-multiarch, LLVM, Clang, and LLD. `tools/audit-session.py` checks binary hash, ELF architecture, Docker engine/image, and actual supported formats before disassembly. It neither downloads nor restarts acquisition. Outputs are atomically published after success; structured reports retain state and errors.

One complete run produced nine disassemblies. The ten earlier memory tests remain distinct from the IPI test. At E24, no modified full kernel had yet been built; having Clang did not prove this branch would compile without changes.

```sh
docker build -t obsidian360-toolchain:bookworm - < research/Dockerfile.toolchain
python3 tools/audit-session.py --disassemble --output evidence/2026-10-01/binary-audit/session-check.json
```

The first command prepares the environment. `toolchain-image.txt` and `toolchain-packages.txt` record the built image/packages. A Debian tag plus recorded identity does not promise future bit-identical reconstruction. Preserve prior report files before repeating historical output paths.
