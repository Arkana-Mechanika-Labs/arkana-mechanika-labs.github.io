---
title: "Devlog #017 - Tracing The Story Continues"
date: 2026-04-12T12:00:00
summary: "A runtime pass on the load/save screen decoded the full Down Arrow navigation path and identified four overlay families that own it, none of which are explained by the Create New World loader machinery."
---

## Two Paths from the Main Menu

After Quickstart and Create New World are well-characterised, the third main-menu option gets its first proper runtime analysis: **The Story Continues**, the load/save game screen.

The working hypothesis was that it might share the same `11E3:052B` loader wrapper already confirmed for Create New World. That turned out to be wrong. The Story Continues screen uses a distinct overlay family that the loader model does not yet explain.

## Four Families

A guided runtime session on the load/save screen, armed with the patched DOSBox-X stepping capability from [devlog 014](/posts/014-the-debugger-gets-a-real-debugger/), identified four overlay families that own this UI path:

| Segment | Role |
|---------|------|
| `24A0:*` | Higher-level controller logic |
| `0C9F:*` | Veneer / trampoline layer |
| `4A3E:*` | Input / action helper |
| `4A65:*` | Redraw and list update |

The session reached the controller entry point at `24A0:01C2` and the action-code decoder at `24A0:030A`, then stepped through a concrete user action (pressing Down Arrow on the save-game list) to trace the full dispatch path.

## The Down Arrow Path

Starting from the input helper and working outward:

1. `4A3E:0049`: action-driven navigation helper. This is where keyboard input for this screen enters the picture.
2. Returns to `24A0:01CB`, which is inside the enclosing controller loop at `24A0:01C2`.
3. `24A0:030A`: the action-code decoder. It receives `AX = SI = 0x5000` for the Down Arrow action.
4. The `0x5000` case resolves to `24A0:065A`, the concrete navigation/update handler.
5. `24A0:065A` updates four screen/list state globals (`8C4C`, `8C50`, `8C52`, `8C54`) then calls the veneer at `0C9F:04DC`.
6. `0C9F:04DC` is a thin trampoline on this path.
7. The real redraw/update worker is `4A65:009A`. This is where the list visually refreshes after cursor movement.
8. Returns to `24A0:067B`, back inside the `0x5000` handler.

The full path is linear: one user action → action code → one case handler → four state-global updates → veneer → redraw worker → return. No branch, no retry loop, no fallback.

## The Redraw Worker Is Real

The entry-frame reconstruction for `4A65:009A` is concrete:

- Far return address: `24A0:067B`
- Argument block on the stack at call time: `27F4, 00C4, 0016, 007B, 0010, 0012, 0010`

The first instructions at `4A65:009A` consume these stack/frame arguments directly. This is not another veneer: it is the genuine redraw/update logic for the load/save list.

The argument values look like display geometry: `0x00C4` = 196, `0x0016` = 22, `0x007B` = 123, `0x0010` = 16, `0x0012` = 18. These are plausibly viewport or item-row dimensions for the scrollable save-game list.

## The Loader Connection Is Missing

A widened resolver-record dump around `11E3:0E80` (the Create New World record) was checked for adjacent records whose `+00` field would match `4A3E`. No match. The `4A3E` family is not currently explained by the same slice of the resolver-record table that covers Create New World metadata id `0x002B`.

This means the load/save screen either:
- uses a different range of the resolver-record table (the table has more entries than the current slice shows), or
- is loaded through a different mechanism entirely

The four families identified here (`24A0`, `0C9F`, `4A3E`, `4A65`) are now confirmed runtime anchors. The highest-value next question is not "what helper does `4A65:009A` call?" but "which loader record and metadata ID owns this family?"

{{< figure src="/images/darkland_004.png" caption="The Quickstart party at the tavern, the state you're in when you'd press Escape to reach the main menu and choose The Story Continues." >}}

## What This Establishes

The load/save screen runtime model is now grounded in concrete anchors rather than inference from the Create New World path. The session confirmed:

- the controller is resident at `24A0:01C2` with its decoder at `24A0:030A`
- one complete action cycle (Down Arrow) traces cleanly end-to-end
- the globals `8C4C/8C50/8C52/8C54` are the live state for the visible save-game list
- the redraw callee `4A65:009A` takes real geometry arguments, not a token call

For static work, these are the ownership anchors to search for in Ghidra before doing more runtime descent into this UI path.
