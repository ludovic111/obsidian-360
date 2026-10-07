# Chronological journal

Timestamps in UTC. Earlier experiments E01–E38 are described in EXPERIMENTS with their dated evidence; do not invent a timestamp for a hands-on action when none was recorded.

## 2026-10-01 — 21:45:47 — E38

- Objective: identify the kernel actually booted after user selection.
- Action: SSH, desktop state, udev, graphics log and standard interfaces.
- Observation: obsidian4, internal root, Xorg/IceWM active, allocation 0x398000, zero failed services.
- Result: first candidate boot confirmed.
- Interpretation: graphics fix effectively active; no evidence of prolonged stability or of the cause of the earlier freeze.
- Next: establish a performance baseline without changing the configuration.

## 2026-10-01 — 21:50:15 — E39

- Objective: measure boot, memory, topology and two short userspace workloads.
- Action: collect-baseline.py with three samples, then collect-boot-detail.py.
- Observation: graphical target at 34.1 s, 118.5 MiB available at the first reading, median SHA-256 22.553 MiB/s; two systemd analyses timed out.
- Result: baseline kept and targeted follow-up succeeded; /proc/slabinfo absent, initial error kept, then interface made optional.
- Interpretation: baseline of a single boot; the Python copy does not measure raw RAM, and the graphical target does not measure the visible desktop.
- Next: break down boot and memory; compare any future optimization using an equivalent method.

## 2026-10-01 — objective revision during E39

- Objective: integrate the updated reference text without losing history.
- Action: keep both detailed versions, their hashes and a map of unknowns.
- Observation: addition of game analysis, modernization, overnight autonomy and a public GitHub authorization conditional on audit.
- Result: OBJECTIVE, RESEARCH-MAP and BLOCKED updated.
- Interpretation: publication does not authorize sending confidential data or the old private history.
- Next: controlled public export, license and reproducible instructions. No reboot requested from the absent user.

## 2026-10-01 — 22:01 UTC — E40

- Objective: publish the authorized project without exporting the private history.
- Action: text export with explicit selection, hash checks, search for secrets/identifiers, syntax compilation of the Python scripts, new Git with project identity, audit of reachable objects, then GitHub creation/push.
- Observation: the first review finds the MAC address in two records; blocking rule added and masking applied in derived files. Local originals intact. Upstream attributions distinguished from the operator's personal data.
- Result: 187 public files, 17 paths excluded from the initial selection; first commit f9da49e with no parent. The GitHub API confirms public visibility and a tree identical to the controlled export.
- Interpretation: publication of knowledge/tools and selected evidence, not distribution of firmware or games. The pattern scanner is not universal proof of the absence of secrets.
- Next: keep the two histories separate, refresh exports after audit, continue measurements and format analysis with synthetic samples while waiting for accessible legitimate media.

## 2026-10-02T07:07:37.271107+00:00 — E41

- Objective: prepare a reproducible inspection of game executables without acquiring or distributing any proprietary binary.
- Action: reading of pinned Xenia and Free60 sources, original Rust implementation, structural and CLI tests with synthetic samples.
- Observation: difference in handling of zero-size keys across the references; ten Rust tests and nine CLI cases pass, as well as 10,000 deterministic mutations.
- Result: structural JSON, checked bounds, opaque fields not read in the instrumented test; input files unchanged.
- Interpretation: metadata tool validated on the host; no authentication, game disassembly or validation on a commercial file.
- Next: compatibility validation on legitimate input, import and PE formats, then profiling; export and public audit before publication. No interaction with the console during E41.

## 2026-10-02T07:10:20.726239+00:00 — E42

- Objective: make the audit required before each publication reproducible.
- Action: check of the manifest, the selection, the evidence checksums and reachable Git objects; five cases in a throwaway repository.
- Observation: the check also finds the dummy marker removed from the current file but still present in an old commit.
- Result: five cases with the expected results; existing public history audited with no anomaly detected.
- Interpretation: pattern and provenance check, with explicit limits; does not demonstrate the absence of every arbitrary secret.
- Next: export the Rust sources and their evidence, audit before commit and then before push, verify the remote SHA.

E41/E42 publication verified at 2026-10-02T07:14:53.060765+00:00: public commit `2d31efbd2230c28dfd23ad199ffab231c7a12b12`, 203 files, GitHub tree identical to the audited export. Ten Rust tests also pass after compilation in the public checkout. Private local history not pushed.

