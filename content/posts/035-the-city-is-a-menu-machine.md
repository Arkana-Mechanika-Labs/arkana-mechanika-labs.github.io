---
title: "Devlog #035 - The City Is a Menu Machine"
date: 2026-06-17T09:00:00
summary: "City navigation looked like a list of places connected by routes. It is not. The original game runs it through a shared menu machine with status rules, handlers, side effects, random gates, services, and card selection."
---

City navigation looked, at first, like one of the simpler parts of Darklands.

A city has streets. Streets lead to buildings. Buildings have exits. The game
shows a paragraph of text, a picture, and a list of options. Surely the job is to
map each visible row to the next screen.

That was the wrong model.

The last several weeks have been spent replacing that model with one much closer
to how the original game actually works. The result is less flashy than a new
combat screen or a new editor, but it is one of the more important architectural
turns in the restoration project so far: city navigation is no longer being
treated as a hand-written table of routes. It is now being reconstructed as one
client of the original game's shared message-menu system.

## Rows Are Not Routes

The original city screens are stored in MSG files. These files contain text and
option rows, but they do not, by themselves, decide what happens when the player
chooses a row.

That decision belongs to owner code.

An owner is a routine in the original executable that prepares a menu surface. It
chooses which MSG file to publish, which picture to pair with it, which card
inside the MSG file is active, which rows are visible, which rows are disabled,
and which handler each selectable row will call.

That last part is the trap. A row that exists in a MSG file is not necessarily a
row the player can see. A row that has a handler pointer is not necessarily
playable. A row that appears to lead to a destination might first run a service,
advance time, test the party's local reputation, scan active events, roll random
state, or prepare a later result card.

In other words, the option text is a label. The behavior is code.

This is why a simple "route table" kept breaking down. Some routes looked open
when the original hid them. Some destinations looked obvious from the text, but
the original reached a different card through a shared service path. Some
transitions worked visually while silently missing time advancement or other
state changes. A route table can describe where a click seems to go. It cannot
describe what the original engine did on the way.

## The MSG Menu VM

The project now models the city screens through a clean MSG Menu runtime.

The term "VM" here does not mean the original game used a virtual machine in a
modern scripting-language sense. It means the game has a repeatable menu
pipeline with a stable contract:

- owner code publishes a message key and picture stem;
- status slots decide which rows are hidden, disabled, or selectable;
- a renderer-facing mirror exposes those statuses to the menu driver;
- a handler table maps selected rows to owner-local code;
- the selected handler updates state, latches, time, random state, or enters a
  service boundary;
- the next owner opens the next menu surface.

That pipeline is shared by city navigation, result cards, selectors, saint
popups, and other message-driven situations. City navigation is not special. It
is one use of the same machine.

This was the important strategic shift. Instead of asking "where does this city
option go?", the reconstruction now asks:

What did the owner publish?
What status did it publish for this row?
Which handler did it publish?
What did that handler write?
Which helper or service did it call?
Which side effects happened before the next surface appeared?

Those questions are slower to answer, but they scale. Once a shared helper is
decoded, every row using that helper benefits.

## Clean Mode Replaces Legacy

Earlier city-navigation code had accumulated too many layers. Some came from
reasonable first attempts. Some came from runtime captures. Some came from
partial assembly reads. Some came from trying to make a screen playable before
the original mechanism was fully understood.

That is a dangerous place for a faithful reimplementation. It becomes hard to
tell whether a behavior comes from the original game or from a stale
reconstruction shortcut.

The current direction is stricter: clean mode is the real path. It consumes the
generated MSG menu specification and executes only behavior supported by original
evidence. If a row is known to be visible but the service behind it is not yet
decoded, clean mode returns a named boundary instead of guessing.

That can feel less playable in the short term, but it is much healthier. A named
boundary says: the original code goes here, and we know exactly which mechanism
is still missing. A guessed route says: the screen changed, and we hope the rest
does not matter.

The rest does matter.

## Side Effects Matter

One of the clearest examples was time.

Some city transitions in the original advance the clock. Moving through the
city, entering certain areas, taking a boat, waiting through a service result:
these are not just screen changes. The calendar helper can update the hour, roll
the day, scan active records, and reseed random state. That means a visually
correct route can still be wrong if the party information screen later shows the
wrong time, or if a scheduled event fails to trigger because time did not
advance.

The clean MSG menu model now treats side effects as part of row execution.
Before a row can be considered complete, the reconstruction must account for
what the original writes:

- route state and menu latches;
- active card index;
- time and calendar updates;
- random state;
- active-event maintenance;
- money or inventory changes;
- city and location record changes;
- result-card continuations.

Unknown side effects are no longer allowed to hide behind "the destination looks
right." They are either implemented, or the row remains a boundary with a
specific reason.

This led to a new class of audits. Runtime captures are compared against the
generated spec not just for the next MSG file, but for observed side-effect
deltas. If the original changes something and the clean runtime does not explain
it, the row is not complete.

