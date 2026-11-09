---
title: Download
description: Download the Darklands Restoration Project for Windows, or for Linux and the Steam Deck (experimental). Requires your own copy of Darklands.
toc: true
width: normal
---

<div class="drp-hero-buttons">
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/download/v1.0.0-rc2/DarklandsRP-1.0.0-rc2-win-x64.zip" class="drp-btn drp-btn-primary">Download 1.0.0-rc2 for Windows (42 MB)</a>
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/download/v1.0.0-rc2/DarklandsRP-1.0.0-rc2-linux-x64.tar.gz" class="drp-btn drp-btn-outline">Linux and Steam Deck, experimental (41 MB)</a>
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">All releases ↗</a>
</div>

**You need your own copy of Darklands** (version 483.07, for example the GOG or Steam release). Nothing from the game is included: the program reads your installation.

## Getting started

1. Download `DarklandsRP-1.0.0-rc2-win-x64.zip` and unpack it into a folder of its own. It holds `DarklandsRP.exe`, `DarklandsRP Launcher.exe`, `SDL3.dll`, `libmt32emu.dll`, an empty `MT32_ROMS` folder, a `SOUNDFONT` folder for a SoundFont of your own, the licence, the third-party notices, the guides, an example mod and sound pack, and the release notes.
2. Start `DarklandsRP Launcher.exe`. The launcher finds your Darklands by itself (GOG, Steam, or a folder next to it); check the game folder and the settings (display, picture filter with a preview, sound, packs), then press Play. They are kept in `darklands.settings.json`. Later, `DarklandsRP.exe` starts the game directly; the launcher is there whenever you want to change something.
3. Play. It starts like the original: the banner, the opening, then the start screen.

No .NET installation is needed.

### Linux and the Steam Deck (experimental)

