---
title: "FAQ"
toc: true
width: normal
---

## Playing

### Is it playable?

Yes. Version 0.9.0 plays the whole game: character creation, cities, inns and shops, guilds, banks and churches, the world map and its encounters, real-time battles, camping, saints and alchemy, saving and loading. [Download it here](/download/). Version 1.0 will follow once the remaining faithfulness checks are finished.

### Do I need the original game?

Yes, your own copy of Darklands 483.07, for example the GOG or Steam release. Nothing from the game is included: the program reads your installation, and finds a GOG or Steam copy by itself.

### What do I need to run it?

Windows x64. No .NET installation and no DOSBox: unpack the zip and start `DarklandsRP.exe`.

### Does it play like the original?

That is the point. Every rule is rewritten from the original program and checked against it, the screens, music and sound are the original's, and even the original's bugs are kept, because they are part of Darklands. What knowingly differs is listed openly, and the oddities are collected in [Bugs & Oddities](/formats/original-bugs-and-oddities/).

### Can I use my old saved games?

Yes. Saves go to the game's own `SAVES` folder, shared with the original both ways.

### What about the MT-32 music?

Put your MT-32 or CM-32L ROM files in the `MT32_ROMS` folder next to the program; the game's own Roland driver then plays through an MT-32 emulation. Without them the Sound Blaster Pro's FM music plays. AdLib and Sound Blaster are always available.

### Can I play in a bigger window, or full screen?

Yes: `darklands.settings.json`, created next to the program on the first run, sets the window scale, any resolution, or full screen, and also the sound card and more.

### Is the old darklands.net FAQ still right?

Mostly. [The Classic FAQ, Checked](/classic-faq/) goes through it section by section against the original program's rules, and gives the corrections and the exact figures.

### Where do I report a bug?

On the [Discord](https://discord.gg/HjzWvmHhqZ), or as an issue on [GitHub](https://github.com/Arkana-Mechanika-Studios/darklands-restoration).

## The project

### Is it a remake or an emulator?

Neither. It is a reimplementation: the original's game logic rewritten in C#, rule by rule, and run natively. The screens, music and sound are produced from your copy of the game.

### How do you know it is faithful?

The original program's own functions run in an emulated processor, from your copy of the game, next to the C# on the same inputs — tens of thousands of cases — and every card of the game runs against its original. Every deliberate difference, every original bug kept, and every open question is listed with its reason. [How it is made](/method/) explains more.

### Is the source code available?

Yes, on GitHub: [Arkana-Mechanika-Studios/darklands-restoration](https://github.com/Arkana-Mechanika-Studios/darklands-restoration). The game logic is kept apart from graphics, sound and input, so other hosts can be built on the same core; each piece of code cites the place in the original program it reproduces.

### Why C#?

The goal is a readable, testable rewrite of the original's behaviour that runs natively. C# lets each rule be written clearly, tested quickly and checked against the original; the original program, not the choice of language, defines the behaviour.

### How is AI used?

AI assistance helped read the original program, write the C#, and build the checks. Nothing is taken on trust: what the C# does is compared with what the original program does, and the open questions are listed rather than guessed.

### Didn't the community already document Darklands?

Community research documented the file formats, and the [format reference](/formats/) builds on it and credits its authors. The program itself also decides how menus, time, combat, events and encounters work, which the file formats alone cannot answer; recovering those decisions is the restoration's additional work.

### Where are the old devlogs?

In the [archives](/archives/), with the earlier presentations and method. They record what was known at the time; later findings may supersede them.
