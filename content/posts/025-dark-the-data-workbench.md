---
title: "Devlog #025 - DARK: A Workbench for Darklands Data"
date: 2026-04-19T12:00:00
summary: "A single tool that brings together years of community format research: browse save games, enemies, cities, items, dialog trees, images, fonts, and archives, all in one place, on a modern system."
---

## Standing on Other People's Work

Before describing what DARK does, it is worth being clear about where it comes from.

Most of Darklands' file formats were documented years ago by a small group of dedicated researchers, primarily working in and around the Darklands Yahoo Group. Merle, Joel "Quadko" McIntyre, and others spent real time reversing binary structures, writing format specifications, and building tools, largely without automated help, largely because they cared about the game. Those XML specifications are preserved in [Wendigo's Darklands repository](https://github.com/vvendigo/Darklands) ([wendigo.online-siesta.com/darklands](https://wendigo.online-siesta.com/darklands/)) and are still the reference source for most of what this project understands. On the game-knowledge side, [darklands.net](https://www.darklands.net) by Matt Wirkkala is the reference the community has relied on for decades.

That community also produced tools: save editors, archive extractors, map viewers. Some of them still work perfectly. Some have grown harder to run on modern systems. And they were always separate: open one to edit a save, a different one to look inside a catalog, something else for images.

DARK's starting point is that body of existing knowledge. The format library underneath it is built on those same XML specs. The goal is not to redo what was done, but to gather it in one place, make it run reliably today, and extend it into the areas where the original documentation ran out.

## What the Tool Is

DARK (Darklands Authoring & Resource Kit) is a desktop application that reads Darklands game files directly from a standard installation and presents them in a single workbench. You point it at a game folder and everything becomes accessible from one interface, without installing anything else.

![DARK welcome screen showing the full sidebar navigation](/images/dark_welcome.png)

The sidebar organises everything into seven sections.

## Save Games

Any save file opens into a structured view of the party: all seven attributes with their current and maximum values, all 19 skills laid out with their names rather than raw numbers, equipment in each slot, inventory contents, and the party-level state: currency split across florins, groschens, and pfenniges, the bank note balance, fame, and the Philosopher's Stone quality. Every field is editable and saves back to the original file.

The **Quests / Events tab** lists every active and completed quest and event record in the save: status, open date, destination city, source location, required item, and a text summary for each entry. A panel on the right plots the quest destination on a mini-map of the game world, so it is immediately clear where each objective is sending the party.

![Save Game Editor showing the Quests / Events tab with mini-map locator](/images/dark_saveeditor_quests.png)

## Enemies

The enemy data from `DARKLAND.ENM` decoded into a navigable list. All 71 enemy types with their full stat blocks: base attributes, skill ratings, weapon assignments, armor and shield item codes with quality values, palette chunk references, and variant counts. The 82 named enemies reference their type and show their name strings. The tool resolves the image group to the actual IMC files it covers, previews the sprite directly from the loaded catalog with the correct palette applied, and flags known data issues such as invalid item references.

![Enemies editor showing Sergeant1 with sprite preview, attributes and skills](/images/dark_enemies.png)

## Locations and Cities

All 414 world locations with icon type, map coordinates, city size, and name. The location list and city database are presented together so cross-referencing between the two files is straightforward. The 92 city records include all their internal location names (inn, cathedral, market, fortress, kloster, university), building-presence flags, dock destination links, and the nine shop quality ratings.

## Items, Saints & Formulae

The complete item table from `DARKLAND.LST` in a searchable, filterable grid: item code, full name, short name, type, weight, base quality, and value, all decoded from the binary flags into readable columns. Saints and alchemical formulae live on adjacent tabs in the same editor, loaded and saved together.

![Items, Saints & Formulae editor showing the full item table](/images/dark_items.png)

## World Map

The full Darklands wilderness map rendered as a navigable, pannable, zoomable image. The underlying `DARKLAND.MAP` is a 328×932 hex-grid of RLE-encoded tile data drawing from two PIC tile palettes; the viewer decodes that and renders the complete geography (terrain, rivers, coastlines, roads) at any scale. Location icons and labels are overlaid on top. Clicking any tile shows its raw encoding and terrain type in the status bar; clicking a location or city pulls up its full data panel on the right: name, type, size, buildings, services with quality bars, ruler, dock connections, and description. An edit mode allows tile changes to be written back to `DARKLAND.MAP` directly, with undo and revert.

![World Map editor showing Wittenberg selected with full city data panel](/images/dark_worldmap.png)

## Text: Dialog Cards

The `DARKLAND.MSG` dialog files contain the branching conversation trees that appear throughout the game: city menus, quest dialogues, encounter scripts. The tool renders these as structured card lists: select a file from the left panel, select a card, and the right panel shows every text element and option in sequence with a rendered preview below. Cards and elements can be added, removed, and reordered; the result saves back as a valid MSG file.

![Dialog Cards editor showing a branching conversation with rendered preview](/images/dark_dialogs.png)

## Images: PIC and IMC

PIC sprite sheets are decoded and displayed with correct palette mapping: the tool resolves the embedded palette and renders the image as the game would show it, with export to PNG. The example below is `APROCH2.PIC`, one of the city approach background paintings.

![PIC Image Viewer showing a night scene with a cathedral silhouette](/images/dark_pic.png)

Tactical combat sprites from the IMC format get a dedicated animated viewer. Selecting a sprite from a CAT catalog shows the full animation strip with frame-by-frame navigation and playback. The enemy palette from `ENEMYPAL.DAT` is applied automatically so each sprite renders in its actual in-game colours. Individual frames or full contact sheets can be exported.

![IMC Sprite Viewer showing an animated enemy with frame strip](/images/dark_imc.png)

## Fonts

The game's bitmap font sets from `FONTS.FNT` and `FONTS.UTL` rendered glyph by glyph in an editable grid. The whole-font preview on the right shows every character at once; selecting a glyph opens its pixel bitmap for editing. Changes apply immediately to the preview and can be saved back to the font file.

![Font Editor showing the complete Darklands glyph set with editable bitmap grid](/images/dark_fonts.png)

## Archive: CAT Extractor

A browser for the CAT archive format that holds most of the game's packed assets. The directory of any archive opens as a file list alongside a hex view of the selected entry. PIC images can be previewed inline; everything else shows its raw bytes. Individual files and the full archive can be extracted to disk.

![CAT Archive Browser with hex view of a selected entry](/images/dark_cat.png)

## Research

The forward-looking section of the tool. The **DGT Audio** viewer decodes and plays back Darklands' presentation audio files. All `.DGT` files in the game folder are listed; selecting one shows the waveform alongside file metadata: sample count, playback format (unsigned 8-bit PCM, mono, 8000 Hz), and duration. Play and stop controls let you audition the audio directly; an Export WAV button converts any file to a standard WAV for use outside the tool.

![DGT Audio player showing ENDDARK1.DGT waveform with playback controls](/images/dark_dgt.png)

Also here: viewers for image bank formats such as `COMMONSP.IMG` and `BATTLEGR.IMG`, a workbench for the PAN presentation format used in the intro sequences, a standalone DRLE decompressor, and general-purpose hex viewers for data structures that are still being decoded. These are surfaces for ongoing analysis work, not finished features.

![IMG Banks research viewer showing BATTLEGR.IMG in hex view](/images/dark_imgbanks.png)

## A Validation Layer

After loading a game folder, the tool can run a validation pass across the world data: city dock destinations, location reference integrity, enemy item assignments, palette range bounds, dialog option counts. The report is navigable: clicking a finding takes you to the relevant record. It is useful both for catching format decode errors and for finding quirks in the original data.

## Download

**[DARK on GitHub Releases](https://github.com/Arkana-Mechanika-Labs/DARK/releases)**

Unzip and run `DARK.exe`. Requires a Darklands installation; point the tool at your game folder on first launch.

The tool is a community project, developed openly alongside the reverse engineering work documented in these devlogs.
