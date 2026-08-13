---
title: "Devlog #059 - A Quest Falls Out of a Shopping Trip"
date: 2026-08-13T14:00:00+02:00
summary: "Leaving an ordinary Goods Merchant can create a persistent event, choose a random quest class and location, generate a name, and enter the ten-owner $MCGUF12 job controller."
---

The most surprising part of the Goods Merchant was not buying or selling.
It was leaving.

Most of the time the controller restores the marketplace. Occasionally the
original generates a persistent event. On a rarer branch, the merchant shows
the party a heavy purse and offers a job. That small detour exposed a complete
procedural quest-construction pipeline.

## The Leave Command Keeps Playing

The merchant's raw Leave command is `011Bh`. After the nested controller
returns, the marketplace owner consumes another `RNG(100)` result and checks
several due-event predicates.

The ordinary high-roll path creates a kind-`0007h` event with field
`+1Ah=00FEh`, then returns to the marketplace. That event is persistent and
can influence later marketplace publication. It is not a decorative random
message.

Results `0002h..000Dh` take the rare purse branch. The game advances one hour,
loads `PICS\XPURSE.PIC` through an initialized far pointer, and presents
`$MARKE00.MSG` card 2. Runtime memory bytes established the resource name;
we did not infer it from the picture.

After acknowledgement, the marketplace calls `proc_0039_1712(0)` to build a
new event record.

## Constructing the Event

The event builder draws `RNG(7)` and maps its result through original tables.
The seven possible classification words are:

```text
0000h, 0001h, 0003h, 0004h, 0007h, 0008h, 0009h
```

Each classification carries a paired message code and can select additional
context through more ordered RNG calls. The builder reads current-location
coordinates, chooses another relevant location, schedules the event, and
allocates the first free event slot through the same general event machinery
used elsewhere in the game.

The slot is stored in `DS:E7D8h`. A day/night return state is stored in
`DS:E896h`, and raw state `0151h` is published.

State `0151h` enters `proc_0128_0BF0`, which loads `$MCGUF12` and initializes
a ten-owner quest/job controller. It reads the event's classification,
message code, selected location, and a derived neighboring location. The
classification selects different result cards and later owner behavior.

## Generating Names and Directions

The classification-zero path calls `proc_0029_5CC4` before showing its first
card. This helper made it impossible to fake the visible result safely.

Its selected path combines the startup BIOS timer word, the current location,
and an original constant, reseeds the random generator, consumes a discarded
`RNG(1000)` result, and uses `RNG(108)` to select from the executable's exact
108-entry male-name table. It then samples the clock and reseeds the random
generator again.

The card also needs `$Direction2` and `$LocName2`. These come from the
original first-92-record nearest-location scan and an eight-way coordinate
classifier. The direction is not guessed by comparing city names or choosing
a modern compass function.

In the guided original run, the helper selected **Gregor**. The event pointed
to location record `00B5h`, while the nearest-location scan selected record
`0053h` for the location and direction tokens.

## The First Job Card

The original state-`0151h` controller loads `PICS\XMS126.PIC`. Classification
zero presents `$MCGUF12.MSG` card 1.

An important correction came from decoding the card bytes: card 1 is a
blocking informational card, not the ten-row action menu itself. The ten
owners belong to the later controller entered after acknowledgement.

SDL now reproduces the event construction, exact name generation, nearest
location and direction tokens, XMS126 presentation, and card-1 acknowledgement
boundary. It stops before those ten later quest actions because their effects
must be certified independently.

## Why This Matters

This route demonstrates how Darklands creates the feeling of a living world.
An ordinary shopping trip can seed a durable event; that event contains a
random scenario class, message code, places, schedule, generated person, and
day/night continuation; a later controller turns those fields into text and
choices.

The game is not selecting one prewritten quest object from a modern database.
It is composing a job from shared tables, world records, RNG, calendar state,
and generic MSG substitutions.

By reconstructing that machinery rather than scripting the observed Gregor
case, every future classification and location can reuse the original system.
