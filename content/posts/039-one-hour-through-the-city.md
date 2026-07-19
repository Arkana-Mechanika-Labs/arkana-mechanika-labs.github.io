---
title: "Devlog #039 - One Hour Through the City"
date: 2026-07-19T08:45:00
summary: "One click in the city square now follows the original clock, row handler, state dispatcher, overlay resolver, city-north owner, and office notice before returning to the city."
---

The first selectable row on the city-square screen does not look especially
important.

Click it and the game moves on. The text changes, another set of options
appears, and the player continues through the city. In a conventional menu
system, this might be one line in a route table.

In Darklands, that click advances the clock, updates controller state, returns
through a selected-row owner, passes through a central dispatcher, loads another
overlay, publishes another MSG card, waits for acknowledgement, enters an
office routine, shows a curfew proclamation, and finally restores the previous
city state.

After rebuilding the MSG presentation and input path, we followed that click
all the way through.

The result is the first substantial city route executed as a chain of
reconstructed original units rather than a modern description of where the row
ought to lead.

## The Route in One View

The complete path is easier to understand when its four kinds of identity stay
separate: controller state, original owner, MSG resource, and card number.

For this route, the visible sequence is:

```text
state 0012 -> $CITYS00.MSG card 0
  select visible row 0
  advance the game clock by one hour

state 0066 -> $CITYN00.MSG card 0
  acknowledge the card
  select visible row 0

state 006D -> $OFFIC00.MSG card 6
  acknowledge the Curfew proclamation

return to state 0066 -> $CITYN00.MSG
```

Those labels are useful, but none of them authorizes the next step by itself.
The state transition comes from the handler that writes it. The resource name
comes from the owner that copies and loads it. The card number belongs to the
presentation call, not to the state dispatcher.

This sounds like bookkeeping until two values happen to be the same. On this
route, `0006h` appears both as a familiar city state and as the card number of
the office notice. Treating those as one concept would send the reconstruction
in entirely the wrong direction.

## One Click, One Hour

The selected row begins in `$CITYS00.MSG` card 0. Its handler does not
immediately write the destination state. It first calls the game's time-advance
machinery with a one-hour request.

That machinery is more involved than adding one to an hour field. It samples
DOS date and time, updates the internal calendar, maintains active records,
handles rollover, and passes through the original random-seed tails. Some of
those effects can influence future events even when nothing visible happens on
the current screen.

A modern implementation could ask the host for the current time and update a
friendly `DateTime` object. That would be convenient and wrong for this path.

The headless replay instead supplies six ordered DOS date/time responses behind
a raw INT 21h boundary. The reconstructed units consume them in the same order
as the original. There is no host-clock fallback and no default answer if the
contracts run out.

The starting game calendar held hour `0009h`. After the selected route
completed, it held `000Ah`. A targeted observation of the live DOS game showed
the same advanced value at the corresponding point.

Only after the time helper returns does the row owner write the next controller
state:

```text
E7D8 = 0012h
E48A = 0066h
```

`E48A` is the state to execute now. `E7D8` preserves the city-square state for
the surrounding route. The click is therefore not "open city north." It is a
specific sequence of time effects followed by two original state writes.

## Recovering the Full State Table

Following `E48A=0066h` required returning to the game's central state
dispatcher.

Years of earlier research had captured a 99-entry table from the live runtime.
That capture was valid, but it was only the beginning of the table. Reading the
original executable with the new overlay and ownership model revealed the full
structure: 366 unique far pointers, one for every selector from `0000h` through
`016Dh`, followed by a null entry.

Each pointer leads to a compact resident wrapper. The wrapper calls the
record-driven overlay resolver, jumps through the linked target, and carries
the resolver token needed to load the correct code.

The recovered table answers a routing question:

```text
for raw state 0066h, which original entry does the game dispatch?
```

It does not answer whether that target is fully understood, where its procedure
ends, or whether all of its branches can be implemented. The table is therefore
kept as routing evidence, not turned into an executable modern dispatcher.

For state `0066h`, the exact target is the owner at `proc_0069_1250`.

## The City-North Owner Has Two Moments

The state-0066 owner prepares `$CITYN00.MSG` card 0, the screen beginning with
"Eyes and ears open, you..."

It copies the resource name through the original string machinery, initializes
its raw state, calculates ten publication bytes, installs ten far handler cells,
and enters the shared MSG presentation path.

The first return from that presentation is not yet a row choice. It is selector
`0009h`, the acknowledgement of the card header. The owner dispatches that
selector through its installed table, retains state `0066h`, and loops back to
the input controller.

