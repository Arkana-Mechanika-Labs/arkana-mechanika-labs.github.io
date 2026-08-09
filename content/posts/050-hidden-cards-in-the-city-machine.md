---
title: "Devlog #050 - Hidden Cards in the City Machine"
date: 2026-08-09T16:00:00
summary: "Main Street, the night streets, and the side streets can publish conditional entry cards before their normal rows. The original guards, pictures, RNG, disabled actions, and redispatch routes are now closed independently."
---

The city-navigation graph looked stable enough to move past.

Main Street, nighttime Main Street, and the side streets all displayed their
normal card-zero rows. Their city-dependent options worked. The route from
Quickstart could reach them in SDL.

But “usually displays card zero” is not the same as “the owner begins at card
zero.” Several owners contain optional entry arms that publish another card
first. Closing those arms exposed why a generic route table can never fully
replace the original MSG state machine.

## One Shared Query, Three Different Consequences

All three entry owners consult the same event query:

```text
proc_0029_3742(2, 0, current city)
```

A result of `FFFFh` is significant, but the consequences are owner-specific.

### Nighttime Main Street: `$MAINS02`

The nighttime owner presents card 1 in mode 0 over the inherited
`PICS\XNMAIN.PIC` visual. It consumes no extra RNG and does not replace the
picture. After acknowledgement it rejoins the ordinary owner and publishes
card-zero rows.

### Daytime Main Street: `$MAINS01`

The daytime owner adds another gate. Only after the event query returns
`FFFFh` does it consume `RNG(100)`. A signed result below 35 selects card 1.

The picture is not a guess derived from the card text. A live relocated
descriptor capture proved `POST-UP.PIC`. After the card is acknowledged, the
owner publishes normal Main Street rows over the retained poster visual. It
does not reload `MAIN-ST.PIC` at the rejoin.

That retained picture may look like an oddity in a modern UI, but it is the
original behavior and therefore part of the reconstructed state.

### Daytime Side Streets: `$SIDES00`

The side-street owner uses card 1 in mode 2 and consumes no RNG. Its optional
and primary picture descriptors are independent far pointers, but both decode
to `xsid`. After acknowledgement the owner recomposes a fresh card-zero header
and rows.

These siblings now have separate StateEffect certificates. Similar-looking
entry cards cannot borrow each other's mode, picture lifetime, RNG, or rejoin
behavior.

## A Disabled Handbill Row Is Not a Transition

`$MAINS01` also contains a due-event check for kind `0051h`.

When the event is due for the current city and date, owner ordinal 5 is
published in state 2: it remains visible but is greyed out and absent from the
selectable-row table.

The resource text may suggest posters or handbills, but no card transition was
invented from that prose. The evidence currently proves a row-publication
effect. Its later gameplay consequence is a different frontier.

This is a small example of a general rule. Text explains what the player sees;
the owner bytes decide what the engine does.

## Night Main Street Rejoins the Generic City

One `$MAINS02` action was already byte-closed but had not been projected into
clean gameplay.

Raw ordinal zero now executes its exact signed relation:

```text
RNG(100) < 100 - raw range
```

The ordinary result publishes state `0019h`, which central redispatch resolves
through the generic `$CITYS01` presentation. The exceptional patrol result,
state `003Ch`, remains stopped at its own boundary.

This is the desired architecture: `$MAINS02` does not know how to draw a city
square. It publishes a raw result, and the central state system selects the
destination owner.

## Evidence Became a Reusable Product

The last day was not only about adding routes. It strengthened how routes are
added.

Each selected path now carries a narrow certificate over its exact original
instruction slice. Parent owners and blocking presentation children are bound
separately. Ghidra and Reko are used to cross-check focused cones. Live DOSBox-X
observations close relocated pointers or ambiguous helpers. SDL smoke tests
then validate the clean product without becoming semantic authority.

That discipline caught several details a looser reconstruction would erase:

- a picture that remains after acknowledgement;
- a mode-2 card where a neighboring owner uses mode 0;
- a disabled visible row rather than a hidden row;
- RNG that belongs to one sibling but not another;
- owner-local no-RNG claims that must end before central redispatch consumes
  its own randomness.

The complete engine suite reached 2,927 passing tests after these closures.
More important than the count is what the tests pin: ordered gameplay effects,
raw-state results, picture provenance, forbidden writes, and exact stopping
boundaries.

## What Is Actually Implemented

The clean engine and SDL host now execute the optional entry-card sequences for
`$MAINS01`, `$MAINS02`, and `$SIDES00`; the due-event disabled-row publication
on daytime Main Street; and the ordinary `$MAINS02` ordinal-zero route back to
`$CITYS01`.

The exceptional patrol state and unproven handbill consequence remain closed.
The next work returns to the central MSG owner census: choose high-value
non-combat ordinals, reuse the shared machinery where the bytes actually do,
and continue turning the city from a corridor into the original state graph.
