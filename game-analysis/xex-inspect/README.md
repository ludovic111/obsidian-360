# obsidian-xex-inspect

Read-only XEX2 inspector in Rust, with no external dependencies or `unsafe` code. It runs on the host without connecting to a console. Tests construct synthetic samples in memory or temporary directories; no game is required.

```sh
cargo test --offline --manifest-path game-analysis/xex-inspect/Cargo.toml
cargo clippy --offline --manifest-path game-analysis/xex-inspect/Cargo.toml --all-targets -- -D warnings
cargo build --offline --release --manifest-path game-analysis/xex-inspect/Cargo.toml
python3 game-analysis/xex-inspect/tests/check_cli.py --binary game-analysis/xex-inspect/target/release/obsidian-xex-inspect
game-analysis/xex-inspect/target/release/obsidian-xex-inspect LOCAL_FILE_PATH
```

The recorded host used Rust 1.99.0. No PowerPC build or performance comparison is claimed. Replace the placeholder with a legitimately obtained local regular file and keep it outside Git. JSON goes to stdout and errors to stderr. Exit status is 0 for a successful structural check, 2 for an error.

## Inspection scope

The inspector reads the main header, direct/fixed/variable optional entries, declared security-block dimensions, page-descriptor count, compression/encryption types, and execution metadata where present. Bytes are explicitly decoded as big-endian; file size comes from the opened descriptor.

Reads use checked offsets and small fixed arrays. No allocation scales with a declared payload size; collections are capped at 4,096 entries. Duplicate keys, optional-block overlaps, aliases into security data, and ranges outside the headers are rejected. These are conservative inspector policies, not proof that every legitimate variant obeys them.

Unknown fields remain descriptive. No raw external-block payload, LAN key, signature, encryption key, or program body is printed. Instrumented tests verify that opaque sample regions remain unread. Concurrent modification of an inspected file is unsupported; use a stable local copy.

## Limitations

`structural_check: passed` does not mean a valid signature, a complete executable, or a compatible game. Signatures, individual descriptors, imports, PE image, shaders, and assets are not validated. XEX1 is explicitly rejected. Unknown compression/encryption types remain numeric; no decompression or decryption occurs.

Ten Rust tests include 1,024 truncations and 10,000 deterministic mutations; nine CLI cases check errors and input invariance. No real game executable has validated compatibility. These mutations are not coverage-guided fuzzing.

Primary references and analysis scope: [XEX2 research report](../../docs/XEX2-INSPECTION.md). Original implementation under MIT; format facts cross-checked against Xenia and historical Free60 documentation.
