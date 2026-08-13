---
title: "Devlog #056 - From the City Guard to a Cell"
date: 2026-08-13T11:00:00+02:00
summary: "$CHALL00, surrender, prison, and the priest visit now form one evidence-backed gameplay corridor, while combat and magistrate controllers remain cleanly separated."
---

Some Darklands screens are places. Others are decisions that can send the
party into an entirely different subsystem.

`$CHALL00` is the latter. It is the guard confrontation reached from several
city routes. Its rows can lead toward combat, chase, surrender, or other
guard-owned consequences. Following one of those consequences all the way to
the dungeon taught us how much state can sit between two apparently simple
MSG cards.

## The Guard Screen Is an Owner Table

`$CHALL00.MSG` card 0 publishes seven original owner ordinals. Dynamic item
and saint predicates determine which choices are selectable. The first owner
passes through the original BTL preparation corridor and stops at tactical
combat. The second ordinary route publishes state `007Ah`, which enters the
chase machinery rather than jumping directly to a guessed result screen.

That distinction matters. “Fight,” “run,” and “surrender” are not labels in a
modern menu switch. The card returns an ordinal; its owner performs the
effects and decides the next state.

The `$CHASE00` work eventually closed six actions independently: escape,
hide, ambush, saint, alchemy, and surrender. Some end in combat, some mutate
inventory or time, and some show blocking result cards before continuing.

## Surrender Is a Transaction

The surrender route is not just “go to jail.” It advances time, removes the
party's money and possessions through original inventory owners, preserves
the appropriate inherited route words, and enters raw state `000Dh`.

That state belongs to `$DUNGE00`.

The entry loads the runtime-bound cell picture `PICS\XCELL.PIC`, initializes
nine owners, evaluates party-, event-, and inherited-route predicates, and
publishes the surviving rows. A runtime capture proved an easy-to-miss detail:
owner ordinals and visible-row positions are not interchangeable. In the
observed party state, one owner was omitted and others were disabled, so a
compact visible index would have selected the wrong action.

The clean engine computes those classifications instead of preserving the
single captured row vector as a fixture.

## What the Prisoner Can Do

The nine dungeon actions include attempts to use resources, wait for legal
proceedings, and ask for religious assistance. Each is being closed as its
own owner.

The “ask for a priest” action provided a complete vertical slice. Its 29-byte
owner:

1. advances the calendar three hours;
2. copies the inherited dungeon route words;
3. publishes raw state `0083h`.

State `0083h` enters `$DUNGE01`, a four-choice priest controller over
`PICS\XMS014.PIC`. The priest can hear confession, help with an escape, speak
to the magistrate, or leave the party alone.

Leaving the party alone performs a zero-hour calendar maintenance call and
returns to `$DUNGE00`. Confession applies the selected improvement and field
mutation helpers, advances three hours, displays card 1 over
`PICS\XMS013.PIC`, and returns only after acknowledgement. The selected
escape-failure route advances one hour, displays card 4 over
`PICS\XMS058.PIC`, then returns to the cell with the inherited route value
updated.

Those hourglass sequences are original behavior. They are produced by the
same calendar service used elsewhere, not inserted into SDL for atmosphere.

## Prison Is Not Just a City Row

The city screen can contain a prison-related row when the relevant event and
location predicates publish it. Reaching `$DUNGE00`, however, is not modeled
as setting a convenient “in prison” Boolean. The original uses raw states,
event records, inherited words, and separate controllers.

This is why the reconstruction does not invent a direct `$CITYS00 ->
$DUNGE00` shortcut. The visible city row and the incarceration corridor may
share event facts, but their owners must prove the relationship.

## What Is Implemented

SDL now executes the ordinary four-member surrender-to-cell corridor, the
dynamic `$DUNGE00` publication, the priest request, `$DUNGE01` presentation,
confession, selected escape failure, and the zero-hour return from “leave me
alone.” The corresponding pictures, time costs, cards, and acknowledgement
ordering are evidence-backed.

Combat entry remains a typed handoff to the separately reconstructed combat
layer. Waiting for the magistrate enters another large record-127 controller
and remains stopped at that owner's boundary. The less common dungeon entry
that inserts a missing party character is also kept separate until its
persistent party mutation is certified.

We now have a real prison corridor, but we have not hidden the unexplored
courtroom and combat systems behind plausible shortcuts.
