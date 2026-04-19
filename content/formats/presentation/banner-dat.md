---
title: BANNER.DAT
weight: 2
---

Text-mode startup resource. Loaded by `DARKLAND.EXE` before the VGA mode switch. Contains the welcome banner rows, the startup selection menu, and the memory/disk diagnostic strings.

*Reverse-engineered from `DARKLAND.EXE` startup analysis and direct file inspection (2026-04-16).*

## File Facts

| Property | Value |
|----------|-------|
| Path | `DARKLAND\BANNER.DAT` |
| Size | 1519 bytes |
| Format | Uncompressed — offset table + inline strings |

## File Layout

```
Offset 0x0000 – 0x0027:  word[20]  offset_table  — 20 absolute byte offsets into this file
Offset 0x0028 – EOF:     entries 0..19             — display rows and diagnostic strings
```

The header is 20 little-endian `uint16` values. Each value is a file-absolute byte offset to one entry.

## Entry Table

| Entry | File offset | Content |
|-------|-------------|---------|
| 0 | `0x0028` | Blank top row (79 spaces + CR LF $) |
| 1 | `0x007B` | Banner row 1 |
| 2 | `0x00CC` | Banner row 2 |
| 3 | `0x011D` | Banner row 3 |
| 4 | `0x016E` | Banner row 4 |
| 5 | `0x01BF` | Banner row 5 |
| 6 | `0x0210` | Banner row 6 |
| 7 | `0x0261` | Banner row 7 |
| 8 | `0x02B2` | Banner row 8 |
| 9 | `0x0303` | Banner row 9 |
| 10 | `0x0354` | Banner row 10 |
| 11 | `0x03A5` | Banner row 11 (highlighted) |
| 12 | `0x03F6` | Banner row 12 (highlighted) |
| 13 | `0x0447` | Banner row 13 (highlighted) |
| 14 | `0x0498` | Diagnostic: disk space error |
| 15 | `0x04C6` | Diagnostic: conventional memory required |
| 16 | `0x0502` | Diagnostic: conventional memory available |
| 17 | `0x0541` | Diagnostic: additional memory needed |
| 18 | `0x057E` | Diagnostic: memory override warning |
| 19 | `0x05B9` | Diagnostic: EMS requirement |

Entries 0–13 are display rows; entries 14–19 are startup diagnostic strings.

## Display Rows

Entries 1–10 are 80-column CP437 null-terminated rows that build the text-mode banner:

```
+----------------------------------------------------------------------------+
|                       Darklands(TM) - Version 483.07                       |
|        In Medieval Germany, reality is more horrifying than fantasy        |
|        Program & Audio-Visual Copyright (C) 1992 by MicroProse,Inc.,       |
|                            All Rights Reserved.                            |
+----------------------------------------------------------------------------+

                              1) Tactical Battle code
                              2) Role-Playing code
                              Select:
```

Entries 11–13 (the menu rows) each begin with raw bytes `FF 0F`. The startup renderer interprets `0xFF` as an inline control/escape byte: the following byte is applied as the current text attribute. `0x0F` is bright white on black — the attribute used for the menu prompt rows.

## Diagnostic Strings

These are plain null-terminated C-style strings used by the memory-check stage at `1699:1150`:

| Entry | String |
|-------|--------|
| 14 | `Insufficient free disk space - 512K required.` |
| 15 | `Darklands requires %ld bytes (%dK) of conventional memory.` |
| 16 | `Your machine has only %ld bytes (%dK) of conventional memory.` |
| 17 | `Therefore, you need to free an additional %ld bytes (%dK) .` |
| 18 | `You have chosen to override the memory check - BEWARE!!` |
| 19 | `Darklands requires at least 176K of EMS memory free.` |

Entry 14 (disk-space check) is consumed by an earlier startup path; entries 15–19 are used by the conventional/EMS memory check.

## Inline Attribute Encoding

Rows that need custom text colours embed a two-byte escape sequence inline:

```
0xFF  <attribute>  rest of row text ...
```

The renderer at `0C6D:00A9` recognises `0xFF` and applies the following byte as the current DOS text mode attribute byte before continuing. This allows the banner to display distinct foreground/background colour combinations without switching video modes.

## Consumer

`DARKLAND.EXE` function `1699:0114` loads `BANNER.DAT` as a loose file and uses the 20-entry offset table to index the in-memory blob. The startup memory-check helper at `1699:1150` later reuses entries 14–19 for formatted diagnostic output through `INT 21h / AH=09`.

## Confidence

High. File layout and all 20 entry offsets confirmed by direct byte inspection. Renderer behaviour confirmed by runtime tracing.
