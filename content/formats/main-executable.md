---
title: Main Executable (DARKLAND.EXE)
weight: 11
---

Historical reference note for the main Darklands executable. Unlike the data-file pages in this section, this is not a stable binary format so much as a catalog of known offsets, string tables, and pointer arrays preserved from the legacy community corpus.

*Canonical source: `darkland.exe.xml` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## Scope

`DARKLAND.EXE` is the main game executable. The KB treats this note as a **historical cross-reference** rather than a primary source of live RE conclusions.

It contains:

- segmented pointer arrays
- string tables and UI text
- lookup data for skills, attributes, names, and menu-adjacent text
- other partially decoded executable-owned tables

## Important Caveat

Because this is compiled executable code rather than a pure data file, most of the content is only meaningful alongside disassembly and runtime tracing. Current executable RE notes should take precedence over this legacy XML-derived reference when they disagree.

## Why The KB Keeps It

The current KB treats this note mainly as a historical cross-reference. It is still useful because it preserves:

- several large segmented-pointer tables near `0x17d0b0`
- string tables for months, occupations, reputations, skills, names, and card variables
- older offset correlations that still help map legacy community findings onto modern tracing work
- evidence for executable-owned token vocabularies used by `MSGFILES`
- a bridge between XML-derived format notes and newer executable RE notes

## Notable Preserved Tables

The XML-derived reference still records a few especially useful executable-owned data groups:

- segmented pointer arrays around `0x17d0b0`, `0x17eb18`, and `0x18a60f`
- string tables near `0x1872d0` through `0x189a43` for months, copy-protection words, occupations, reputations, names, skills, jobs, and card variables
- historical lookup text for city/location labels, menu text, and character-generation content

## Variable Tokens And Localization Notes

One of the most useful surviving tables is the executable variable-name list used by message cards.

The KB currently notes that shipped `MSGFILES` makes live use of many city/runtime variables from this table, including:

- `ChosenOneName`
- `PlaceName`
- `citySquare`
- `councilHall`
- `cityBarracks`
- `marketplace`
- `fortress`
- `pawnshop`
- `hospital`
- `poorhouse`
- `slum`
- `monastery`
- `cathedral`
- `cityChurch`

The same KB note also calls out variables that are listed in the executable but are not referenced by shipped English or German `MSGFILES` payloads:

- `imperialMint`
- `CityLocation`
- `whorehouse`
- `warehouse`
- `docks`

That matters for interpreting some `DARKLAND.CTY` landmark slots: the German executable and German city data make `imperialMint` look like a strong candidate for the rare `Munzenplatz` / `Reichsmuenzstaette` slot, even though shipped message cards do not currently exercise that token.

The German executable also appends additional grammar-sensitive variable tokens not present in the English one:

- `his1..his6`
- `His1..His6`
- `him1`
- `him2`
- `Him1`
- `CON`

These are actively used by shipped German `MSGFILES` and support localized grammatical substitution in card text.

## Merged-Note Status

The KB explicitly treats the imported file-format note as historical data-format documentation only. For live reverse-engineering conclusions, it now defers to the deeper executable RE material in `RE\reports\darkland_exe_notes.md` and the KB executable-RE notes.

## Confidence

Medium-high. This page is a pointer to the preserved community reference, not a complete executable RE substitute.