The second invocation returns selector `0000h`, representing the first visible
row. This time the owner reaches a different handler and returns state `006Dh`.

This two-step shape matters. A semantic host command such as "choose row zero"
could easily collapse acknowledgement and activation into one action. The
original controller does not. It performs two separate input cycles with a
loopback between them.

The certified reconstruction preserves that distinction. It starts at the
canonical owner entry, executes the acknowledgement invocation, follows the
original loop, executes the row-zero invocation, and fails closed for every
other selector or branch that is not part of the current certificate.

## State 006D Is an Office Notice

State `006Dh` passes through its own resident wrapper and overlay-resolver
contract before reaching `proc_0071_0D82`.

That owner copies the resource name `$Offic00`, loads the MSG entry, and calls
the generic presentation machinery with card index `0006h`. The original
`$OFFIC00.MSG` resource contains seventeen cards. Card 6 is the Curfew
proclamation observed in the live game.

This discovery corrected an earlier, tempting interpretation. The raw `0006h`
near the presentation call is not state `0006h`, and the proclamation is not a
hidden card inside `$CITYS00.MSG`. It belongs to a different resource selected
by a different owner.

After the player acknowledges the notice, the office owner copies the saved
state `0066h` back into the current-state latch and returns to city north.

The route has now settled:

```text
city square
-> one hour passes
-> city north
-> office curfew notice
-> city north
```

What looks like a short conversation is actually a tour through the shared MSG
system, two overlay owners, the time subsystem, the state vector, and the
resident resolver.

## The Controller Around the Controllers

Closing the state-006D wrapper exposed the larger owner surrounding the whole
process.

The resident routine at `03A1:000A` initializes the game's central controller,
dispatches the current state through the 366-entry vector, stores the value
returned by the selected owner, rotates that value into the next-state latch,
and repeats the loop. It also owns the startup path that eventually reaches the
first interactive controller.

This is the machinery that turns individual state owners into a running game.
It is also large: more than 1,200 bytes and 366 instructions, with calls into
graphics, input, DOS, audio, resource loading, and overlay transport.

Rather than treating all of those calls as engine logic, the reconstruction
separates two questions. If a platform call only moves pixels, polls hardware,
or loads an overlay, its exact input and output contract can remain behind a
typed host boundary. If the controller consumes a returned value or memory
effect to decide game behavior, that dependency has to be reconstructed.

One certified path through the resident owner now covers the startup prefix up
to the next unresolved logic-bearing controller. That work produced an
unexpected correction.

## The Start Screen Reappears

Old runtime research had already found the start-screen controller at a loaded
address and mapped its Q, C, and T choices. What it had not established was the
controller's canonical place in the original overlay system.

The resident startup owner reaches it through resolver record 37. Darklays maps
that target to `proc_0037_9C48`, byte-for-byte identical to the controller seen
in the older runtime session.

This meant an earlier attempt to continue the resident path past that call was
wrong. The target was not a harmless platform transfer. It was original
logic-bearing behavior, so the engine path was shortened and made to fail at
the call until the controller could be assessed independently.

That assessment recovered the three choice roots:

```text
Q/q -> proc_0037_4184
C/c -> proc_0037_0000
T/t -> proc_0037_81B2
```

Each target is a substantial controller of its own. One manages default and
file setup, one performs broad resource and interface initialization, and one
runs a modal path with dozens of calls. They are mapped, but they are not yet
implemented.

Stopping there is important. The old research is not lost; it now has a stable
home and a verified route from the original executable. But familiar button
meanings are not a substitute for the code behind those buttons.

## What Is Complete, and What Is Not

The city route is currently a deterministic reconstruction replay. It begins
from an exact bounded fixture, consumes raw platform responses, and executes the
certified original units and paths needed for this scenario. The engine test
suite currently passes 776 tests.

It is not yet a complete SDL gameplay corridor. Several large owners remain
partially implemented and fail closed outside their certified routes. The
resident controller does not yet run every state from startup to termination,
and the newly anchored start-screen branches remain research frontiers.

That is why the project tracks different milestones separately. Twenty-six
complete original owners are executable. Ten canonical-entry paths through
larger owners are promoted. The number of fully integrated gameplay corridors
is still zero.

The route nevertheless changes the nature of the work ahead. We are no longer
connecting city labels with hand-written destinations. We are extending a real
chain of original controllers, one owner and one dependency at a time.

One click now passes through the original clock, the original state table, the
original overlay resolver, and the original result card before returning to the
city.

The next click has somewhere honest to begin.
