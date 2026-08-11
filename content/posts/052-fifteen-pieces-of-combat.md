---
title: "Devlog #052 - Fifteen Pieces of Combat"
date: 2026-08-11T09:05:00+02:00
summary: "Fifteen original combat procedures now execute as byte-certified raw C# owners. Here is what they do, why they are not yet a playable battle, and how 94 research commits were reconciled without importing a speculative combat rewrite."
---

Knowing the shape of combat is not the same as implementing it.

The project now has fifteen combat-related procedures executing in C#. They
cover RNG, geometry, battlefield preparation, record publication,
initialization, placement dependencies, inventory mutation, and transition
cleanup.

That sounds close to a combat subsystem. It is not.

What we have is a growing set of exact machine-level owners. What we do not yet
have is the complete orchestration that connects them into a fight. This
devlog is about that distinction and why it is the safest way to make progress.

## The Required Path to C#

Every executable reconstruction follows the same chain:

```text
original DARKLAND.EXE bytes
        ↓
Ghidra + Reko + exact instruction reconciliation
        ↓
current COAB packet or StateEffect certificate
        ↓
raw C# owner in Darklands.Engine/Segments
        ↓
raw memory-contract tests
        ↓
optional clean gameplay projection
        ↓
optional SDL integration
```

Ghidra and Reko are discovery tools. They can expose structure, calls, and
pseudocode, but neither decompiler is the final authority. Several combat
procedures produced empty or incomplete decompilations. In those cases we kept
the failure as evidence and reconciled every original instruction with an
independent disassembly witness.

The raw C# layer is mandatory because it preserves things a clean gameplay API
would otherwise erase: 16-bit wrapping, signed comparisons, far pointers,
memory order, helper order, RNG draws, stack-shaped outputs, and exactly which
neighboring bytes remain untouched.

Only after that contract is stable can a clean service safely summarize it.

## The Fifteen Owners

The current set divides into seven useful groups.

| Area | Raw C# owners | What is closed |
|---|---|---|
| RNG and geometry | `Ovl0004_20F6`, `Ovl0004_2160` | Bounded dice with exact RNG shortcuts; four-way wrapping coordinate classification |
| Battlefield preparation | `Ovl0010_26F8`, `Ovl0010_2A2C`, `Ovl0010_2B42` | Family-7 grid mutation; prepared-surface record selection; generated-record publication |
| Initialization | `Ovl0014_0D86`, `Ovl0014_9C4C`, `Resident047C_040B` | Combat-state initialization, lookup adjustment, and a literal-segment flag clear |
| Placement dependencies | `Ovl0014_5D04`, `Ovl0014_63CC` | Six-field table snapshots and one complete placement-mask rejection leaf |
| Resource transformation | `Ovl0014_1060A` | Selector publication and in-place caller-buffer translation |
| Inventory effects | `Ovl0014_B244`, selected paths of `Ovl0019_0DFE` | Party-slot item consumption, compaction, and guarded forwarding |
| Transition cleanup | `Ovl0025_0BE4`, selected paths of `Ovl0025_0C02` | Ordered cleanup for the certified index-5 and index-6 paths |

These are internal engine owners, not public gameplay APIs. Their names retain
the original segment and offset because several raw fields still have no
certified semantic name.

## Small Procedures Can Carry Large Contracts

The shared dice wrapper, `proc_0004_20F6`, illustrates the level of fidelity.

If the signed count or number of sides is below one, it returns zero without
touching RNG. If the number of sides is one, it returns the count without
touching RNG. Otherwise it advances the original resident RNG once per die,
adds `(raw % sides) + 1`, and preserves wrapping 16-bit accumulation.

Replacing that with `Random.Next` would produce plausible dice and a different
game.

The coordinate classifier, `proc_0004_2160`, performs two wrapping
subtractions, follows the original ordered signed comparisons, and returns one
of four raw even values. The `8000h` negation edge and diagonal ties matter.

The prepared-record publisher corrected two mistakes found in an earlier clean
prototype: a coordinate pair had been reversed, and signed `8000h` did not pass
through the original absolute-shift-absolute sequence. The raw-owner tests
caught both because they test the memory and arithmetic contract rather than a
friendly interpreted result.

## Generation Preserves RNG and Publication Order