## 2026-10-02 — morning — E43/E44

- Objective: verify prolonged operation, then take advantage of the user's return to diagnose the drive.
- Action: standard Linux interfaces; twelve-second observation of the launcher; audio CD inserted by the user, TOC read and four audio sectors.
- Observation: obsidian4 active after nine hours, no failed service; no launcher write observed during the window. The CD has 20 tracks; three audio positions readable, reread of the first one identical.
- Result: first evidence of the drive actually reading, limited to the CD and the sampled sectors. Metadata and hashes kept, not the audio content.
- Interpretation: the initial lead of unnecessary rewrites by the launcher comes from the code, but is not confirmed on the live process; do not claim a gain. The DVD fault is neither identified nor repaired.
- Next: comparison with a DVD requested; launcher diagnosis and measurements before any change. No reboot or firmware command.

## 2026-10-02 — 07:30–07:37 UTC Mac — E45/E46

- Objective: compare CD/DVD and restore the frozen desktop.
- Action: Just Cause 2 disc inserted by the user; standard read and SCSI status. Graphics diagnosis and targeted restarts, without a Linux reboot.
- Observation: the drive returns "medium not present" for the game. The user corrects their first report: a resize the day before, followed by a freeze. Force-stopping the window manager, unlike stopping the launcher and SIGHUP, restores X11 requests.
- Result: OpaqueMove/Resize enabled with a backup of the preferences; controller reopened by the launcher. Five synthetic sense tests pass.
- Interpretation: XGrabServer mechanism consistent with the code and the symptoms; not yet a controlled reproduction nor manual confirmation of the fix. CD/DVD difference is real, faulty part still unknown.
- Next: user invited to resize again; a known-working video DVD is needed to distinguish a DVD fault from a particular disc.

E43–E46 publication verified at 2026-10-02T07:41:15.538940+00:00: public commit `ec431c9c7e114e11074628d0fb95358d1128a752`, 221 files, remote tree identical; evidence `public-audit/optical-publication.json`. Manual validation of resizing still pending.

## 2026-10-02 — 07:42–07:49 UTC — E47

- Objective: go beyond the resize-freeze hypothesis by reproducing the mechanism independently of the Xbox hardware.
- Action: Docker service initially stopped, restarted after checking its state; IceWM 4.0.0 source pinned and verified, aarch64 compilation, two private Xvfb servers without network or host graphics socket.
- Observation: the old mode prevents an XTest request from completing and another client from responding. The new mode actually resizes and both clients respond. The first test, which missed the theme border, had resized nothing and is kept as a failure.
- Result: discriminating automated test succeeded; no Xbox interaction during this experiment.
- Interpretation: evidence of the X11 mechanism and of the configuration fix in this environment. Not evidence for all controller functions, the graphics driver or prolonged stability on the Xbox.
- Next: manual confirmation on the Xbox; keep the upstream network applet compilation warnings as a separate lead, without attributing them to the freeze.

## 2026-10-02 — PAL/NTSC user lead

- Reported observation: Just Cause 2 and the other game boxes are marked PAL.
- Action: check archived Microsoft documentation on regions and the T10 meaning of code 3a/00; ask whether these games previously worked on this console.
- Interpretation: region unverified, box marking insufficient; the measured medium-not-present error differs from an explicit region refusal. No hardware command or region modification executed.

User feedback: console and games bought together at a second-hand store; prior operation of this set unknown. Regional compatibility still unconfirmed; availability of a video DVD requested.

E47 and PAL lead publication verified at 2026-10-02T07:57:41.408927+00:00: public commit `a67d28f83a160fde6048efc74a9824c808745f74`, 230 files, GitHub tree identical; evidence `evidence/2026-10-02/public-audit/resize-publication.json`.

## 2026-10-02 — 07:58 UTC Mac — E48

- Objective: distinguish a restriction specific to the Xbox game from a more general DVD refusal.
- Action: the user inserts Big Order; two standard TEST UNIT READY commands, observed interval 59.2 s, no firmware/region change.
- Observation: 02/3a/00 each time; the observation is therefore not limited to the moment of insertion. No video sector read.
- Result: second DVD not recognized, of a different category from the game.
- Interpretation: DVD recognition lead strengthened; laser fault not proven, disc condition and noises still to be confirmed.
- Next: feedback on spinning/clicks requested; comparison under the original system before any opening of the drive.

