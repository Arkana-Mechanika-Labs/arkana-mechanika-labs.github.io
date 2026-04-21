---
title: File Formats
weight: 1
---

On-disk format documentation for every Darklands data file, produced by cross-referencing community research with reverse-engineered code from DARKLAND.EXE.

The primary source for community-documented formats is [Wendigo's Darklands repository](https://github.com/vvendigo/Darklands) ([wendigo.online-siesta.com/darklands](https://wendigo.online-siesta.com/darklands/)), which preserves the XML format specifications originally assembled by Merle, Quadko (Joel McIntyre), and others. For general Darklands reference — game mechanics, items, locations, and lore — [darklands.net](https://www.darklands.net) by Matt Wirkkala remains the authoritative community resource.

All formats documented here are based on the original game files and are public knowledge. Sources are cited per page.

| Section | Contents |
|---------|----------|
| **Catalog Files** | CAT archive format; BC combat tile archive; IMAPS encounter grid |
| **Presentation** | PAN animated scene format; BANNER.DAT startup banner |
| **Graphics** | PIC sprites; IMC icons; MSG font bitmaps; COMMONSP.IMG startup sprite bank; enemy palettes |
| **Audio** | DGT raw PCM audio |
| **World Data** | Locations, cities, city descriptions, enemies, items, alchemy, saints, CFILE.DAT |
| **Common** | Shared structures are currently documented across the Save File and Structs pages rather than in a standalone common note |
| **Save File** | Full save-game format including character, item, and quest structures |
| **Temporary** | Runtime files created on save-load: CACHE.TMP, CHARACTR.TMP, LOCS.TMP |
| **Structs** | Shared in-memory structures (character, item, etc.) |
| **Wilderness Map** | DARKLAND.MAP RLE tile format |
| **Executable** | Main executable reference note for `DARKLAND.EXE` |
| **Auxiliary Executables** | MGRAPHIC.EXE, MISC.EXE, MPSCOPY.EXE, DKED.EXE, DKQUE.EXE, installer tools |