`Ovl0010_26F8` scans the 38 by 38 interior of a prepared surface in original
row-major order. It preserves blocked-cell gates, conditional dice calls,
packed-nibble changes, companion-map writes, direction changes, and signed
rectangle fills.

`Ovl0010_2A2C` selects matching records from either prepared surface. Invalid
surface indices leave the caller word untouched. A valid search with no match
writes zero. One candidate consumes no RNG; multiple candidates consume
exactly one original RNG advance.

`Ovl0010_2B42` publishes one generated record with up to three ordered
ordinal/quantity pairs and an optional nested secondary record. The partition
count increments only if at least one pair was accepted.

None of these owners claims to be “encounter generation” as a complete modern
service. Their family callers remain separate original procedures.

## Initialization and Placement Leaves

The certified initializer clears and publishes state in an exact order. It
composes the existing lookup-adjustment and resident flag-clear owners rather
than copying their visible effects.

The snapshot loader copies four words and two bytes from parallel far tables
into six fixed fields of a caller-owned record. We know the live caller index
domain is zero through nine; we do not invent names for the retained fields.

The newest owner, `proc_0014_63CC`, is a complete 563-byte placement-mask leaf.
It contains 48 resolved predicates. On success it changes nothing. On rejection
it performs one publication:

```text
DS:E138 = 4000h
```

Its C# implementation preserves low- and high-nibble gates, signed wrapping
arithmetic, short-circuit read order, and no-extra-write behavior. Eight focused
tests exercise sentinel-filled memory and the internal raw ABI.

That leaf is complete. Its parent, `proc_0014_5ECA`, is not.

## Selected Paths Stay Selected

Some original procedures are only executable under a proved caller predicate.

The inventory consumer is implemented for concrete party slots zero through
four. It matches raw type and quality bytes, decrements quantity, shifts later
six-byte records left when an item is depleted, decrements the live count, and
leaves the inactive trailing bytes untouched exactly as the original does.

Other storage layouts inside the same original procedure remain unavailable.

The transition-cleanup child is likewise executable only for indices 5 and 6
under its certified parent. The parent calls index 5 first, then index 6, and
publishes its terminal words only after normal child returns. Every other index
fails before memory access or a resident call.

This is not defensive programming added to Darklands. It is how the
reconstruction states, in executable form, exactly which original path has
been proved.

## What Happened to the Old Combat Branch

The original combat research branch contained 94 commits. We did not merge it
wholesale.

Every commit was inventoried and assigned to one of 19 coherent groups. Useful
original-byte findings were rebuilt under the current evidence rules. Clean
gameplay projections were deferred until they have certified consumers.
Platform and resource boundaries were separated. One historical table-layout
implementation with 36 writes was preserved as research but rejected as
runtime authority because its destination boundary was not independently
proved.

The final audit accounts for all 94 commits: nothing missing, duplicated,
pending, or left in limbo.

That work was slower than merging a large prototype. It also prevented two
independent combat architectures from surviving in the engine.

## Why This Is Not Playable Combat Yet

Fifteen procedures are components. The missing work is the conductor.

The current frontier still includes:

- several independent leaves required by the placement-mask producer;
- the complete placement predicate and its conditionally live stack values;
- the main combat controller and mode orchestration;
- rendering, animation, visual-resource, and input ownership;
- sixteen unresolved helper edges in the exit owner;
- complete calendar, event, party, and inventory mutation ordering;
- the exact caller-visible bindings needed for a route-neutral launch request;
- the caller continuation that interprets the raw combat result.

Until those are closed, there is no clean `Game/Combat` service and no SDL
combat consumer. The city ambush correctly stops when it reaches this boundary.

## Progress Without Pretending

At the integration point for the newest owner, all eight focused tests passed,
the full engine Release suite passed 3,413 tests, and the independent Darklays
suite passed 1,056 tests. The canonical annotations and engine-side evidence
mirror agreed exactly.

Those numbers do not mean combat is finished. They mean every currently
claimed executable piece is healthy under the same authority chain as the rest
of the engine.

That is the milestone.

Combat is no longer one mysterious destination behind a menu choice. It is a
mapped pipeline with fifteen faithful C# components, explicit unsupported
boundaries, and a dependency graph we can close one original owner at a time.

The next useful step is not to draw a battle screen around the gaps. It is to
close the remaining placement leaves, reconnect their parent, and keep moving
up the original call graph until the orchestration itself is earned.
