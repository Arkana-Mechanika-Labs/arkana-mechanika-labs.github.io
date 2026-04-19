---
title: "Devlog #023 - Mapping the Battleground"
date: 2026-04-18
summary: "The BC archive cracked open: 65 entries, seven combat art families, a 33×33 encounter-map grid, and a hidden string bank that names every battle environment in the game."
---

## The Combat Art Vault

Darklands has five kinds of combat location: outdoors in the wild, inside mines, in cities, at fortifications, and in tombs and caves. Each environment needs a full set of artwork: floors, walls, monsters, items. All of that comes from a single archive called `BC.CAT` (or sometimes referenced as the BC archive).

This session cracked it open.

## Archive Structure

The BC archive uses the same CAT format seen elsewhere in Darklands: a directory of 24-byte entries, each holding a 12-character filename and a length. The BC archive contains **65 entries** with a total uncompressed size of **189,815 bytes**.

The filenames sort cleanly into seven families:

| Suffix | Count | Content |
|--------|-------|---------|
| `FLC` | 9 | Floor tiles, lit (combat) |
| `FFC` | 9 | Floor tiles, far (ceiling or distance) |
| `NWC` | 9 | Near-wall tiles |
| `NFC` | 9 | Far-wall tiles |
| `WWC` | 9 | Wide-wall tiles |
| `WFC` | 9 | Wide-far-wall tiles |
| `FRC` | 9 | Filler/trim tiles |

Seven tile families times nine variants each = 63 entries. The remaining two entries in the 65-entry archive are structural records: an index header and a blank/null entry.

Nine variants per family maps directly to the five combat environments plus four special-case variants. The correspondence is:

- **Outdoor (Wild)**: `OUT.*` files
- **Mine**: `MINE.*`
- **City**: mixed naming (`CIT*`, `URB*`)
- **Fort**: `FORTMONS.*`
- **Tomb/Cave**: `KEEP.*` and `CAVEDRAG.*`

All five environment bundles are confirmed; their filenames appear in the archive directory and the tile data has been extracted and matched to each context.

## IMAPS: The 33×33 Grid

One of the more unexpected findings in the BC work was `IMAPS`. Every combat encounter in Darklands takes place on a map, and the map grid is defined by a structure called IMAPS.

IMAPS contains **1,109 records**, each exactly **12 bytes** long, preceded by a **20-byte header**. The total size: `20 + 1109 × 12 = 13,328 bytes`.

The records encode a **33×33 grid** (1,089 cells) with the remaining 20 records used for supplementary lookup data. Each 12-byte cell entry describes the tile type, height, wall flags, and passability for one grid position.

This is the data structure the combat engine uses to know where walls are, where characters can stand, and how line-of-sight works. It is not generated procedurally at runtime; it is a static lookup table embedded in the archive. Every combat map in Darklands is built from a combination of IMAPS grid cells and the seven BC tile families.

## Section 138: The Environment String Bank

The most surprising find was a hidden string bank at EXE offset `0x17F670`.

The Darklands executable is large, and most of its string content is in obvious clusters. But at flat offset `0x17F670`, there is a dense bank of environment-related text strings: the names, descriptors, and configuration tokens for the five combat environments.

This string bank belongs to **section 138** of the executable's overlay layout. Section 138 is owned by resolver record `0x0088`, which points to logical module `0x008A`. The predicted stub aliases for this section are in the range `11E3:32AF..3327`.

The strings at `0x17F670` are not visible in the ordinary startup open-trace; they are part of the code that selects and configures combat environments when a fight is about to begin. Finding the exact runtime caller into section 138 is the next step for fully connecting this string bank to the combat initialization path.

## Confirmed Environment Bundles

Five environment bundles are now confirmed end-to-end, from archive filename to IMAPS grid variant to section-138 string identifier:

**Wild (Outdoor)**
- Tile set: `OUT.*`
- Typical feel: open fields, sparse trees, wide sightlines

**Mine**
- Tile set: `MINE.*`
- Typical feel: narrow corridors, irregular walls, low ceilings

**City**
- Tile set: mixed `CIT*`/`URB*`
- Typical feel: cobblestones, building walls, cramped alleys

**Fort**
- Tile set: `FORTMONS.*`
- Typical feel: stone flags, heavy walls, fortification geometry

**Tomb/Cave**
- Tile sets: `KEEP.*` and `CAVEDRAG.*`
- Two sub-variants covering different dungeon aesthetics: the keep-style tomb and the natural cave/dragon-den style

## The BC Format and the CAT Format

BC uses the same CAT directory format as Darklands' other archive files. A 24-byte directory entry:

```
Offset  Size  Description
0x00    12    Filename (null-padded, no extension separator)
0x0C    4     Entry length in bytes
0x10    4     Entry offset in archive
0x18    4     Flags / reserved
```

The full 65-entry directory parses cleanly against this layout, and extracted tile data matches the expected palette-indexed art format consistent with other Darklands graphics files.

## What This Means for the Rewrite

The combat art system is now modelled well enough to plan a rewrite path:

- The tile families map to clear roles in a combat renderer.
- The IMAPS 33×33 grid is a static lookup that can be loaded and consumed directly.
- The environment selection logic lives in section 138 of the EXE, not in the archive.
- The archive itself is the asset store; no generated content, no procedural tile logic.

What is still open: the exact runtime path from combat-encounter initialization into section 138, and the precise meaning of each of the 12 bytes in an IMAPS cell.
