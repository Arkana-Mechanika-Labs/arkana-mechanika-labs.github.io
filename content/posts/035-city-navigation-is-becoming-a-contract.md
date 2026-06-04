---
title: "Devlog #035 - City Navigation Is Becoming a Contract"
date: 2026-06-04T00:00:00
summary: "The city is no longer a menu-shaped mystery. It is a state machine with owner routines, row-status producers, selected-row handlers, service boundaries, day/night routing, and explicit stop signs."
---

City navigation is where Darklands stops being a sequence and starts being a
place.

The main street, the city square, the marketplace, the side streets, the city
gates, political notices, rumors, services, churches, inns, docks, and guards
are not just menu labels. They are a compact little operating system. The
original executable is constantly deciding which card to show, which rows to
publish, which rows to hide, which state to enter next, whether to remember a
return point, whether a service body owns the next step, and whether the time of
day changes the answer.

That is the part we now understand much better.

The goal is not to write a pleasant modern city menu that resembles Darklands.
The goal is to reconstruct the contract the original city system was using:
given this city state, this owner routine, this visible card, and this selected
row, what did the DOS game actually do?

## The City Has a State Latch

The central mechanic is the city state latch. In the original runtime, the
current city controller state is carried through a word we track as `E48A`.

That word is the spine of the city. When the player chooses an option, the
selected-row handler often writes a new value to `E48A`. That value tells the
outer city dispatcher which owner body should run next.

For example, the first playable slice starts at state `0006`, the main street.
Selecting the city square writes `0012`. Selecting the marketplace writes
`0015`. Selecting a side street writes `0009`. Selecting the gate path writes
`003A`.

This sounds simple until the important detail appears: the text does not prove
the state. A row can say "the marketplace," but the reimplementation is not
allowed to treat that text as evidence. The destination is only promoted when
the selected-row code itself writes the destination state, calls a known helper,
enters a service boundary, or stops at a named unresolved boundary.

That rule keeps the city from turning into a hand-authored menu tree.

At a high level, the loop looks like this:

```text
E48A current state
  -> dispatch to owner body
  -> owner publishes card text, row status, and row handlers
  -> renderer/input loop returns selected row SI
  -> selected-row handler writes E48A/E7D8/context or enters a boundary
  -> dispatch again
```

The selected row is usually tracked as `SI`, so a route is best described as a
pair: current state plus selected row. `0006/SI=0000` is not the same fact as
`0012/SI=0000`, even if both rows are visually "top options" on their cards.
The row number is only meaningful inside the owner that published it.

## Owners Are the Bodies Behind the Screens

Each state has an owner body. The owner is the original routine that prepares
the card, publishes row status, installs selected-row handlers, and eventually
hands control to the renderer/input loop.

The player sees "Main street." The implementation sees something more precise:
state `0006`, owner entry for the main-street card, published row statuses, and
selected-row handlers. The same pattern applies to the city square, marketplace,
side streets, city north, gate selection, and special services.

This is why the current runtime has moved toward ASM-backed owner states. The
active city source is no longer a comfortable C# catalog of guesses. Promoted
owner-state bindings come from recovered original-code evidence. If a state or
row is not backed, the runtime stops cleanly instead of falling through to an
older interpretation.

That change is less glamorous than drawing a new screen, but it is the kind of
change that makes the whole system trustworthy.

There are three owner facts we care about before a state becomes cleanly
playable:

```text
entry     = where this owner body begins
surface   = which MSG/card/PIC material it publishes
handlers  = what each selectable row does after SI is chosen
```

If we only know the surface, we can show text but not safely advance. If we only
know a handler table, we might know destinations for rows the player never sees.
If we only know an entry address, we have bytes but not yet a city behavior. The
useful runtime state is the overlap of all three.

## Selecting a Row Is Not Just Clicking a Button

A city option has two separate lives.

First, the owner has to decide whether the row is visible. Then, if the player
selects it, the selected-row handler decides what happens.

Those two pieces are independent. This was one of the biggest corrections in
the city-navigation work.

At first glance, a decoded card can make a row look solved. There is text. There
may even be handler-looking code nearby. But the original owner might hide that
row before the renderer ever sees it. The city-square barracks/university
mismatch exposed this clearly: route-looking material existed for rows that the
original card owner was not publishing as visible options.

So the rule is now stricter:

```text
A promoted city row needs both:
1. a selected-row outcome;
2. a proven option-status producer.
```

That second phrase, "option-status producer," is the less obvious machinery. The
owner routine writes scratch status words for rows 0 through 9. We track those
scratch words as `EE76..EE88`. Later, the owner mirrors them into the
renderer-facing bytes `E99C..E9A5`.

The renderer-side rule is shared:

```text
0 = hidden
1 = visible and selectable
other nonzero = visible but not selectable
```

The status words are laid out as a ten-row strip:

