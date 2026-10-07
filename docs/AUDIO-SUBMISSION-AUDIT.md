# Audio sample publication — E58

E57 tracking does not make the driver usable: pointer still contains incorrect publication logic. A new harness reproduces its effects using the actual C function and actual ALSA conversions off-console. No submission fix is activated in this experiment.

## Host measurements

For a 4,096-byte ring with 32 descriptors of 128 bytes, hardware index remains 7. Three identical pointer queries return the same 224-frame position, yet alternately write two different queue indices.

Across 32 descriptor indices and three application offsets per descriptor (**96 cases**), an application index D and initial queue field D produce writes D−1, D, D−1 modulo 32. The historical condition depends on the field reread, without requiring newly committed application data. This proves non-idempotence in the model, not a live-register observation.

The MMIO model changes only the queue-index bits and preserves position bits, matching the source interpretation. Exact physical register behavior remains unverified.

With one committed frame (four bytes), another case publishes an entire descriptor 0. If the field means last valid descriptor, as in LibXenon, it announces 128 bytes with only four committed. That consequence is conditional on the register meaning, not observed Xbox DMA beyond committed content. The allocation remains larger, so it is distinct from E51's allocation overflow.

## Overflow before reduction

The routine converts the full application counter to bytes before reducing modulo buffer size. Actual frames_to_bytes first computes signed `size * runtime->frame_bits / 8`. For 32 bits/frame and `LONG_MAX/32 + 1` frames on the 64-bit host, UBSan reports the expected signed overflow. The retained diagnostic is a successful defect reproduction, not a normal successful execution.

The synthetic value is below a possible native ALSA boundary: pcm_native.c doubles boundary while it remains below LONG_MAX−buffer_size. The 32-bit compatibility path recomputes a smaller limit; reachability is therefore not claimed for the installed PPC32 applications. No extremely long physical stream ran. The correction must bound/reduce frames before conversion or convert an explicitly bounded delta.

## Replacement contract

ALSA ack tracks appl_ptr changes. pcm_lib_apply_appl_ptr updates that pointer before the callback and restores the previous value on failure. A rejected callback must therefore neither consume private progress nor partially publish a queue. NO_REWINDS can declare monotonic consumption; boundary wrap must remain valid and distinct from rewind.

| Case | Required behavior |
|---|---|
| No new data | No publication even if pointer is queried again |
| Full ring committed at once | Do not confuse modulo zero with no data |
| Write completes a descriptor | Publish complete blocks only after DMA barrier |
| Partial final write followed by drain | Exact final content or defined silent padding, without indefinite wait |
| Counter wraps at boundary | Correct forward delta without signed overflow |
| Invalid rewind/jump | Reject before mutation, consistent with ALSA rollback |
| Prepare/reset/stop then restart | Rebase private accounting to core conventions |
| Two outputs | Independent counters and publication |

Prepare runs before the core's generic reset, so capturing old appl_ptr there is wrong. Reset during playback also has a separate path. At E58 descriptor-length encoding still differed between Linux and LibXenon; changing a partial descriptor during DMA without understanding fetch behavior would introduce another hardware assumption.

## Additional references and limits

[Xenon Emulator AudioController](https://github.com/xenon-emu/xenon/blob/0284bbe6c8125935d97bf54ab3132089c6c65c8b/Xenon/Core/PCI/Devices/AUDIOCTRLLR/AudioController.cpp), revision `0284bbe6c8125935d97bf54ab3132089c6c65c8b`, logs writes but implements no descriptor consumption/sample reading in that class. It is not a reference model for length or end-of-queue semantics. This conclusion concerns that file/revision, not every emulator device.

Pinned local sources: Linux `a293dd19311668900eb1eeb2f6cb01dcac54f330` and LibXenon `a333adef440f28b436a667be0a4f014afce6349d`. LibXenon sound.c uses a last-complete-block index, but its submission routine does not by itself solve arbitrary ALSA drain lengths. Its suspicious base-register read during restart must not be copied without verification.

Evidence: `evidence/2026-10-02/audio-submission/validation.json` and `sources.json`. Retrieved third-party sources remain local; public material contains hashes, references, original models, and assertions.

```sh
python3 research/tests/check-audio-submission.py --source AFTER_0012/sound/pci/snd-xenon.c --pcm-header SOURCE/include/sound/pcm.h --output submission.json
```

E58 performs no console interaction. The next step is a complete submission/end-of-stream contract before replacing pointer/ack. The audio variants remain unsuitable for activation until these paths and the DMA protocol are validated.
