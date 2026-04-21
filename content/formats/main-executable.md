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

## What The KB Preserves

The canonical KB note records:

- several large segmented-pointer tables near `0x17d0b0`
- string tables for months, occupations, reputations, skills, names, and card variables
- historical data offsets that can still help correlate old community findings with modern tracing work

## Confidence

Medium-high. This page is a pointer to the preserved community reference, not a complete executable RE substitute.
