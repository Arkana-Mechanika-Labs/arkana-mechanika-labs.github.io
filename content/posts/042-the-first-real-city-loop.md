---
title: "Devlog #042 - The First Real City Loop"
date: 2026-07-28T20:10:00
summary: "Quickstart now continues into a reconstructed city-navigation corridor that works across all 90 starting cities and reaches the first Main Street choices through the original game states."
---

Devlog #039 followed one click through the city.

That was an important milestone. A prepared city-square replay could pass
through the original row handler, advance the clock, enter city north, show a
curfew notice, and return. It proved that several reconstructed pieces could
cooperate.

It was still a bounded replay. The route began from a carefully prepared
fixture, not from launching the game.

The new city work closes that gap.

We can now start the C# host, watch or skip the introduction, press Q, load the
default party, pass through the Quickstart cards, make the first choice, and
continue into a real city-navigation corridor.

This is the first reconstructed city route reached naturally from the start of
the program.

## Following the State, Not the Label

The final Quickstart choice returns raw state `001Dh`. The central Darklands
controller uses that value to select the next original owner, which prepares
the first `$URBAN00` presentation.

From there, the current route continues through:

```text
$URBAN00
-> $CITYN00
-> $URBAN00
-> $SIDES00
-> $MAINS01
```

These names identify original MSG resources. They are not a hand-written list
of screens in the modern host.

At each step, the original owner prepares the resource, decides which rows are
available, installs the row handlers, enters the shared presentation system,
and returns the next state after a choice. The central controller then uses
that state to find the following owner.

The host sees pictures, paragraphs, row rectangles, and input requests. It does
not decide that a row should lead from "urban" to "city north" because those
labels sound related.

## Cards and Choices Are Different Things

One lesson from the earlier MSG reconstruction keeps appearing: showing a card
and selecting a row are separate moments.

Some cards first require an acknowledgement. The player reads the paragraph
and clicks, presses Enter, or presses Space. Only after that return does the
owner publish or accept the selectable rows.

Other presentations can move directly into row input. Hidden rows must stay
out of pointer scanning. Disabled rows may still be visible. A selectable row
needs both geometry and an original handler.

The city route now preserves those distinctions as it moves between resources.
It also preserves owner loopbacks. A presentation may return to the same owner
before a later input produces a new state.

This makes the route feel ordinary when played, which is exactly the goal. The
complexity should live in the reconstruction, not in the controls.

## From One Test City to All 90

The first version of the corridor worked with one known starting city. That was
enough to connect the path, but it was not enough to call the route general.

Quickstart can choose any city index from 0 through 89. Those city records do
not all publish the same information. Flags in the original data affect which
rows appear on `$SIDES00` and `$MAINS01`. Names and local values also vary.

The route now reads the current city record and applies the original
publication rules for every starting location. `$URBAN00`, `$CITYN00`,
`$SIDES00`, and `$MAINS01` share the reconstructed row-layout behavior instead
of relying on screen-specific coordinates copied from one example.

We ran the full corridor for all 90 city indices. Every one reaches the
`$MAINS01` presentation while preserving its own resource-backed text and
available choices.

This all-city pass found and removed one lingering shortcut: a fixed
`$SIDES00` row layout that happened to fit the original test location. The
generic original layout now handles that screen too.

This is why broad input coverage matters even before many actions are
implemented. It reveals where a reconstruction is genuinely driven by game
data and where it is quietly shaped around one familiar sample.

## Main Street Is a New Kind of Frontier

The corridor currently reaches `$MAINS01` card 0 and publishes its ten
resource-backed rows.

It does not yet execute those ten actions.

That stopping point is more significant than it may sound. Earlier frontiers
often ended at file loading, a graphics operation, or an unidentified overlay
call. This one ends at a list of visible things a player can choose to do on
Main Street.

The remaining work is increasingly about gameplay:

- which rows appear under which city conditions;
- how time and the calendar affect an action;
- which events, skills, saints, or inventory items change a result;
- which card or state follows a selected choice;
- how the result is stored for later decisions.

The reconstruction has moved from asking how Darklands displays a menu to
asking what happens when the player acts.

## The First Branches Beyond the Corridor

Work has already begun on several of those branches.

One selected saint callback is now reconstructed through its return to the MSG
system. A challenge choice has been followed into the game's battle setup
route. Another challenge choice advances the clock by one hour and opens
`$CHASE00`, where the player can keep running, draw weapons, prepare an ambush,
hide, throw a potion, or surrender.

The first chase action already reaches its original random threshold
calculation. The next owner is intentionally still closed while its two
possible outcomes are certified.

A potion-related city action has also crossed its first callback and reached
the owner that will present the result, advance time, and restore the next game
state. That route likewise stops before behavior that is not ready.

These are not yet complete player stories, so they are not part of the
playable corridor described above. They show what is waiting immediately
beyond it.

## Why the Stops Still Matter

The SDL frontend could easily make the unfinished rows appear to work. It could
attach a friendly command to each sentence, choose a plausible next card, and
fill the missing behavior in later.

We continue to avoid that.

An unsupported choice stops at the first unresolved original boundary. That
can be less impressive in a demonstration, but it keeps the executable route
honest. When a row finally works, we know which original owner handled it,
which state it returned, what persistent data it changed, and which branches
remain outside the reconstruction.

Darklays has continued to evolve around this work. Its path certificates,
dependency checks, and release workflow now make it harder for an old or
partial result to remain executable after its evidence changes. Those tool
improvements are not the headline this time. Their value is visible in the
city route's ability to grow without quietly turning assumptions into game
logic.

## A Small, Continuous Piece of Darklands

The project now has a continuous graphical route:

```text
startup banner
-> complete animated introduction
-> main menu
-> Quickstart
-> default party and PARTY02 cards
-> first urban state
-> city north
-> urban navigation
-> city sides
-> Main Street
```

The current engine passes 1,605 tests. Darklays passes another 1,005. More
important than either count, the route works across every original Quickstart
city and remains closed where the evidence ends.

This is not a full first playable yet. It is a small, continuous piece of
Darklands that begins where the program begins and ends at a meaningful set of
player choices.

For the first time, the next step is not simply another screen.

It is deciding what to do in the city.