User feedback E48: the DVD spins briefly then stops, like Just Cause 2. Check under the original Xbox dashboard requested, with a clean shutdown from Linux and without relaunching the boot game. The result is still pending.

E48 publication verified at 2026-10-02T08:03:48.586991+00:00: public commit `b4b49e2b2fdcc42f522fbc6cd4b74b1b96202632`, 234 files and remote tree compliant; evidence `evidence/2026-10-02/public-audit/video-publication.json`. Result of the stock dashboard check still pending.


## 2026-10-02 — E49/E50 — shutdown and comparison under the original system

- Objective: compare Big Order behavior outside Linux.
- User observation: the desktop shutdown button displays "failed request". Prior administrative measurement: CanPowerOff = challenge, no inhibitor.
- Action: normal shutdown requested via an administrator timer, accepted at 08:05:45 UTC; no forced power-off or permission change. Physical power-off not directly observed.
- Result reported afterwards: no DVD detected during the requested stock check. Exact wording not provided; no capture or confirmation of media readability elsewhere.
- Interpretation: an exclusively Linux cause is less likely; precise hardware fault not demonstrated. The Shut Down button defect remains to be fixed after checking the normal session context.
- Next: return to Linux via Rock Band Blitz, choose obsidian4, and Ethernet only after reaching the desktop. No new connection initiated during the user's hands-on manipulation.


## 2026-10-02 — E51/E52 — off-hardware audio and Linux return

- Objective: make progress on sound during the DVD manipulation, then verify the console's return.
- Off-console action: new build output, original audio as a module; reproduction of the calculations by extracting the real C, hooks for cache/MMIO and ASan/UBSan.
- Observation: removed APIs confirmed by compilation; 98 sizes produce a table overflowing the buffer according to the driver's encoding, five cache-loop cases exceed the expected number of lines. Frame splitting is a distinct property, not a proven hardware fault.
- Result: partial fix 0008, 512 sizes accepted without out-of-buffer geometry out of 16,369 examined; complete port and sound still not validated.
- Hardware measurement: at 08:17:42 UTC obsidian4 responds after 201.58 s, zero failed units, XRandR responds in 720p. Anti-freeze preferences retained.
- Correction of the shutdown diagnosis: CanPowerOff from runuser within SSH still returns challenge, but pkcheck on the real PID 429 of the local launcher allows power-off and power-off-multiple-sessions. The narrow rule already existed. The context of the launcher restarted from SSH is a consistent explanation of the earlier refusal, not a full reproduction.
- Next: user temporarily away, autonomous work requested; no voluntary reboot nor actual test of the button. Continue the off-hardware audio port and validate shutdown during a physical-access window.

E49–E52 publication verified at 2026-10-02T08:25:04.519035+00:00: public commit `fd75dd4f20e7d0c0d0fc1475b1423d013d7cfa00`, 248 files, parent and GitHub tree compliant after audits. Evidence `evidence/2026-10-02/public-audit/audio-publication.json`. Audio not enabled; no shutdown since the Linux return.


## 2026-10-02 — E53 — audio lifecycle and protocol divergence

- Objective: fix the driver's resources before activation.
- Action: single ALSA owner, cleanup of partial acquisitions, stop before destroying PCMs, modern DMA/timer APIs, shared SMC transport. Test bench of extracted C functions under ASan/UBSan, off-hardware.
- Observation: twelve expected failures in thirteen scenarios of the original; sixteen candidate scenarios pass. The first bench attempt did not compile; fixed and kept as a tooling failure. Buffer regression unchanged.
- Result: PPC object compiled without warnings; kernel/module compilation started separately with pinned source. No file installed on the Xbox.
- Code analysis: LibXenon mentions the first 32 MiB and encodes lengths differently; HDMI there requires an initialization absent from the Linux driver. 29-bit mask and historical encoding not validated on hardware. ALSA already provides coherent DMA memory, to be used directly for PCMs.
- Next: finish and verify the full compilation; continue DMA contract, callbacks/timer and protocol. No reboot while the user is away.


## 2026-10-02 — E54 — bounded SMC post and audio linking

