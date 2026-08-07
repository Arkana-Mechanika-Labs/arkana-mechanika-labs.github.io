---
title: "Devlog #043 - A State Atlas for Darklands"
date: 2026-08-02T21:00:00
summary: "Darklands' complete 366-entry state vector is now a navigable research atlas, connecting raw states to original owners without turning the atlas itself into game code."
---

The last devlog ended on Main Street.

That was a satisfying place to stop. The reconstructed route could begin at
power-on, pass through the introduction and Quickstart, and reach a real city
screen whose choices came from the original data and original owner code.

It also exposed a new problem.

Once the player can move through several city screens, the project accumulates
raw states very quickly. A row returns `0009h`. Another branch publishes
`0013h`. A night route chooses `0022h`. Each value passes through a resident
wrapper, requests an overlay record, and lands at a canonical owner that may
select a different MSG resource according to the city, the date, active events,
or another piece of world state.

The information existed. It was spread across disassemblies, runtime captures,
Darklays packets, annotations, handoff notes, tests, and several generations of
research reports.

We needed a map that could answer one narrow question immediately:

```text
The original game just published raw state 0034h.
Where does that state really go?
```

That map is the raw-state atlas.

## The Table Was Larger Than We Thought

Earlier runtime research had captured the first 99 entries of the central
state table. That was enough to reveal the broad design: Darklands does not
hard-code a modern menu graph. It stores a raw state word, looks that word up in
a table of far pointers, enters a small resident wrapper, and asks the overlay
resolver to load the corresponding original owner.

Darklays later recovered the complete table from the original executable.

It contains 366 entries, covering selectors `0000h` through `016Dh`, followed
by a null terminator. Every entry can now be traced through:

```text
raw selector
-> table offset
-> resident wrapper
-> overlay resolver
-> overlay record and token
-> normalized canonical entry
```

For example:

```text
0034h
-> wrapper 09C0:2ACB
-> overlay record 57
-> ovl_0057:0000
```

That is a strong routing fact. It is not yet a claim that `ovl_0057:0000` is a
fully understood owner, that all of its branches are executable, or that state
`0034h` has one simple gameplay name.

The atlas preserves that distinction.

## A State Is Not a Screen Name

One of the most persistent traps in the city work has been the temptation to
name a raw state after the first MSG file observed there.

A runtime session may show `$CHURC00.MSG` after state `0013h`. Another city,
date, or event configuration may send the same canonical owner through a
different resource path. The state selects a controller. The controller selects
the resource.

The atlas therefore has two layers.

The first is mechanical and static:

```text
0013h -> ovl_0048:2504
```

The second is contextual:

```text
under this exact entry predicate,
with this city record and event state,
proc_0048_2504 published $CHURC00.MSG card 0
```

The contextual layer records how strong each statement is. A fact may be
certified from original bytes, observed in one natural runtime scenario,
cross-correlated from several sources, retained as a semantic hypothesis, or
left explicitly unresolved.

That prevents a useful observation from quietly becoming a universal rule.

## Incoming and Outgoing Edges

The atlas became more useful when it stopped being only a table lookup.

Certified transitions can now be attached to the mechanical destinations. A
state owner may have several outgoing edges, each with its own exact predicate:

```text
state 0013h, owner ordinal 0007h
  -> state 0001h, 0006h, or 0008h
  depending on the signed RNG threshold and calendar result
```

The atlas records all three outcomes without deciding which one is “the real
one.” The selected StateEffect certificate records the condition that makes
each outcome legal. Unsupported alternatives remain visible and fail closed.

The reverse index is just as important. It can answer:

```text
Which already reconstructed actions can reach state 0008h?
Which raw states share one canonical owner?
Does this new route reconnect to a presentation we already know?
```

That changed how we choose the next piece of work. Instead of following the
next address in the current overlay, we can prefer an edge that reaches an
existing city hub, closes a reusable interaction pattern, or unlocks several
states at once.

## Two Grove States, One Family

States `0021h` and `0022h` provided a good test of the new approach.

They resolve to two different canonical owners in overlay record 52. One
publishes `$CITYG05.MSG`; the other publishes `$CITYG06.MSG`. Their resources
and state values are distinct, but their control-flow shape is almost the same.

Darklays and the evidence index made it possible to inspect them as a family:

- separate original byte identities;
- separate canonical entries;
- one shared generic presentation/input structure;
- one shared parent return tail;
- separate certificates and tests.

The first selected row in both owners returns through an unusual shared tail at
`ovl_0052:0254`. It does not enter the nearby local action that first looked
like the obvious destination. The tail reads the current state, consumes the
active parent frame, and returns directly to the central controller.

That correction is exactly why the atlas is not executable code. A research
map can point to the frontier. The original bytes still decide how control
actually moves.

## The Decision Census

Routing alone is not enough.

A city owner may choose rows according to current-city flags, event records,
time of day, party abilities, inventory, known saints, random values, or fields
whose gameplay meaning is still unknown. If we only record the states that were
seen in one replay, those hidden decisions disappear.

Alongside the atlas, the project now maintains a decision census for the owners
and selected paths we actively reconstruct. For each scope, it accounts for:

- every reachable conditional branch;
- every indirect dispatch or handler table;
- every call result used by a branch;
- every persistent write;
- every MSG resource and card selection;
- every row visibility or selectability change;
- every raw-state publication;
- every unresolved input to those decisions.

The census is intentionally shallow for most of the 366 states. It becomes deep
only when a route is selected for implementation. This keeps the global map
complete enough to expose blind spots without turning the project into an
instruction-by-instruction encyclopedia.

## A Map That Must Never Drive the Game

The atlas begins with two blunt declarations:

```json
{
  "authority": "research_control_only",
  "executable_use_forbidden": true
}
```

The engine is not allowed to load it. The clean C# session is not allowed to
turn it into a switch statement. No action registration may be generated from
its edges.

Runtime behavior still comes from certified original owners, selected path
compositions, and explicit clean projections backed by those certificates.

That separation gives the atlas room to be useful. It can contain unresolved
entries, multiple contextual interpretations, research links, and coverage
metrics without pretending to be a finished game model.

Architecture tests enforce the boundary. If production code starts referring
to the atlas schema or path, the build fails.

## What the Atlas Changed

The atlas did not decode 366 state owners overnight.

It did something more practical. It made the growing reconstruction
navigable.

When an action now returns a raw state, the next intake begins with one lookup.
We can see the wrapper, the overlay record, the canonical destination, known
incoming edges, existing packets, prior runtime observations, and whether the
route reconnects to clean gameplay that already exists.

The atlas also makes corrections durable. A visible row may map to a different
raw owner ordinal than expected. A state may select a controller rather than a
fixed MSG file. Two nearby addresses may belong to different canonical owners.
Once corrected, those relations no longer have to be rediscovered from old
session notes.

The city is still far from complete. Many states are only mechanically mapped,
many owners are only partly certified, and many outgoing edges remain unknown.

But the project no longer sees them as 366 isolated mysteries.

It sees a graph.

The next challenge was to make all of the evidence around that graph reusable,
so that understanding one owner would make the next one genuinely faster.
