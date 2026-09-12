---
title: "Devlog #071 - Before the battlefield appears"
date: 2026-09-11
draft: false
tags: ["combat", "graphics", "animation", "reverse-engineering", "darklands"]
description: "From attacking the city guards to the preparations behind the first combat frame."
summary: "From attacking the city guards to the preparations behind the first combat frame."
---

“Draw weapons and attack the guards!”

It is a short choice. From the player's side, it leads toward a battlefield. From the reconstruction's side, it opens a chain of encounter preparation, map generation, resource loading, party placement, and actor initialization.

The current combat branch follows that specific journey. The first native SDL battlefield frame is not complete yet, but the work between the menu and that frame has become much more substantial: connected preparation routines and selected sword- and bow-guard loading chains now execute in C# and can be compared with the original.

This is a progress report from inside that transition.

## Start before the battle exists

The reference journey began in the original game with a fresh Quickstart party. It continued to the city gates and selected the attack choice naturally, without using a saved combat fixture or editing game memory to supply the entry state.

That matters because a battlefield snapshot begins after many of the difficult decisions have already been made. It contains a map, participants, resources, and inherited state. Replaying from it can tell us useful things about combat, but cannot explain how the game created that situation.

Our target starts earlier: with the choice that asks the game to construct it.

Even there, the visible row number is not a reliable action identity. Hidden and disabled choices affect how the menu is presented. We follow the encoded source choice and its actual callback and action, rather than assuming that the fourth line on one screenshot will always mean the same thing.

## Preparing a place to fight

The selected action constructs the encounter arguments using the live city and party state and the original sequence of random calls. Those arguments feed the preparation machinery rather than a manually assembled list of combatants.

The reconstructed preparation owner now connects guard and map generation with the required tables, portraits, battle graphics, animation storage, and item names. In three selected comparisons, the C# preparation ran continuously and matched the corresponding original results under declared platform-test conditions.

There was no restoration of a captured original snapshot between each child routine. The output produced by one reconstructed child became input to the next.

That is a different milestone from having a collection of individually tested functions. It begins to show that the functions agree about the state they share.

The platform qualification still matters: these tests supply bounded observations for file, allocation, and other transport operations. They do not yet establish that the clean graphical runtime arrives with all the right incoming state or has every concrete service needed to continue.

## One guard's walk animation

A particularly tangible part of the work is a guard sprite named `E02wkSW.imc`, stored inside `E00C.CAT`.

Loading it means more than finding an image. The original path decodes 19,636 bytes, interprets the metadata, installs the sprite data, and prepares seventy-two frame pointers for the code that will use it.

An earlier selected decoder path reproduced a prefix but stopped when this resource required another input refill. A convincing partial image would not have made that loader complete. The full selected decoder now handles the two-read path and has been compared against the original output, along with its stream bookkeeping and memory effects.

The surrounding sprite routine and initial stance have also been reconstructed. They establish the descriptor and frame state that a combatant will need before it can be drawn or animated correctly.

This is the point where a compressed archive member starts becoming a usable actor resource.

## Beyond the first guard

The work now extends through complete selected group-loading returns for both the sword guard and a bow-guard path using `E00wkBW`.

The bow path provides a useful second case because it must preserve inherited provider-cache behavior while following its own allocation, loading, sprite, and stance sequence. The comparisons begin at the group routine's entry and let the actual reconstructed child routines run through to the return.

One small initialization detail illustrates why this surrounding state matters. The original fills a ten-entry queue with the values zero through nine. Ten zeroes occupy the same amount of storage but do not represent the same state. The recovered ordering is now preserved and covered by tests that reject the zero-filled alternative.

Correct pixels are necessary. Correct preparation for using those pixels is necessary too.

## The remaining distance

The selected preparations and guard-loading chains are internal reconstruction milestones on a working branch, not a newly playable combat mode. Their grouped release and the larger integration still remain to be completed.

The enclosing controllers must be composed, remaining platform and resource-lifetime questions resolved, and terrain and actor rendering connected to the SDL route. Some controlled original continuations deliberately supplied failed expanded-memory mapping responses; they do not prove successful mappings or every original DOS allocation outcome.

We still need to verify that the normal menu route supplies the starting state assumed by these tests. Passing an internal comparison cannot substitute for that connection.

The next visible milestone is therefore quite specific: the reconstructed game must reach and draw its first battlefield as the consequence of selecting the original attack action. A standalone viewer displaying extracted graphics would answer a different question.

There is still work between the click and the frame. We can now point to much more of that interval as executing code, with original comparisons behind it—and to the remaining gaps without hiding them inside a screenshot.
