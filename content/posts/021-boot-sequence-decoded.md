---
title: "Devlog #021 - The Boot Sequence Decoded"
date: 2026-04-16
summary: "From blank screen to game: the full Darklands startup chain now mapped. BANNER.DAT, CONFIG.DRK, sound driver selection, the memory check stage, and the graphics bootstrap, one function at a time."
---

## The Wall Before the Game

Every time Darklands starts, a sequence of things has to go right before the player sees anything useful. The text banner. The memory check. The graphics mode switch. The sound driver. If any of them fail, the game simply stops.

Until now, this startup chain was one of the least-documented areas of the codebase. We've spent the last several sessions filling it in, function by function.

Here's what we know.

## Stage 1: Text-Mode Banner

The very first visible output from Darklands is a text-mode banner: white text on black, rendered before the VGA mode switch. This is handled by the startup function at `1699:0114`.

The function draws a blank top row from `DS:0C03`, then walks an offset table at `A895` into a structure called `BANNER.DAT`. Each entry in that table is a cumulative delta into the file, and the walk renders banner rows through the helper at `0C6D:00A9`.

BANNER.DAT is not a bitmap or a font file. It is a compact offset-indexed resource with 20 entries, a simple but functional way to store multiple text-mode rows without a fixed-width slot scheme.

The function `1699:0114` is not a leaf routine. It is called from the pre-banner startup wrapper at `1699:0022`, which also pushes the process argument list (argc/argv) into position. So this function receives the command line and acts on it.

## Stage 2: Config File and Sound Driver

After the banner is painted, `1699:0114` opens the startup config file `config.drk` with mode `"rb"`. If the open succeeds, it reads 8 bytes into `DS:A86E`.

On a real installation, those 8 bytes are: `04 00 20 02 05 00 01 00`. The first byte is a driver index.

The driver index maps to a letter through a table of one-byte strings:

| Index | Letter | Driver file |
|-------|--------|-------------|
| 0 | `a` | `asound.dlc` |
| 1 | `p` | `psound.dlc` |
| 2 | `r` | `rsound.dlc` |
| 3 | `i` | `isound.dlc` |
| 4 | `n` | `nsound.dlc` |

Index 1 → letter `p` → `psound.dlc`. That letter is appended to the string `"sound.dlc"` in a result buffer at `DS:A876`. On a typical install, `DS:A876 = "psound.dlc"`, confirmed by runtime inspection.

If `config.drk` is missing, the fallback is `nsound.dlc` at `DS:0C14`.

## Stage 3: Command-Line Switches

After resolving the config-based default, the function scans the remaining `argv` entries for startup switches beginning with `-` or `/`. Three switch shapes are now confirmed:

- **`/A`**: takes the next character and builds a `?sound.dlc` override name; tries to open the chosen driver file and reports an error if it is missing.
- **`/O`**: sets a startup flag at `DS:0BF4`; later used in the memory check stage as a low-memory override.
- **`/Q`**: sets a word at `DS:0BF2`; runtime-confirmed to skip the intro/presentation sequence.

The `/Q` switch was verified live: launching `darkland.exe /Q` reaches the parser with `argc = 2`, sets `0BF2 = 0001`, still selects `psound.dlc`, and still reaches the sound-driver load at `1699:067B`. But it skips the intro PAN sequence entirely when the flag is checked later in the presentation path.

## Stage 4: Memory Check

The function at `1699:0522` calls a helper (`1699:1150`) before handing off to the graphics bootstrap. This helper is the memory check stage.

It checks two things:

**EMS memory**: Free EMS pages must be at least `0x000B` (176 KiB). If not, it prints entry `19` from the BANNER.DAT table and aborts.

**Conventional memory**: The required amount depends on the selected sound driver:

| Driver | Extra bytes required |
|--------|----------------------|
| `a` | `0x2C90` |
| `i` | `0x2FC0` |
| `p` | `0x290C` |
| `r` | `0x1C60` |
| `n` | `0x03B0` |

