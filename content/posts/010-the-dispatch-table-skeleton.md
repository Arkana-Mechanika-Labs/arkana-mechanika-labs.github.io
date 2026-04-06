---
title: "Devlog #010 - Reading the State Machine's Skeleton"
date: 2026-04-04
draft: false
tags: ["phase2", "state-machine", "rtlink", "runtime", "dosbox-x", "dispatch-table"]
---

_Published April 4, 2026_

The last devlog ended with a plan: follow the XREFs from `0xa891`, the travel map active
flag, and use them to find which Ghidra functions belong to the travelling-map state
family. That plan failed immediately. The failure was informative.

---

## The XREF wall

In Ghidra's model of this binary, cross-references for data globals in the BSS segment,
addresses like `0xa891`, `0x9C00`, `0xa772`, come back empty. The reason is specific to
16-bit real-mode analysis: Ghidra stores data references against segment-relative addresses,
not flat physical addresses. When you ask for XREFs on a flat BSS address, it does not find
the DS-relative accesses the compiler actually generated. Code XREFs work fine; data XREFs
on BSS globals do not.

The agent spent a session trying six different approaches to this, different addresses,
different call directions, different starting points, and got empty results every time
before cleanly calling `finish` with zero findings. That is the system working as intended.
The real fix was to document the limitation and change strategy.

---

## A better protocol

The right next question was not "which static function reads `0xa891`!=" but "what is in the
dispatch table!=" The game's state machine dispatches via a far-pointer table loaded at
runtime into an overlay segment invisible to Ghidra. The agent had been circling that fact
for two sessions. The question was how to get the data out.

The answer was a structured handoff. The agent writes a `runtime_request.json`,
specifying exactly what runtime address to probe, what memory to read, what the operator
needs to do to set up the right game state, and what each possible answer would unlock for
static analysis. That request sits in the repo until a human-driven DOSBox-X session
satisfies it and writes back `runtime_evidence.json`. The evidence gets injected automatically
at the next agent resume.

It sounds like overhead. In practice it collapsed three sessions of circling into one clean
exchange. The agent's part was asking the right question precisely. The runtime part was
answering it.

---

## What the dispatch table actually looks like

To capture the table, the DOSBox-X patch needed one new capability: `read_memory`.
We added it to the debug socket backend, rebuilt the binary, and ran a guided
Quickstart → world-map session. At the world map, a forced live break confirmed the state
(`DS:[0xa772] = 0x000C`), the dispatch table segment (`DS:[0x7d10] = 0x35D2`), and then
dumped all 396 bytes from `35D2:0000`.

<figure class="drp-screenshot">
  <img src="/images/dosbox_capture.png" alt="Custom DOSBox-X running Darklands on the world map with the debug socket active and register state captured" />
  <figcaption>The patched DOSBox-X mid-session on the world map. The debug socket is active, a forced break has halted execution, and the dispatcher read the dispatch table segment from <code>DS:[0x7d10]</code>. This is what the runtime evidence protocol looks like in practice.</figcaption>
</figure>

The result: 99 entries, each a 4-byte far pointer (offset:segment in little-endian).
Every single one uses segment **`11E4`**. The table is homogeneous, one overlay, all
state handlers, same segment.

Then the spacing became obvious.

States 0x00 through 0x62 (all 99 of them) except one fall at `11E4:2CC9` down to
`11E4:28FF`, **exactly 10 bytes apart**. That is not a coincidence. That is an array of
RTLink trampoline stubs, and every one of them has the same structure:

```asm
PUSH  overlay_id       ; which overlay to load
CALL  FAR rtlink_call_overlay  ; 0x1a12b, the RTLink loader
RETF
```

Ten bytes. Ninety-eight states. The game's state machine is not a table of function
pointers to resident handlers. It is a table of load-on-demand trampolines. When you
transition to state `0x2a` (for example), what actually runs is a 10-byte stub that loads
the relevant overlay and transfers control there. Most of the game logic never lives in
resident memory at all.

---

## The one exception

State `0x0c`, the travelling-map state, the world map, breaks the pattern entirely.

Its entry is `11E4:1F9F`. That is approximately 0xCBC bytes below the bottom of the stub
cluster. It is not a trampoline. It is a resident handler already loaded in the `11E4`
overlay when the dispatch fires.

This is consistent with what the earlier DOSBox-X sessions showed: `4A66:0E20`, the
confirmed recurring operational hook inside the world-map state, fires autonomously and
continuously while the map is active, not on a load-then-call-once pattern. A trampoline
would not explain that. A resident handler does.

So state `0x0c` is different in kind from the other 98. The travel map stays in memory.
Everything else loads on demand.

---

## What this means for static analysis

The dispatch table gives us the skeleton of the state machine for the first time. We can
now say: 99 states, all in segment `11E4`, 98 of which are RTLink trampolines. The actual
game logic for 98 states lives in overlays whose EXE file offsets are recorded in the
RTLink descriptor table at `0xb7a` in the static image.

The next static task is to find `11E4` in Ghidra. The runtime segment address
`0x11E4 × 16 + 0x1F9F = 0x13DDF` means nothing to the static analyser, that is a
physical runtime address, not a Ghidra flat address. To find the overlay, you read the
descriptor table at `0xb7a` (18-byte entries, `[6]` = EXE file offset for the overlay
payload), then locate that byte offset in Ghidra's flat address space. The resident handler
for the travel map, `state_handler_travel_map`, lives at `flat_base + 0x1F9F`.

That is the next session's opening move.

---

## The short version

- XREF strategy from devlog 009 hit a known 16-bit Ghidra limitation, documented and
  permanently redirected away from data-global XREFs
- Runtime evidence protocol tested end-to-end: agent asks, DOSBox-X answers, evidence
  injected at next resume, one exchange replaced two sessions of circling
- Dispatch table fully captured: 99 states, all in segment 11E4, uniform 10-byte RTLink
  stubs for 98 states
- State 0x0c (travel map) is the anomaly: `11E4:1F9F`, a resident handler, not a trampoline
- Path forward is clear: RTLink descriptor table at `0xb7a` → `link_offset` → Ghidra flat
  address → `state_handler_travel_map`
