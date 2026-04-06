---
title: "Devlog #006 - When the AI Catches Its Own Mistakes"
date: 2026-04-02
tags: ["devlog", "reverse-engineering", "darklands", "character-struct"]
description: "The agent corrects a major misidentification from a previous session and maps the in-memory character layout."
summary: "The agent corrects a major misidentification from a previous session and maps the in-memory character layout."
---

_Published April 2, 2026_

One of the questions people ask about AI-assisted reverse engineering is whether the model
can be trusted to stay accurate across sessions. Today's session is a useful data point,
because the agent caught a significant mistake it had made in a previous run, and corrected
the record before it could propagate further.

---

## The Misidentification

In an earlier session, the agent identified function `0x1873a` as `party_add_member`, the
routine that adds a new character to your adventuring party. The reasoning looked plausible
at the time: the function iterates an array of slots, parses a sequence of single-character
tokens ('r', 'w', 'a', 'b', 't', '+'), and increments a counter at `0x77b6`. The agent
labelled those characters as "class codes" for party members and filed the finding in the
knowledge base.

This session, the agent went back to that function for a different reason, it was trying to
cross-reference known Borland C runtime patterns, and the context clicked differently.
Those characters are not class codes. They are standard C file mode string characters:
'r' = read, 'w' = write, 'a' = append, '+' = update, 'b' = binary, 't' = text. The
function is `crt_fdopen`, the Borland runtime's file-open implementation.

The same correction applied to a nearby function. `0x17c82`, previously labelled
`find_free_char_slot`, is actually `crt_find_free_file_slot`, it scans the C runtime's
internal FILE struct array looking for an unused descriptor. The globals the agent had
attributed to party tracking (`0x77b8`, `0x77b6`, `0x7767`) are CRT internals: the FILE
array pointer, the open file count, and the maximum descriptor count respectively. None of
them have anything to do with the party.

The real `party_add_member` is still unidentified.

---

## Why This Happens

This kind of misidentification is an inherent risk in AI-assisted reverse engineering.
The model reasons about functions by pattern-matching their structure against things it
already knows. A function that iterates an array of fixed-size slots and parses character
tokens looks, at surface level, like it could be many things. If the model's working
hypothesis at the time is "find the party management code", it will weight that
interpretation more heavily.

The correction happened because the agent re-examined the function from a different angle.
It already had detailed notes about the Borland CRT layout, file descriptors, the fopen
family, the FILE struct array. When it tried to reconcile those notes with the surrounding
code, the match was unambiguous. CRT file modes, not party classes.

This is one argument for the approach we're taking: keeping a structured knowledge base
that the agent reads back on every session, rather than relying on the model's memory of
what it concluded previously. The prior findings became evidence to reason against, not
just conclusions to accept.

The lesson for anyone doing similar work: treat any AI-generated label as provisional until
it has been cross-referenced against at least two independent lines of evidence. One
pattern match is a hypothesis. Two independent matches start to look like a finding.

---

## The Character Hot-Slot Array

On a more productive note, the session produced a cleaner picture of how the game tracks
characters in memory during play.

There is a "hot-slot" array at `0x9C00`: five slots, each `0x80` (128) bytes, one per
party member. These are the active, in-use representations of your characters while the
game is running.

Within each slot, two fields are of particular interest:

- **Offset +0x65**, the character's current action or state. `0` means idle. `0x400`
  means in-combat. The main loop reads this to determine which characters need processing
  after each state transition.
- **Offset +0x69**, an RTLink overlay load state byte. `0` means the character's overlay
  data is already loaded. `3` means it needs to be loaded. `5` means skip. After every
  state handler returns, `game_main_loop` scans this field for each slot and calls the
  overlay loader for any character marked `3`.

Running alongside these slots, not embedded in them, but indexed in parallel by character
number, are three flat byte arrays:

- `0x9064 + index`, health or presence flag
- `0xa3d8 + index`, combat binding status
- `0xa6c4 + index`, combat condition flags (unconscious, down, dead, and similar states)

The parallel array pattern is consistent with what we already knew about the entity status
block from the previous session. The game keeps high-frequency, per-tick data in tight,
cache-friendly flat arrays rather than embedded in larger structs.

---

## The Full Character Struct Is Still Elsewhere

The important implication of the 128-byte slot size: these hot slots cannot contain the
full character record.

The save file analysis established that each character's persistent data is `0x22a` (554)
bytes, name, attributes, skills, equipment, inventory. That does not fit in 128 bytes.
The hot-slot holds only the runtime bookkeeping the game loop needs to operate moment to
moment. The full struct lives somewhere else in memory, at an address the agent has not
yet pinned down.

---

## What's Next

Two clear priorities for the next session:

1. Find the real `party_add_member`. Now that the CRT file-management functions are
   correctly identified and removed from consideration, the search space for genuine
   party management code is narrower.

2. Locate the base address of the full `0x22a`-byte character struct in memory. The hot
   slots at `0x9C00` reference or point to it, following those references is the most
   direct path. Once the base address is confirmed, the in-memory struct layout can be
   cross-referenced against the save file layout to validate both.

Progress is not always a straight line. Sometimes a session's most valuable output is
finding out that last session's output was wrong. That still counts.
