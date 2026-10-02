# Session interruptions and recovery

October 1, 2026 diagnosis based on structured local transcript events inspected read-only. Full logs remain outside Git.

Turns ending at 20:33:16, 20:34:10, 20:35:20, 20:55:01, and 20:55:34 UTC contain `last_agent_message: null` and `error.codex_error_info: cyber_policy`, with a possible cybersecurity-risk message. That platform control explains these particular interruptions. Earlier compiler/tool incompatibilities are separate incidents; repairing those does not repair or disable the platform control or guarantee uninterrupted future sessions.

The control cannot be disabled from this repository. Do not rephrase or split operations to bypass it. Documentation, verification, and driver work must be evaluated on their actual content. The diagnosis does not establish which specific operation caused every signal.

On resumption, `get_goal` reported active. The existing compiler process/container were still live, so no duplicate build was launched. The process later completed normally at 21:00:03 UTC with exit zero; the kernel and its ELF64 big-endian PowerPC format were verified.

To resume a build:

1. Read `.local/kernel-build/build-state.json` to locate the log/container.
2. Verify the actual process/container is live. A state file alone is not evidence.
3. Continue observing that same process if running. An observation timeout is not a failed build.
4. After confirmed termination, inspect the exit code and log, then verify artifacts before claiming success.

`tools/build-kernel.py` preserves each attempt and refuses to start while a build container already exists. This protects build recovery; it does not modify Codex or automatically restart interrupted turns.

Reference used to locate logs: [official troubleshooting documentation](https://learn.chatgpt.com/docs/reference/troubleshooting), “Feedback and logs.” No report or transcript was sent to a third party.
