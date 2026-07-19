---
title: "Devlog #038 - From MSGFILES to a Clickable Screen"
date: 2026-07-19T08:30:00
summary: "A Darklands city screen now travels through the original loading, text, token, layout, presentation, acknowledgement, and input machinery. The result is an exact headless replay rather than a modern menu made to look similar."
---

A city screen in Darklands looks simple enough.

There is a picture, a paragraph, and a list of things the player can do. Move
the pointer over a row, click it, and the game goes somewhere else. From the
outside, it resembles a menu that could be rebuilt with a few strings and
buttons.

From the inside, it is a long conversation between the file loader, the text
system, the renderer, the mouse and keyboard controller, and the original owner
of the screen.

The last devlog described Darklays, the workbench we built to recover those
original code units. This time, the subject is what happened when enough of
those units were connected to make a city card appear and respond to input.

It is the difference between displaying the right words and reconstructing the
machine that displayed them.

## MSG Files Are Not Menus

Most of the game's long-form text lives in the `MSGFILES` archive. Individual
entries such as `$CITYS00.MSG`, `$CITYN00.MSG`, or `$OFFIC00.MSG` contain cards
with paragraphs and option text.

That makes the archive look like a menu database, but it is not one.

The file can tell us that a row says "the marketplace" or "ask about the
city." It cannot tell us whether that row is currently visible, whether it is
disabled, which handler is installed behind it, what the handler changes, or
which card should be shown afterward. Those decisions belong to executable
owner code.

The new model therefore keeps the parser deliberately modest. It exposes the
archive entries, card boundaries, text bytes, and fields that have been
confirmed from the format. It does not group rows into modern actions or attach
destinations inferred from their labels.

The data says what is available to display. The original code says what it
means in this moment.

## Loading a Card the DOS Way

Before Darklands can display a card, it has to find the resource in the archive.
The path crosses the original file-provider and catalog machinery: construct
the name, open the archive, locate the entry, read its payload, close the file,
and scan the card structure.

The modern engine could have replaced all of that with a convenient file API
and returned a ready-made object. That would reproduce the result, but it would
skip the code we are trying to preserve.

Instead, the reconstructed loader follows the original normal path. DOS file
operations sit behind a narrow host boundary, but the sequence, inputs, return
values, buffer writes, and failure decisions remain owned by the translated
Darklands routines.

This boundary is useful beyond historical neatness. The original code does not
always ask for a complete file. It carries its own provider state, offsets,
catalog information, and scratch buffers. Replaying those operations exposes
assumptions that disappear if the host simply hands Core a parsed card.

The result is a scanner-backed data surface. It can load and identify the card
the way the original game did without pretending that the resource file itself
contains the controller.

## Text Is Built, Not Merely Read

The bytes in an MSG card are not necessarily the final sentence shown to the
player.

Darklands uses `$` tokens to insert names, money, places, directions, party
information, dates, and other pieces of live state. Some tokens select a value
from a table. Some format signed or unsigned numbers. Some call helpers that
walk party or event records. A token may also expand into text containing
another token, so the transformation is not always a single substitution.

Earlier in the project, we understood many of these tokens as a format feature.
The new reconstruction follows the executable dispatcher that implements them.
Its 73 selector entries are tracked individually, along with the helpers and
state each path requires. A selector whose dependencies are not ready stops at
the original boundary instead of producing a plausible replacement string.

This work also corrected several attractive but false interpretations.
Encoded values that looked like procedure targets turned out to be table data.
Two selectors that produced similar text could still reach different helper
families. A token observed with one party could not be treated as a constant
because its owner was reading live character or world data.

By the time the text reaches the presentation routines, it has travelled
through the same broad stages as the DOS game:

```text
raw MSG bytes
-> text transform
-> token dispatch and expansion
-> final control-byte stream
```

Only then is it ready to be measured.

## Measuring Text Like the Original

Darklands does not hand its strings to a modern font-layout library. It walks
the text stream, interprets its control bytes, measures characters through the
MGRAPHIC routines, wraps lines, and chooses left, centered, or right placement.

This area produced some of the least glamorous and most necessary
reconstruction work.