- Objective: avoid unbounded waits on the new audio path and confirm module linking.
- Action: new process API with two trylocks, atomic polling budget, aligned message and no write on failure; probe/remove protection specific to this path. The old senders are not migrated.
- Observation: nineteen scenarios of the real C and real iopoll macros pass; audio regression extended to eighteen scenarios. First tooling failure on an unused parameter kept.
- Result: first complete audio-lifecycle compilation finished with code 0; independent copy, then audio-post compilation code 0. Seventy modules each, no warnings, PowerPC formats and vermagic verified, new GPL export present.
- Limits: logical budget, not an MMIO transaction bound; sequential tests without SMP validation. The mutex does not protect the old paths. No real send, kernel/image or module installed.
- Next: publication after audit; PCM DMA contract, timer/notifications and protocol before activation.

E53/E54 publication verified at 2026-10-02T08:57:54.026744+00:00: public commit `5dd3293b9936669ba7a8e25935de8dd6b918fafc`, 273 files, parent and GitHub tree compliant after audits. Evidence `evidence/2026-10-02/public-audit/smc-publication.json`. Two complete audio builds validated, none installed.


## 2026-10-02T09:43:49.512960+00:00 — E55/E56 — PCM memory and live check

- Objective: remove the erroneous CPU remapping of DMA buffers and clarify their owner.
- Action: fix 0011 after 0008–0010, ALSA constraints, managed buffers, barriers, channel stop before freeing and bounds validation. No loading.
- Observation: 20 resource scenarios and 12 callbacks pass under ASan/UBSan; 16,369 sizes examined, 512 accepted without overflow. Removal of the private cache function, not a hardware coherence test.
- Result: audio-pcm kernel and 70 modules compiled without warnings, ELF/vermagic and patch reconstruction verified. Check tool extended to a mode without a XeLL image; full obsidian4 path still valid.
- Separate direct measurement: at 2026-10-02T09:40:09.815799+00:00, SSH responds under obsidian4, uptime 5,139.44 s, zero failed units, 720p framebuffer. Visual responsiveness not verified.
- User feedback: available again; no physical action needed for this work.
- Limits: no sound, no real DMA validation; old timer not armed, callback synchronization and protocol to be resolved. Next step: progress notifications and stream lifetime, off-hardware.

E55/E56 publication verified at 2026-10-02T09:45:58.581719+00:00: public commit `74ba6693755aaef77e96d016bbcbc6e7cf473713`, 287 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/pcm-publication.json`. audio-pcm candidate not installed.


## 2026-10-02T10:04:39.273970+00:00 — E57 — per-output audio tracking

- Objective: correctly start and synchronize playback tracking.
- Observation: START does not arm the timer; two direct calls to the old callback with an identical position produce two false notifications. Off-hardware reproduction, not a live reading.
- Action: per-output hrtimer, modulo progression and period remainder, XRUN if the observation is too late, notification outside the driver lock, sync_stop/hw_free wait for the callback.
- Host result: 15 timer scenarios, 20 resource and 15 PCM scenarios pass under ASan/UBSan; pthread case with a notification held during close. Geometry: 512 sizes accepted out of 16,369, with no overflow among them.
- Failures kept: two signed comparisons in the first bench; incorrect --output option for the geometry bench. Fixed, recipes updated.
- Configuration: old kernel without HIGH_RES_TIMERS, incompatible with the nominal rate for the smallest buffers. Enabled in the candidate copy, and open refused if high resolution is inactive. Two intermediate builds succeeded; final build started at 2026-10-02T09:59:37Z, still running at the time of the reading.
- Limits: timing model and a single deterministic interleaving; no SMP/latency/DMA validation. No installation or new Xbox interaction. Next focus: publishing samples via ack, then the hardware protocol.


## 2026-10-02T10:16:13.670215+00:00 — end of E57 and E58 audit

- E57 result: high-resolution build finished with code 0; 70 modules, ELF/vermagic and hashes verified, no warnings. The existing process was followed until it finished, without restarting it. No deployment.
- E58 objective: understand audio publication before migrating to ack.
- Host observation: three identical requests alternate the queue over 96 cases. The real ALSA helpers reproduce a signed overflow for a synthetic native 64-bit value; reachability by current 32-bit applications not demonstrated. Publication of a partially committed block interpreted under the last-valid-descriptor hypothesis.
- Analysis: ack must preserve rollback, boundary wraparound, full buffer, partial writes, drain and reset. Simply moving the writes would not suffice.
- Reference examined: xenon-emu/xenon at commit 0284bbe6c8125935d97bf54ab3132089c6c65c8b; audio class without descriptor consumption, hence no protocol validation.
- Next: document and publish after audit; design submission/end of stream, without enabling the still-incomplete audio kernels. Last hardware reading unchanged: E56.

E57/E58 publication verified at 2026-10-02T10:19:25.216637+00:00: public commit `987fea14abdeb6059b4b8d4a6b1215345cefabbe`, 312 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/poll-publication.json`. audio-poll kernel compiled, not installed; submission still to be fixed.


