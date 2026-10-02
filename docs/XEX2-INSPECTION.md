# Initial game-analysis component: XEX2 — E41

Source analysis and synthetic tests on the Mac. This experiment used no game files, console dumps, or hardware access.

## Sources and interpretation

The primary implementation reference is Xenia at `95a5c3ee250f80c3b9d139658649d9ffb6db3eec`: [XEX2 structures](https://github.com/xenia-project/xenia/blob/95a5c3ee250f80c3b9d139658649d9ffb6db3eec/src/xenia/kernel/util/xex2_info.h) and [GetOptHeader / loading](https://github.com/xenia-project/xenia/blob/95a5c3ee250f80c3b9d139658649d9ffb6db3eec/src/xenia/cpu/xex_module.cc). The source copy is outside Git; URLs and hashes are in `evidence/2026-10-02/xex-inspect/sources.json`. Emulator code is a reference implementation, not a measurement of this Xbox.

The [historical Free60 page](https://free60.org/System-Software/Formats/XEX/) confirms the 24-byte big-endian header and entry table. Its wording about the low key byte is incomplete for zero. Xenia explicitly distinguishes zero (direct value), one (word in the entry), and other cases (external offset). The parser preserves this distinction: interpreting a direct entry address as a file offset would incorrectly reject it.

## Read contract

| Offset | Interpretation |
|---|---|
| 0x00 | XEX2 magic |
| 0x04 | Module flags |
| 0x08 | Header end / image-body start |
| 0x0c | Reserved value, retained |
| 0x10 | Security-block offset |
| 0x14 | Optional-entry count |
| 0x18 onward | Key/value or key/offset pairs |

For external entries, size codes 2–254 count four-byte words; 255 reads a length from the block. The image body may be packed: its offset does not guarantee an immediately readable PE signature. Compression and encryption types are reported without extraction.

The security block receives bounds checks only: dimensions and descriptor count. Signatures, sensitive identifiers, and keys are not interpreted or copied. No authenticity verdict is produced. Duplicate/overlap rejection is a conservative local policy, not a proven universal format rule.

## Implementation and evidence

`game-analysis/xex-inspect` is an original Rust library and CLI with no external crates and forbidden unsafe code. Numbers are decoded from bytes rather than cast native structures. Range arithmetic uses checked u64 additions; entry counts are capped. Errors produce no partial JSON report.

Ten Rust tests passed, including 10,000 deterministic mutations and every truncation before the sample's image offset. An instrumented reader forbids opaque-region access and counts 108 bytes read from the 1,040-byte sample. Nine CLI cases passed; input bytes remained unchanged and output did not disclose the supplied path. Clippy with warnings denied, formatting, and release compilation passed. Evidence and hashes: `evidence/2026-10-02/xex-inspect/validation.json`.

This modernizes analysis tooling, not console firmware or drivers, and demonstrates no speed improvement. Real-file compatibility remains unvalidated. Further work requires legitimate samples, imports and available PE images, then instruction/system-call/frame analysis. E41 performs no game disassembly, shader analysis, or optical-drive repair.
