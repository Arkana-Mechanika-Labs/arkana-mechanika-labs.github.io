---
title: Download
description: Download the Darklands Restoration Project for Windows, or for Linux and the Steam Deck (experimental). Requires your own copy of Darklands.
toc: true
width: normal
---

<div class="drp-hero-buttons">
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/download/v1.1.0/DarklandsRP-1.1.0-win-x64.zip" class="drp-btn drp-btn-primary">Download 1.1 for Windows (43 MB)</a>
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/download/v1.1.0/DarklandsRP-1.1.0-linux-x64.tar.gz" class="drp-btn drp-btn-outline">Linux and Steam Deck, experimental (43 MB)</a>
  <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">All releases ↗</a>
</div>

**You need your own copy of Darklands** (version 483.07, for example the GOG or Steam release). Nothing from the game is included: the program reads your installation.

## Getting started

1. Download `DarklandsRP-1.1.0-win-x64.zip` and unpack it into a folder of its own, or over your 1.0 folder. It holds `DarklandsRP.exe`, `DarklandsRP Launcher.exe`, `SDL3.dll`, `libmt32emu.dll`, an `MT32_ROMS` folder for your MT-32 ROM files, a `SOUNDFONT` folder for a SoundFont of your own, `mods` and `packs` folders (with the HD fonts pack, and room for language and sound packs), the licence, the third-party notices, the guides and the release notes.
2. Start `DarklandsRP Launcher.exe`. The launcher finds your Darklands by itself (GOG, Steam, or a folder next to it); check the game folder and the settings (display, picture filter with a preview, sound, packs), then press Play. They are kept in `darklands.settings.json`. Later, `DarklandsRP.exe` starts the game directly; the launcher is there whenever you want to change something.
3. Play. It starts like the original: the banner, the opening, then the start screen.

No .NET installation is needed.

## Translating: the Darklands Workshop (beta)

The **Darklands Workshop** is the translators' editor, a separate download: [Workshop 1.1.0-beta.1 on GitHub](https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases/tag/workshop-v1.1.0-beta.1) (Windows, 77 MB; Linux, experimental). Unzip it into the game's folder; it makes a `Workshop` folder there. It shows every text as the game draws it, checks your pack, opens the game at the text you are translating, and comes with sample packs, the translator's guide, and the example sound pack and mod. Watch the [video tutorial](https://youtu.be/tPzPl-0qWg4) to get started.

To play in another language, put a language pack in `packs/languages` and choose it on the launcher's Advanced tab.

### Linux and the Steam Deck (experimental)

`DarklandsRP-1.1.0-linux-x64.tar.gz` runs on Linux x64 and on the Steam Deck, in desktop mode or added to Steam as a non-Steam game. Unpack it with `tar` so that `DarklandsRP` stays executable, then start `./DarklandsRP-Launcher` for the settings or `./DarklandsRP` for the game. **SDL 3** comes with it (`libSDL3.so.0`, beside the program), so it also runs on systems without SDL 3 of their own, such as Ubuntu 24.04 and 22.04 or Debian 12. It finds the game in Steam's libraries (including the Deck's SD card), Heroic, GOG/Lutris and Wine prefixes. This build has been tested by the automated builds only; if something does not work, please report it with your distribution and what you saw.

## Music and sound

The game's own sound drivers play, as on a 1992 PC: by default the card set up in your copy (usually a Roland MT-32 for music with a Sound Blaster for speech). For the MT-32, put your MT-32 or CM-32L ROM files in the `MT32_ROMS` folder. Without them the Sound Blaster Pro's FM music plays instead.

## Saved games

Saves go to the game's own `SAVES` folder, shared with the original game both ways. If that folder can't be written (a game installed under Program Files), they go to `%APPDATA%\DarklandsRestoration\SAVES`.

## Settings and keys

`darklands.settings.json` is commented and shows every default: the game folder, the saves folder, the window size (`"scale": 2`, any `"resolution"`, or `"fullscreen": true`), the picture filter (Sharp, Even, Soft, Soft CRT, HQ, CRT, CRT+), the sound card, the MT-32 ROM folder, and skipping the banner or the opening.

The keys and the mouse are the original's (Alt-S save, Alt-L load, Alt-P pause, F1–F5 character sheets, the menu bar on the right button or F10...). A few are new: **F12** saves a screenshot, **F11** opens a developer console, **Ctrl+F11** cycles the picture filters, and the mouse wheel moves the highlight in menus and lists (in a card's menu, ↑, ↓, the wheel and the number keys work wherever the pointer is).

