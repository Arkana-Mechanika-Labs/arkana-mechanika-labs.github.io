---
title: "Devlog #062 - The Street of the Blacksmiths"
date: 2026-08-17T05:30:00+02:00
summary: "Street of the Blacksmiths appears in only 32 of 92 city records, then chooses among a direct merchant, a daytime street controller, and a nighttime controller from original world and party conditions."
---

Soldier's Road is globally hidden. **Street of the Blacksmiths** is not. It is
real, playable content whose first condition is buried in the current city's
raw data.

That difference was easy to miss. Testing in Pressburg showed no blacksmith
street, which initially made it look like another dormant row. Testing the
owner against the complete city database revealed a much more interesting
system.

## The First Gate Is the City

The route begins during the day, because the business-district state presents
`$BUSIN00` by day and the Main Street night screen after hours.

```text
daytime business district
  “Shops dealing in arms and armor”
        ↓
$MILCR00 card 0 — Military Crafts
        ↓
“Street of the Blacksmiths” only if city byte +62h is nonzero
```

The Military Crafts owner reads byte `+62h` from the current `DARKLAND.CTY`
record. At this call site, only zero versus nonzero matters.

Pressburg has zero, so the row is suppressed. Steyr has a nonzero value, so it
is published. Across the 92 shipped city records, exactly 32 enable the street
and 60 hide it.

This is why a route can be difficult to find without being removed. A player
can visit the correct broad district, choose the correct trade category, and
still never see the option because the current city was not assigned that
craft selector.

The reconstructed engine obviously preserves that distribution. It does not make the
row globally available for convenience, and a regression test fixes the
32-of-92 result against the shipped city data.

## One Selection, Three Destinations

But seeing the row is only the first condition. Selecting it does not always open
the same screen and that's what is interesting.

The original action has three destination classes:

1. **Ordinary daytime visit.** If an internal flag is zero and a computed
   unsigned threshold is below 100 (both not quite identified yet), the game opens
   the selector-zero **Blacksmith** merchant directly. Leaving advances one hour 
   and returns to Military Crafts.
2. **Daytime fallback.** If that flag is nonzero or the threshold reaches at
   least 100, the game enters raw state `004Bh`, the richer `$BLACK00`
   blacksmith-street controller with `PICS\\BKSMITH.PIC`. 
3. **Nighttime fallback.** Outside the original daytime interval, the threshold
   is not evaluated. The game enters raw state `004Ch`, `$BLACK01`, with
   `PICS\\XMS043.PIC`.

Entering Military Crafts normally requires the daytime business screen, but
other interactions can advance the clock while the party remains inside this
part of the city graph. The original action therefore still owns a genuine
night destination.

## The Threshold Is About the Party and the Place

The daytime direct-merchant decision is deterministic. It does not roll the
random generator and does not ask the player to select a character.

Its threshold combines:

```text
a city-and-season term reduced modulo 21
+ party fame divided by 20
+ local reputation divided by 2
+ average current Charisma of the active party
```

A guided original run in Groningen at 10:00 produced a threshold of 41. The
internal flag was zero, so the result was below 100 and the party entered the
direct Blacksmith merchant. That observation matched the static arithmetic and
confirmed that `$BLACK00` is a fallback, not the unconditional daytime
result.

This is a good example of why endpoint reconstruction is dangerous. A capture
in one city with one party can make “Street of the Blacksmiths opens a shop”
look like the whole rule. Another city, another reputation value, or another
hour can select a different owner entirely.

## The Street Controllers Are Larger Than the Shop

The daytime `$BLACK00` owner publishes seven possible rows. The nighttime
`$BLACK01` owner publishes ten. Their availability depends partly on persistent
event records and, on one daytime row, on whether the party carries one of a
small set of items or formulas.

The clean engine now reproduces both presentations, their exact day and night
pictures, their ordinary Leave actions back to Military Crafts, and the first
`$BLACK00` merchant action. That merchant consumes one hour and returns to the
appropriate day-or-night street screen after the clock advances.

The remaining actions stay fail-closed until their callbacks and effects are
certified. The visible menu is therefore no longer mistaken for a simple list
of shops, but neither is its unfinished reconstruction padded with plausible
blacksmith services.

## Rare Content Is Still Canonical Content

Street of the Blacksmiths belongs in the faithful reconstruction. Its scarcity
is part of the original world model. The correct restoration is not to expose
it everywhere, but to preserve the city field, time classification, party
calculation, fallback owners, persistent-event predicates, and return loops
that make it rare.

Alongside Soldier's Road and the callerless night-gate cards, it gives us three
different restoration categories:

```text
conditional content: original route exists and should remain conditional
hidden content:      complete route survives but ordinary publication is off
orphaned content:    original cards survive but no executable caller is known
```

That classification will matter later. It lets the project finish the faithful
483.07 game without silently “fixing” it, while also building enough evidence
to support an optional restored-content edition. Removed branches could be
re-enabled, unfinished branches could be completed cautiously, and every
editorial step could remain separate from the historical reconstruction.
