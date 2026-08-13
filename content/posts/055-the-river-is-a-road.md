---
title: "Devlog #055 - The River Is a Road"
date: 2026-08-13T10:00:00+02:00
summary: "Darklands boat travel is now a real multi-city system: fares, waiting, long calendar advances, city-data replacement, arrival choices, and onward voyages all come from the original machinery."
---

The docks looked like another city menu. They were not.

Behind `$DOCKS00` is a compact transportation system that reads the active
city record, offers routes that really exist from that port, charges the
party, advances time twice, replaces the current city data, and hands control
to a separate arrival controller. Completing it connected several systems we
had previously reconstructed in isolation.

## Five Copied Owners, One Sailing Family

The original contains five sailing handlers. The first four correspond to
visible destinations; the fifth exists but is not published as a selectable
row by the current presentation.

Comparing their bytes showed that they are copies of one algorithm. They vary
only in the fare-record address, the destination word in `DARKLAND.CTY`, and
relative call displacements caused by their positions in the overlay. That
gave us the right clean model: one parameterized sailing action, not a set of
city-specific routes.

Each city record holds as many as five boat connections at offsets
`+4Ah..+52h`. Missing routes remain absent. The game is building the menu from
world data, just as it builds other city rows from city flags.

## Paying in Florins, Groschen, and Pfennigs

The fare is not flattened to a modern integer and subtracted casually.
Darklands keeps its three denominations and performs the original borrow
sequence:

- 12 pfennigs borrow from one groschen;
- 20 groschen borrow from one florin;
- the three words are written in the original order.

An unaffordable fare takes a different route. The game advances one hour and
can mention selling mounts to reduce the price. That text is useful evidence
for the recurring item-definition mask `2000h`, which strongly correlates
with horses or mounts, though the raw flag remains conservatively named until
the data relation itself proves the vocabulary.

The successful route subtracts the fare before the voyage starts.

## Two Clocks, Not One Travel Duration

A paid voyage consumes two separate random calendar effects.

First, `RNG(3)+1` chooses a wait of one to three hours. `$DOCKS00.MSG` card 9
is displayed over the retained dock picture while the party waits to cast
off. Only after acknowledging that card does the calendar advance.

Then the destination city and description records replace the active
`DARKLAND.CTY` and `DARKLAND.DSC` data. A second random draw selects 48 to 95
hours of sailing.

The total is therefore 49 to 98 hours, but the two steps must remain ordered.
Combining them into a convenient “travel for N days” operation would lose the
original acknowledgement boundary, RNG order, and calendar side effects.

This work also exposed a valuable calendar boundary. A second consecutive
voyage crossed August into September and entered the monthly world-maintenance
owner. Until that owner was certified, SDL correctly stopped instead of
pretending a same-month helper could handle the transition. The calendar work
later closed that general rollover path.

## Arrival Is Its Own Controller

The sailing owner publishes raw state `005Ah`, which enters `$ENTER00`.
The original loads `PICS\XRIVER.PIC` and offers a new set of choices:

- disembark outside the city;
- pay the wharf toll;
- persuade the wharfmaster;
- sneak ashore;
- invoke a saint;
- remain aboard and continue to another connected port.

This corrected an earlier visual assumption. The arrival screen does not
retain the previous city or dock picture. Runtime pointer bytes established
`XRIVER` directly; the screenshot merely corroborated it.

The guarded and besieged variants come from city flags. Toll admission uses
local reputation and events. Persuasion uses the leader's Charisma and Speak
Common with reputation adjustment. Sneaking combines party Streetwise and
Stealth before its success or combat result.

The onward-voyage choices form a particularly satisfying loop. They advance
time, load the newly selected city and description records, and republish
state `005Ah`. The boat can therefore continue from port to port through the
same original controller.

## What Is Implemented

SDL can now execute the paid voyage for every published dock destination,
including exact fare subtraction, the one-to-three-hour departure card, the
48-to-95-hour voyage, city and description replacement, hourglass/calendar
effects, and the `$ENTER00` arrival presentation. It can also follow the
published onward-boat routes generically.

Several arrival choices are independently implemented, including land
approach, toll acceptance and rejection, and persuasion outcomes. Uncertified
saint effects and combat-bearing failures remain explicit boundaries.

The important result is larger than “boats work.” The river network now uses
the same city data, calendar, money, event, MSG, and redispatch mechanisms as
the rest of the game.
