---
title: "Devlog #008 — First Contact with the World Map"
date: 2026-04-03
tags: ["devlog", "reverse-engineering", "darklands", "dosbox-x", "runtime", "tooling", "world-map"]
description: "Static analysis hits its limits, so we build a live runtime path. A patched DOSBox-X finally yields the world map's first confirmed breakpoint — and changes what it means to be blocked."
summary: "Static analysis hits its limits, so we build a live runtime path. A patched DOSBox-X finally yields the world map's first confirmed breakpoint — and changes what it means to be blocked."
---

Every analysis session so far has worked the same way: the agent opens Ghidra, decompiles
functions, follows cross-references, saves findings. That model got us 382 named functions,
a fully mapped dispatch table, a complete memory pool layout, and a decoded status icon set.
It is a good model — until it isn't.

This session is about what happens when static analysis runs into something it genuinely
cannot answer alone, and what we built to handle that cleanly.

---

## The Problem: The World Map Has No Static Anchor

Phase 2's current goal is mapping the dispatch table — specifically, which function handles
which of the 99 game states. The state machine is confirmed: `MOV ES,[0x7d10]` / `SHL BX,2`
/ `CALLF ES:[BX]`. The table entries are 4-byte far pointers. The initial state is `0x29`.

The problem is that Darklands uses RTLink overlays. The functions that handle individual
game states are loaded dynamically into overlay segments whose addresses change at runtime.
Static analysis can see the dispatch mechanism but not the targets. Reading the table requires
a live process.

For city navigation, this was already partially solved by earlier Codex sessions on the master
machine. Three gates were confirmed: `20F7:036F` for the side-street departure action,
`169A:347C` for named-place / interior-action entry, `2120:00DF` for the broader movement
circulation. These are now in the knowledge base as established facts, not raw session notes.

The world map had no equivalent. Every static lead pointed to the overlay loader family —
`19C0:021C`, `19C0:052B`, `19C0:07A2` — but those are the overlay manager itself, not the
game logic. We needed a runtime session to find out where the world-map code actually lives.

---

## Four Negative Probes and One Patch

The first attempt set breakpoints on the two most promising candidates — `19C0:021C`
(the `rtlink_overlay_dispatch` anchor) and the old Quickstart lead `20F6:0008` — then had
an operator pilot Darklands through `Quickstart → departure choice → leave for open country`.
The world map appeared on screen. No breakpoint fired.

The second attempt replaced those two with `19C0:052B` and `19C0:07A2`, the next candidates
in the overlay-manager family. Same path, same result: the world map loaded cleanly, the event
log contained only startup and breakpoint-arm acknowledgements.

Two clean negatives established something important: first world-map arrival in the current
DOSBox-X setup does not pass through the trusted overlay-manager family at all. The world-map
branch uses a different code path, or a different segment family, or arrives too early or
too late for the probes to catch it.

At that point we tried a different approach: instead of setting breakpoints on suspected
addresses, just break into the debugger mid-session once the world map is visible and read
wherever the CPU happens to be standing. That should give a real runtime foothold regardless
of which code path was used to arrive there.

It didn't work. The socket accepted the connection, the attach succeeded, but `queue_debug_break`
produced no response during normal gameplay. The command socket was only being drained from
debugger and event-emission paths — not from the main emulation loop. Commands sent while
the game was running simply sat in the buffer.

Codex identified the issue in `debug_socket.cpp` and patched the main emulation loop to call
`DEBUG_Socket_Poll()` continuously when the socket is enabled. One rebuild later, mid-session
commands worked. The patch is now the standard binary on the master machine.

---

## `4A66:0E20`

With the patched binary, the first live world-map break worked immediately. The operator
reached the world map, the socket client sent `queue_debug_break`, and the debugger entered
at `CS:IP = 4A66:0E20`. Registers: `EAX=0xE9`, `EBX=0x07`, `ECX=0x01`, `EDX=0x00`,
`DS=7A3E`, `SS=3A3E`.

That address was then set as a breakpoint and the game was resumed. The breakpoint fired
again within milliseconds — without any input from the operator. Then again. Then again.
The address re-enters continuously while the player sprite is simply present on the world
map and idly animating. It is not a one-shot arrival event. It is a recurring hook inside
whatever loop keeps the world map alive.

