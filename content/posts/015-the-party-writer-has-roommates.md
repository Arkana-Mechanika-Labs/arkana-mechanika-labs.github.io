---
title: "Devlog #015 - The Party Writer Has Roommates"
date: 2026-04-12T04:00:00
summary: "The function that adds a character to the party is not a function — it is one case in a large selector-dispatch worker that manages the entire character lifecycle. Five confirmed cases, a multi-phase linear body, and an RTLink integrity mechanism that validates every overlay before it dispatches."
---

## Where We Left Off

In [devlog 012](/posts/012-catching-the-party-writer/) we caught `15DF:0D5F` — the exact instruction that writes `1` into a party slot's active flag during the Add to Party flow. We had the address, the caller chain, and a runtime dump of the overlay bytes. The plan was to recover the owning function from that dump.

What we found instead was that the owning function is not the party writer at all. The party writer is a case body inside something much larger.

## The Frame That Contains Everything

Working outward from `15DF:0D5F` through the dump, the first thing that becomes clear is that the function boundary is not where earlier sessions assumed. The gate at `15DF:0329` — which checks `AX == 0x011B` and conditionally calls `15DF:0348` — is not the entry point of the owning routine. It is the tail of a caller further up.

The real entry is `15DF:0444`: `ENTER 0x00A8,0`. A 168-byte local frame. This is a large selector-dispatch worker that takes a 16-bit selector argument at `[BP+6]` and dispatches to one of several case bodies based on its value.

Five case edges are confirmed from the dump:

| Selector | Target |
|----------|--------|
| `0x1E41` | `15DF:09AF` — add-to-party |
| `0x2368` | `15DF:0F5F` |
| `0x0433` | `15DF:2174` |
| `0x0231` | `15DF:14D1` |
| `0x0332` | `15DF:1A59` |

Unmatched selectors fall through to the epilogue. So this is not `party_add_member` — it is a general character-management dispatcher that handles add-to-party as selector `0x1E41`. The party writer lives inside one of its case bodies.

## The Add-to-Party Case Body

Following selector `0x1E41` to `15DF:09AF`, the case body begins with ES-segment attribute and init writes — fields around `[ES:BX+0x340A]` through at least `[ES:BX+0x3413]` — plus direct writes to globals like `[0xE762]=0x1C` and `[0xE765]=0x17`. These look like character presentation state initialization before the slot is formally claimed.

Then a pre-finalization call chain through segment `0x05F9`: three far calls at `0x058B`, `0x0553`, and `0x05A5`. These appear to set up the display context for the character being added.

The case body then stays in a single straight-line run from `0x309AE` all the way to the activation write at `0x30ACE`. No conditional branches, no loop, no internal callee boundary interrupts the path. The entire add-to-party commit is a linear sequence.

## Slot Resolution

Before the slot is marked active, the worker needs to know *which* slot to use. It does not receive the slot index directly as an argument. Instead, it scans a staged 4-entry local handle table at `[BP+DI-0x1c]` against the global current-world ID at `[0xE7DA]`. The matching entry's index becomes `[BP-0x0e]`, which drives everything downstream.

This is significant: the slot chosen during Add to Party is keyed to the current world, not passed in from the caller. The character management layer knows which world is active and picks the right slot automatically.

## Pre-Write Initialization

Three rounds of setup happen before the slot is marked active.

**The copy/setup trio:** `081E:1DE2([BP-0x0a], AX, 0, 1)` — `081E:0716(0x9C55 + slot*0x80, 0x80, 1, [BP-0x0a])` — `081E:1DE2([BP-0x0a], 0, 0, 1)`. This initializes the per-slot record region at `0x9C55 + slot_index*0x80` before filling it.

**Three bulk-transfer calls:** The same resolved slot index drives three slot-indexed destinations at `0x082C + slot*0x14`, `0x07BE + slot*0x16`, and `0x3E00 + slot*0x180`. These copy pre-computed tables into the slot's data regions.

**The activation write:** `mov byte ptr [bx+0x9c69],0x01` — the same instruction caught at runtime in devlog 012. Slot stride `0x80`. The `0x9c69` write is offset `+0x14` inside the per-slot record based at `0x9C55 + slot_index*0x80`.

## After the Write

The case body does not end at the activation write. It pivots into a separate finalization/UI phase via `081E:1DE2` driven by local `[BP-0x0a]` rather than the slot index. This builds a keyed message buffer at `[BP-0x0c]` through two `081E:2CBD` calls, then continues through `081E:05E2`, `F905:1293`, `F905:12C3`, and a fixed-geometry `F905:0553` UI/dialog call.

The final recovered bytes show `15DF:0DF9` near-calling `15DF:275F`, then `15DF:0DFF` unconditionally jumping to `15DF:275B` — continuation beyond the current dump window. The add-to-party path does not end at the writer; it hands off into more overlay code that the current `0000-0EFF` dump does not cover.

## RTLink Stub Integrity

While working through the RTLink overlay machinery in context, the session surfaced a detail that had not been characterised before: the loader revalidates the overlay stub window on every dispatch.

There is an optional stub-integrity mode gated by flag `0x0100` in `DAT_19c0_0b68`. When enabled, `rtlink_init_stub_scan_bounds` walks the overlay records, finds the maximum record offset, and defines the start of a candidate contiguous service-stub window. `rtlink_check_stub_format` then walks that window validating the expected stub shape — `CALL rel16 rtlink_call_overlay; JMP FAR target; trailing 16-bit service index` — and records the accepted window boundaries in `rtlink_stub_scan_start` and `rtlink_stub_scan_end`.

Every subsequent `rtlink_call_overlay` invocation replays the scan through `rtlink_scan_verify_stubs` and raises RTLink error `0x12` if the scan does not stop exactly at the stored end boundary.

This is the overlay manager protecting itself against memory corruption. The stub table is checked on every use, not just at startup.

## What This Changes

`party_add_member` as a standalone resident function no longer exists in the naming model. What exists instead is a character-management selector-dispatch worker in the `15DF` overlay family with at least five known cases. The add-to-party path is selector `0x1E41`.

The `15DF` dump covers `0000-0EFF`. Given that cases include targets at `0x0F5F`, `0x14D1`, `0x1A59`, and `0x2174`, the overlay is substantially larger. Only the add-to-party case has been traced in detail; four others remain open.
