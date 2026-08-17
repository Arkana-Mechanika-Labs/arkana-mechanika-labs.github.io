---
title: "Devlog #061 - The Road Darklands Refuses to Show"
date: 2026-08-16T22:00:00+02:00
summary: "Soldier's Road is suppressed by the ordinary owner, yet a one-byte forced publication proves that its original cards, Arms Outfitter, two-hour cost, and return loop still work."
---

Some lost content survives as text with no caller but "Soldier's Road" is stranger:
the text, callback, action, merchant, clock effect, and return path are all
still connected. The released game simply refuses to publish the choice.

We found it inside `$MILCR00`, the Military Crafts screen reached from the
daytime business district by choosing the shops dealing in arms and armor.
The MSG card contains a first source row named **Soldier's Road**, followed by
the city-dependent blacksmith, armorer, swordsmith, and bowyer streets.

In ordinary play, Soldier's Road is absent.

## The missing first row

The natural route is:

```text
daytime business district
  “Shops dealing in arms and armor”
        ↓
$MILCR00 card 0 — Military Crafts
        ↓
Soldier's Road is not published
```

The reason is surprisingly blunt. The `$MILCR00` owner initializes
the publication state for source row 0 to zero. It never writes a nonzero value
to that slot on the ordinary path. The generic layout controller suppresses
rows whose owner state is zero, which means this specific row is NEVER shown.

This is not a city-specific restriction. It is not a failed skill check, a
missing event, or an unlucky random result. The ordinary owner itself hides the
row before the player can select it.

At first, the dormant callback table and local action looked like proof that
the row was playable. That was a useful correction in the research process:
code behind a row proves what would happen after selection, but not that the
row is ever published. Reachability has to be demonstrated separately.

## Forcing one byte, then letting the original run

To test whether the branch was merely debris, we performed a tightly bounded
experiment in the original DOS executable.

At the instruction where the owner copied the hidden row's zero publication
byte into the controller, the probe changed only that byte to one. No callback,
state, merchant result, clock value, or destination was patched. The original
generic controller then drew Soldier's Road and returned source ordinal zero
when it was selected.

![Soldier's Road made visible in the original game](/images/devlogs/061/soldiers-road-visible.png)

From that point onward, all execution was original.

The dormant callback ran. The local action selected one of two introductory
cards from a signed parity result. One describes searching dark streets for a
sign; the other uses the congestion of a city fair. Both continue to the same
merchant profile: **Arms Outfitter**.

![The dark streets approach card showing after clicking on Soldier's road](/images/devlogs/061/soldiers-road-dark-streets.png)

Leaving the outfitter advances the calendar by exactly two hours, writes raw
state `0017h`, and returns to `$MILCR00`. The route adds no new sound command;
it inherits the Military Crafts cue.

The forced experiment therefore produced a complete loop:

```text
forced Soldier's Road publication
        ↓
one of two original approach cards
        ↓
Arms Outfitter merchant
        ↓
+2 hours
        ↓
return to Military Crafts
```

The original screen remained internally coherent throughout. We did not have
to invent a card, shop type, price format, time cost, or return destination.

## Removed, Not Merely Unfinished

Soldier's Road is currently our clearest example of content that appears to
have been removed from ordinary play without being removed from the program.
The branch is more complete than several visible routes elsewhere in the game.
Only its publication is missing.

We still do not know why. It may have been disabled for balance, because it
duplicated another service, because one of its item tables was unsatisfactory,
or simply because the release was frozen while the row was switched off. The
bytes establish behavior, not design intent.

Nor have we ruled out every alternate publication mechanism. The controller
contains an alternate callback lane that remains an explicit research
boundary. Until an original predicate is found that naturally publishes source
row 0, the faithful reconstruction must keep Soldier's Road hidden.

## The Safest Kind of Restoration Candidate

A future restored-content mode could re-enable Soldier's Road with unusually
little speculation. Unlike the callerless night-gate cards, this branch already
has an original selection handler and a complete observable result.

The restoration policy could be simple and transparent:

```text
faithful 483.07 mode:  keep the row hidden
restored-content mode: publish the row and execute the surviving original path
```

Even then, the mode would be clearly labelled. Re-enabling a dormant row is a
change to the released game, however strong the evidence behind it.

The important achievement is that the choice is no longer between forgetting
the branch and inventing it from scratch. We can preserve the released
behavior, preserve the dormant behavior, and let a future player decide which
historical layer to experience.