The full formula is `current_program_block_bytes + 0x4B6B0 + driver_delta`. If the machine falls short, it prints entries `15..18` and may abort, unless `/O` is set, which forces the memory report but allows startup to continue.

On a `/O` probe run, the helper printed a negative `additional needed` value, which is only possible because `/O` forces the block unconditionally.

## Stage 5: Graphics Bootstrap

After the memory check, the startup wrapper calls `1699:052A`, the graphics/bootstrap stage. This is where Darklands crosses from text mode into the game's VGA presentation environment.

The function opens `fonts.fnt` and `mgraphic.exe`. A helper at `0C9F:07CE` loads `mgraphic.exe` using `INT 21h / AX=4B03`, not as a standalone EXE to run and exit, but as a callable module that gets installed into the running process. Mouse state is initialized through `INT 33h` immediately after.

`mgraphic.exe` is a MicroProse graphics/blit dispatch module. `misc.exe` (loaded earlier, before the banner stage) is the input dispatch module. Together they form a two-part helper layer that the main game calls through trampolines rather than implementing in the main binary.

After the module is in place, the function performs a VGA mode switch to mode 13h (320×200, 256 colours), then handles a split:

- **EMS available**: allocates graphics buffer through the EMS interface at `0E1B:00F3/0117/00A9`, stores the result in `C105`.
- **EMS unavailable**: falls back to `0C9F:04C7(1)`, also stored in `C105`.

The result is the staging buffer for the presentation system.

## Stage 6: COMMONSP.IMG

After the graphics buffer is set up, the helper `1699:179A0` loads `commonsp.img`.

This is a compact common-sprites bank. Its layout:

- Word `0x0000`: payload length (`0x0FD0` = 4048 bytes)
- Words `0x0002..0x001C`: 14 payload-relative offsets for internal slices
- Payload (14 slices, `0x001E` bytes into file)

The 14 slices range from tiny 2-byte entries to a 3,807-byte body. The large body is dominated by palette-range bytes (`0x96..0x9F`) and contains named compact image records. Embedded labels like `HALLEN`, `CORIDO`, `KBATLMN`, and `BCHANGE` are followed by dimension bytes and pixel data, a bank of compact named shapes used throughout the game.

The startup code registers this bank through `0DDD:0004` (a shared object-allocation service), stores the returned handle at `9C42`, and seeds 13 globals in the `A2xx/A3xx/A6xx` regions from the file's offset table. The count is an exact match: 13 non-zero offsets in the file header, 13 rebased startup globals.

## Stage 7: Sound Driver Activation

Also inside `1699:052A`, the earlier-selected sound driver is finally loaded:

```
1699:06FE  push 0000
1699:06FE  push A876
1699:06FE  call 0C9F:07CE
```

The same module-loader helper that loaded `mgraphic.exe` now loads `psound.dlc` (or whichever driver was selected). The returned segment is stored at `9417`, and the loaded module is registered through `0C9F:08C8`. The config bytes from `A86E..A874` are then passed into the sound driver's initialization entry.

## The Confirmed Boot Order

From runtime file-open tracing, the complete sequence is:

1. `misc.exe`: input helper module
2. `banner.dat`: text-mode banner
3. `config.drk`: sound driver selection
4. `mgraphic.exe` + `fonts.fnt`: graphics module install
5. VGA mode 13h switch
6. `commonsp.img`: common sprite bank
7. `psound.dlc`: sound driver activation
8. `opendark.dgt` + `opening2.PAN` ... `opening9.PAN`: intro presentation
9. `msgfiles`, `darkland.lst`, `darkland.cty`, etc.: game data

The function `1699:052A` spans stages 4–7. Everything after it belongs to the intro presentation layer, which is its own story.

## What Remains Open

- The exact role of `0C6D:0100`, which sits between the text-mode helper and the graphics bootstrap.
- The exact registration semantics of the `CnnmSp` tag string used when loading `commonsp.img`.
- How the graphics bootstrap hands off into the intro PAN player overlay family.
