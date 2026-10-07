# ALSA submission adapter — E60

Patch `0013-xenon-audio-submission.patch`, following 0008–0012, integrates the E59 queue into the candidate driver. Position queries no longer publish data. Commitments pass through ack, with bounded frame delta before byte conversion. The candidate remains experimental and uninstalled: final DMA descriptor completion is not decoded.

## Software contract

- Prepare initializes the queue, resets the channel, and expects ALSA's subsequent RESET. It does not use old appl_ptr as origin; post_prepare rebases it after the driver callback.
- Ack works on a queue copy, validates delta and initial position as needed, then commits. Failure changes neither queue, cursor, nor register. Actual pcm_lib_apply_appl_ptr restores the application's cursor on callback failure.
- Only complete blocks are published, after a DMA barrier. A full ring publishes all 32 blocks; an identical request publishes nothing. NO_REWINDS and internal checks reject rewind.
- Both outputs advertise SYNC_APPLPTR. ALSA then rejects control mmap, requiring cursor synchronization through ioctl so ack runs. Without this, moving publication out of pointer would be incomplete. Sample mmap remains allowed; the core also rejects status mmap for older alsa-lib compatibility.
- START arms tracking but starts DMA only after a whole block exists, supporting ALSA's START-then-DRAIN sequence for short streams.
- DRAIN rejects new commitments, zeros the final block's remainder, and publishes it. Silence is excluded from logical position reported to ALSA. Repeated drain does not write again.
- Pointer returns cached logical position, performs no MMIO, and never converts the full application counter.
- The timer accounts for index movement, rejects progress beyond submitted data, and notifies outside the driver lock. Close still waits for an active callback.
- RESET is accepted only for a prepared, empty queue at origin. Reset during playback or after submission returns -EBUSY without arbitrary rebasing. STOP followed by PREPARE allows a new stream. This is an explicit functional restriction.

RESET follows ALSA-then-driver lock order. Notifications happen after releasing the driver lock. The queue component itself provides neither synchronization nor hardware access.

## Final block remains unresolved

Tracking treats hardware index as the current block; index advancement means preceding blocks completed in the model. That interpretation and fetch-ahead behavior still need console verification.

An unchanged final index and zero residual can exist before the engine starts. The candidate does not treat them as playback success. If hardware remains on that index after playing the last block, drain completion will not be recognized. `stalled_final` reproduces this limitation and ends in stream error, not successful playback.

Late observation, backward time, or no progress for one theoretical ring duration triggers XRUN. This is software policy at 192,000 bytes/s, not a measured real-time bound; false refusals are possible. A synthetic advance to the next index tests final-padding accounting but does not prove hardware generates that event.

Descriptor encoding, DMA range, and HDMI/analog initialization were also unresolved at E60. Compilation does not resolve them. Do not load this candidate merely to declare functional audio.

## Reproducible verification

Use reconstructed candidate sources and Linux `a293dd19311668900eb1eeb2f6cb01dcac54f330`:

```sh
python3 research/tests/check-audio-adapter.py \
  --source CANDIDATE/sound/pci/snd-xenon.c \
  --kernel LINUX_SOURCE --output adapter-validation.json
python3 research/tests/check-audio-queue.py --output queue-validation.json
python3 research/tests/check-audio-lifecycle.py \
  --original LINUX_SOURCE/sound/pci/snd-xenon.c \
  --candidate CANDIDATE/sound/pci/snd-xenon.c --output lifecycle-validation.json
```

The harness extracts actual candidate callbacks, pcm_lib_apply_appl_ptr, and both ALSA control/status mmap decision functions. Fifteen ASan/UBSan scenarios cover fragments, full ring, rollback, reset, large counters/boundary wrap, both outputs, stagnation, delay, mmap, and controlled concurrent close. One scenario enumerates all 512 geometries. Other registers, clocks, and ALSA services are mocked; this is not complete ALSA execution or a general SMP proof.

Twenty candidate resource cases and thirteen expected original outcomes pass. The renamed queue repeats **54,008 operations and 24,544,033 compared frames**. Patch reconstruction matches all three compiled files; the integrated queue matches its canonical source except for the header filename.

## Retained failures and build

1. The first harness treated an upstream ALSA signed comparison as an error. Its warning is suppressed only around that unchanged function, not candidate code.
2. Docker could not create new mount targets inside a read-only source directory. A separate copy of sound/pci containing new files was overlaid instead; reference sources remain unchanged.
3. Initial integration found queue parameter `current` colliding with a kernel macro. Canonical sources renamed it `position`. The isolated E59 test did not include the macro and could not catch this conflict.

Initial failures, recipes, hashes, and final results are in `evidence/2026-10-02/audio-adapter/`. Build output is independent of audio-poll; obsidian4 artifacts are preserved. **6.18.11-xenon-audio-submit** and 70 modules compiled without warnings at 10:52:58 UTC, with PowerPC ELF/vermagic checks. No initramfs, XeLL image, installation, or boot was produced.

## Separate live check — E61

At 10:49:58 console UTC on October 2, SSH reported obsidian4, 9,327.35 seconds uptime, no failed units, and 1280 × 720 framebuffer. Standard kernel/systemd interfaces only; no visual, audio, or load validation. E60/E61 changed no console configuration and sent no reboot.
