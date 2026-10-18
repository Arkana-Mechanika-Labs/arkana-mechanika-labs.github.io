---
title: Download
description: Download the Darklands Restoration Project for Windows. Requires your own copy of Darklands.
toc: true
width: normal
---

<div class="drp-hero-buttons">
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/download/v0.9.0/DarklandsRP-0.9.0-win-x64.zip" class="drp-btn drp-btn-primary">Download 0.9.0 for Windows (34 MB)</a>
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">All releases ↗</a>
</div>

**You need your own copy of Darklands** (version 483.07, for example the GOG or Steam release). Nothing from the game is included: the program reads your installation.

## Getting started

1. Download `DarklandsRP-0.9.0-win-x64.zip` and unpack it into a folder of its own. It holds `DarklandsRP.exe`, `SDL2.dll`, `libmt32emu.dll`, an empty `MT32_ROMS` folder and the third-party notices.
2. Start `DarklandsRP.exe`. It finds your Darklands by itself (GOG, Steam, or a folder next to it) and remembers it in `darklands.settings.json`, which it creates on the first run. If it can't find the game, it asks you for the folder.
3. Play. It starts like the original: the banner, the opening, then the start screen.

No .NET installation is needed. Windows x64 only for now.

## Music and sound

The game's own sound drivers play, as on a 1992 PC: by default the card set up in your copy (usually a Roland MT-32 for music with a Sound Blaster for speech). For the MT-32, put your MT-32 or CM-32L ROM files in the `MT32_ROMS` folder. Without them the Sound Blaster Pro's FM music plays instead.

## Saved games

Saves go to the game's own `SAVES` folder, shared with the original game both ways. If that folder can't be written (a game installed under Program Files), they go to `%APPDATA%\DarklandsRestoration\SAVES`.

## Settings and keys

`darklands.settings.json` is commented and shows every default: the game folder, the saves folder, the window size (`"scale": 2`, any `"resolution"`, or `"fullscreen": true`), the sound card, the MT-32 ROM folder, and skipping the banner or the opening.

The keys and the mouse are the original's (Alt-S save, Alt-L load, Alt-P pause, F1–F5 character sheets, the menu bar on the right button or F10...). Two keys are new: **F12** saves a screenshot and **F11** opens a developer console.

## Release notes

### 0.9.0 — October 18, 2026

The first release.

- The whole game: character creation, cities, inns and shops, guilds, banks and churches, the world map and its encounters, real-time battles, camping, saints and alchemy, saving and loading (compatible with the original's saves).
- The original's screens, music and sound from your copy of the game: AdLib, Sound Blaster, and MT-32 with your ROMs.
- Windowed at any size or full screen; a commented settings file; F12 screenshots; F11 developer console.
- Every rule rewritten from the original program and checked against it; the known differences and the original bugs kept on purpose are listed in the repository's `docs/faithfulness`.

SHA-256 of the zip: `37210ac1723abbe66aa0b709f55b0869dcd330ea470bcd87a617b631d03ba724`

## Source code

The source code is on GitHub: [Arkana-Mechanika-Studios/darklands-restoration](https://github.com/Arkana-Mechanika-Studios/darklands-restoration). Its README explains how to build it and how it is organized.
