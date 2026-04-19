---
title: "Devlog #018 - Create New World: Full Coverage"
date: 2026-04-13
summary: "The third and widest runtime dump of the Create New World worker closes the tail that used to escape the window. A full seven-anchor structure map now covers the function from entry guard to slot activation."
---

## Three Windows on the Same Function

The Create New World slot-commit worker has been recovered incrementally across three overlapping runtime dumps of the `1C85` overlay family:

| Block | Range | Flat Base |
|-------|-------|-----------|
| `RUNTIME_1C85_0900` | `1C85:0900-1FFF` | `0x1D150` |
| `RUNTIME_1C85_0700_EXPANDED` | `1C85:0700-21FF` | `0x32000` |
| `RUNTIME_1C85_0500_WIDE` | `1C85:0500-21FF` | `0x36000` |

Each window was taken from a live DOSBox-X session while the Create New World family was resident. The first gave us the trusted entry point. The second gave us the slot-scan branch split. The third — taken this session — closes the tail.

`RUNTIME_1C85_0500_WIDE` is now the preferred static surface. The earlier blocks are kept as overlap comparison slices.

## Why a Third Window Was Needed

After [devlog 016](/posts/016-the-world-slot-machine/), the recovered body ended around `0x326F9` with two far calls that left the window:

```
0x326F9 -> 0x3000:4060
0x32700 -> 0x3000:405C
```

These were exits into an unresolved continuation — real code that follows the slot-indexed table copies, but beyond what the previous dump captured. The only way to recover it without guessing was another wider dump.

The `1C85:0500-21FF` range brought those exits inside the window. The tail is no longer unresolved.

## The Full Structure Map

With all three windows reconciled, the worker now has seven confirmed anchor points:

| Flat Address | Anchor |
|-------------|--------|
| `0x364AE` | Bounded worker gate — compare `[0xE7DC]` against zero, exit on non-positive |
| `0x36556` | Existing-slot scan — walk four local entries against `DS:E7DA` (current world ID) |
| `0x3657D` | Empty-slot scan — walk the same four entries for `0xFFFF` |
| `0x365BA` | Commit slot setup — store world ID, copy slot name from `A668 + slot*0x80`, refresh `E88E` |
| `0x36697` | Default-template / seed burst — mirror 24 bytes into globals `E753..E76A` and per-slot record |
| `0x36785` | Post-init refresh / presentation phase — update display state |
| `0x36801` | Slot-indexed payload copy + activation + follow-up initializer chain |

These addresses are from the `RUNTIME_1C85_0500_WIDE` block. The same structure carries through all three windows at different flat offsets (the relative layout is preserved; only the base changes between materialization sessions).

## The `0x36801` Frontier

The activation chain at `0x36801` is the current frontier of the recovered body:

- Copies three slot-keyed payload tables from bases `0x082C` (stride `0x14`), `0x07BE` (stride `0x16`), and `0x003E` (stride `0x180`)
- Marks the slot active: `[0x9C69 + slot*0x80] = 1`
- Runs two slot-indexed follow-up initializers
- Refreshes presentation state

This is structurally identical to the write pattern seen in [devlog 015](/posts/015-the-party-writer-has-roommates/) for the party-add case in the `15DF` overlay. The same table bases, the same slot activation write, the same follow-up initializer shape — the slot management model is consistent across both paths.

After `0x36801`, execution continues into code that the widened block still has not fully characterized. The next static session should treat "what happens after `0x36801`" as the single highest-value bounded question for this function.

## Cross-Window Validation

Having three overlapping windows for the same runtime body is not redundant — it is the validation protocol. Each window was captured in a separate live session with the overlay freshly loaded. All three agree over their overlapping ranges:

- The slot-scan logic matches at every overlap address
- The resident helper trio `0xDCB3`, `0xCF95`, `0xA884` appears in the same order in all three
- The activation write and table copy sequence is consistent

This means the recovered structure is not a session artifact. The `1C85` worker body is stable and the seven anchor points are genuine internal landmarks, not one-off observations.

## The Confirmed Thunk/Resolver Path

The Create New World flow through the loader is now confirmed end-to-end:

```
11E3:052B  →  rewrites pending far return to continuation bridge 11E3:0698
11E3:05A6  →  return through thunk table at 11E3:1ADE
11E3:18F4  →  far jump entry
1C85:09AE  →  trusted internal cut point (= 0x364AE in RUNTIME_1C85_0500_WIDE)
```

Metadata id `0x002B` selects resolver record at `11E3:0E80`, which contains the seek offset and load size that bring the `1C85` overlay into memory. The loader path is fully characterised at the entry side; only the tail of the loaded function body remains to be recovered.
