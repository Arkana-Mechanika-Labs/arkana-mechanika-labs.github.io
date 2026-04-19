---
title: "025 - DARK: A Workbench for Darklands Data"
date: 2026-04-20
summary: "All the reverse-engineered format knowledge, in one place: DARK (Darklands Authoring & Resource Kit) is a standalone desktop tool that lets you browse, inspect, and edit Darklands game data — save files, enemies, cities, items, dialog, images, fonts, and archives."
---

## The Problem With Having a Knowledge Base

The format work has been producing results for months. Save file layout. City structs with 19 named fields. Enemy attribute tables. CAT archive extraction. PIC image decoding. DRLE decompression. Dialog card trees. Font bitmaps.

All of this lives in markdown notes and Python scripts. It is useful for the rewrite. It is not useful for someone who just wants to open a save file and see what it contains.

So we built a tool.

## DARK

**DARK** — Darklands Authoring & Resource Kit — is a standalone Windows desktop application built on top of everything the format research has produced. Point it at your Darklands installation folder and it becomes a complete workbench for the game's data.

It is a Python/Qt6 application packaged as a self-contained `DarklandsBrowser.exe`. No installation. No Python required. Open the exe, set the path, start exploring.

> **Download:** [Releases page — link coming when 1.0 ships]([PLACEHOLDER_LINK])

---

## What Is In There

The sidebar organises everything into seven sections.

### Save Games

Load any `DKSAVE??.SAV` file and see the full state of the party. Characters with all seven attributes and all 19 skills (7 weapon + 12 non-combat), current and maximum values. Equipment slots. Inventory. Party-level state: florins, groschens, pfenniges, bank notes, fame, and the Philosopher's Stone. Edit any field and save back.

### Data

The world data files decoded into human-readable tables.

**Enemies** — all 71 enemy types and 82 named enemies. Attributes, skills, weapon types, armor and shield assignments, palette references, variant counts.

**Locations** — all 414 world locations with icon type, map coordinates, city size, and name.

**Items / Saints / Formulae** — from `DARKLAND.LST`. Item definitions with all five flag bitmasks decoded, weight, quality, and value. Saint names (full and short). Formula names.

**World Map** — an interactive viewer for `DARKLAND.MAP`. The 328×932 hex-grid wilderness map rendered from its RLE tile data and the two PIC tile palettes.

**Cities** — all 92 cities from `DARKLAND.CTY`. The full 19-field city struct: short name, full name, coordinates, dock connections, building-presence bitmask, shop quality ratings, all named locations within the city.

### Text

**Dialog Cards** — `DARKLAND.MSG` conversation trees with all branches and options, readable as structured text rather than a packed binary blob.

**Descriptions** — the 92 city descriptions from `DARKLAND.DSC`, 80 bytes each, cross-referenced with city order.

### Images

**PIC Images** — palette-indexed sprite sheets decoded and rendered. Palette-aware: the tool understands the standard VGA palette and displays images correctly.

**IMC Sprites** — tactical combat sprites with enemy palette overlay support. The palette-chunk system from `ENEMYPAL.DAT` is applied so sprites render in the colours the game would actually show.

### Fonts

The game's bitmap font sets from `FONTS.FNT` and `FONTS.UTL`, rendered glyph-by-glyph. Editable — if you want to patch font glyphs for a port or a mod, this is where you do it.

### Archive

A CAT archive browser for all the game's packed assets: `E00C.CAT`, `M00C.CAT`, `MSGFILES`, `EINFO.CAT`, and others. Navigate the directory, preview files inline (PIC images shown as images; everything else shown in a hex view), and extract individual entries to disk.

This is where the format RE work on the CAT archive structure — 24-byte directory entries, timestamp, length, offset — turns into something practical.

### Research

The forward-looking section. Tools for formats that are still being decoded:

- **IMG Banks** — viewer for the named image-bank format (`COMMONSP.IMG`, `BATTLEGR.IMG`, and their relatives).
- **PAN Sequences** — a workbench for `OPENING*.PAN` playback research.
- **DRLE Decompressor** — the DRLE decompressor exposed as a standalone tool; useful for testing individual compressed streams.
- **Miscellaneous** — additional research files and hex views for undocumented or partially-decoded data.

These are live research surfaces, not finished features. The point is to have the tooling close to the analysis.

---

## Under the Hood

DARK bundles a `darklands` Python package that contains all the format readers and writers accumulated over the project. The library includes:

- Readers for ENM, LOC, MSG, LST, SAV, IMC, ENEMYPAL, DRLE
- Format parsers for DSC, CTY, FNT, PIC
- CAT archive extraction
- World map writer
- LZW and RLE decompression

Every format the app shows was first documented in the KB, then implemented as a library reader, then surfaced in DARK. The tool is downstream of the RE work, not upstream of it.

---

## Validation

One of the more useful features for development work is the built-in validator. **View → Validation Report** runs a consistency check across the loaded world data:

- 92 cities cross-checked for dock destination validity
- 414 locations checked for reference integrity
- Enemy type item references checked against the item table
- Palette range checks on enemy type records
- Dialog option count checks across MSG cards

The validator reports problems with clickable navigation to the relevant tool and field. When a format decode is wrong, it shows up here.

---

## Why It Exists

The longer-term goal of this project is a C# rewrite of Darklands — new code, original data, the same game. That rewrite needs a complete understanding of every data file the original engine touches.

DARK is the workbench that makes that understanding practical. It is also a way of making the format research useful to anyone in the community who wants to explore the game's internals — without needing to understand segmented 16-bit real-mode x86 assembly to do it.

The tool is dedicated to Arnold Hendrick, the lead designer of Darklands.

---

> **Download:** Available soon — [link to be added when 1.0 ships]([PLACEHOLDER_LINK])
