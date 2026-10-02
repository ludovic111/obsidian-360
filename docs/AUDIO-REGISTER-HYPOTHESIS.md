# Audio lengths and SiS protocol hypothesis — E62

LibXenon history resolves a choice for the software candidate: descriptor lengths become literal bytes, without subtracting one. Patch 0014 adopts that behavior and removes compensation made unnecessary by bounded geometry. No sound or live register is measured in E62.

## Historical evidence

The [December 15, 2010 LibXenon fix](https://github.com/Free60Project/libxenon/commit/30966e043f4b1e488967142bafb680286552d77f) explicitly changes size−1 to size to address noise. The studied modern revision retains it. This is stronger evidence than an unexplained difference between contemporaneous files.

The [June 25, 2011 fix](https://github.com/Free60Project/libxenon/commit/80cc0f2bcaac4827152eb4dd323cbd34cbeaeb39) also moves publication to the last complete block, supporting E59/E60's choice. The [2012 memory-placement change](https://github.com/Free60Project/libxenon/commit/34dd21465b6b9ee7ac747bb2723d8a402d299a03) is an author-reported workaround, not proof of DMA bus width. The possible first-32-MiB restriction remains unresolved; a 29-bit mask does not guarantee it.

Public evidence preserves commits, dates, diff hashes, and links. Raw API responses with identity metadata remain in .local. General web searches mostly found peripheral pages; the useful evidence came from primary commits and drivers.

## ALSA SiS correspondence

In pinned Linux `sound/pci/intel8x0.c`, SiS7012 uses ICH base definitions but swaps SR/PICB positions and counts bytes. The mapping below is a protocol-family hypothesis, not identification of Xbox's endpoint as a standard SiS7012.

| Reference field | Channel offset | Xenon source correspondence |
|---|---:|---|
| BDBAR table address | +0x00 | 32 two-word descriptors |
| CIV current index | +0x04, bits 4:0 | reg & 0x1f |
| LVI last index | +0x05, bits 4:0 | (reg >> 8) & 0x1f in word +4 |
| PICB remaining count | +0x06, 16 bits | reg >> 16 in word +4 |
| SR status | +0x08, 16 bits | Low half of historical 0x1c08001c |
| PIV prefetch | +0x0a | Byte historically containing 0x08 |
| CR control | +0x0b | RUN/RESET at word +8 bits 24/25 |

The harness compiles actual ALSA definitions and compares ten offsets/masks to Xenon values. The historical prepare constant contains the three reference status bits below and three interrupt enables above. This guides targeted observation, not proof of Xbox access effects. Writing historical PIV, read-only in the reference, still needs explanation before replacing every magic word.

## Memory completion versus emitted sound

[Intel ICH4 sections 14.2.4–14.2.7](https://www.intel.com/content/dam/www/public/us/en/documents/datasheets/82801db-io-controller-hub-4-datasheet.pdf) describe playback LVBCI as fetching the last memory buffer, not necessarily transmitting its contents. PICB also concerns memory access. DCH can indicate several halt causes; CELV is state, whereas LVBCI is a latched event requiring acknowledgement. Status bits include write-one-to-clear behavior. These definitions apply to ICH4; Xbox application remains to be tested. Rendered tables on printed pages 484 and 486 were consulted.

Design consequences, not implemented by 0014:

- Memory completion may permit buffer release without proving empty audio output. Final drain needs the downstream path, whose depth/rate remain unknown.
- Zero residual and equal indices do not identify a fresh completion. Actual LibXenon helpers tested on 32 synthetic words report zero remaining/full free space without history to distinguish startup from completion.
- Future tracking needs initial state, fresh event ownership, and association with the last published index. An old latched interrupt must not complete new work.
- Reading +8 and writing it back with RUN may also acknowledge status under the SiS interpretation. The E62 candidate still does this; E63 subsequently separates control and acknowledgement.
- Historical IRQ enables must be reconciled with polling and absence of an audio handler. PCI INTx masking alone does not establish internal status handling.

Patch 0014 changes only table lengths/geometry. It adds no final-completion decoder. `stalled_final` must still report a stream error rather than infer success from zero.

## Host measurements

Actual prepare is executed before/after for 512 buffer sizes and 32 entries each. Checks cover addresses, lengths, high flag, allocation bounds, and sentinels. Under literal-byte semantics:

| Quantity | Before 0014 | After 0014 |
|---|---:|---:|
| Descriptors checked | 16,384 | 16,384 |
| Lengths not divisible by a stereo frame | 16,384 | 0 |
| Bytes omitted per 32-entry ring | 32 | 0 |

The total modeled deficit is 16,384 bytes across tested sizes, not measured real-stream loss. The correction agrees with LibXenon history and SiS source but lacks Xbox playback validation. Fifteen adapter and twenty resource scenarios pass again.

```sh
python3 research/tests/check-audio-descriptors.py \
  --previous AFTER_0013/sound/pci/snd-xenon.c \
  --candidate AFTER_0014/sound/pci/snd-xenon.c \
  --kernel LINUX_SOURCE --libxenon LIBXENON_SOURCE --output descriptors.json
```

Pinned revisions: Linux `a293dd19311668900eb1eeb2f6cb01dcac54f330`, LibXenon `a333adef440f28b436a667be0a4f014afce6349d`. Reports retain hashes. Final ASan/UBSan executions are clean. An initial macro extraction omitted a newline between fragments; its harness compilation failure is preserved separately.

## Build and follow-up

Two initial builds exited zero but warned of under-three-millisecond timestamp skew on Mac/Linux shared files. A second identical attempt reproduced it; repeating a command does not establish a reliable build chain. Output was moved to a project-owned Linux volume, sources stayed read-only, and artifacts were exported only after completion. Commands/diagnostics remain in `evidence/2026-10-02/audio-protocol/`.

The final Linux-volume build completed October 2 at **11:09:56 UTC**, exit zero without warnings: **6.18.11-xenon-audio-bytes**, kernel and 70 PowerPC modules verified after export. No initramfs, XeLL image, installation, or boot. Final success does not erase the two earlier warnings.

Next work is status/acknowledgement control, a prepared reversible targeted observation, and measured separation of DMA consumption from output drain. E61 remained the latest hardware check during E62; no console configuration, reboot, or driver load occurred.
