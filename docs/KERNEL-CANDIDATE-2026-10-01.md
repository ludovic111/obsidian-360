# Linux kernel candidate — artifact validation

Checkpoint E30: **6.18.11-xenon-obsidian3**, compiled on the Mac in Linux ARM64 Docker using Clang/LLVM 16. This version was not installed or booted on Xbox. It was followed by obsidian4; see [boot preparation and validation](BOOT-PREFLIGHT-2026-10-01.md) and [current state](STATE.md).

## Provenance and differences

Base: `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330`, identified from the installed kernel package recipe. The complete source archive matched the recipe's SHA-256. Configuration came from the installed kernel and passed through `olddefconfig`; final configuration is preserved with each build. Image identity and patch hashes are recorded in `kernel-build-obsidian3/provenance.json`.

Five Linux patches were applied: 0001 framebuffer allocation, 0003 IPI mask, 0004 SMC cache, 0005 LED lifecycle, and 0006 SMC-ready export. XeLL patch 0002 is not part of this build. The candidate remains 720p with sound disabled.

This is not a bit-identical package rebuild: LLVM 16 replaces GCC, build time differs, and the release suffix is distinct. Installed and candidate binaries are retained outside Git.

## Results

| Check | Result | Limit |
|---|---|---|
| vmlinux build | Exit zero, no warning in its log | No boot performed |
| Selected modules | 65 files, build exit zero without warnings | No actual loading |
| Module format | ELF64 big-endian PowerPC, matching obsidian3 release | Not proof of every hardware/ABI interaction |
| Separate LED driver | Compilation and modpost pass after SMC export | Build test, not a load test |
| zImage.xenon | Exit zero, ELF32 big-endian PowerPC wrapper containing 64-bit kernel payload | Physical boot compatibility untested at this checkpoint |
| Converted payload | `.head.text`, `.text`, `.rodata`, `.init.text`, `.data`, `.notes` match vmlinux | Six-section comparison, not execution |

`arch/powerpc/boot/Makefile` defines two zImage.xenon recipes: a generic wrapper rule and a specific strip/ELF-conversion rule. Make reports the override and uses the specific rule, explaining the two build-recipe warnings without compiler errors. A copy to the upstream developer's absolute TFTP path also existed; that path was absent in our container and no file was transmitted. Patch 0007 later removes that copy and recipe collision for obsidian4.

## Reproduce local checks

A prepared source tree and output directory containing `.config` are required. Tools neither fetch sources nor deploy artifacts. Build sequentially with one consistent suffix:

```sh
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian3 --target vmlinux
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian3 --target modules
python3 tools/build-kernel.py --source SOURCE_DIR --output BUILD_DIR --jobs 4 --localversion=-obsidian3 --target zImage.xenon
python3 tools/check-kernel-artifacts.py --build BUILD_DIR --output NEW_REPORT.json
```

The verifier uses `modules.order`, checks every selected module, and writes its report only after format, release, and section validation. Hashes are in `kernel-build-obsidian3/artifacts.json`. Preserve dated logs when resuming work.

## Hardware-test gate

At this checkpoint, matching modules and initramfs still needed staging in an independent boot set, with explicit access to the previous system and live USB recovery. A verified zImage.xenon alone does not establish that complete set. No NAND, eFuse, stock firmware, or default-boot change was part of these experiments.
