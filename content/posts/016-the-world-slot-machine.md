---
title: "Devlog #016 - The World Slot Machine"
date: 2026-04-12T08:00:00
summary: "A wide runtime dump of the 1C85 overlay materialized the Create New World function in Ghidra. It turns out to be a four-slot commit worker — and it initializes slots from the same table bases as Add to Party."
---

## The Target

The game's main loop dispatches through a table of far pointers keyed by state number. State `0x29` is the startup state — it includes the path through `Quickstart` and `Create New World`. The `1C85` overlay family handles that state, and the Create New World path lives somewhere inside it.

A bounded slice of `1C85` had already been captured in an earlier session and materialized in Ghidra as `RUNTIME_1C85_0900`. That gave us a trusted entry label at flat address `0x1D1FE`. But the window was narrow — the function prologue was outside the captured range, and the body was truncated.

The session described here widened the dump to `1C85:0700-21FF`, producing a new block `RUNTIME_1C85_0700_EXPANDED`. Both windows agree over their overlap. The wider block is the working surface.

## A Four-Slot Scan

Starting from the trusted entry at `0x1D1FE`, the recovered body is a **four-slot setup/commit worker**. The game maintains up to four saved worlds. When Create New World is called, this function needs to either find an existing slot that already holds the current world ID, or claim a free slot.

The scan structure is clear from the recovered bytes:

- `0x32356` — the existing-slot scan: compare each of the four 16-bit local handle entries against `DS:E7DA` (current world ID). If a match is found, skip to the reuse-existing path.
- `0x3237D` — the free-slot scan: search the same four entries for `0xFFFF` (empty slot marker).
- `0x323BA` — the commit path: once a usable slot is chosen, execution branches here.

Before the slot loop begins, `[0xE7DC]` is checked against zero. A non-positive value exits the worker immediately. The positive branch enters the four-slot scan.

Three resident far calls appear in consistent order before two later unresolved far calls: `0xDCB3`, `0xCF95`, and `0xA884`. These are stable landmarks across both recovered windows.

## Committing the Slot

At the commit path `0x323BA`, once a slot has been chosen:

- The current world ID from `DS:E7DA` is stored into the selected slot entry.
- The slot name is copied from `DS:A668 + slot*0x80` into `DS:E7E2`.
- The active handle `DS:E88E` is refreshed.
- `DS:E753..E76A` and `ES:[BX+33FC..3413]` are seeded with initial bytes for the new world-slot record.

Then at `0x32497`, a 24-byte default template is mirrored into two places: the globals at `0xE753..0xE76A` and the per-slot record at `ES:[slot*0x18 + 0x33FC..0x3413]`.

## Three Slot-Keyed Table Copies

At `0x32601`, three bulk-transfer calls initialize the slot's data regions from pre-computed tables:

| Base | Stride |
|------|--------|
| `0x082C` | `0x14` (20 bytes) |
| `0x07BE` | `0x16` (22 bytes) |
| `0x003E` | `0x180` (384 bytes) |

Readers of [devlog 015](/posts/015-the-party-writer-has-roommates/) will recognize the first two bases immediately. The add-to-party case in the `15DF` overlay uses `0x082C + slot*0x14` and `0x07BE + slot*0x16` for the same bulk-transfer step before marking a party slot active.

Both flows — creating a world slot and adding a character to the party — draw initialization data from the same pair of tables. The slot management model is unified: the same table-driven initialization applies whether the slot being claimed is a saved world or a party member.

## The Activation Write

After the table copies, the slot is marked active:

```
[0x9C69 + slot*0x80] = 1
```

This is the same write pattern as the party activation flag. The `0x9C00` hot-slot array is not just for party members — it also tracks active world slots via the same stride and the same offset convention.

After the activation write, two slot-indexed follow-up initializers run, then presentation state is refreshed, and execution exits into code beyond the current dump window.

## What This Connects

The recovered Create New World body gives us:

- The exact slot-scan logic (existing → free → commit)
- The world-slot record layout bases (`0x33FC + slot*0x18`, `0xA668 + slot*0x80`, `0xE7E2`, `0xE88E`)
- The global world-context state (`0xE7DA` = current world ID, `0xE7DC` = validity check, `0xE753..0xE76A` = world seed/template)
- A confirmed connection between world-slot initialization and party-slot initialization through shared table bases

The same three functions (`0xDCB3`, `0xCF95`, `0xA884`) recur here as in other high-value path traces. They are likely general slot/state management helpers used across multiple overlay families. Naming them properly is now a concrete near-term target.

## The Limits of the Current Window

The dump covers `1C85:0700-21FF`. The function prologue is still outside that range — the true entry point is unknown, and the argument layout has not been confirmed from actual caller evidence. The body is recovered as a truncated slice.

What is established: the bounded behavior from the trusted entry at `0x1D1FE` through the commit tail. The structure is stable across both recovered windows. That is enough to treat this as the Create New World slot-commit body in the analysis model, with the caveat that the outer caller/argument shape is not yet pinned.
