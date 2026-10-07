# Audio shutdown and PCI guarantees — E72

## Question

E66 shows that returning an ALSA callback error does not retain managed buffers. One possible approach is to block new PCI transactions and wait for outstanding ones. Before using that as a memory-release condition, the actual Linux helper contracts must be established.

This experiment extracts **seven real PCI functions** from pinned `techflashYT/linux-custom@a293dd19311668900eb1eeb2f6cb01dcac54f330` and executes them under ASan/UBSan with mocked configuration accesses and delays. No console register is written.

## Source and test results

- `pci_wait_for_pending_transaction` returns **1 immediately** when `pci_is_pcie` is false. The harness counts **zero reads and zero waits** in that path. Success is therefore not an observation that transactions finished.
- In the PCIe path, the helper reads status at most four times, with 100, 200, and 400 ms delays. Six cases cover no capability, every possible clearing observation, and persistence. Delays are simulated; no hardware latency is measured.
- `pci_clear_master` reads PCI_COMMAND, writes it with MASTER removed if necessary, then sets `is_busmaster` false. It neither waits for DMA completion nor verifies the write by reading it back.
- An injected write failure leaves the simulated hardware MASTER bit set while the software flag becomes false. For a non-PCIe device, the generic wait still returns 1. This demonstrates an inadequate proof combination, not an observed Xbox failure or a newly claimed generic kernel bug.
- 512 cases test capability-search start for 256 header types with two status values; sixteen cases exercise MASTER clearing with/without write failure and preservation of other command bits. Read failures are not injected.

## Relationship to console evidence

E64's **October 2, 11:22:10 console-time** capture contains a 64-byte `1414:580c` header: type 0, PCI_STATUS **0x0288**, and a zero capability pointer. CAP_LIST (0x10) is absent. With that configuration and standard kernel enumeration, no PCI Express capability is found; `set_pcie_port_type` does not populate `pcie_cap`, so `pci_is_pcie` remains false.

This is an inference from a configuration capture and source behavior, not a direct read of the live `pci_dev` structure. A refresh attempt at 13:47:19 host UTC timed out while the user's boot test was pending; it supplied no new header and did not prove a freeze. The later E73 runtime capture, received at **13:54:16 host UTC**, successfully read the header under obsidian-clock: it matches E64 byte for byte and still shows no bound audio driver. `audio-isolation/header-refresh.json` records that update.

The platform's ECAM configuration mechanism does not itself give every endpoint a PCIe capability. No audio BAR registers were read after the reboot, so no current analog/digital engine state is inferred from this header.

## Driver consequence

Do not use `pci_clear_master(); pci_wait_for_pending_transaction();` as a sufficient buffer-release guarantee. On the identified path the second operation does not interrogate the endpoint. A successful readback of MASTER clear would establish PCI_COMMAND contents, not by itself completion of every previously initiated access.

The issue covers both PCM samples and descriptors. The candidate already calls quiesce before `snd_card_free` on remove and failed-probe paths. Deferring all shutdown to `card->private_free` would be too late: `snd_card_do_free` first frees ALSA devices and their buffers, then invokes that private callback. Nevertheless, the current quiesce still lacks the necessary hardware-completion proof.

The next design must separate ALSA lifetime from DMA lifetime, retain memory in quarantine on unconfirmed stop, and prevent reuse of the affected channel. Merely retaining a pointer does not retain an ALSA-owned allocation. A complete solution must address remove, failed probe, user mmap, descriptors, and module reload. This analysis does not claim to implement that quarantine.

## Reproduce without hardware

```sh
python3 research/tests/check-pci-quiescence.py \
  --kernel LINUX_SOURCE_DIR \
  --header-capture evidence/2026-10-02/audio-control/pci-state.json \
  --output NEW_REPORT.json
```

The output path must be new. Upstream functions are extracted locally, not copied into the repository. Source/function hashes are in `evidence/2026-10-02/audio-isolation/pci-contract.json`. The harness does not simulate internal controller queues, the physical bus, or electrical reset effects.
