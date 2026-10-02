# Licenses and provenance

The root MIT license covers original project tools, tests, and writing. It does not replace the licenses of upstream sources, excerpts, patches, or derived outputs.

- Linux patches 0001 and 0003–0007 target `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330`. Kernel-derived portions retain GPL-2.0 terms; see `LICENSES/GPL-2.0.txt`. Recorded disassemblies originate from this kernel, not proprietary games.
- Analyzed video functions come from Free60Project/libxenon commit `a333adef440f28b436a667be0a4f014afce6349d`. Full upstream sources are not bundled; the harness extracts functions from an operator-supplied local checkout. Its BSD notice is retained in `LICENSES/libxenon-BSD.txt`.
- Experimental XeLL patch 0002 and third-party initramfs copies remain outside the controlled public export pending complete provenance/license review. Their analysis is documented; no firmware is distributed.
- Tools may inspect operator-supplied local files. This grants no redistribution right to those files. Games, assets, proprietary executables, disc images, secrets, and firmware remain outside Git.
- The XEX2 parser is an original implementation of format facts cross-checked against Xenia `95a5c3ee250f80c3b9d139658649d9ffb6db3eec` and Free60. Neither Xenia binaries nor decryption code are bundled. The reference project's license notice is retained in `LICENSES/xenia-BSD.txt` for attribution.
- The X11 harness rebuilds IceWM 4.0.0 (`5ebafddba37de22fc115d6cde43cb01cfc9ef263`) from its upstream archive; its binary is not tracked. Short compiler-diagnostic source excerpts retain the upstream GNU Library GPL version 2 license, copied in `LICENSES/icewm-LGPL-2.0.txt`. They are not relicensed under the original tests' MIT license.

Upstream authors retain their rights. Repository links and exact revisions appear in `docs/SOURCES.md` and provenance reports. No upstream component is presented as an original OBSIDIAN-360 discovery or creation.

## Audio and extracted-function tests

Patches 0008, 0009, 0011, 0012, 0013, 0014, and 0015 derive from jc4360's 2009 `snd-xenon.c`, GPL-2.0-or-later, in the same linux-custom tree. Their derived portions retain that license. Resource, PCM, timer, pthread, submission, geometry, and protocol models/assertions are original; actual driver routines are extracted from the supplied source at test runtime.

Patch 0010 changes the SMC core (GPL-2.0), its header, and the audio driver (GPL-2.0-or-later). The SMC harness extracts GPL-2.0-only iopoll macros from the supplied kernel at runtime; it does not redistribute them as MIT code.

The E58 submission harness also extracts conversion helpers from the reference kernel's `include/sound/pcm.h`. Those functions retain their upstream license. AudioController files from xenon-emu/xenon were only analyzed locally; public material contains links and hashes.

E66 extracts actual ALSA stop/free functions. E72 extracts seven PCI functions. Their source bodies are not copied into the original test scripts; only extraction logic, mocks, assertions, and hashes are tracked. Kernel source licenses continue to apply to generated local test translation units.

Patch 0016 modifies the Xenon kernel platform calibration code and retains its applicable kernel license. Its original measurement tools and tests are MIT project code.
