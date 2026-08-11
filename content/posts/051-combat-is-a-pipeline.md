---
title: "Devlog #051 - Combat Is a Pipeline"
date: 2026-08-11T18:00:00+02:00
summary: "Darklands combat is no longer a black box behind an encounter choice: its generic entry, three generation families, prepared battlefield, placement search, and raw result protocol are now mapped from the original bytes."
---

The previous devlog on the city ambush stopped at a deliberate boundary.

Choosing a direct attack reaches combat. Failing to flee reaches combat. Some
weapon tests reach combat. But none of those encounter owners *is* combat. They
hand control to a shared subsystem used across the game.

We have now followed that handoff far enough to describe the subsystem's
shape. The result is more interesting than a conventional `StartBattle`
function. Darklands combat is a pipeline: callers publish a compact structural
request, generation code prepares records and battlefield surfaces, placement
code searches the map, a root controller runs the fight, and a raw result is
returned to the caller for interpretation.

Several parts of that pipeline are now exact. Several are still missing. The
line between the two is finally clear.

## One Front Door, Many Encounters

The generic entry is `proc_0029_2278`.

It is not tied to `$CITYT00`, Quickstart, or any one city. We found at least 110
direct calls to it across 52 resolver records. Road encounters, city events,
and other owner routines converge on the same machinery.

The entry receives eleven raw words:

- one selector;
- one seed-normalization input;
- three ordered triples, each containing a descriptor key, a variant selector,
  and a positive quantity.

That is the complete structural shape proved so far. It is tempting to rename
the triples `enemy`, `faction`, or `side`, but the original consumers do not yet
justify those names. A descriptor selects a bounded record in the second
`DARKLAND.ENM` table, a variant is clamped by the first table, and a quantity is
paired with the resulting ordinal. That is what the bytes prove.

The distinction matters. A plausible name can become a bad API surprisingly
quickly.

## The Root Does Not Take Arguments

The entry prepares inherited state and eventually reaches `proc_0014_0000`,
the combat root.

The root has no explicit arguments. By the time it runs, the request has been
distributed across prepared records, pointer tables, mode words, resource
state, clock and deadline state, the live RNG, and a persistent result word.

This explains why a clean `CombatLaunchRequest` has not appeared in the C#
engine yet. The eleven entry words are only part of the contract. Other values
arrive through inherited state, and we have not closed their complete liveness
or upstream provenance.

Some globals that initially looked like caller inputs are now known to be
combat-owned:

- `D661` and `D662` belong to generation and selection;
- `E0A2` is placement-search state;
- `E13C` is a temporary set/call/reset latch;
- `C600` is inherited persistent state whose domain depends on an upstream
  bit, so it cannot be replaced by a convenient default.

Surprise, awareness, terrain, event state, party state, and time may all matter
to combat, but they are not yet certified as fields of one caller-visible
object. For now, inventing that object would hide uncertainty instead of
removing it.

## Three Generation Families

The preparation code divides into three families numbered 7, 8, and 9.

Family 7 consumes all three structural triples in order and uses the default
group-zero construction path.

Family 8 has four selector-dependent topologies. Different topologies consume
different subsets of the triples and publish different flag combinations.

Family 9 also has four topologies, but it can split quantities, cross-couple
the supplied groups, and mutate the combat-owned selected index at `D662`.

These are not three cosmetic map themes. They are materially different record
construction algorithms. The family number alone is not enough to infer a
species, faction, encounter class, or party role.

Every generated surface also passes through an ordered
`level<index>.atv` read, transform, and rewrite attempt. Even when the writer's
status is discarded, the attempt itself is observable and must stay in the
original order.

## A Correction to Our Earlier Battleground Model

[Devlog #023](/posts/023-mapping-the-battleground/) correctly opened the combat
asset vault, but it treated the discovered IMAPS data as if it described the
whole live battlefield.

We now know that was only one layer of the system.

The runtime preparation path uses a 40 by 40 array of four-byte packed cells
plus a parallel 40 by 40 companion map. Original procedures scan and rewrite
the 38 by 38 interior, modify packed nibbles, directions, companion bytes, and
signed rectangles, and sometimes consume RNG while doing so.

In other words, the battlefield is resource-backed, but it is not simply a
static grid copied to the screen. The original engine prepares and mutates a
working surface before placement and play.

That correction is exactly why the project keeps old conclusions revisable.
The archive investigation found real data. Following its runtime consumers
revealed the missing layer.

## Placement Is an Ordered Search

The main placement owner, `proc_0014_4188`, first tries deterministic
positions around an anchor. If those fail, it enters a randomized search with
fixed retry and relaxation budgets.

Each random candidate consumes exactly two RNG draws. That count is part of the
game state: changing it would alter every later random event.

The coordinate conversion is now known:

```text
cell_x = truncate_toward_zero(raw_x / 32)
cell_y = truncate_toward_zero(raw_y / 16)
```

For the complete search, including its 3 by 3 relaxation, the presently proved
safe anchor domain is:

```text
X: 32..1232
Y: 16..616
```

The stock `ICITY.600`, `.700`, `.701`, `.800`, and `.801` resource closures we
reviewed stay within those bounds. Modified resources and several alternate
rebuild paths are not silently assumed to do so.

One deeper placement predicate still reads two conditionally uninitialized
stack words on a reachable family. Until their liveness is resolved, that
owner remains a hard stop rather than a guessed boolean.

## The Result Is a Protocol, Not an Enum

Combat does not simply return `Victory` or `Defeat`.

The root exit owner returns `AX = 1` when the root loop should end and `AX = 0`
when it should continue. Separately, a persistent word can receive raw values
including `0000`, `0002`, `0003`, `0005`, `0008`, and `FFFF`.

Those values are not yet authorized as a gameplay enum.

After combat returns, its caller performs more work. One confirmed caller
normalizes raw result 8 to 2. If the combat subsystem performed that
normalization itself, it would steal behavior from its caller and change the
original boundary.

The same principle applies to calendar effects, event mutation, and inventory
changes: each belongs to the original owner that performs it, not whichever
modern class would be most convenient.

## What We Can Say Now

Darklands has one generic combat infrastructure reached by many encounter
owners. Its launch data is partly explicit and partly inherited. Three distinct
generation families prepare resource-backed working surfaces. Placement is a
deterministic-then-random search with exact RNG consumption. The root publishes
a raw result that its caller continues to interpret.

That is a real architecture, recovered from the executable rather than designed
after the fact.

It is not yet a complete combat implementation. The next devlog covers the
other half of the story: which parts of this architecture have already become
certified C#, why fifteen working procedures still do not add up to a playable
fight, and how we are preserving the gap honestly.