## Release notes

The full notes of each release are on [GitHub](https://github.com/Arkana-Mechanika-Studios/darklands-restoration/releases).

### 1.1.0 — November 22, 2026

Darklands Restoration 1.1 makes Darklands translatable: language packs for the card texts, the screens, the names and the battle messages, in Latin, Greek and Cyrillic letters and in Chinese, Japanese and Korean, with pixel or TrueType fonts. HD fonts for English, and the Interface switch: Comfort (the default) walks on over the map with a double tap or Shift and a direction and has a clearer saved-games list; Classic keeps the 1992 map and saved-games screens. The character sheet's skill values now line up. The Darklands Workshop beta, the translators' editor, is a download of its own. The game's rules are those of 1.0: all 1,040 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `SHA-WIN-1.1.0`; of the Linux archive: `SHA-LINUX-1.1.0`

### 1.0.0 — November 18, 2026

Darklands Restoration 1.0: the game of the release candidates, with one small fix. Saving inside a battle now stores each party member's slot number exactly as the original does; before, a game saved in a battle in a newly started game could carry a wrong slot number in the saved file. All 1,029 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `5eb0587b82efa5a77d405133726cd2b62b690341d5877a8f210279e0684f622e`; of the Linux archive: `8926b275ec51c24048ee0e0aa65ace06e8761d0416e31435b52281e48afb6bd0`

### 1.0.0-rc6 — November 15, 2026

The sixth release candidate of 1.0. The game plays as in rc5, with two fixes from a tester's report on Linux. With the Sound Blaster Pro 2 or the Pro AudioSpectrum, and with the FM music played when MT-32 is chosen without its ROM files, some voices were much too quiet and came and went (the lower melody at character creation); our sound chip emulation now plays them at the right level. The Linux package now includes SDL 3, so it runs on Ubuntu 24.04 and 22.04 and Debian 12 without installing anything. All 1,028 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `9e519b498155dd95d8e6091286e68f2caa4ec36284437bb74e017d88bafc93b3`; of the Linux archive: `48b11259091c367d389373f67906c5ec080e37bb9f55de854c80fc0221f69d98`

### 1.0.0-rc5 — November 14, 2026

The fifth release candidate of 1.0. The game plays as in rc4, with one small display fix in battles: the party panel keeps a member's order letter until his row is drawn again, as the 1992 game does. The code was gone through name by name for 1.0; three reviews found no change in logic, and all 1,028 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `8c98cce8801627e34a1808df7b2f6fa9ce3604e231afe0f7b9adc73344c20e79`; of the Linux archive: `827a87ac12b9275087103d2cd298b62fe82e1125bfc00ac4de94a101695e7e37`

### 1.0.0-rc4 — November 12, 2026

The fourth release candidate of 1.0. It fixes what goes wrong when you split the party over several floors of a castle, a mine or another dungeon, from a player's report ([issue #3](https://github.com/Arkana-Mechanika-Studios/darklands-restoration/issues/3)). Use Stairs and U bring members back by their own stairs. Doors, chests, traps, alarms, enemies and missiles act only on their own floor. Nobody is lost as "Away", stuck in a wall or left outside the map by a split. These are bugs of the 1992 game: the testers' faithful mode keeps them. Everything else plays as in rc3; all 1,017 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `e005e465a31b294926f435efcef293af50595ded27fe6fcbc1ed024b4aefe8f2`; of the Linux archive: `09a080abeef8bf214dd709f97b739fddba3f22e23685a5f1abeafcad01b0137a`

### 1.0.0-rc3 — November 10, 2026

The third release candidate of 1.0, a short round of fixes from players' reports: card menus answer ↑, ↓, the mouse wheel and the number keys wherever the pointer is (the original's way is a switch on the launcher's Advanced tab), Shift-scrolling at the edges of a battle is slower, the Soft filter keeps text sharp, and the flashes of colour when a battle starts from a card, on the saved games list in a battle and on the party information in a battle are gone. The game plays as in rc2; all 1,001 recorded battles and sessions agree with the original. Your saved games and settings carry over.

SHA-256 of the Windows zip: `20279c8a31222c25739a63c13b84b6807a3b98ceac5ce9fcd86d71cc74685425`; of the Linux archive: `a306a759de052717673a9ba478c903658d3d2ce2ca455f3a563825bd64f53e93`

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