## 2026-10-02T10:33:39.076776+00:00 — E59 — software PCM queue

- Objective: replace the unstable submission calculations without losing partial writes or end of stream.
- Action: original C component without MMIO/allocation; separate physical/logical states, publishable complete blocks, unpublished remainder, silence plan at drain, frame deltas bounded before conversion. Errors without mutation.
- Observation: independent content test over 512 sizes and two interleaved queues; 54,008 operations, 24,544,033 logical frames compared, 4,333 expected refusals. No ASan/UBSan diagnostics.
- Failure kept: LeakSanitizer unavailable on this Mac; first run stopped before the cases, option disabled, then tests succeeded.
- Result: Clang analysis without diagnostics; freestanding PPC64 object, then link module with __KERNEL__ against audio-poll, no warnings, functions and vermagic verified. Kernel sources/build mounted read-only. No module loaded.
- Limits: queue algorithm tested, not the register protocol or DMA completion. The historical driver retains E58 as long as its adapter does not replace pointer/ack; ALSA reset, real drain and prefetch to be verified.
- Next: integrate the queue contract into the callbacks while keeping the separation between software tests and hardware evidence. No additional live check.

E59 publication verified at 2026-10-02T10:36:04.104109+00:00: public commit `3a98dcf5b0977a33251748255f186c25cfcf2da0`, 324 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/queue-publication.json`. PCM queue tested and linked for PowerPC, not integrated into the driver and not loaded.


## 2026-10-02T10:56:46.731605+00:00 — E60/E61 — audio adapter and live check

- Objective: remove the unstable pointer publication and integrate ALSA commitments without losing rollback.
- Action: fix 0013 with transactional ack, SYNC_APPLPTR/NO_REWINDS, start deferred until the first block, drain with silence, cached logical position and RESET limited to empty prepared queues. Resumption of prepare after STOP, tracking and synchronized close retained.
- Observation: fifteen scenarios pass with real callbacks and three extracted ALSA functions, including 512 sizes and a controlled concurrent close. Twenty resource scenarios; queue: 54,008 operations, 24,544,033 frames compared.
- Failures kept: signed comparison in the ALSA code rejected by the bench; Docker mount of new files impossible under a read-only source; parameter current colliding with a kernel macro during the integrated compilation. Fixes with explicit scope, no failure disguised as success.
- Result: audio-submit build finished with code 0 at 2026-10-02T10:52:58.835912+00:00, zero warnings, 70 PowerPC modules and vermagic verified. Patch reconstruction and identity of the canonical component checked.
- Limit: completion of the last descriptor not decoded; an unchanged zero residual is not evidence of a read. Simulated stagnation deliberately ends in XRUN. Audible drain, DMA length/addresses, prefetch, HDMI initialization and real behavior remain open. No loading or booting of this variant.
- Separate E61 measurement: SSH at 10:49:58 UTC, obsidian4, uptime 9,327.35 s, no failed unit listed, 720p framebuffer. No visual test; console configuration unchanged.
- Next: resolve the last block and check the protocol against the references before any activation. Publication only from the audited export.

E60/E61 publication verified at 2026-10-02T10:58:31.472464+00:00: public commit `f8989261de3589ec3b3c3276b9e4ef66646795f3`, 342 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/adapter-publication.json`. audio-submit kernel compiled, not installed; completion of the last descriptor still not decoded.


## 2026-10-02T11:13:34.630501+00:00 — E62 — history, lengths and SiS lead