To check whether it responded to input, the socket client queued a single right-arrow keypress.
The next hit at `4A66:0E20` came back with a noticeably different register pattern: `EBX=8`
instead of the `EBX=6` seen on idle re-entries, plus a shifted `EAX`/`ECX`/`ESI`/`EDI` cluster.

So `4A66:0E20` is both autonomous and direction-input-sensitive. It fires while idle, and it
changes signature when the player does something. That places it firmly inside the active
travelling-map state family — consistent with the static lead that state `0x0c` corresponds
to the Darklands world map — though it is not yet confirmed as the dispatch-head for that
state. It could be a callee two levels deep.

The world map is no longer unanchored.

---

## The Adapter

Parallel to the corroboration work, the DOSBox-X debug socket adapter was implemented and
corrected. `dosboxx_client.py` is a thin Python adapter over the patched DOSBox-X socket
protocol: attach, set breakpoints, continue, read registers, wait for events, take screenshots.

Getting the wire format right took several rounds. The patch source uses `"command"` not `"cmd"`,
`"address"` not `"addr"`, `"delay_ms"` not `"delay"`, and events carry an `"event"` field not
`"type"`. Registers arrive in a separate `registers` event after the `command_result`
acknowledgement, with lowercase extended field names (`eax`, `ebx`, `cs`, `ip`) rather than
short-register names. These were all corrected against the source.

The one permanent limitation: there is no backend breakpoint index in `command_result`,
so individual breakpoint deletion cannot be routed to the backend. `delete_breakpoint`
de-registers from the adapter only; the backend continues to break at that address.
`clear_all_breakpoints` works by sending `delete_breakpoint` with no index, which the patch
routes to `BPDEL *`. That is enough for session teardown.

Eleven MCP tools are now available for guided sessions: `dosboxx_attach`, `dosboxx_detach`,
`dosboxx_set_breakpoint`, `dosboxx_delete_breakpoint`, `dosboxx_list_breakpoints`,
`dosboxx_clear_all_breakpoints`, `dosboxx_continue`, `dosboxx_read_registers`,
`dosboxx_wait_event`, `dosboxx_take_screenshot`, `dosboxx_read_events`.

---

## Knowing When to Stop

The deeper tooling change this session is in the agent's own decision-making.

Until now, when static analysis ran out of road, the agent's options were: escalate to Opus
(useful for hard reasoning), or keep going and risk speculating. Neither is right when the
blocker is a runtime fact — a dispatch table that can only be read from a live process, a
branch condition that requires a register value that Ghidra cannot determine.

The agent now has a third option: `request_runtime_evidence`. Calling it writes a structured
request to `output/runtime_request.json` — question, why blocked, address to observe,
what observables are needed, possible outcomes — then pauses the session cleanly with
`stop_reason: pending_runtime_evidence`. A human takes the request to Codex on the master
machine, a guided session produces the answers, and the results are written to
`output/runtime_evidence.json`. On `--resume`, the evidence is injected into the initial
message so the agent picks up exactly where it stopped.

The session prompt now includes an explicit boundary: call this tool when further progress
would mostly be speculation. Do not call it for things Ghidra or Opus could resolve.

This matters because the state-handler mapping work — the current highest priority — is
exactly the kind of problem that hits this boundary. The dispatch table is live data.
Reading it requires a running process. When the agent reaches that wall, it now has a way
to ask precisely the right question rather than guess.

---

## What's Next

The immediate priorities going into Session 009:

1. **Correlate `4A66:0E20` with the static state-handler work.** In Ghidra: find the
   function at that address, determine whether it is directly referenced by the dispatch
   table or is a callee, and look for branches on the values 6 and 8 — the constants
   that distinguish idle from direction-input re-entry. This is likely the fastest path
   to binding the runtime anchor to a named function.

2. **Use `request_runtime_evidence` to read the dispatch table.** Once the agent reaches
   the point where only a live segment read will resolve the table targets, it should stop
   and ask. The infrastructure is now in place for that to be a clean handoff rather than
   a dead end.

3. **Follow `0x9060`/`0x9062` to the character data area.** This thread from Session 007
   is still open. Every function that reads through that far pointer is a candidate for
   touching the full `0x22a`-byte character struct.

The world-map anchor changes the shape of the next session. The agent no longer needs to
hope that the dispatch table can be inferred statically — it can ask for a live read and
resume with the answer.
