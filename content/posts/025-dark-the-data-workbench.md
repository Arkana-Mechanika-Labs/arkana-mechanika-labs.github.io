---
title: "025 - DARK: A Workbench for Darklands Data"
date: 2026-04-19
summary: "A single tool that brings together years of community format research: browse save games, enemies, cities, items, dialog trees, images, fonts, and archives — with new coverage for formats that were still undocumented."
---

## Standing on Other People's Work

Before describing what DARK does, it is worth being clear about where it comes from.

Most of Darklands' file formats were documented years ago by a small group of dedicated researchers, primarily working in and around the Darklands Yahoo Group. Merle, Joel "Quadko" McIntyre, and others spent real time reversing binary structures, writing format specifications, and building tools — largely without automated help, largely because they cared about the game. The XML specifications at wallace.net are the canonical record of that work and are still the reference source for most of what this project understands.

That community also produced tools. Save editors, archive extractors, map viewers — the pieces existed. Some of them still work perfectly. Some have grown harder to run on modern systems. And they were always separate: open one to edit a save, a different one to look inside a catalog, something else for images.

DARK's starting point is that body of existing knowledge. The format library underneath it is built on those same XML specs. The goal is not to redo what was done, but to bring it together and extend it in the areas where the original documentation ran out.

## What the Tool Is

DARK — Darklands Authoring & Resource Kit — is a desktop application that reads Darklands game files from a standard installation and presents them in a single tabbed workbench. You point it at a game folder and everything is available from one interface.

The seven sections of the sidebar cover the full range of the game's data.

**Save Games.** Any save file opens into a full character view: all seven attributes (current and maximum), all 19 skills — 7 weapon types plus 12 non-combat — equipment, inventory, and party-level state including currency and fame. Fields are editable and the result can be saved back.

**Data.** The world data files in human-readable form. Enemies: 71 types and 82 named encounters, with attributes, weapon assignments, armor, and palette references decoded. Locations: all 414 world locations with icon type, coordinates, and names. Items, saints, and alchemical formulae from the item list. An interactive world map rendered from its RLE tile data. And the full city database: all 92 cities with their named internal locations, building flags, dock connections, and shop quality ratings.

**Text.** The message files exposed as readable dialog trees with all branches and option text visible. City descriptions alongside the corresponding city records for cross-reference.

**Images.** PIC sprite sheets decoded and displayed with correct palette mapping. Tactical combat sprites from the IMC format, with enemy palette chunk overlays applied so they appear in the colours the game would show.

**Fonts.** The game's bitmap font sets rendered glyph by glyph. Editing is supported — for anyone working on a port or a translation.

**Archive.** A browser for the CAT archive format that underlies most of the game's asset storage. Navigate the directory, preview entries inline (images render as images, everything else shows in a hex view), and extract files individually.

**Research.** The forward edge of the project. Viewers for the named image-bank format, a workbench for the PAN presentation format, a standalone DRLE decompressor, and general-purpose hex viewers for data structures that are still being decoded. These are not finished tools — they are surfaces for ongoing analysis work.

## The Formats the Community Did Not Document

The well-documented formats are well-served by the existing tools. Where DARK adds something genuinely new is in the formats that were not previously understood.

The PAN format — the animated scene container used for the entire intro sequence — had no public documentation before this project. The format, its blit bytecode grammar, and the player architecture in the executable were all recovered through runtime tracing of the live DOS binary. The same applies to the DRLE compression used inside PAN files, to the BANNER.DAT startup resource, to the COMMONSP.IMG sprite bank and its named subrecord structure, and to the late OPENING2 pipeline that drives animated elements through a reused overlay resolver.

The workbench's Research section is where that work is being turned into tooling. It is a work in progress by definition.

## A Validation Layer

One feature worth calling out specifically: the validation report. After loading a game folder, the tool can run a consistency check across the loaded world data — verifying city dock destinations, location references, enemy item assignments, palette range bounds, and dialog option counts. When the format decode is wrong somewhere, the validator is often what surfaces it first.

## Download

**[PLACEHOLDER_LINK]**

The tool is a community project, developed openly alongside the broader reverse engineering work documented in these devlogs.