- Objective: make progress on hardware playback completion and audio format divergences.
- Primary analysis: LibXenon history retrieved via the API, including an explicit size−1 to size correction in 2010 and a last-complete-block index in 2011. Comparison of Linux's SiS7012 definitions with the Xenon words: ten offset/mask matches in the bench.
- Research result: LVBCI/PICB in the ICH4 reference concern the memory transfer, not evidence of an empty audio FIFO. Application to the Xbox not validated; a read-modify-write of the control register may acknowledge statuses under this hypothesis. Do not announce a resolved drain.
- Action: fix 0014 with literal length and exact geometry. Test of the real prepare before/after over 512 sizes, 16,384 entries per variant: all candidate counts are aligned to four bytes; under this interpretation, the old code omits 32 bytes per ring. No real loss measured.
- Regression: fifteen callbacks and twenty resources pass under ASan/UBSan; real LibXenon functions ambiguous for the 32 synthetic words with zero residual. First macro extraction badly split by a line break; failure kept, then fixed.
- Build: two zero exit codes with real clock skew warnings under Mac/Linux sharing. Third build on a dedicated Linux volume finished 2026-10-02T11:09:56.522693+00:00, zero warnings. Export after the process ended; kernel and 70 modules ELF/vermagic verified. Intermediate check explicitly marked provisional, not evidence that the second build finished.
- Limits: no console interaction, live state still E61. Neither sound nor end decoder enabled. Source/register correspondence and FIFO to be tested separately; no definitive identification of the controller as SiS7012.
- Next: separate control and acknowledgment; prepare a targeted reversible observation before DMA progression and real audio. Publication after audit.

E62 publication verified at 2026-10-02T11:15:01.783984+00:00: public commit `cbd5b02b2d87b4dbaddf23ebcfdf91a172e719e7`, 362 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/protocol-publication.json`. audio-bytes candidate compiled, not installed; SiS hypothesis and end of audio output not measured.


## 2026-10-02T12:06:27Z — E63/E64 — audio control and first register observation

- Objective: avoid unintended acknowledgments and distinguish the absence of a Linux driver from a hardware state that is actually stopped.
- E63, code/model: fix 0015. START/STOP mask the presumed W1C statuses and the IRQs; prepare acknowledges explicitly. 4,096 transitions per variant: 3,584 modeled losses before, zero after; fifteen callbacks, twenty resources and 16,384 descriptors pass. No live W1C fact claimed.
- Compilation: PowerPC64 big-endian module, audio-bytes vermagic, no warnings. The isolated target had failed for lack of ALSA dependencies; full modules target succeeded, failure kept. No new vmlinux or loading.
- E64, standard measurement: PCI 1414:580c, no driver, enable=0 but command=0x0006. SSH access verified under obsidian4; 64 KiB pages.
- Review of the probe before MMIO: sysfs maps the page containing the BAR. Fix of the 0x1600 offset, test of 31,744 geometries and seven invalid cases. The earlier binary did not access the hardware. The original C compilation had required _Noreturn to clear an initialization flow error; kept.
- Tooling: two cross-compiler attempts failed; the historical Docker builder had kept ARM despite --platform. Explicit amd64 base and architecture assertion succeed. A rerun of the descriptor test used an old, nonexistent folder name; real submission path identified, final test succeeded. A local tool process refused its creation; an absolute non-login shell works, repository accessible via its project path and its resolved my_repos path. None of these failures is a hardware result.
- Static ELF32 binary verified, four lwz and eight eieio in the sequence; remote hash identical. Running without arguments confirms the usage message before any hardware access.
- MMIO measurement: three successful captures of four registers, between 12:05:30 and 12:06:27 UTC. Controls 0x1d08001c for both channels; analog index 0x00008000, digital 0x00009616; identical. Twelve reads in total, no write or SMC command, no sound started. SSH remains accessible, no visual reaction observed.
- Limit: the SiS breakdown gives apparent RUN and a status without halted, despite equal indices and zero residual. Stable values do not prove a stopped engine; bit 15 of the indices unexplained. No confirmation of W1C or FIFO completion. Do not turn the software model into a hardware identification.
- Next: design bounded stop/reset and confirmation before any audio activation. Document and publish from the audited export; stock firmware and existing boot retained.

E63/E64 publication verified at 2026-10-02T12:11:33.298267+00:00: public commit `962219272919b6446c7593b5fd5ced9f9fce8656`, 396 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/control-publication.json`. Audio control tested under the model; three hardware observations without writes, no sound enabled.


