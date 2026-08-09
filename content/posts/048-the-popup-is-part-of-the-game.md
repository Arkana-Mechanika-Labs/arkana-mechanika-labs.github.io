---
title: "Devlog #048 - The Popup Is Part of the Game"
date: 2026-08-09T08:00:00
summary: "Darklands' saint and potion choices are not modal menus pasted over MSG cards. Their hover lifecycle, candidate filtering, prayer controller, and character-sheet integration are now reconstructed from the original owners."
---

The most revealing interface work this week began with a correction.

On `$CITYT00.MSG`, rows such as “use an alchemical distraction” and “call upon
a saint” do not behave like ordinary buttons. Hovering the row opens a compact
choice window. Moving into that window lets the player inspect a potion or
saint. Moving elsewhere closes it. Clicking the parent row itself is not a
shortcut to the first candidate.

Our first implementation treated the popup as modal. It worked well enough to
select a potion, but it did not behave like Darklands. Returning to the original
record-43 input code exposed a much richer shared mechanism.

## Three Input Regions, Not One Modal Dialog

The original controller maintains three related regions:

1. the primary MSG row that owns the alternate choice;
2. the complete popup rectangle;
3. the smaller selectable rectangles published inside the popup.

When the pointer first reaches an `SNT` or `PTN` row, Darklands draws the popup
but keeps the primary row publication active. The row's horizontal hit extent
is temporarily extended to meet the popup. A later pointer sample inside the
popup swaps input to the alternate publication.

This permits direct movement from the owner row into the popup. Moving back to
the owner restores the primary publication without erasing the popup. Blank
space and disabled candidates inside the popup retain it. Only a pointer sample
outside both the popup and its retained owner closes the window and restores
the captured background.

There is no grace timer and no modern trajectory heuristic. The behavior comes
from the original rectangle tests and publication swaps.

The clean engine now models those states explicitly. The SDL frontend retains
the underlying MSG framebuffer, draws the original popup background and border,
uses the published row rectangles for hit testing, and keeps the parent row
non-clickable.

## The Candidate List Comes from the Party

The popup is not a static submenu.

The original selector walks active party members and builds candidate records
from their live data. For potions, it consults inventory and item definitions.
For saints, it consults the saints known by the party. Names and quantities come
from the original resources. Missing choices are omitted; visible-but-disabled
choices remain unselectable.

This also governs the parent row. If the selector cannot publish an applicable
candidate, the `SNT` or `PTN` action is disabled. We no longer present an active
“use a potion” row backed by an empty choice window.

The control streams used to compose candidate rows were recovered directly
from the executable. They include the party-name prefix, candidate-state
markers, item-name insertion, quantity wrapper, line endings, and active-slot
suffix. The clean renderer interprets those bytes instead of replacing them
with an invented English prompt.

## Potion Selection Rejoins the Real Owner

The first executable potion outcome is the candidate-zero path.

Selecting it publishes the original candidate remainder and party quotient,
copies the selected text and party slot into the owner scratch fields, and
rejoins `$CITYT00` through its record-53 callback. The callback presents card
13 over `PICS\explshn.PIC`. Only acknowledgement advances one hour and returns
to the deferred day-or-night city state.

The selected path does not decrement inventory because the certified original
slice contains no such mutation. Other potion callbacks remain closed at their
own boundaries rather than borrowing candidate zero's behavior.

## The Shared Saint Invocation Controller

Saint selection leads into another reusable original subsystem.

The `$CITYT00` owner supplies a saint and party context, then invokes the shared
prayer controller in mode 1. The controller displays the saint panel, permits
the player to spend more or less Divine Favor, recalculates the success chance,
and returns a result to the caller.

Cancel is caller-neutral. It does not contain a hidden “return to `$CITYT00`”
rule. The calling owner republishes its own card and acknowledgement phase.
That distinction matters because the same prayer controller is also used by
the character sheet.

For Saint Apollinarius, index `000Ch`, the confirmed path is now executable:

- the exact success threshold is calculated from the selected character;
- the original RNG sequence is consumed;
- Divine Favor is spent in the original order;
- the optional failure penalty and half-cost behavior are preserved;
- the selector-8 effect applies the decoded timed Strength and Endurance
  increases;
- success returns to `$CITYT00` card 8 and then the deferred city state;
- failure republishes the encounter card.

The remaining saint effects are still separate evidence targets. Sharing a
controller does not imply that every saint shares the same gameplay effect.

## Character Sheet Integration

The character sheet's Saints page now uses the same controller rather than a
second approximation.

Some saints require a target character; others do not. The original mode-0
path carries a target chooser where required and the `FFFFh` no-target sentinel
where it is not. The clean frontend follows that distinction. It does not ask
the player to choose a target merely because a generic popup component exists.

This work also closed several presentation details: the real saint descriptions
from `DARKLAND.SNT`, selector-chosen backgrounds, original menu geometry,
success and Divine Favor status fields, and the More/Less/Pray/Cancel input
rows.

## What Is Actually Implemented

This is now executable in the SDL development host:

- hover-driven, non-modal `SNT` and `PTN` alternate popups;
- party- and inventory-derived candidate publication;
- original popup geometry, background retention, disabled rows, and hitboxes;
- the certified potion candidate-zero outcome through card 13 and its one-hour
  continuation;
- shared saint invocation with live Divine Favor adjustment;
- Saint Apollinarius' confirmed success/failure path and timed effects;
- character-sheet saint selection and target handling where required.

Uncertified potion outcomes and the other saint-specific effects still stop at
their exact original boundaries. The important gain is larger than one tavern
encounter: we now possess the shared choice machinery that other MSG owners can
reuse.