## Evidence Instead of Memory

Another important change is organizational.

The research had become too scattered: assembly packages in one folder, runtime
captures in another, C# audits elsewhere, workbench sessions elsewhere, and too
many conclusions living only in conversation. That does not work for a project
with this much state.

The active reconstruction lane now acts as a
curated evidence lane rather than a dumping ground. It contains:

- the MSG menu ABI;
- owner contracts;
- service and helper contracts;
- side-effect audits;
- context predicate atlas;
- cutover readiness data;
- Ghidra synchronization notes;
- the generated implementation-facing spec consumed by C#.

Every generated row carries a readiness classification. Some rows execute
exactly. Some execute with runtime context. Some publish hidden or disabled
status. Some return a decoded RNG boundary. Some return a service boundary. The
point is not that everything is finished. The point is that every known row has
a reason attached to its current state.

That reason is evidence-backed, not inferred from screenshots or option text.

## Runtime Captures Have a Smaller Job

Runtime captures are still useful, but their role has changed.

At one stage, the project was using runtime captures too broadly: navigate to a
screen, click a row, see what happened, then try to reconcile it afterward. That
produced useful data, but it also risked turning runtime state into a general
rule. A capture taken in one city, on one day, with one party, one local
reputation score, one event table, and one amount of money is only a sample of
that context.

The new policy is static-first. Read the owner code. Decode the helper family.
Use runtime only to validate a precise hypothesis.

For example: "this handler should advance one hour before restoring the previous
menu state" is a good capture target. "click around the city and see what
happens" is not.

The project still built better recorder tools along the way, because those tools
help preserve evidence when a capture is needed. They record the current state,
message, picture, active card, row statuses, handler table, before/after state,
random state, and side-effect summaries. But the recorder is now a microscope,
not a fishing net.

## Ghidra as a Code-Truth Workspace

The Ghidra project has also been brought back into the loop.

Not every runtime capture belongs in Ghidra. Bulk-importing every session would
make the project noisy and less useful. What belongs there are distilled
code-truth facts: helper contracts, materialized owner blocks, confirmed
side-effect routines, and corrected interpretations of previously ambiguous
code.

Recent syncs added comments for the shared calendar helper, result-card
continuation helper, active-record maintenance, RNG core, RNG modulo wrapper, and
day/night helper family. The Ghidra project now records, for example, that the
calendar helper is not merely "advance time"; it also performs active-record
maintenance and reseeds random state, and clean execution is only safe when no
callback dispatch occurs.

Equally important: the sync process avoids inventing flat addresses for owner
blocks that have not been materialized and byte-verified. Ghidra is useful
because it is curated. It should stay that way.

## Where City Navigation Stands

The clean city navigation path is now substantially more honest than it was.

Core city surfaces such as main street, side streets, city square, church
district, cathedral, monastery, walls, gates, docks, business district, market,
and several service buildings are represented through the MSG menu spec. The
engine can publish content, row status, disabled rows, visible rows, and many
ordinary deterministic transitions from the spec rather than from legacy route
code.

The test suite has grown with the model. The current full test run is 966 tests,
and the MSG menu gates check that:

- truth-audit issues remain at zero;
- runtime snapshot review issues remain at zero;
- unknown atlas dependencies remain at zero;
- unmodeled runtime side-effect deltas remain at zero;
- stale C# quarantine rows remain at zero;
- embedded runtime resources match the generated clean-lane spec.

That last point matters. The C# runtime is not carrying a private truth. It
consumes generated resources from the clean research lane, and tests verify that
the embedded resources are synchronized.

There are still many boundaries. That is expected. Some city actions are not
routes at all; they are services. They involve prices, inventory, active events,
selector lists, result cards, scheduled records, reputation, random gates, or
future callbacks. Opening those rows without decoding the service would be a
step backward.

Recent work moved the Docks destination path forward significantly: the normal
money-success path and insufficient-money fallback are now much better modeled,
including travel time, money handling, result-card continuation, and the
remaining callback boundary. Other service families, such as fortress challenge
and sneak actions, have been decoded enough to expose their ordered branch
structure without pretending they are executable yet.

This is the pattern going forward: decode the shared mechanism once, then let
every row using it improve together.

## What This Buys

The visible result is modest: city navigation feels better, but many complicated
rows still stop at named boundaries.

The structural result is much larger.

The project now has a working way to talk about the original MSG menu system as
a real subsystem. It can distinguish a displayed row from a raw MSG row, a
handler pointer from a playable action, a route state write from a service
side effect, and a faithful boundary from an unfinished implementation.

That distinction is what makes continued progress possible. Without it, every
new mismatch would be another local mystery. With it, a mismatch becomes a
question inside a known machine:

Which owner published this surface?
Which predicate controlled this row?
Which helper supplied the branch?
Which side effect did we miss?
Which shared family does this belong to?

The city is still complicated. But it is no longer a fog of special cases.

It is a menu machine. And now the project has the beginnings of the machine's
specification.
