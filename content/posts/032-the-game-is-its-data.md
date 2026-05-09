---
title: "Devlog #032 - The Game Is Its Data"
date: 2026-05-04T09:00:00
summary: "Every file format the original game touches is an implicit specification. Understanding what Darklands does means understanding what those formats mean, and five of them opened up this month."
---

There is a temptation, when working on a project like this, to treat the game's
files as assets and the game's executable as the real subject. The executable is
where the logic lives, so the thinking goes. The data files are just content that
the logic consumes.

That is backwards.

The data files are Darklands. The executable exists to interpret them. And
understanding what the game actually does means reading those files the same way
the game does, with the same layout, the same assumptions, and the same
arithmetic.

Five formats opened up during the work covered by this and the following two
devlogs. Each one changed what the restoration project can model with confidence
rather than approximation.

## COMMONSP.IMG

The party creation screen shows character slots with a distinctive visual: a
bordered frame, a blue body, a narrow side strip, a top and bottom edge. The
surface-level question is where the game draws this frame. The right question is
where the source pixels come from.

The answer is surprising. `COMMONSP.IMG` is loaded at startup, before
`OPENDARK.DGT`, before any intro animation. Its load sits at sequence event 69
in a traced startup run. By the time the intro begins, the tile graphics are
already resident in memory.

The format is a container. It holds 14 sections of pre-rendered row-run art,
each addressed by a paragraph offset stored in the file header. The startup
loader reads the file into a temporary segment, calls an allocator to reserve a
resident block, copies the payload there, and writes 13 global pointers into
the game's data segment pointing at the individual section records. The
arithmetic from file offset to resident address is paragraph-based: add the
section's paragraph index to the base resident token and the section sits at
that segment address.

Four of these sections are the party slot base tiles: the frame edges and the
body fill that appear on the party creation screen. Runtime comparison confirms
the match byte-for-byte: the pixels that appear in a character slot on screen
are exactly the bytes from those four sections of `COMMONSP.IMG`, composited in
the order the original slot helper code specifies.

The tile container was loaded before the intro for a reason. The original game
needed those graphics in resident memory before the startup sequence finished.
Understanding this is not trivia. It determines where the reimplementation
sources the party slot art and how it models the startup install sequence.

## EVENTS.TMP

Darklands simulates time. The party trains, travels, and rests. Quests mature
and events come due. `EVENTS.TMP` is where that state lives between sessions.

The format: a two-byte count at offset zero, followed by that many fixed-stride
records of 48 bytes each. Within each record, four words carry the creation
timestamp and two groups of four words carry the scheduled comparison times, all
in hour, day, month, year order. A word near the end of each record distinguishes
deadline-bounded events from open-ended ones, a distinction that corresponds to
how the in-game display labels them.

This was confirmed against a real `EVENTS.TMP` file from an original install,
cross-referenced with a same-session memory log showing an event count that
matches the file exactly. The calendar advance routine in the original game reads
elapsed hours, wraps through a month-length table, and sweeps the event queue
for records that have crossed their due time. When one does, it dispatches to a
handler that can affect party slots, update location flags, and queue follow-up
events.

The event system is the game's simulation backbone. The file format is its
persistent representation. Neither can be approximated without breaking the
simulation logic that depends on them.

## LOCS.TMP and the Location Record

`LOCS.TMP` is the game's working location table during a session. A natural
assumption is that it is generated fresh on each new game from some internal
seed. The reality is simpler: it is a byte-exact copy of `DARKLAND.LOC` from the
game's data directory. The game reads the disk master at startup and writes a
working copy. The two files share the same 414 records at the same stride.

This matters for the restoration project because it tells us where the location
data comes from and what happens to it during a session. Any changes the game
makes during play go into `LOCS.TMP`. The disk master is never modified. Save
games capture the current `LOCS.TMP` state and restore it on load.

## The Save Format

The save game format is a layered snapshot of memory. The roster starts at a
fixed offset and occupies character-record-sized blocks at a confirmed stride.
The event queue begins at a computed offset, positioned immediately after the
last character record. Location state and the cache region follow at further
computed positions.

The Load Game path has been traced: it opens the selected save, reads the roster
records starting at the confirmed offset, reconstructs the working temp files
from the save data, and then hands control to the same party creation controller
entry that a new game uses. Two different entry paths, one shared temp-file
format, one shared controller.

This means the restoration project's model of the party creation screen works
for both new and loaded games. The distinction is upstream of the controller, in
how the temp files get built.

## The Music Format

The intro music and the main theme do not live in audio files. They live inside
the sound module as sequenced cue data.

Cue `0x0014` is the Create New World theme. It begins playing when the player
chooses Create New World from the start screen, dispatched from inside the party
creation overlay. Its playback model is now proven against a full original
hardware reference: 48 bytes of initial setup commands, then a loop of 7,288
bytes, repeated. The match covers all 30,119 bytes of the original MT-32 capture
through the end of the file.

`JUKEBOX.EXE`, included with the game, is a standalone cue frontend. It maps
human-readable song names to cue IDs and drives the same sound module the game
uses. It serves as a catalog of the full music library, with cue numbers that
correspond directly to the dispatch identifiers in the game code.

The implication for the restoration project is that the engine can reproduce not
just audio output but the exact sequence of hardware commands that produced it.
The source of truth is the cue data in the module, not a recording.

## Why Format Decoding Is the Reimplementation

A common framing treats format decoding as preparatory work: you decode the
formats, and then you build the game. This project's experience is that the
decoding and the building are the same work.

Every format decoded is a decision the original developers made that the
reimplementation has to respect. The tile container was pre-loaded for a
performance reason. The event record stride was chosen because the original code
iterates it by pointer arithmetic. The save format reflects what the game held
in memory at the moment of saving, in the order it was held.

A reimplementation that approximates its way past these formats ends up
faithfully replicating the appearance of the original while quietly substituting
different decisions underneath. The goal here is the original decisions. The
format is the specification. Reading it carefully is how the project stays honest
about what it knows.

The implementation questions raised by these formats, and how the engine models
them in C#, are the subject of [devlog #033](/posts/033-the-long-game-of-faithful-reimplementation/).
