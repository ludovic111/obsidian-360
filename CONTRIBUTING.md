# Contributing

Read [AGENTS.md](AGENTS.md), [STATE](docs/STATE.md), and [EXPERIMENTS](docs/EXPERIMENTS.md). Write contributions in English. For each change, explain the concrete problem, exact source revision, test, limitations, and recovery path. Distinguish host simulation from console validation.

Do not attach secrets, firmware dumps, proprietary game executables, or assets to issues or commits. Use synthetic parser fixtures and keep personal acquisitions outside Git. Never replay archived installation scripts or the flash probe that hung the console.

Do not change power settings or thermal protections for benchmarks. Prefer off-console software tests for memory faults. Every proposed boot change must preserve an explicit selection of the last working system and explain recovery limits.

Original contributions use the MIT license unless they modify material under another upstream license; preserve that license and its attribution. Kernel-derived patches retain the kernel's applicable GPL terms. See [THIRD_PARTY.md](THIRD_PARTY.md).

A useful experiment submission includes:

1. A precise question and a falsifiable expectation.
2. The initial hardware/software state and source identities.
3. The exact action, duration and access limits, and what would stop the experiment.
4. Machine-readable observations and checksums, with private identifiers removed wherever they are not needed for the result.
5. The result, competing explanations, recovery steps, and a justified next action.

A passing model is evidence about that model and the exercised code. It is not proof of undocumented silicon behavior, DMA completion, electrical safety, or general compatibility across Xbox 360 revisions.
