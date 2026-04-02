---
title: "Devlog #003 — The Knowledge Base"
date: 2026-03-20
tags: ["darklands", "reverse-engineering", "file-formats", "community"]
description: "Community researchers documented Darklands file formats in the mid-2000s with hex editors and patience. We found it, verified it, and built on it."
summary: "Community researchers documented Darklands file formats in the mid-2000s with hex editors and patience. We found it, verified it, and built on it."
---

One of the things I didn't expect when I started this project was how much prior work already existed.

Darklands has a small but devoted community that has been quietly reverse engineering it for decades. Not with AI tools — with hex editors, patience, and the kind of obsessive focus that comes from really loving a game that no one else talks about anymore. A researcher going by the name "Merle" had a now-defunct page "Reversing Darklands: an analysis of Darklands game data files" covering almost every file format the game uses. Others contributed code, notes, and corrections. Most of this work dates from the mid-2000s.

It was sitting there, organized and documented, like a buried treasure. The `DARKLANDS_KB` is my local copy of all of it — annotated, extended, and cross-referenced against what the agent finds in the executable.

---

## What The Community Already Knew

The community had already documented the game's file formats with impressive precision. Here's what was confirmed:

**The catalog system.** Darklands doesn't use one big archive file — it uses a family of catalog files (`.CAT` files, plus a few extensionless ones like `BC`, `LCASTLE`, and `MSGFILES`). Each catalog is a flat directory of 24-byte entries followed by file data. The entry structure: 12 bytes of filename (8.3 format, null-padded), 4 bytes of timestamp, 4 bytes of length, 4 bytes of offset. Simple and solid.

The specific catalogs: `A00C.CAT` holds the alchemist battle sprites. `C00C.CAT` the cleric. `F01C.CAT` the male fighter, `F60C.CAT` the female fighter. `E00C.CAT` and `M00C.CAT` cover human and non-human enemies respectively. `MSGFILES` contains all the game's text menus and situation descriptions. `IMAPS.CAT` has the city, mine, outdoor, and castle tile graphics.

**The wilderness map.** `DARKLAND.MAP` uses a row-based RLE compression scheme. Each byte encodes 1–7 identical tiles: 3 bits for repeat count, 1 bit for which tile palette, and 4 bits for the tile row within that palette. The map dimensions are stored big-endian — unusual for Darklands, which is otherwise little-endian throughout. The grid uses a hex offset: odd rows are shifted half a tile to the right.

**The save file.** This is the big one. The `dksave*.sav` format is fully documented. The file starts with world state (current location, date, party money, reputation, current map coordinates, which menu/screen you're on). At offset `0xEF`: how many characters are in your party and how many total characters exist. At `0x189`: the character array, each record exactly **554 bytes** (0x22A).

The character struct is more complicated than I expected. Fields are not laid out sequentially — there are gaps and unknowns throughout. The names aren't at the start: `full_name` is at offset `+0x25`, `short_name` at `+0x3E`. Equipment type and quality bytes for each slot are scattered across the struct: `equip_missile_type` is at `+0x22` but `equip_missile_q` (the quality of the same weapon) is at `+0x5A`, 56 bytes later. The attribute set is at `+0x5D`, skills at `+0x6B`, and the items array at `+0xAA`.

**Enemy definitions.** `DARKLAND.ENM` has 71 enemy type definitions (204 bytes each) and 82 named individual enemies. Each type includes an `image_group` code, full attribute and skill sets, equipment, and palette information for combat rendering.

**Item data.** `DARKLAND.LST` has the master list of 200 item slots, 136 saint definitions, and 66 alchemical formula names. Each item definition is 46 bytes with 5 separate flag bitmasks.

**Alchemy.** `DARKLAND.ALC` has the descriptions, base difficulty, risk factor, and up to 5 ingredients for each of the 66 formulae.

---

## What This Means For Phase 2

Having confirmed file formats changes what Phase 2 looks like. Instead of decompiling a function and guessing what the struct fields mean, the agent can read the character save record spec and immediately know that the function accessing `[SI + 0x6B]` is reading the first skill (Edged Weapon). Instead of inferring the catalog format from the resource loading code, we can confirm it and move on.

The KB is now directly referenced in the agent's priorities file. Before each session, it reads the canonical XML specs as ground truth. Anything the decompilation finds gets cross-checked against what the community already documented.

---

## A Note On Accuracy

Working with 30-year-old code analyzed by an AI, cross-referenced against 20-year-old community notes — accuracy has to be earned carefully. Early in this project I made the mistake of writing documentation from inference rather than from sources. Wrong filenames, wrong struct layouts, wrong field interpretations. I've been correcting those as they're caught.

The rule now: nothing goes into the public docs unless it's sourced. Either from the canonical XML specs, or from the decompiled code, or from both agreeing. "Probably" and "likely" are clearly marked as such. If something is unknown, it says unknown.

---

*Next: Phase 2 begins — going deeper into the game logic.*
