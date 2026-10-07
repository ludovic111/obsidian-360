# Audio stream tracking and synchronization — E57

Patch 0012 follows 0011. Each output owns its timer; START arms it, STOP marks the stream stopped, and sync_stop waits for callbacks before reconfiguration. Host tests pass. The final high-resolution variant builds with 70 modules and no warnings; nothing was installed on the console.

## Previous defects reproduced

The harness extracts 0011's actual C functions. START arms no timer. Directly invoking the historical callback twice with unchanged zero position generates two period notifications despite no movement. This reproduces a latent accounting defect off hardware; the unarmed timer itself prevented normal execution of that callback on this path.

Historical calculation compared buffer size minus estimated queued data against one period, without tracking progress since the previous notification. The callback also unlocked and reread playback_substream without a PCM lifetime guarantee.

## New tracking

Each channel gets a relative soft hrtimer before ALSA takes resource ownership. Open no longer clears the whole device structure and destroys its timer. START records initial position, resets period progress, and arms a nominal **200-microsecond** interval.

Under the driver lock, the callback reads descriptor index, computes modulo-buffer movement, and accumulates bytes. Unchanged position adds nothing. Remainder survives notification. If multiple periods elapsed, one snd_pcm_period_elapsed call suffices for the ALSA core to update position/availability, as documented in `sound/core/pcm_lib.c`.

Position remains descriptor-granular. Residual length is not used until hardware semantics are established. Periods smaller than a descriptor may be reported late; no real latency target is claimed.

A modulo counter cannot distinguish no movement from a complete unobserved ring. If elapsed time reaches one theoretical buffer duration at 48 kHz, stereo 16-bit, the candidate stops and reports XRUN instead of guessing. Negative simulated elapsed time is rejected too. This conservative policy can stop a stream after scheduler delay even if hardware did not consume a full ring. It assumes the expected rate; it does not validate actual controller throughput.

## Locks and close

In the examined ALSA contract, trigger/pointer are atomic with local interrupts disabled. The timer takes the driver lock with interrupt-state preservation and releases it before snd_pcm_period_elapsed or snd_pcm_stop_xrun, which may acquire the ALSA lock and call STOP. STOP during notification prevents rearming.

STOP does not cancel synchronously: waiting for a callback that needs the already-held ALSA lock could deadlock. sync_stop cancels outside the driver lock after stop and before reconfiguration. Hw_free stops the channel, invalidates geometry, then synchronizes before returning to ALSA. Close uses that path before clearing ownership.

Card removal marks shutting_down, stops both channels, cancels both timers, and clears bus mastering before releasing resources. The flag blocks START. Actual DMA completion is not proven by a register write/readback; E66 and E72 later analyze this lifetime gap.

## Separate high-resolution configuration

Inherited configuration had HIGH_RES_TIMERS disabled and HZ=300. Requesting 200 microseconds cannot provide that cadence with approximately 3.33 ms ticks, while the minimum 128-byte buffer contains only **0.667 ms** of audio.

The candidate enables CONFIG_HIGH_RES_TIMERS; derived choices include TICK_ONESHOT and SCHED_HRTICK, with the full diff retained. Open returns -ENODEV unless the channel timer reports active high-resolution mode. Compilation does not prove activation on every CPU or actual latency. Nominal cost can reach **5,000 callbacks per second per output**; CPU cost needs measurement after a coordinated boot once protocol issues are resolved.

## Evidence and failures

Actual driver functions are extracted, not rewritten in the harness.

- Fifteen tracking scenarios cover fixed/nonzero start positions, threshold/remainder, multiple periods, wrap, per-output stop/cancel, stop during notification, delay boundaries, backward simulated time, zero period, remove, and concurrent close.
- The concurrent pthread case suspends notification at a controlled point; hw_free must wait at cancellation before simulated free. The other channel stays armed. This covers one explicit interleaving, not every kernel schedule.
- Twenty resource cases cover both active timers and partial allocation failures.
- Fifteen PCM cases include zero/oversized period and unavailable high resolution. Geometry regression retains 512 accepted sizes among 16,369 with no out-of-buffer descriptor.

ASan/UBSan are active; kernel locks, ALSA, DMA, MMIO, and hardware time are models. Clean output is not an SMP, real-time, or hardware proof.

Two initial full builds succeeded with the old low-resolution configuration. The first source variant failed the stricter host harness on two signed/unsigned comparisons; conversions and negative-time handling were corrected. Initial artifacts remain separately hashed and do not prove the final high-resolution build.

A geometry-test invocation used unsupported --output; redirecting JSON stdout fixed the command, and E55's recipe was corrected. This was not a geometry failure. Evidence: `evidence/2026-10-02/audio-poll/`. Patches 0008–0012 reconstruct the three candidate sources exactly; final configuration and earlier logs remain identifiable.

## Reproduction and remaining work

```sh
python3 research/tests/check-audio-poll.py --previous AFTER_0011/sound/pci/snd-xenon.c --candidate AFTER_0012/sound/pci/snd-xenon.c --output polling.json
python3 research/tests/check-audio-lifecycle.py --original ORIGINAL/sound/pci/snd-xenon.c --candidate AFTER_0012/sound/pci/snd-xenon.c --output lifecycle.json
python3 research/tests/check-audio-pcm.py --source AFTER_0012/sound/pci/snd-xenon.c --output pcm.json
python3 research/tests/check-audio-buffers.py --original ORIGINAL/sound/pci/snd-xenon.c --candidate AFTER_0012/sound/pci/snd-xenon.c > buffers.json
```

Use the supplied configuration and E53 LLVM 16 environment, LOCALVERSION=-audio-poll, and olddefconfig/vmlinux/modules targets. No initramfs or XeLL image was prepared.

At E57, sample publication in pointer still needed replacement by bounded appl_ptr tracking through ack. Descriptor length, low-memory range, and analog/HDMI initialization remained unresolved. No sound or new hardware interaction occurred; E56 was the latest live check.

## Final build verified

**6.18.11-xenon-audio-poll**, with HIGH_RES_TIMERS enabled, completed olddefconfig, vmlinux, and modules with exit zero. Kernel and all 70 modules are ELF64 big-endian PowerPC with matching vermagic and source/config hashes. No warnings. Evidence: `final-build.json`, `final-build.log`, `final-artifacts.json`. No boot/load validation. E58 investigates remaining publication defects in [AUDIO-SUBMISSION-AUDIT](AUDIO-SUBMISSION-AUDIT.md).
