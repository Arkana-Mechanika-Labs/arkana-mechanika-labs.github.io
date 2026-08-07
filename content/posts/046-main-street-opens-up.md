---
title: "Devlog #046 - Main Street Opens Up"
date: 2026-08-04T22:00:00
summary: "Main Street is no longer the end of the reconstructed corridor. Certified actions now branch into day and night streets, city services, groves, docks, markets, churches, and returning city loops."
---

Devlog #042 ended with ten choices on `$MAINS01.MSG`.

The route was continuous from power-on, but the city itself still behaved like
a beautifully reconstructed lobby. The rows were real, their visibility came
from the current city record, and their geometry matched the original. Most
clicks still stopped at the first unresolved owner.

That frontier has moved.

Main Street now acts like a hub. Several of its raw owner ordinals execute
their original handlers, consume the appropriate random or calendar state,
return through the common owner suffix, pass through the central dispatcher,
and arrive at real destination presentations.

The city is beginning to branch.

## Raw Ordinals, Not Row Numbers

The visible order of `$MAINS01` is not fixed.

City flags can hide some options and leave others in place. A row that appears
first in one city may appear third in another. The selected input path therefore
returns the raw owner ordinal published by the original owner.

Every new action is keyed to that identity.

For example, raw ordinal `0008h` is the option whose resource text describes a
scenic grove where the party can wait and relax. Its screen position is
city-dependent. Its owner identity is not.

This distinction allowed the same clean action to work across the Quickstart
city range without attaching behavior to a screenshot coordinate.

## Day Streets and Night Streets

Several Main Street actions branch according to the original hour classifier.

The classifier uses the raw 24-hour game state. Day is the signed range from
hour 5 through hour 18. Other hours select the night owners.

That produces paired destinations:

```text
daytime main street  -> $MAINS01
nighttime main street -> $MAINS02

daytime side streets -> $SIDES00
nighttime side streets -> $SIDES01
```

The actions do not merely inspect a clean `Hour` property. Their COAB paths
preserve the original RNG call, any requested calendar advance, event
maintenance, the later hour classification, state publication, and common
post-action predicates.

The clean projection receives the resulting raw destination and presents the
matching resource.

The practical result is simple: walking through the city at night no longer
uses the daytime menu with darker colors. It follows different original
controllers and different MSG resources.

## The Grove Branch

Raw owner ordinal `0008h` gave the new graph one of its first paired
destination families.

The selected action:

```text
$MAINS01
-> EA14[8]
-> one RNG(0064h)
-> hour classification
-> state 0021h or 0022h
```

State `0021h` presents `$CITYG05.MSG`. State `0022h` presents `$CITYG06.MSG`.

Both owners use the generic MSG engine, but they remain distinct canonical
owners with separate resources and separate certificates. Their first selected
row returns through a shared parent epilogue, preserving the current state.
Other grove actions were left closed until their own consequences could be
proved.

The branch later gained certified exits back toward the ordinary city graph.
That made the grove a place the player can enter and leave, not a decorative
dead end.

## CITYF00 and the Missing Middle of the City

Another Main Street action publishes state `001Bh`.

The state atlas resolves it to `ovl_0050:1CEE`, an owner that presents
`$CITYF00.MSG`. The first assessment was deliberately destination-aware: there
was little value in certifying a click that only reached an unresolved state
number.

Once the destination presentation was closed, the action became useful.

`$CITYF00` led to further certified routes, including returns toward Main
Street and the side streets. Related state `001Fh` work opened the docks
presentation and its own selected return.

This filled in a part of the city graph that had previously existed only as raw
state labels and old runtime correlations.

## Markets, Docks, and Business Hours

The city data and owner predicates also control service destinations.

The reconstructed routes now include marketplace and docks presentations,
along with day/night resource selection and original fare or option text where
those paths have been certified. The owners still decide which options are
present. The generic message engine only lays out the rows they publish.

A later city-square action advances one hour and routes to a marketplace state.
The destination uses the original post-calendar classification to choose the
appropriate business or night presentation.

This matters because “go to the marketplace” is not one timeless transition.
The original path may consume RNG, advance the calendar, maintain events, cross
a day boundary, and choose a different destination owner.

The clean action keeps that behavior without exposing the calendar owner's raw
stack frame to the product layer.

## The Central Suffixes Matter

A local action often writes a plausible next state before the parent owner is
finished.

Afterward, the parent may still run a common sequence of event, city, and
record predicates. Any of them can replace the state.

Early in the project, it would have been tempting to stop at the local write
and declare the route complete. The newer Main Street work follows each
selected action through:

```text
local handler
-> owner-specific action
-> common post-action predicates
-> owner epilogue
-> resident central redispatch
-> destination owner
-> stable destination presentation
```

Only then does the clean route expose the transition.

This is one reason the raw-state graph has grown more trustworthy even as it
has grown more complex.

## Midnight Is Not Just Hour Zero

Time passage exposed another important edge case.

Advancing from hour 23 by one hour is not equivalent to assigning zero to the
hour field. The original calendar path performs date maintenance, event
maintenance, and ordered RNG reseeds. It may cross the month boundary or reach
callbacks that are not yet supported.

A selected Quickstart midnight route is now certified for the exact same-month
shape. Unsupported rollover and callback paths still fail closed.

The clean session therefore no longer has a generic `AdvanceHour` escape hatch
that mutates only visible time. Certified actions compose the original calendar
effect or stop.

That is less convenient and much safer.

## Main Street Is No Longer One Screen

By the end of this work, the selected `$MAINS01` owner had executable
transitions for all ten raw owner ordinals, each with its own exact constraints.
Some outcomes remain unavailable in the clean frontend because their
destination owners or rare branches are still closed. The action identities
themselves are no longer a blank table.

The route can now move among:

```text
city square
main streets
side streets
churches
groves
markets
docks
day and night variants
several service and encounter states
```

Not every row in every destination is complete. Combat, special encounters,
saint and potion consequences, and many service actions remain frontier work.

But the city is no longer a single corridor ending at Main Street.

It is a growing network of original owners, joined by the same generic MSG
machine and the same central state dispatcher.

The next step was not another navigation edge. It was letting the player open
systems that sit beside the city menus: Party Info, the character sheet,
saints, and the interior life of a church.