## 2026-10-02T12:48:41Z — E65/E66 — first audio STOP and ALSA memory contract

- Objective: establish a live stop indicator before replacing descriptors or making buffers reusable.
- Analysis: candidate 0015 requests STOP without checking halted. The intel8x0 driver waits for this status in an unbounded loop; do not transpose this wait. Primary ICH4 documentation reviewed, Xbox identity kept distinct.
- Tool: stop_analog_once refuses any variation of the two E64 controls; only one possible write, 0x00080000 at +8. No START, reset, PCI or SMC. Filter and write footprint tested on ordinary memory, 64 single-bit alterations refused, ASan/UBSan. ELF32 verified and one aligned stw inspected with barriers.
- Tooling failures: unused bench counter under Werror, then disassembly extraction looking for sync instead of the hwsync mnemonic. Fixed and kept before the console run.
- Pre-check: transferred hash identical, run without arguments code 2, obsidian4 responds. Test plan and recovery documented before writing.
- Direct measurement: 12:47:31 UTC, analog STOP executed once; control 0x1d08001c → 0x0008001d, index 0x00008000 → 0. Digital 0x1d08001c / 0x00009616 unchanged. Code 0, six reads and one write.
- Direct follow-up: 12:48:41 UTC, analog 0x0000001d / 0, digital unchanged; four reads and no write. SSH responds, uptime 16,464.45 s, no failed service listed, 720p framebuffer. No visual test. No reboot.
- Interpretation: removal of RUN and appearance of the DCH bit support the breakdown; presumed W1C bits preserved by writing zero. Acknowledgment by writing one, reset, in-flight transactions, FIFO and digital channel not proven. Intermediate field became zero at the follow-up, precise delay/role unknown. Analog left in STOP, no automatic return to RUN.
- E66, off-console: extraction of snd_pcm_sync_stop, do_hw_free and snd_pcm_lib_free_pages. 144 cases pass; 24 detachments after a callback error, including 12 dynamic allocations actually freed in the model. Preallocations only detached and reusable; not a claim of an ALSA bug or of systematic physical freeing of the candidate's buffer.
- Decision: do not treat return -ETIMEDOUT as protection of the managed buffer. The stop strategy must cover the free/reuse contract and possible isolation; next, targeted acknowledgment/reset trials before integration.