The text scanner has to preserve 16-bit arithmetic and pointer movement. It has
to know when a byte changes the drawing state rather than producing a glyph. It
has to carry the current width across a possible wrap and publish the exact
placement values the next routine consumes.

A shortcut here can look correct for one English paragraph and still fail on a
different card, a substituted name, or the German edition. Reconstructing the
measurement path means the renderer receives the same line decisions the game
would have made, rather than a modern approximation that happens to fit the
first screenshot.

The current resident text routine covers scanning, control interpretation,
wrapping, state publication, and left, center, and right placement. Hardware
drawing remains behind a typed boundary, but the decisions that determine what
and where to draw belong to the engine.

## Publishing Rows Is a Separate Job

Once the paragraph has been prepared, the screen owner still has to publish the
options.

There are three meaningful row states:

```text
hidden
displayed and selectable
displayed but not selectable
```

These states are not interchangeable. A disabled row may still be drawn. A
hidden row must not participate in pointer scanning. A selectable row needs an
owner handler, and the row number returned by the input controller is only
meaningful inside the owner that installed it.

The reconstructed publication machinery preserves the raw status bytes and far
handler pointers used by the original. It also preserves the order in which the
screen is prepared: palette work, video-memory operations, row publication,
acknowledgement, and the final input phase are not collapsed into one host call.

The host is allowed to provide a mouse, keyboard, and display. It is not allowed
to decide which row the pointer means or what that row does.

## Input Without Modern Meaning

The original controller receives low-level input. Keyboard choices arrive as
BIOS-style words. Mouse requests return raw button state and coordinates. The
controller scans the published row geometry, updates hover state, redraws when
the selection changes, waits for a release, and eventually returns the selected
row value.

The headless host supplies those raw responses in a fixed order. It does not
send a command such as `SelectCitySquareRowZero`. It says, in effect, "the
pointer is here," "the button is down," or "the Enter key produced `1C0D`."
The reconstructed controller decides what those facts mean.

That difference is essential for testing. A semantic command can jump over a
bad hit box, missing acknowledgement, or incorrect row-status byte. Raw input
has to survive the same logic the original game used.

## Replaying the Road to CITYS00

To test the complete chain without depending on SDL, we built a headless replay
around a carefully bounded runtime checkpoint.

The starting fixture represents the original game on the main-street screen. It
contains the exact registers and memory regions needed before the next gate,
along with hashes that tie it to the original executable and resources. It is
not a full DOS memory snapshot, and uncaptured areas are not filled with helpful
zeros.

The input script is equally small: move the pointer, click, move it away, and
send Enter when acknowledgement is required. It contains inputs only. There is
no recorded final memory state for the candidate engine to copy.

The golden run established a stable checkpoint on `$CITYS00.MSG` card 0. At
that checkpoint, seven rows are visible and selectable, their raw status bytes
are published, and ten far handler cells have been installed.

Reaching it required more than loading a string. The candidate replay passed
through the resource, token, layout, presentation, acknowledgement, and input
owners. It performed 11,142 byte writes, issued the expected MGRAPHIC sequence,
consumed two mouse responses and two BIOS Enter words, captured the palette
twice, and rewrote the emulated A000 video surface twice.

There were no uncaptured platform calls and no writes injected after the replay
started.

The final checkpoint matched.

## Why the Headless Result Matters

This is not yet a production city screen in the SDL host. The replay starts at a
controlled original checkpoint, and several larger owners are executable only
through certified paths. Alternative branches still stop where their evidence
runs out.

That limitation is useful. It tells us exactly what has been demonstrated:

```text
given this original starting state
and these raw inputs,
the reconstructed units produce this original screen state
without a modern menu implementation or injected result
```

The same MSG machinery is not limited to the city square. It is shared by
services, notices, conversations, selection lists, and result cards across the
game. Every recovered token helper, input routine, or presentation owner can
therefore improve more than one screen.

More importantly, we now have a way to test those screens as sequences of
original decisions rather than collections of expected strings.

The next question was what happened after the screen became clickable.

The first visible row on `$CITYS00.MSG` did much more than change the message
file. It advanced the game clock, crossed the central state dispatcher, loaded
another city card, entered an office owner, displayed a curfew notice, and
returned to the previous city state.

That route is the subject of the next devlog.