```text
row 0 -> EE76 -> E99C
row 1 -> EE78 -> E99D
row 2 -> EE7A -> E99E
row 3 -> EE7C -> E99F
row 4 -> EE7E -> E9A0
row 5 -> EE80 -> E9A1
row 6 -> EE82 -> E9A2
row 7 -> EE84 -> E9A3
row 8 -> EE86 -> E9A4
row 9 -> EE88 -> E9A5
```

That mirror is easy to describe and dangerous to oversimplify. The interesting
part is everything that happens before the mirror: owners seed all ten rows,
then clear or alter individual rows based on city flags, event flags, random or
threshold helpers, local conditions, and service availability. The same visible
card can therefore behave differently by city, time, or campaign state without
the text itself changing.

The producer is not shared. Each owner can compute those row statuses in its own
way, using city flags, event flags, helper calls, or local predicates.

That is why city navigation is no longer only about destinations. We now also
have to prove how each screen decides what the player can see.

## The First Playable Spine

The first ordinary city loop is now covered by executable contracts.

From the main street, the player can reach the city square, marketplace, side
street, and gate-selection screen. From the city square, the player can reach
the city-north information screen, marketplace, and day/night side-street path.
From the side street, the player can return to main street, city square, or
marketplace. From the marketplace, one row returns to main street. From gate
selection, one row restores the previous city state. From city north, the proved
rows reach office, affairs, situation, special services, and return to the city
square. Special services has a proved return to city north.

The shape looks like this:

```text
Main street -> City square -> City north -> Special services -> City north
Main street -> Marketplace -> Main street
Main street -> Side street -> City square
Main street -> Gate selection -> previous city state
```

That is a real playable spine. More importantly, it is typed. Some rows are
fixed state writes. Some rows write a remembered state. Some rows require the
calendar/day-night decision. Some restore previous context. Some stop at service
bodies. Some are explicit gaps.

The win is not just movement. The win is that movement now has accountable
mechanics.

Here are a few route shapes from that spine in plain terms:

```text
0006/SI=0000  main street -> city square      writes E48A=0012
0006/SI=0002  main street -> marketplace      writes E48A=0015
0006/SI=0007  main street -> side street      writes E48A=0009
0006/SI=0009  main street -> gate selection   writes E48A=003A
0015/SI=0008  marketplace -> main street      writes E48A=0006
003A/SI=0006  gate selection -> previous      restores remembered state
0067/SI=0009  special services -> city north  writes E48A=0066
```

Those examples are deliberately boring. Boring routes are good. They give the
engine stable stepping stones before it reaches the rows that branch through
services, thresholds, or delayed state.

## Deferred State and Remembered Context

`E48A` is the current-state latch, but it is not the only word that matters.

The city also uses `E7D8` as a deferred or remembered transition. A row can
write a next state into `E48A` and also preserve another state in `E7D8`. That
matters for routes where the city needs to enter an intermediate owner and later
return to the place that made sense in context.

There is also previous-state behavior. Gate selection is the clearest current
example. The gate screen is entered from the city, but the "do not leave yet"
option should not blindly jump to one hard-coded place. It restores the prior
city state. The clean runtime models that as previous-state restoration rather
than as a fake fixed route.

This is one of the quiet ways the original game feels coherent. The city does
not only know where a button points. It often knows where the player came from.

There is a useful way to think about these latches:

```text
E48A = run this state now
E7D8 = remember this state for a later/deferred transition
E896 = context-like saved state used by some restore paths
previous state = host/runtime memory of where this screen was entered from
```

The modern runtime does not expose these as raw DOS memory. It turns them into a
small `CityFrame`: current state, previous state, deferred state, current date,
and optional context state. That gives hosts a simple object to carry forward
while still preserving the original contract.

## Day and Night Are a Route Mechanic

Some city choices are paired. A side-street route can land on the day side
street (`0009`) or the night side street (`000A`). The choice depends on the
calendar/time helper.

The clean runtime has to be careful here because there are two similar-looking
helper identities in the evidence. The translated live day/night helper is
understood well enough to use. A related source callsite remains review-only and
must not be treated as the same thing.

That distinction sounds fussy, but it prevents a bad shortcut. If we collapse
the two, the runtime might execute a row because the idea of the helper is
known, even though the actual callable helper path has not been proven in that
context.

So day/night routing is allowed only through the translated helper contract.
When the runtime has a current date, it can decide the route itself. When it does
not, it asks for calendar information instead of guessing.

In practice, a paired route behaves like a tiny predicate:

```text
if is_daytime(current_date):
    E48A = 0009
else:
    E48A = 000A
```

The exact implementation is more careful than that, because some routes also
advance time or use a helper result supplied by a test/probe harness. But this
is the important semantic: day/night is not a cosmetic skin. It can choose the
next owner state.

## Services Are Boundaries, Not Missing Menus

The marketplace is a good example of another important mechanic.

