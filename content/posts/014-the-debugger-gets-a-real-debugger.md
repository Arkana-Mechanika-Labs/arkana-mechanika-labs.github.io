---
title: "014 - The Debugger Gets a Real Debugger"
date: 2026-04-12
summary: "Socket-driven breakpoints kept failing while manual DOSBox-X debugger UI worked fine. A day of systematic isolation identified one flag as the culprit, rebuilt the binary with native stepping and disassembly, and left the toolchain in better shape than it has ever been."
---

## The Problem That Wouldn't Die

After catching the exact instruction that adds a character to the party in [devlog 012](/posts/012-catching-the-party-writer/), and characterising the custom record-driven loader in [devlog 013](/posts/013-anatomy-of-the-loader/), the expectation was that the hard runtime work was behind us. The toolchain had produced real results. Time to keep going.

Except the socket-driven breakpoints kept failing.

The session would launch, attach, arm `11E3:052B` — the confirmed Quickstart loader entry — and then the breakpoint would simply not hit. No event. No stop. Meanwhile, if you opened the DOSBox-X debugger UI and typed `BP 11E3:052B` by hand, it hit immediately. Every time. The manual path worked. The socket-driven path did not.

This had been attributed to timing, stale state, adapter quirks. Today that explanation ran out of road.

## Divide and Conquer

Rather than continuing to patch symptoms, we introduced **staged launch modes** — a way to reintroduce DOSBox-X startup arguments one group at a time and test the known anchor `11E3:052B` after each addition. The baseline (`-debug-socket` only) worked. Adding the `C:` mount worked. Adding `c:` and `darkland.exe` and `-fastlaunch` all worked. The anchor continued to hit at every stage.

Then `-defaultconf` was added.

The breakpoint stopped hitting. Not just through the socket path — in the *manual debugger UI* too. This was not a transport regression. The `-defaultconf` flag changes the runtime layout enough that the trusted `11E3:052B` anchor no longer corresponds to the same code. The whole `11E3:*` Quickstart family silently becomes invalid.

This is now a **hard guard**: `-defaultconf` is prohibited for any Darklands runtime session that relies on known anchor addresses. The guard is enforced in code — the host runner refuses to launch with that flag rather than silently producing misleading breakpoint behavior.

## What the Root Cause Was

Digging into why socket-driven breakpoints differed from the manual UI path revealed a separate but related issue: the socket `set_breakpoint` command was bypassing the internal DOSBox-X debugger `BP` parser path and trying to create breakpoints directly in the backend. Something in that parser path — likely a debugger-loop or cache coordination side effect — was needed for breakpoints to actually arm correctly in the running emulator.

The fix was to route socket `set_breakpoint` through the real `BP` parser, recover the backend breakpoint ID afterward via `list_breakpoints`, and resume the emulator only if the adapter had interrupted a running session to install the breakpoint. This made socket-driven breakpoints behave the same way as manual `BP` commands.

## New Capabilities

While isolating the launch issue, Codex added several capabilities that had been missing from the toolchain:

**Native stepping.** `step`, `step_over`, and `step_out` are now socket commands backed by the DOSBox-X debugger internals directly — not fake stepping from the adapter side. Validated live: `step` advanced deterministically from `11E3:052B` through the far call at `11E3:0598 -> 11E3:021C`; `step_out` from inside that call returned cleanly to `11E3:059D`; `step_over` at the same far call landed at the same return site.

**Native disassembly.** A new `disassemble` socket command accepts a segment, offset, and instruction count and returns structured per-instruction output — bytes, size, and rendered text — directly from the DOSBox-X backend. No more byte-scraping or ad-hoc text parsing.

**Chunked memory dump.** `dosboxx_dump_memory_range` reads an arbitrary memory range in chunks, writes a hex artifact and a metadata JSON to `output/dosboxx_dumps/`, and handles the chunking automatically. This is what now feeds the overlay materialisation workflow that created the `15DF` dump in [devlog 012](/posts/012-catching-the-party-writer/).

**Transport recovery.** The MCP layer can now recover from stale adapter/wrapper state around DOSBox-X and Ghidra without treating every transport hiccup as a total session loss. Safe operations retry after probing the socket; Ghidra-backed operations retry after verifying the REST server is alive. Diagnostics are written to `output/mcp_transport_diagnostics.jsonl` so future failures leave a useful record.

**Raw debugger passthrough.** `debugger_command` and `break_into_debugger` are now first-class tools, letting guided sessions send arbitrary debugger commands over the socket when the higher-level helpers are not the right fit.

## Stepping Through the Quickstart Chain

With the rebuilt binary (version `2026.04.12`), one clean end-to-end validation: attach on the minimal launch path, arm `11E3:052B` via the socket, have the operator click Quickstart, and watch it stop. Then step through the loader chain:

- `11E3:052B` → reads caller thunk entry, rewrites pending far return to `11E3:0698`
- `11E3:0598` → far call into `11E3:021C` (the resolved-record dispatcher)
- `11E3:021C` → calls `11E3:05A7`, stores resolved record pointer into `[09E8]`, returns
- `11E3:059D` → return from the far call
- Through `11E3:05A6 ret -> 11E3:1ADE -> jmp 1699:0000`

The full handoff chain, stepped instruction by instruction, confirmed live. The toolchain now has enough debugger-grade control to do this without touching the UI.

## State of the Toolchain

The DOSBox-X socket layer is no longer a thin "send a command and hope" interface. After this session it supports: attach/detach, set/delete/list/clear breakpoints with backend-native IDs, continue, step/step_over/step_out, read registers, read memory, disassemble, take screenshots, queue keyboard/mouse input, and dump memory ranges to artifacts. Everything is documented in `coordination/dosboxx_capability_inventory.md` as the single source of truth for what the stack can actually do.

The next session can open with a running Darklands, arm a breakpoint, and step through real code without fighting the infrastructure.