`DarklandsRP-1.0.0-rc2-linux-x64.tar.gz` runs on Linux x64 and on the Steam Deck, in desktop mode or added to Steam as a non-Steam game. Unpack it with `tar` so that `DarklandsRP` stays executable, then start `./DarklandsRP-Launcher` for the settings or `./DarklandsRP` for the game. It needs the system's **SDL 3** (`libSDL3.so.0`, SDL 3.2 or later), which SteamOS, the Steam runtime, Arch, Fedora, Debian 13 and Ubuntu 25.04 or later have; on Ubuntu 24.04 or Debian 12 install it yourself or run the game through Steam. It finds the game in Steam's libraries (including the Deck's SD card), Heroic, GOG/Lutris and Wine prefixes. This build has been tested by the automated builds only; if something does not work, please report it with your distribution and what you saw.

## Music and sound

The game's own sound drivers play, as on a 1992 PC: by default the card set up in your copy (usually a Roland MT-32 for music with a Sound Blaster for speech). For the MT-32, put your MT-32 or CM-32L ROM files in the `MT32_ROMS` folder. Without them the Sound Blaster Pro's FM music plays instead.

## Saved games

Saves go to the game's own `SAVES` folder, shared with the original game both ways. If that folder can't be written (a game installed under Program Files), they go to `%APPDATA%\DarklandsRestoration\SAVES`.

## Settings and keys

`darklands.settings.json` is commented and shows every default: the game folder, the saves folder, the window size (`"scale": 2`, any `"resolution"`, or `"fullscreen": true`), the picture filter (Sharp, Even, Soft, Soft CRT, HQ, CRT, CRT+), the sound card, the MT-32 ROM folder, and skipping the banner or the opening.

The keys and the mouse are the original's (Alt-S save, Alt-L load, Alt-P pause, F1–F5 character sheets, the menu bar on the right button or F10...). A few are new: **F12** saves a screenshot, **F11** opens a developer console, **Ctrl+F11** cycles the picture filters, and the mouse wheel moves the highlight in menus and lists.

## Release notes

The full notes of each release are on [GitHub](https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases).

### 1.0.0-rc2 — November 9, 2026

The second release candidate of 1.0. It brings a new launcher (a painted window with the settings on two tabs, and its own `DarklandsRP Launcher.exe`), seven picture filters for large screens with a live preview, the mouse wheel in menus, right click and + / − in character creation, and a move to SDL 3. The game plays as in rc1, with the last differences we found in battles closed; all 1,001 recorded battles and sessions agree with the original. Your saved games and settings carry over. On Linux it now needs SDL 3.

SHA-256 of the Windows zip: `990c18d2882842a1a826cb9a3cb39cd420c965f21e296e77217d7e599908c447`; of the Linux archive: `cda56dafcc89424d49397565f003d8efcc1e0f82e38b090943ccd943b761eed5`

### 1.0.0-rc1 — November 5, 2026

The first release candidate of 1.0. It is meant for playing and for checking: if nothing serious turns up, 1.0 follows with the same game. It adds General MIDI music to sound packs (played through a SoundFont of your own), music per card for packs and mods, and a check of the game program at start, and brings the game closer to the original again in battles, card menus, the travel map and a handful of rare cases. Your saved games carry over.

SHA-256 of the Windows zip: `248700b2e4eb8276262a3fddd64826520b8ed4af5a44c6e1c8a175598f0fbe69`; of the Linux archive: `e46a1005c5e3966f7610c93f07146ce4c8f90a8ce4859108308aedfedbd517f2`

### 0.9.6 — November 2, 2026

A new release, with four additions around the game: an experimental Linux and Steam Deck build, sound packs (your own OGG or WAV music and effects, chosen in the launcher), data mods with a card registry, and a command layer for scripts. It also brings the game closer to the original again: drawing as the 1992 game draws it (the cleaner drawing of 0.9.5 is a setting, `display.cleanDrawing`), battle colours and the party panel, keys typed during the hourglass, hot-key boxes and menus, and a handful of rare cards and rules. Your saved games carry over.

SHA-256 of the Windows zip: `312030f696d799c8f53802cb5e682301e30d251aa83198c6139a2bdfeae0828c`; of the Linux archive: `994f4c80ab1f512403abdeb1f3bd14501e76b5c38bffea4b764ab7ee9369b9b0`

### 0.9.5 — October 28, 2026

A new release. Walking on the map with a held arrow key is smooth, as in DOSBox: the party keeps its facing and stops when you let go. In battles the mouse pointer hides while a message box waits, the party panel uses the original's font and shows "near a door" and the like, and a few sounds and small timings match the original. All 769 battles and whole-game sessions of the side-by-side comparison agree with the original, now including the sound and music requests.

SHA-256 of the zip: `eaad6d8d73db21d0bbaeb8c614e49b02e97e8a33f3ce2ffb9555c1061145525f`

### 0.9.4 — October 25, 2026

A test build: closer to the original in travel on the overland map, the map's keys and drawing, the card menus, the character generator and battles; a `quests` command in the developer console.

### 0.9.3 — October 23, 2026

A hotfix for 0.9.2: in a battle, the character information could only be closed with Esc.

### 0.9.2 — October 23, 2026

A test release ahead of 1.0: a settings launcher, two crashes fixed, saved games and inn caches made safe, and many details corrected by playing the original and the restoration side by side. Saved games still load in the original game.

### 0.9.1 — October 21, 2026

A bug-fix release: a crash when the world map opened, and a party stuck at a place it had just left.

### 0.9.0 — October 18, 2026

The first release.

- The whole game: character creation, cities, inns and shops, guilds, banks and churches, the world map and its encounters, real-time battles, camping, saints and alchemy, saving and loading (compatible with the original's saves).
- The original's screens, music and sound from your copy of the game: AdLib, Sound Blaster, and MT-32 with your ROMs.
- Windowed at any size or full screen; a commented settings file; F12 screenshots; F11 developer console.
- Every rule rewritten from the original program and checked against it; the known differences and the original bugs kept on purpose are listed in the repository's `docs/faithfulness`.

SHA-256 of the zip: `5455c82c80939a7b74487fbd34041b10793c044470adc1c8d43acedd34b66e46`

## Source code

The source code is on GitHub: [Arkana-Mechanika-Studios/darklands-restoration](https://github.com/Arkana-Mechanika-Studios/darklands-restoration). Its README explains how to build it and how it is organized.
