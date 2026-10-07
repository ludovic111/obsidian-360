# Research map for this console

This map organizes the current objective; dated evidence in STATE and EXPERIMENTS takes precedence. Source analysis, direct measurement, simulation, and hypotheses are distinct. Software identification cannot replace physical chip markings.

| Area | Established evidence | Unknowns and useful next evidence |
|---|---|---|
| Board and chips | GPU PCI signature compatible with the Jasper family; 12 PCI functions inventoried | Physical motherboard, RAM, flash, and Southbridge markings; exact revision |
| CPU and interrupts | Six visible threads; IPI callback source/binary analysis and correction in obsidian4 | IRQ affinity, load behavior, and real reachability of the corrected callback |
| Timebase | E73 clock kernel booted; 60-second raw-rate bounds −28.16 to +14.43 ppm relative to Mac | Longer independent measurements; absolute wall clock still approximately 243 seconds behind |
| RAM / DMA | 64 KiB pages; source audits of DMA and graphics allocations | Reservations, cache/coherency constraints, isolated bandwidth measurements |
| GPU / HDMI | Measured 720p desktop and corrected allocation; offline libxenon f1/f2 traces | Complete 1080p clocks and ANA/HANA sequence, acceleration, command formats |
| Boot / security | Observed stock → game → temporary patches → XeLL → kernel → HDD chain | Exact loader identity, independent boot, validated recovery before replacement |
| ROM / hypervisor / dashboard | Functional dependencies in the current boot path | Exact component analysis; interfaces and silicon are not exhaustively understood |
| NAND | BAR1 mmap freeze archived; separate source-level HTTP buffer defect found | Restorable acquisition appropriate to flash geometry, ECC, bad blocks, matching reads; do not repeat mmap |
| SMC / thermal / power | hwmon temperatures, historical status requests, corrected cache bounds | Concurrency and timing contracts; instrumented power measurement; protections preserved |
| Ethernet | Observed 100 Mbit/s full duplex and SSH; GRO disabled | Sustained throughput and stability; historical watchdog cause unresolved |
| SATA / storage | Working internal ext4 root and swap | Controlled cache/disk-separated throughput, controller details, historical backup structure |
| Optical drive | PLDS DG-16D2S 0251; partial audio CD reads succeed; two DVDs report absent | Known-good DVD elsewhere, capabilities response, optics/mechanics; exact firmware unacquired |
| USB / controls | Keyboard/controller identified and historical events observed; E73 desktop responsiveness reported | Physical resize regression, keyboard repetition, HID consistency and latency |
| Audio | Offline geometry/lifecycle/queue/adapter contracts; bounded historical STOP/ACK experiments | Completion and DMA quiescence unresolved; prior register state superseded by E73 reboot; no sound validation |
| Linux / desktop | obsidian4 and later clock boot verified; Xorg/IceWM; isolated resize deadlock reproduced and avoided | Physical resize test, memory/startup optimization, package-signature policy, launcher cost |
| Rust / replacements | Original dependency-free, unsafe-free XEX2 inspector tested on host | Real-file compatibility, PowerPC ABI/build, measured benefit; no performance gain claimed |
| Games and formats | XEX2 headers compared with Xenia; synthetic parser tests | Legitimate real samples, imports, PE, instructions, APIs, shaders, assets, and frame lifecycle |

Every experiment should retain exact code, versions, commands, failures, hashes, results, and limitations. Confidential dumps belong in ignored storage. Publish shareable metadata and analysis only. Readers must be able to distinguish hardware observations from local models and locate an actually validated recovery path.
