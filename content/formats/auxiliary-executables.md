---
title: Auxiliary Executables
weight: 10
---

Darklands ships several supporting executables alongside the main game. Some are pure
install-time artifacts; others are diagnostic tools that reveal details about internal
data structures. Analysis here is based on static inspection of the binaries (string
extraction, disassembly) cross-referenced with the main RE work on `DARKLAND.EXE`.

---

## DKED.EXE — Save Game Editor

Third-party save game editor v1.1 by Steven J. Cotellesse (MSC 1992, Vermont Views TUI).
Useful for RE because the editor's field layout mirrors the actual character struct.

### Character fields

**Attributes (7 current + 7 max)**

```
End  Str  Agl  Per  Int  Chr  DF
```

**Weapon skills (7)**

```
WEdge  WImp  WFll  WPol  WThr  WBow  WMsl
```

**Non-combat skills (12)**

```
Alch  Relg  Virt  SpkC  SpkL  R&W  Heal  Arti  Stlth  StrWs  Ride  WdWse
```

**Party-level**

```
Florins / Groschens / Pfenniges / Bank Note  —  Fame  —  Philosopher's Stone quality
```

The 19-skill layout matches the `skill_set` structure in the game's data — 7 weapon skills
followed by 12 non-combat skills. Equipment is stored as Name + Quantity + Quality (1–99).

---

## DKQUE.EXE — Quest Log Viewer

Official MicroProse diagnostic tool. Reads any save file and dumps the active quest log.
Confirms the event queue structure that follows the character array in the save file.

### Quest types

- **Fetch quest** — `Get <item> from <city>`
- **Return quest** — `Return <item> to <contact> at <city>`
- **Raubritter bounty** — `Raubritter Quest (<name>) - go to - <city>`

### Contact types (stored as numeric ID 0–10)

| ID | Contact |
|----|---------|
| 0 | Merchant |
| 4 | Foreign Trader |
| 5 | Pharmacist |
| 6 | Medici (banking) |
| 7 | Hanseatic League |
| 8 | Fugger (banking) |
| 10 | Mayor |

Quests have either a deadline (`by year/month/day`) or are open-ended
(`no limit from year/month/day`). Dates are stored as separate year, month, day fields.

---

## MGRAPHIC.EXE — VGA Blit Engine

MicroProse hardware abstraction module dated September 19, 1991 — loaded by Darklands at
startup. Provides a 56-function far-call dispatch table for all pixel-level graphics.

Targets VGA mode 13h (320×200, 256 colours). Ships with an embedded EGA-compatible default
palette (256 RGB triplets, 6-bit per channel) and a pre-computed scanline offset table
(200 rows × Y×320) to avoid runtime multiply.

Key operations exposed by the dispatch table:
- Sprite blit (`REP MOVSB/W` block copy)
- Screen fill / clear (`REP STOSB`)
- Transparency scan (`REP SCASB`)
- Palette upload (VGA port `0x03C8`)
- Vsync wait (VGA port `0x03DA`)
- Mode 13h set and detection

The two Darklands segments that handle sprites (`147Ch`) and the screen blit cache (`13ECh`)
both far-call into this module for actual pixel writes.

---

## MISC.EXE — Input Hardware Abstraction

MicroProse input driver dated February 20, 1989 — the same module was reused across their
game lineup. Provides a 15-function far-call dispatch table for all keyboard and joystick
input. Darklands calls input by table index, so the same game code works for both input
devices.

Key table entries:

| Index | Function |
|-------|----------|
| 3 | Read joystick analog (RC timing loop on port `0x201`) |
| 4 | Read joystick digital buttons |
| 6 | Peek keystroke, non-blocking (`BIOS INT 16h`) |
| 7 | Get keystroke, blocking (`BIOS INT 16h`) |
| 8 | Read character with echo (`DOS INT 21h`) |

---

## MPSCOPY.EXE — Installer / Asset Unpacker

MicroProse Software Unpacker v4.12 (February 1993) by Brian Reynolds (Darklands lead
programmer; later co-founder of Firaxis). Transforms floppy `.HAG` archives into the
runtime `.CAT` pack files using an embedded PKWARE DCL v1.02 decompressor.

### Full asset pipeline

```
Floppy .HAG archives
  →  MPSCOPY.EXE  (PKWARE DCL decompress)
  →  .CAT pack files on disk
  →  Resource loader in DARKLAND.EXE  (24-byte directory entries, 12-char names)
  →  LZSS / LZW decompressors
  →  MGRAPHIC.EXE  (VGA output)
```

### MADS asset section categories

The `.CAT` files are MADS archives with 10 named sections:

```
OBJECTS  INTER  TEXT  QUOTES  FONT  SOUND  CONV  SPEECH  SECTION  GLOBAL
```

---

## Installer Tools (DARKPOP.COM, XTRACT.EXE, QUERY.EXE, BOOTDISK.EXE)

Four floppy-era installation utilities. None are part of the game runtime.

**DARKPOP.COM** — standalone PKUNZJR extractor (v2.04c, PKWARE). Used during floppy
installation to unpack ZIP archives; a leftover artifact after install completes.

**XTRACT.EXE** — orchestration wrapper that calls DARKPOP.COM, validates that extracted
files carry a `.raw` extension, and reports per-file progress.

**QUERY.EXE** — installer configuration prompt. Presents a numbered menu (1–9) to the
user, dispatches to the selected action (sound card selection, config file write, etc.).

**BOOTDISK.EXE** — creates a clean-boot DOS floppy with maximum conventional and EMS
memory. Requires MS-DOS 5.0+; writes a custom `CONFIG.SYS` / `AUTOEXEC.BAT` with
`DOS=HIGH,UMB`, himem.sys, emm386.exe, and optional mouse / sound card drivers.
Confirms that Darklands requires EMS memory to run (used by the overlay manager to
page code segments in and out at runtime).
