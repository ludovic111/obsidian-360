# Analog acknowledgement and reset — E67/E68

## Plan before hardware interaction

E65 left analog control at 0x0000001d and index zero. A new read confirmed this under obsidian4 at 12:58:51 console UTC; digital remained 0x1d08001c / 0x00009616. The hypothesis was that analog status bits 2, 3, and 4 clear independently when written as one, while bit 0 indicates halted state.

`research/audio/analog_protocol_step.c` provides four fixed operations, never automatically chained. Each requires no bound driver, PCI 1414:580c, the expected BAR, and four exact observed words. It can write only one word at +0x08; RUN and IRQ enables remain zero. Accepted paths have at most eight reads and one write. Any precondition mismatch rejects the write.

| Option | Required analog control | Write | Prediction at preparation time |
|---|---|---|---|
| --ack-bit2 | 0x0000001d | 0x00000004 | 0x00000019 |
| --ack-bit3 | 0x00000019 | 0x00000008 | 0x00000011 |
| --ack-bit4 | 0x00000011 | 0x00000010 | 0x00000001 |
| --reset-stopped | 0x00000001 | 0x02000000 | Reset bit clears; observe resulting status |

Every operation also requires analog index zero and unchanged digital words. Inspect each result before the next operation. On divergence, do not silently change expected values or proceed. Reset is allowed only after reviewing acknowledgements and verifying the stopped state. No descriptor publication, START, SMC, PCI configuration, or flash access; digital is not written.

MMIO can hang despite bounded access count. Lost access needs coordinated physical recovery; do not repeat a timed-out operation without establishing its outcome. There is no deliberate reboot or inherited-DMA restart. These are stopped-status/reset tests, not sound-output tests.

## Tool validation

Actual C harness under ASan/UBSan checks four allowed operations, **512** rejected single-bit mutations, and a four-byte write footprint at +8 with no RUN/IRQ enable. Static ELF32 PowerPC builds without warnings; disassembly shows one aligned stw with byte-order conversion and hwsync/eieio. This validates the tool, not the hardware protocol. Evidence: `evidence/2026-10-02/audio-ack/`.

## Observed results

E67's three separate calls produced exactly **0x1d → 0x19 → 0x11 → 0x01** after writes 4, 8, and 16. The halted bit remained set and only the targeted bit disappeared. Digital words and indices remained unchanged. This establishes observed W1C behavior of analog bits 2–4 in this stopped state, not each event's meaning during playback.

Evidence: `ack-bit2.json`, `ack-bit3.json`, `ack-bit4.json`. Twenty-four MMIO reads and three writes total; all calls exited zero and SSH responded. Step timestamps came from the console, while collection envelopes came from the Mac. E69 subsequently investigates their discrepancy; do not infer cross-machine latency from unsynchronized dates.

E68 wrote **0x02000000** from analog 0x00000001, then immediately read **0x00000001**, with zero index and unchanged digital words. Eight reads, one write, exit zero; `reset-stopped.json`. No START or new buffer.

This is compatible with a self-clearing reset bit, but that bit was never observed set and all other observed fields already matched the predicted reset state. These observations therefore cannot distinguish a complete internal reset from an ignored command. Effects on unread registers are unknown. Do not claim full reset validation.

E67/E68 total four analog writes, 32 reads during operations, and four initial reads. Descriptor addresses were neither read nor replaced. The pre-reboot analog channel was left stopped with event bits acknowledged; digital was unchanged. E73's reboot supersedes that state, so future probes need fresh preconditions.