Several marketplace rows do not simply move to another navigation state. They
enter service bodies: merchants, foreign traders, pharmacists, banking offices,
Hanseatic services, and the Leihhaus. Those are downstream systems. They may
open shop logic, banking logic, inventory logic, or special service behavior.

The clean city runtime does not pretend those are already solved city routes. It
marks them as service boundaries.

That is valuable because it lets the city be playable without lying about the
systems behind it. The city can say, "this row enters a service body," and the
future service work can pick up from a named boundary instead of trying to
reverse-engineer from a vague click.

## The Stop Signs Are Part of the Model

The current city system has a healthy number of explicit stop signs.

Some visible rows still have no clean runtime contract. These include ordinary
player-facing places like the fortress, churches, guilds, inn, docks, grove,
night side-street destinations, gate-exit actions, political discussion rows,
and special-services information rows.

Some rows have original bytes that name a target state, but the target owner is
not yet promoted. Those become blocked targets. The runtime knows the named
state value, but it refuses to execute it as a gameplay owner.

Some target entries are even trickier. A captured resident window may contain
status writes, handler-table writes, or plausible-looking code, but the routed
address might land in a tail-like fragment, skip a nearby prologue, or even sit
inside another instruction. Those are not valid clean owner entries until the
callable entry and runtime context are proven.

The rule is simple:

```text
Bytes can prove bytes.
Only a valid owner/context contract proves gameplay behavior.
```

That rule has saved us from several stale interpretations.

## Internal Latches Are Not Public States

Another subtle correction is the distinction between public city states and
internal latch values.

Some owner bodies write values that look like states near real menu-publication
code. Two current examples are `006F` and `00AF`. They are real values. They are
not fake. But the current evidence classifies them as internal latch results,
not clean dispatch-owner states.

That means the runtime must not add public city routines for them just because
they appear near card publication code. Future evidence may promote them, but
promotion needs an actual owner dispatch entry, not just a latch write.

This is exactly the sort of distinction that makes reverse engineering feel slow
in the moment and saves weeks later.

## What the Runtime Now Does

The city resolver has a deliberately small vocabulary.

It can apply fixed state writes. It can apply deferred writes. It can resolve
day/night routes when it has the calendar context. It can restore previous or
context state. It can stop at service boundaries. It can ask for helper results.
It can report a blocked gap.

That is all it should do.

The resolver is not a second reverse-engineering engine. It is not there to
infer the city from text. It consumes the recovered owner/row contract and gives
the host a clean answer:

```text
advanced
deferred
service boundary
needs helper
needs calendar
blocked
```

Those outcomes are easy for a host to render and easy for future research to
improve. They also preserve uncertainty in a useful form. A blocked row is not
dead code. It is a named promise: "we know where the wall is."

A host does not need to know how the original selected-row code was recovered.
It receives a result kind and a next frame:

```text
Advanced        -> display the next city state
Deferred        -> display next state and preserve E7D8
ServiceBoundary -> hand off to a downstream service subsystem
NeedsHelper     -> ask for a helper result before continuing
NeedsCalendar   -> provide date/time before continuing
Blocked         -> show/debug a known unresolved boundary
```

That small vocabulary is also what makes the city runtime portable. SDL, Unity,
or a diagnostic host can consume the same contract without inheriting DOS memory
management or overlay loading as gameplay architecture.

## The Current Balance

The first-slice route coverage is complete for the required playable spine. That
is the good news.

The full visible-option surface is larger. It currently contains many rows whose
text is known but whose clean selected-row contract is not yet promoted. That is
not bad news. It is a map of the remaining work.

The project is now in a better phase: not "what is city navigation?" but "which
specific row, owner, helper, service, or target boundary should we promote
next?"

That is a much sharper question.

## What Comes Next

The next useful work should be row-sized.

Pick one visible missing row. Prove its owner. Prove its status producer. Prove
or classify its selected-row outcome. If it writes `E48A`, promote the route
only when the target owner is known. If it enters a service body, name the
boundary. If it uses a helper, either translate the helper or keep the row as
helper-needed. If it lands on a suspect target entry, keep it blocked.

The highest-value targets are the places ordinary players expect to use:
fortress, churches, guilds, inns, docks, grove, night side-street parity, gate
exit attempts, and special-services rows.

There are also a couple of known hard questions still waiting for focused
runtime evidence: one around the review-only paired-state helper callsite, and
one around the live selector path after a state-0024 return. Those should be
answered with narrow probes, not broad wandering.

## Closing Thought

City navigation used to look like a menu problem.

It is not.

It is a little state machine wrapped in a card renderer, a visibility producer,
a row-handler table, a service dispatcher, a day/night query, and a handful of
remembered-state latches.

The good news is that the machine is no longer a fog. We can walk a meaningful
first slice of it. We can say which rows are real, which rows are visible, which
rows enter services, and which rows must stop.

That is the right kind of progress for this project: not a larger guess, but a
cleaner conversation with the original game.
