---
title: "025 - DARK: A Workbench for Darklands Data"
date: 2026-04-19
summary: "A single tool that brings together years of community format research: browse save games, enemies, cities, items, dialog trees, images, fonts, and archives — all in one place, on a modern system."
---

## Standing on Other People's Work

Before describing what DARK does, it is worth being clear about where it comes from.

Most of Darklands' file formats were documented years ago by a small group of dedicated researchers, primarily working in and around the Darklands Yahoo Group. Merle, Joel "Quadko" McIntyre, and others spent real time reversing binary structures, writing format specifications, and building tools — largely without automated help, largely because they cared about the game. The XML specifications at wallace.net are the canonical record of that work and are still the reference source for most of what this project understands.

That community also produced tools: save editors, archive extractors, map viewers. Some of them still work perfectly. Some have grown harder to run on modern systems. And they were always separate — open one to edit a save, a different one to look inside a catalog, something else for images.

DARK's starting point is that body of existing knowledge. The format library underneath it is built on those same XML specs. The goal is not to redo what was done, but to gather it in one place, make it run reliably today, and extend it into the areas where the original documentation ran out.

## What the Tool Is

DARK — Darklands Authoring & Resource Kit — is a desktop application that reads Darklands game files directly from a standard installation and presents them in a single workbench. You point it at a game folder and everything becomes accessible from one interface, without installing anything else.

The sidebar organises everything into seven sections.

**Save Games.** Any save file opens into a structured view of the party: all seven attributes with their current and maximum values, all 19 skills laid out with their names rather than raw numbers, equipment in each slot, inventory contents, and the party-level state — currency split across florins, groschens, and pfenniges, the bank note balance, fame, and the Philosopher's Stone quality. Every field is editable and saves back to the original file. The tool knows the format well enough to show when a value is out of expected range.

**Enemies.** The enemy data from `DARKLAND.ENM` decoded into a navigable list. All 71 enemy types with their full stat blocks — base attributes, skill ratings, weapon assignments, armor and shield item codes with quality values, palette chunk references, and variant counts. The 82 named enemies reference their type and show their name strings. This is the data that drives every combat encounter in the game, made readable without a hex editor.

**Locations.** All 414 world locations with icon type, map coordinates, city size, and name. The location list and city database are presented together so cross-referencing between `DARKLAND.LOC` and `DARKLAND.CTY` is straightforward. The 92 city records include all their internal location names — inn, cathedral, market, fortress, kloster, university — building-presence flags, dock destination links, and the nine shop quality ratings.

**World Map.** The full Darklands wilderness map rendered as a navigable image. The underlying `DARKLAND.MAP` is a 328×932 hex-grid of RLE-encoded tile data, drawing from two PIC tile palettes. The viewer decodes that data and renders the complete map — every terrain type, every river, every coastline — at a scale where you can actually see the geography. Panning and zooming let you locate specific areas, and clicking tiles shows the raw tile data behind them. This is one of the more useful surfaces for anyone working on the world map system, because seeing the full map in one view is something the original game never offered.

**Text.** The `DARKLAND.MSG` dialog files contain the branching conversation trees that appear throughout the game — city menus, quest dialogues, encounter scripts. The tool renders these as structured trees with all branches and option text visible, making it possible to read the full content of a dialog without guessing which option leads where. City descriptions from `DARKLAND.DSC` are shown alongside their corresponding city records for easy comparison.

**Images.** PIC sprite sheets decoded and displayed with correct palette mapping — the tool understands the standard VGA palette and applies it so images look as they would in the game. Tactical combat sprites from the IMC format come with enemy palette chunk overlays from `ENEMYPAL.DAT`, so each enemy type renders in its actual in-game colours rather than a default palette that makes everything look wrong.

**Fonts.** The game's bitmap font sets from `FONTS.FNT` and `FONTS.UTL` rendered glyph by glyph in an editable grid. Each glyph can be inspected and modified. For anyone working on a port or a translation, this is where the character set lives.

**Archive.** A browser for the CAT archive format — the container that holds most of the game's packed assets. The directory of any archive opens as a file list; selecting an entry previews it inline (PIC images render as images, everything else appears in a hex view with decoded offsets); individual files can be extracted to disk. The archives covered include the battle sprite catalogs, the enemy info catalog, the message file archive, the map tile catalog, and the extensionless archives like `BC` and `LCASTLE`.

**Research.** The forward-looking section of the tool. Viewers for image bank formats, a workbench for the PAN presentation format used in the intro sequences, a standalone DRLE decompressor for testing compressed streams in isolation, and general-purpose hex viewers for data structures that are still being decoded. These are surfaces for ongoing analysis work, not finished features.

## A Validation Layer

One feature worth mentioning separately: after loading a game folder, the tool can run a validation pass across the world data. It checks city dock destinations for consistency, verifies location reference integrity, checks enemy item assignments against the item table, validates palette range bounds, and counts dialog option references. The report is navigable — clicking a finding takes you to the relevant record. It is useful both for catching format decode errors and for finding quirks in the original data.

## Download

**[PLACEHOLDER_LINK]**

The tool is a community project, developed openly alongside the reverse engineering work documented in these devlogs.
