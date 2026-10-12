# Repository and publication history

## Current status

The repository [ludovic111/obsidian-360](https://github.com/ludovic111/obsidian-360) is **public**. Since 2026-10-07, `main` carries the full research history, and all work happens there; branch work is done in separate worktrees and merged back into `main`. `main` is the only branch on GitHub; the former research branch `research/bootstrap` is fully merged into it.

SSH keys, CPU/DVD keys, keyvaults, NAND or firmware dumps, game executables and other non-redistributable material stay out of Git (`.local/` and `private/` are ignored). Because `main` carries the research history, it also contains material the former public export excluded: installation archives, the blocking probe and the installation history. Device identifiers in those files and in the captures (the console's MAC address, disk and USB serial numbers, LAN addresses) are replaced by placeholders such as `REDACTED_MAC_ADDRESS`, `REDACTED_DISK_SERIAL`, `REDACTED_USB_SERIAL` and `XBOX_LINUX_IP`; see History, step 6.

## History

1. **2026-10-01 (UTC): first public export.** A reviewed text-only export of the local research repository was published as a new, independent history: root commit `f9da49e7cc39a3bf06983e97b9fffe73a8e63606`, 187 files (E40).
2. **2026-10-02: export updates.** Each research milestone up to E71 was re-exported, audited and pushed on top of that history; the last export commit is `47b0a02d8820d009aa6cde4741a925b6e6018cae` (452 files). The verified publication log is kept below.
3. **Later: repository made private.** The repository was renamed to lowercase obsidian-360 and made private; `main`'s documentation was updated for this on 2026-10-07.
4. **2026-10-07: research history merged into `main`.** The English research line (`research/bootstrap`, up to E73) was merged into `main`. The export history is the merge's first parent and `research/bootstrap` its second, so no published commit was rewritten. The merged tree is the research tree, plus `PUBLICATION-MANIFEST.json`.
5. **By 2026-10-12: repository made public again.** The full research history on `main` became public.
6. **2026-10-12: device identifiers redacted from every commit.** Before promotion, the history was rewritten once with `git filter-repo`: the console's MAC address (including the `enx...` interface name the 2026-10-01 export had missed), the internal disk and USB drive serial numbers and the console's LAN addresses were replaced by placeholders in every commit, the SHA-256 values of the two affected captures were updated so every `SHA256SUMS` list still verifies, and commit author emails were normalized to a GitHub no-reply address. File contents are otherwise unchanged. **Every commit SHA changed**: the commit SHAs quoted below and in `evidence/*/public-audit/*.json` (for example `f9da49e` and `47b0a02`) identify the history as it was before this rewrite and no longer resolve in this repository.

## Historical: the controlled public export (2026-10-01 to 2026-10-02)

Everything in this section describes the export process as it ran while the repository was public. It is kept as a record and is no longer the publication procedure.

`PUBLICATION-MANIFEST.json` at the repository root is the manifest of the last audited export tree (selected files, before/after hashes, exclusions and transformations). It describes that export, not the current tree, and is kept unchanged at its path because `tools/audit-public.py` reads it from there. `tools/export-public.py` and `tools/audit-public.py` are historical tools: run against the current `main`, the audit would report a mismatch by design. No CI runs them.

The repository was created as a public repository (originally under an uppercase name). First commit: `f9da49e7cc39a3bf06983e97b9fffe73a8e63606`, no parent, 187 files. The GitHub API confirmed public visibility, the main branch, the commit SHA, and equality of the remote tree with the audited export. Evidence: `evidence/2026-10-01/publication/verification.json`.

October 2 update: public commit `2d31efbd2230c28dfd23ad199ffab231c7a12b12`, direct child of f9da49e, 203 files. XEX2 inspector, tests and the history audit tool included; API verification of the commit and tree succeeded. The pre-push audit covered both commits and 213 reachable text objects. See `evidence/2026-10-02/public-audit/publication.json`.

Two captures were derived to mask the MAC address. Seventeen paths were excluded from the initial selection, including the original SHA manifest (replaced by the one for the derivatives), the binary acquisitions, the archives, and third-party excerpts kept locally. Upstream public attributions were preserved; no private Git identity of the operator was in the export history.

The export was prepared in a separate local publication checkout, `.local/public-export-reviewed-20261001`, with its own Git and its origin remote, while the research repository itself had no remote. Each update re-prepared and audited an export without mixing the two histories. That checkout is historical; it is no longer used to publish.

The user authorized a public GitHub publication in objective v2. The research history was then kept local because it contains personal traces and metadata; it was later pushed to the private repository and merged into `main` (see History).

The export was prepared in a separate ignored directory with `tools/export-public.py`. It took only tracked text files and excluded binary acquisitions, installation archives, the blocking probe, old session transcripts, and some third-party excerpts whose license was still to be checked. A local policy provided the replacements for private names, paths and contact details; it was never exported. The public manifest lists the excluded files, the before/after hashes and the reported transformations, without publishing the removed values.

The checksums of the public evidence were recomputed for the published derivatives; they did not replace the hashes of the local originals. A document citing excluded evidence referred to a local experiment, not a file downloadable from GitHub at the time.

Before the first public commit, the process was: inspect the selection, scan for secrets and personal information, verify that no proprietary binary/dump was included, then create a fresh history with a project identity. Before each subsequent push: redo the audit of the files and of all added reachable objects. The research branch was not pushed, `--mirror` was not used, and old tags were not sent.

The built-in scanner detected several obvious patterns and the local policy; it did not replace human/agent review of the selected files. No NAND image, game, key or firmware needs to be published to explain the results.

For each update, `tools/audit-public.py --repo EXPORT_GIT_PATH --policy LOCAL_POLICY_PATH` checked the tracked/non-ignored selection, the manifest and evidence hashes, then the reachable blobs, commits and tags of that public history. It ran before the public commit and after the commit, before the push. A newly prepared export directory was synchronized only after checking the public checkout and its remote parent. The audit program neither commits nor pushes.

### Verified export log

E43–E46 update: `ec431c9c7e114e11074628d0fb95358d1128a752`, 221 files, third public commit. Audit before commit and then before push succeeded (240 text objects); API verification of the tree and parent succeeded. Evidence `evidence/2026-10-02/public-audit/optical-publication.json`.

E47 and PAL lead publication verified at 2026-10-02T07:57:41.408927+00:00: public commit `a67d28f83a160fde6048efc74a9824c808745f74`, 230 files, GitHub tree identical; evidence `evidence/2026-10-02/public-audit/resize-publication.json`.

E48 publication verified at 2026-10-02T08:03:48.586991+00:00: public commit `b4b49e2b2fdcc42f522fbc6cd4b74b1b96202632`, 234 files and remote tree matching; evidence `evidence/2026-10-02/public-audit/video-publication.json`. Result of the stock-dashboard check still pending.

E49–E52 publication verified at 2026-10-02T08:25:04.519035+00:00: public commit `fd75dd4f20e7d0c0d0fc1475b1423d013d7cfa00`, 248 files, GitHub parent and tree matching after audits. Evidence `evidence/2026-10-02/public-audit/audio-publication.json`. Audio not enabled; no shutdown since the return to Linux.

E53/E54 publication verified at 2026-10-02T08:57:54.026744+00:00: public commit `5dd3293b9936669ba7a8e25935de8dd6b918fafc`, 273 files, GitHub parent and tree matching after audits. Evidence `evidence/2026-10-02/public-audit/smc-publication.json`. Two complete audio builds validated, none installed.

E55/E56 publication verified at 2026-10-02T09:45:58.581719+00:00: public commit `74ba6693755aaef77e96d016bbcbc6e7cf473713`, 287 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/pcm-publication.json`. audio-pcm candidate not installed.

E57/E58 publication verified at 2026-10-02T10:19:25.216637+00:00: public commit `987fea14abdeb6059b4b8d4a6b1215345cefabbe`, 312 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/poll-publication.json`. audio-poll kernel compiled, not installed; submission still to be fixed.

E59 publication verified at 2026-10-02T10:36:04.104109+00:00: public commit `3a98dcf5b0977a33251748255f186c25cfcf2da0`, 324 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/queue-publication.json`. PCM queue tested and linked for PowerPC, not integrated into the driver and not loaded.

E60/E61 publication verified at 2026-10-02T10:58:31.472464+00:00: public commit `f8989261de3589ec3b3c3276b9e4ef66646795f3`, 342 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/adapter-publication.json`. audio-submit kernel compiled, not installed; completion of the last descriptor still not decoded.

E62 publication verified at 2026-10-02T11:15:01.783984+00:00: public commit `cbd5b02b2d87b4dbaddf23ebcfdf91a172e719e7`, 362 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/protocol-publication.json`. audio-bytes candidate compiled, not installed; SiS hypothesis and end of sound output not measured.

E63/E64 publication verified at 2026-10-02T12:11:33.298267+00:00: public commit `962219272919b6446c7593b5fd5ced9f9fce8656`, 396 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/control-publication.json`. Audio control tested under the model; three hardware observations without writes, no sound enabled.

E65/E66 publication verified at 2026-10-02T12:57:15.785188+00:00: public commit `6d597f74c644f253f889d7c78e3f05f3113af2c9`, 410 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/stop-publication.json`. Analog STOP observed; ALSA memory contract tested, no sound enabled.

E67–E70 publication verified at 2026-10-02T13:27:32.850304+00:00: public commit `db44cdd3e537a6d0a2dd13ac565a939f9b90e043`, 442 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/timebase-publication.json`. Analog acknowledgements observed; cadence measured and correction kernel compiled, not installed.

E71 publication verified at 2026-10-02T13:43:05.979127+00:00: public commit `47b0a02d8820d009aa6cde4741a925b6e6018cae`, 452 files, GitHub parent and tree matching after audits. Evidence: `evidence/2026-10-02/public-audit/timebase-boot-publication.json`. Boot set ready; physical trial still pending.
