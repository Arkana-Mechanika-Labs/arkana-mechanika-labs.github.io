---
title: "Devlog #047 - A City Beyond Menus"
date: 2026-08-07T09:00:00
summary: "The reconstruction now reaches character sheets, saints, church services, marketplaces, and the council hall—using original resources and certified owner logic rather than modern stand-ins."
---

A city can have many connected screens and still feel like a diagram.

Main Street leads to the side streets. The side streets lead back. A grove,
market, dock, or church can appear at the correct hour. The state graph becomes
larger, but the player is still mostly choosing where to go.

The latest work has started filling those places with behavior.

The party panel can open a reconstructed character sheet. Church actions can
attend Mass or return to the street. A city-square choice can enter the
marketplace or the council hall. Original hour names and reputation labels have
replaced modern placeholder text.

These are smaller systems than combat or world travel. Together, they make the
city feel less like a route test and more like Darklands.

## Party Info and the Character Sheet

The permanent party panel has been visible since the Quickstart reconstruction.
For a long time, it was mainly part of the presentation.

The F6 Party Info route and selected character-sheet slices are now executable.

The sheet is not drawn from a captured screenshot. The SDL host composes it
from the original resources:

- `ARMBACK.PIC` for the base;
- record-selected paper-doll layers;
- the original bitmap font;
- the selected character's copied 0x80-byte record;
- the exact frame and focus lines drawn by the original owner.

The first clean opening stops at a certified original boundary. From there,
several detail panels have been added independently.

The attributes panel shows the seven original labels and the current/maximum
pairs from the selected record. The weapon-skills panel uses its own brush and
seven full skill names. The secondary-skills panel uses another brush and six
original labels.

Opening, replacing, and closing a detail panel follows the original surface
lifetime and focus behavior. Left and right party navigation first restore the
base sheet, release the temporary detail surface, clear the detail state, and
then move focus.

That order matters. A first clean implementation kept the graphical detail
alive too long and effectively trapped the screen. The original input owner
showed exactly where the surface had to be released.

Equipment dragging, formulas, several lower detail buttons, and broader saint
interaction remain closed. The sheet is growing from certified slices, not from
a speculative modern character model.

## Saints and Returning to the Previous State

The generic MSG engine already understood the broad shape of alternate saint
and potion selection. A row can request a candidate matrix, let the player
choose a saint or item and a party context, and return raw selection fields to
the owner.

The newer clean work adds more of the presentation around that mechanism.

A selected saint presentation can now be reached from the character and city
systems. `$SELEC00` also gained an exact prior-state return: one certified row
restores the state remembered by the central navigation history and returns to
the presentation that opened it.

That history is tracked generically by `MessageNavigationSession`. It is not a
special “return to Main Street” rule. The original selected action reads the
prior-state word and publishes it.

Other `$SELEC00` rows remain fail closed. The general pattern is now available
without pretending that every saint, potion, formula, or inventory consequence
has been reconstructed.

## Entering the Church

A certified city-square action now reaches `$CHURC00.MSG`.

The route begins in `$CITYS00`, selects the raw owner ordinal for the church,
copies the selected row into the original scratch area, consumes the required
RNG and calendar effects, crosses the common parent suffix, and publishes state
`0013h`.

The state owner then chooses the church presentation according to current city,
time, events, and raw local conditions.

The clean frontend receives the real message resource, picture, rows, and
original text layout. It does not attach a church screen to the sentence in the
city-square MSG file.

Church exits now return to the certified Main Street and side-street
destinations. That gives the interior a normal place in the city graph.

## Attending Mass

The church route also gained a selected Mass action.

The original logic distinguishes whether the service is currently available
and whether the party meets the raw money threshold. The resulting cards and
pictures come from the original resource descriptors:

```text
church card
-> unavailable service result
or
-> successful Mass result
```

The action preserves the owner's state changes and presentation lifetime. It
does not generalize the money field into a modern economy system or infer
unreconstructed church services from the card text.

This is a good example of the project's current boundary. The player can
perform one real church action, see the original result, and return through the
certified graph. Unselected rows remain visible only when the original owner
publishes them, and unsupported consequences still stop.

## Original Words for Time and Reputation

Some of the most visible corrections did not require a new state owner.

Party Info previously displayed convenient modern labels for time of day and a
generic `Rep:` caption. The original executable uses a more specific vocabulary.

The reconstructed classifiers now produce the canonical-hour names:

```text
Matins
Prime
Terce
Sexts
Nones
Vespers
Compline
```

At hour 9, Party Info displays `Terce` and the raw numeric hour `9`.

Local reputation uses another original classifier:

```text
a local hero
respected
unknown
suspected
wanted
hunted
```

The same relation is reused by map hover and other clean presentations. The
hourglass time-passage panel also renders the original canonical-hour name in
the location the DOS owner used.

These changes removed plausible but unsupported text from the clean frontend.
They also show why data and code have to be reconstructed together: the strings
are embedded in the executable, while the thresholds that select them live in
original owners.

## The Marketplace

Another `$CITYS00` action now leads to the marketplace.

The selected owner consumes a range-100 random value, applies its signed raw
threshold and guard, advances the calendar by zero or one hour as the original
branch requires, classifies the resulting hour, and publishes one of the
marketplace-related states.

The clean destination may therefore differ by time. A daytime business
presentation is not simply the nighttime Main Street card with a different
picture.

The route preserves the selected row scratch text, calendar/event effects, RNG
ordering, parent suffix, central redispatch, and destination presentation.

As usual, marketplace row actions are a separate frontier. Reaching the market
does not silently certify buying, selling, or every service described there.

## The Council Hall

The newest city-square route opens the council hall.

This row is capability-dependent. It is published only when the current
`DARKLAND.CTY` record carries the appropriate flag. Its raw owner ordinal is
`0001h`, but that does not mean it is the second visible row in every city.

The selected action copies the row text, consumes RNG, runs the current
calendar/event operation, and publishes state `002Bh`. The destination owner
loads `$COUNC00.MSG` card 0 and computes ten row states using city, event,
reputation-like, and known-saint predicates.

One remaining input was not initialized by the owner itself: a module-data
pointer used to select the picture name. A narrow natural runtime observation
captured that pointer in the exact scenario. It resolved to the original
`xms047` string, so the SDL presentation uses `PICS\\XMS047.PIC`.

The picture was not guessed from a screenshot or from a similar resource name.
The runtime observation supplied one missing scenario value; the original bytes
still defined the owner, pointer use, rows, and control flow.

Council-hall actions remain closed. The new route stops at the first stable
presentation.

## A City That Can Grow

The reconstruction now contains more than a chain of MSG cards.

It has:

- a state graph recovered from the executable;
- generic loading, token, layout, acknowledgement, and input machinery;
- explicit certified actions;
- original calendar, RNG, event, and row-publication effects;
- clean city navigation independent of Quickstart initialization;
- character-sheet presentation slices;
- saint and prior-state selection behavior;
- church, grove, market, dock, and council-hall destinations;
- original time and reputation text.

Combat, world travel, inventory manipulation, most services, quests, and many
special encounters still lie ahead.

The important change is architectural. New gameplay no longer has to be built
as a special path inside the Quickstart demo. A certified owner action can
publish a raw result, the central graph can find its destination, the generic
MSG engine can present it, and the clean session can expose it without adopting
the original machine model as its public API.

The city is not complete.

It is beginning to behave like a place.