E65/E66 publication verified at 2026-10-02T12:57:15.785188+00:00: public commit `6d597f74c644f253f889d7c78e3f05f3113af2c9`, 410 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/stop-publication.json`. Analog STOP observed; ALSA memory contract tested, no sound enabled.


## 2026-10-02 — E67/E68 — analog acknowledgments and reset request

- Objective: test the presumed W1C bits after the E65 STOP, before audio activation.
- Initial state re-verified: analog 0x0000001d / index zero, digital 0x1d08001c / 0x00009616. One read of four words, no write.
- Original tool with four fixed operations, never chained automatically. Exact filter on four words, 512 single-bit variations refused under ASan/UBSan, four four-byte footprints verified. ELF32 compiled, aligned stw and barriers reviewed; transferred hash identical, no-argument test before access.
- E67: writes 4, 8, 16 in separate invocations, with the result examined each time. Status 0x1d → 0x19 → 0x11 → 0x01, index and digital channel unchanged. Three writes, 24 reads. All exit codes zero; W1C behavior of the three bits observed at rest. The meaning of the events during streaming is not proven.
- E68: one reset write 0x02000000 from the stopped status; next read 0x01, digital unchanged. Eight reads, one write, code zero. Result consistent with self-clearing; no intermediate transition or effect on a non-zero register observed, so a complete internal reset is not demonstrated. No START, sound or new descriptor.
- Next: keep the stop and the evidence; integrate only justified stop/memory-management conditions. Timing checks must distinguish the clocks of the two machines.

## 2026-10-02 — E69/E70 — rate drift and optional correction kernel

- Trigger: repeated difference between console and Mac timestamps in the audio evidence. Hypothesis of an incorrect conversion frequency, to be measured rather than adjusting the date.
- E69: seven persistent SSH exchanges over about 60 s, round trips of 1.37–1.94 ms. Reading of the raw, monotonic, civil and clocksource clocks and of the three DT properties. No reconfiguration.
- Measurement: 50 MHz advertised, timebase clocksource; 59.8864 raw Xbox seconds for 60.0354–60.0384 Mac seconds. Ratio 0.9974687–0.9975187, compatible relative frequency 49.8734–49.8759 MHz. Console time about 44.28 s behind at the end of the capture. Mac not calibrated; no electrical measurement.
- Sources: LibXenon sets 3,192,000,000 / 64 = 49,875,000; pinned file verified via the GitHub API after the raw web fetch failed. Kernel/XeLL DTS at 50 MHz, generic_calibrate_decr reads this property. The plain objcopy to zImage.xenon does not automatically embed the local DTS. A search using a nonexistent wildcard failed; exact files found without interpreting the failure as absence of the source.
- Reproducible tool measure-clock-drift.py: bounded capture, off-console analysis, preservation of outputs and private diagnostics. Seven synthetic/rejection cases pass; a short real capture of three points verifies the collector, without replacing the 60 s reference.
- NTP state: timedatectl reports CanNTP/NTP/NTPSynchronized=yes. This is not enough to contradict the direct comparison and the raw drift; no NTP change attempted.
- E70: independent patch 0016, early option xenon_tb_hz limited to 49,875,000 or 50,000,000 Hz. Without the option, the firmware configuration is retained. Software conversion only; no PLL/power programming. A measurement on this unit does not justify forcing all revisions.
- Separate build from obsidian4, without the audio patches: vmlinux, modules and zImage.xenon exit codes zero without warnings. obsidian-clock, 65 modules ELF/vermagic and six payload sections verified; parser symbol and option present, patch rebuilt identically.
- Limits: correction not installed/not booted. Initramfs and USB entry still to be prepared; measurement after reboot essential. Do not turn the compilation into an already-achieved rate improvement; keep historical timestamps and flag their origin.

E67–E70 publication verified at 2026-10-02T13:27:32.850304+00:00: public commit `db44cdd3e537a6d0a2dd13ac565a939f9b90e043`, 442 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/timebase-publication.json`. Analog acknowledgments observed; rate measured and correction kernel compiled, not installed.

Additional E69 confirmation: /proc/cpuinfo does report timebase=50000000 and no overriding ibm,extended-timebase-frequency property is present. Read-only; evidence clock-calibration/effective-timebase.json, kept for the next publication.

## 2026-10-02 — E71 — obsidian_clock boot set prepared

- Objective: make the E70 candidate testable without replacing obsidian4 or modifying the default.
- Live pre-check: SSH under obsidian4, internal ext4 root, separate ARCH vfat USB drive not mounted, no failed service listed.
- Archive of 65 modules and kernel verified before transfer and after receipt. New /var/tmp directory; depmod with Module.symvers without diagnostics. mkinitcpio limited to this version and --nopost, no preset replayed.
- Initramfs 16,171,806 bytes; extraction then comparison of the 43 included modules, ELF32 PowerPC verification of six executables and confinement of resolved paths. The lsinitcpio analysis command emits a TERM warning with no effect on the build; TERM=dumb from then on.
- Nine USB files recorded read-only. Addition of the obsidian_clock entry (168 bytes) with the same root and xenon_tb_hz=49875000. 65 modules in a separate directory; new USB files checked before replacing the menu. Old menu backed up; eight other files with the same hashes.
- Sync, unmount, read-only remount and reread of the candidate/old files: checks pass. Mac copy of the initramfs also verified. Final SSH under obsidian4, no failed service, drive unmounted; host timestamp 13:38:34 UTC.
- No reboot requested by script, no NAND or audio operation. Physical action proposed to the user: Rock Band Blitz/USB, obsidian_clock entry, Ethernet after the desktop. Boot result still unknown.
- Evidence in timebase-boot/; procedures archived as text, not steps to be replayed blindly. Next: verify the new kernel, then redo E69 and compare the rate intervals.

E71 publication verified at 2026-10-02T13:43:05.979127+00:00: public commit `47b0a02d8820d009aa6cde4741a925b6e6018cae`, 452 files, parent and GitHub tree compliant after audits. Evidence: `evidence/2026-10-02/public-audit/timebase-boot-publication.json`. Boot set ready; physical trial still pending.
