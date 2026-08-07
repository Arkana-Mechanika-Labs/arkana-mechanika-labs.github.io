---
title: "Devlog #045 - The MSG Machine Revealed"
date: 2026-08-03T18:00:00
summary: "The shared Darklands message system is now understood as a complete transaction: owner publication, generic loading and layout, visible-row mapping, callback dispatch, owner consequence, and central redispatch."
---

Several earlier devlogs described pieces of the Darklands MSG system.

We decoded the archive. We reconstructed token expansion. We matched font
measurements and row rectangles. We made a city card clickable. We followed one
choice through the clock and the state dispatcher.

Those pieces now fit into one stable architecture.

Darklands does not contain hundreds of unrelated menu engines. A state owner
prepares a card and a set of actions. Shared record-43 code loads, expands,
lays out, presents, and reads the player's choice. Control then returns to the
owner, which performs the actual gameplay consequence and publishes the next
state.

In compact form:

```text
raw state
-> canonical state owner
-> MSG/card/row publication
-> generic presentation and input
-> visible row to raw owner ordinal
-> EA14 or EB0A callback
-> owner-local action
-> same card, another card, or next raw state
-> central redispatch
```

Understanding that division has changed both the reverse engineering and the
C# architecture.

## The Owner Builds the Situation

The central state table selects an original owner. The owner does much more
than choose a filename.

It may:

- copy the MSG and picture resource names;
- select a card and presentation mode;
- initialize raw row-state words;
- hide, show, or disable rows according to city data and events;
- install a table of far callback pointers;
- publish the current and previous raw states;
- prepare owner-specific scratch data.

The same `$MAINS01.MSG` resource can therefore produce different visible rows
in different cities. The file supplies the text and card structure. The owner
supplies the current gameplay situation.

This is why the clean engine does not load an MSG file and immediately turn
every line into a button.

## The Generic Engine Builds the Screen

Once the owner has published its context, the shared MSG machinery takes over.

It resolves the archive entry, scans the cards, expands `$` tokens against live
party and world state, interprets control bytes, measures the original bitmap
font, wraps and positions the text, and builds the visible row geometry.

Hidden rows disappear from pointer scanning. Disabled rows may remain visible.
Selectable rows retain the raw owner ordinal assigned by the original card and
owner publication.

That last value is crucial.

Suppose three earlier actions are hidden. The first row on screen may have:

```text
visible index = 0
raw owner ordinal = 5
```

The input controller returns the owner ordinal, not the compact visual index.

Several apparently wrong routes were corrected by respecting that distinction.
A click on the second visible line in one city did not mean “case one.” It
meant whichever raw ordinal the published row table assigned to that line.

## Acknowledgement and Selection Are Separate

A card can require acknowledgement before it accepts a row choice.

The generic controller may therefore return once for Enter, Space, or a click,
loop inside the owner, and only later return a raw owner ordinal. Some cards are
purely informational. Some proceed directly to selection. Some display rows
that are not currently selectable.

These are different original control paths, not presentation details the host
can collapse.

The new engine now has certified profiles for several acknowledgement and input
shapes, including the card-one/mode-zero path used by paired grove owners.
Uncovered modes still stop at their original boundaries.

## EA14 and EB0A

Ordinary rows use the primary callback table conventionally called `EA14`.

The raw owner ordinal selects one far pointer:

```text
callback = EA14[owner_ordinal]
```

After that callback returns, the parent uses the same retained ordinal to choose
the matching owner-local action.

Alternate rows use a second family, `EB0A`.

Potion and saint markers do not jump directly into an owner consequence. They
enter a shared candidate-selection system. That system builds a party-dependent
matrix, distinguishes absent, selectable, and displayed-but-disabled entries,
lets the player choose a candidate and a party context, then publishes the raw
selection for the owner callback.

The owner still decides what the selected saint or item actually does.

This separation is one reason the same generic machinery can serve city
services, encounters, saints, potions, challenges, and ordinary navigation.

## The Strange Return Tails

Not every callback behaves like a normal C function.

The paired `$CITYG05` and `$CITYG06` owners exposed a shared tail at
`ovl_0052:0254`. Their first selected row points there through `EA14[0]`.

The tail does not return to a nearby local case. It reads the current raw state,
pops the active owner's saved registers and frame, and returns directly to the
central controller.

A modern decompiler view can make the adjacent local handlers look like the
natural destination. The original callback table proves otherwise.

This is why COAB still matters. The clean engine only needs the observable
result—return the current raw state—but the low-level layer has to prove the
stack and control behavior before that simplification is safe.

## The Owner Applies the Consequence

Once a row is selected, the owner-specific part begins.

A local action may:

- consume an RNG value;
- advance the calendar;
- maintain event records;
- test the time of day;
- check city flags or local reputation;
- create a new event;
- choose a result card;
- restore the previous state;
- enter combat;
- remain inside a mini-game.

The generic MSG engine should not absorb those rules merely because they occur
after a click.

This boundary is now visible in the C# code. Generic presentation, row layout,
acknowledgement, and selection live in shared message components. Certified
actions expose only the caller-visible consequence of an original owner path.

## A Clean Session Above the Oracle

The clean product route now uses a route-neutral `MessageNavigationSession`.

Quickstart is responsible for initialization: loading the default party,
choosing the starting city and time, and producing the initial PARTY02
sequence. It no longer owns every city transition that follows.

The navigation session carries:

- current and prior raw states;
- the original RNG sequence;
- world time and event state;
- the current presentation;
- acknowledgement and selection phase;
- explicit certified action registrations.

A clean action is selected by resource, card, raw state, and raw owner ordinal.
The registrations are reviewed C# code backed by current certificates.

The raw-state atlas and decision census never generate them.

That is an important line. The atlas tells researchers what may be connected.
The certificates authorize an exact original transaction. The clean action is
the product implementation of that transaction.

## Why We Are Not Replacing COAB

The clean session does not know about `DS`, `SS`, `BP`, relocation segments, or
far pointer arithmetic. That is exactly the point.

The COAB layer remains underneath as an executable specification. It preserves
raw memory, registers, stack geometry, helper order, and fail-closed
alternatives where those details are still observable. Differential tests run
the same fixture through COAB and the clean projection and compare the selected
outcome.

As more owners become stable, the product path can use the clean action while
COAB remains the audit oracle and the implementation for unresolved routes.

The project is therefore not waiting to finish all reverse engineering before
writing maintainable C#.

It is lifting one certified transaction at a time.

## What Is Still Missing

The shared architecture is understood. Several profiles are still incomplete:

- some cancellation and refresh paths;
- more alternate saint and potion outcomes;
- battle handoffs;
- unusual shared-tail callbacks;
- special mini-games such as the full shell game;
- many owner-specific event and inventory consequences.

Those gaps no longer look like hidden alternative MSG engines.

They are extensions plugged into one known machine.

That is a major change in the shape of the project. The question for a new city
state is no longer, “How does this screen work?”

It is:

```text
What does this owner publish?
Which generic profile does it use?
What does the selected original action change?
Where does the central state graph go next?
```

The next devlog follows that model back to Main Street, where a once-static list
of choices started opening into a much larger city.
