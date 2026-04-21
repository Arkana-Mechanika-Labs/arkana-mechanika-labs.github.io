---
title: "Devlog #026 - What comparing the English and German editions actually bought us"
date: 2026-04-21T12:00:00
summary: "What the German Edition Revealed About Darklands’ Data, Tokens, and Runtime Structures"
---

I had completely forgotten that a German version of Darklands even existed.

Luckily, James, a fellow member of the Darklands Yahoo Group who goes by “MarbleMunkey,” reminded me and shared some useful leads. It sounded interesting at first, but not necessarily groundbreaking. A lot of cross-version comparisons look promising and end up confirming the obvious. Translated strings differ, UI elements shift a bit, offsets move around. That is useful, but it rarely changes the bigger picture.

This one turned out to be much more than that.

{{< figure src="/images/de_darklands_00.png" caption="The German edition's startup screen. Once it was on hand as a comparison target, it quickly became more than a curiosity." >}}

The German edition is not a different engine, and it does not hide some alternate master format that would invalidate the work done on the English version. If anything, it reinforces it. But once that baseline is confirmed, the comparison starts paying off in ways that go deeper than expected.

It reveals a richer runtime message and token system than the English data suggests, sharpens the meaning of several previously ambiguous city-data strings, and provides a second structural view of at least one real loader-managed object inside the executable.

That combination makes this far more valuable than a simple translation diff.

## First, the reassuring part

At the data format level, the German edition mostly confirms what the English version already suggested.

The core formats look structurally stable across both editions. `CTY`, `LOC`, `DSC`, `LST`, `SNT`, `ALC`, `ENM`, along with shared `CAT`, `IMG`, `PAN`, `MAP`, and sampled `DGT` all line up the way you would hope. Counts match. Numeric fields match. Flags and coordinates behave the same. Nothing points to a rewrite of core mechanics for localization.

What changes is exactly what should change: names, descriptions, and other user-facing text.

That matters more than it might seem at first. It means the current parsing work is not sitting on shaky ground. The German edition acts as a second witness that the structure is sound.

It also helps with interpretation. In a few cases, German labels feel cleaner or historically more plausible than their English counterparts. That does not mean the English version is wrong, but it does give a useful point of comparison when something looks ambiguous.

So if the question is whether the German version destabilizes the current understanding, the answer is clearly no. It strengthens it.

## The message system is where things get interesting

The real surprise is not in the archive formats or graphics. It shows up in the executable-side token system and the message archive.

The German `MSGFILES` are not just translated copies. They are smaller, reorganized, and in many cases clearly reshaped.

The stock English `MSGFILES` archive contains `419` entries. The German one contains `365`. In other words, the German archive is not a one-to-one rewrite of the English set. It is effectively a strict subset, with dozens of English message files missing entirely, and with many shared entries differing in size, card count, and token usage.

That is already more interesting than a straight translation pass.

More importantly, the German executable expands the runtime token vocabulary.

The familiar variables for cities, locations, dates, and actors are still there. But the German version adds a set of grammar-sensitive tokens like `his1` through `his6`, their capitalized variants, `him1` and `him2`, and a token labeled `CON`.

These are not leftovers or unused artifacts. They are actively used in the German message files.

The contexts where they appear make their roles fairly clear. The `his` family behaves like inflected possessive forms, the `him` tokens look like inflected object forms, and `CON` behaves like a compact alias for the current chosen character, essentially functioning like a shortened `ChosenOneName` token in context.

A few examples make this much clearer:

- `his1` behaves like `seinen`
- `his2` behaves like `seiner`
- `his3` behaves like `sein`
- `his4` behaves like `seine`
- `his5` behaves like `seinem`
- `his6` behaves like `seines`
- `him1` behaves like `ihm`
- `him2` behaves like `ihn`

That is a meaningful discovery.

It shows that the German localization did not just translate text. It pushed the runtime substitution system into a space that supports richer grammar. The English data alone would never have suggested that level of capability.

Even more interestingly, some city/location variables are definitely live in shipped content, while others still look dormant. Tokens like `$citySquare`, `$councilHall`, `$cityBarracks`, `$marketplace`, `$fortress`, `$pawnshop`, `$hospital`, `$poorhouse`, `$slum`, `$monastery`, `$cathedral`, and `$cityChurch` are visibly used in shipped cards. Others such as `$imperialMint`, `$CityLocation`, `$whorehouse`, `$warehouse`, and `$docks` still do not appear in shipped English or German message text.

That distinction matters because it helps separate truly active runtime vocabulary from variables that were probably planned, partially implemented, or simply unused in the final content.

Even if nothing else had come out of this comparison, that alone would have made it worth the effort.

## The German strings also clarified some of the city data

One of the nicest surprises was that the German edition helped interpret several previously uncertain strings in `DARKLAND.CTY`.

{{< figure src="/images/de_darklands_01.png" caption="A German in-game city screen. These localized labels and landmark names ended up being some of the strongest clues for interpreting ambiguous CTY-only fields." >}}

A string slot that looked ambiguous in English contains `Munzenplatz` in six cities. In the German edition, that same slot becomes `Reichsmünzstätte`.

That is a much stronger clue than the English alone provided. It makes the connection to the executable variable `$imperialMint` feel much more plausible. At this point, that slot looks very likely to identify cities with an imperial mint-related landmark.

Those six cities are:

- Köln
- Freiberg
- Mainz
- Frankfurt am Main
- Trier
- Prag

Another uncertain CTY string slot also became clearer. English entries like `Zeughaus` often become `Kaserne` in German, while more specific names such as `Hahnentor`, `Eschenheimer Turm`, `Pulverturm`, and `Schloss Neuhaus` remain as landmark-style proper names.

That strongly suggests this field is not a normal location entry like those found in `LOC`. Instead, it looks much more like a city-specific fortification, garrison, or civic-defensive landmark slot.

That matters because none of these names appear as normal `LOC` records. They seem to live only in `CTY`, which makes them look less like ordinary visitable locations and more like special city labels or partially surfaced runtime landmarks.

The German edition did not just translate these names. It made their semantic role easier to see.

## The executable comparison improved once the approach changed

At first, it is tempting to compare executables as if there were a single global offset difference. That approach does not hold up here.

What remains stable between the English and German versions is not a fixed shift in file positions. What remains stable is deeper: resolver record identity, logical module boundaries, internal structure, and recurring value patterns.

Once the comparison moved to that level, the German executable became much more useful.

A good example is resolver record `0x0088`.

This module is ideal for comparison because it is clearly localized, clearly managed by the loader, and still structurally similar enough across both versions to study in detail.

The first clear difference between the English and German versions lands directly on a localized text table. That alone is useful, since it shows that loader-managed chunks can contain embedded string data without losing their overall structure.

But the real insight came later, once it became clear that nearby pointer-like regions were not just simple string tables.

## `0x0088` is not just text with noise around it

The deeper analysis leads to a stronger conclusion. This module contains a conserved serialized runtime object.

That is the point where the comparison stops being about localization and starts becoming a real reverse-engineering tool.

The opening of this object can now be modeled as a shared nine-part sequence that exists in both versions with the same structural pattern. The exact values differ, but the pattern itself holds.

More importantly, those differences are not random. They fall into consistent families. One set behaves like a pair-based seed, another looks like a special or override value, and another acts like a default baseline.

This is exactly what you want from a cross-edition comparison: a stable shape with meaningful variation, not noise.

From there, the structure continues in recognizable phases: a default-heavy continuation, a transition into a new family, a short-lived precursor value, then a stable basis for the next group, followed by another gateway into a third family, and finally a clean break where both versions diverge into unrelated data.

At that point, it no longer makes sense to describe `0x0088` as localized text with some odd structures nearby. It is much better understood as a staged serialized object embedded inside a loader-managed module.

That is a far more interesting result.

## Why this matters beyond `0x0088`

The value here is not that one module was decoded.

The real takeaway is what this comparison makes possible.

It confirms that the current parsing work is built on solid assumptions. It reveals runtime token capabilities that the English data does not advertise. It sharpens the semantics of some previously uncertain city-data landmarks. And it helps separate true runtime structure from localization noise inside executable-managed data.

That last point is the most important.

Without the German version, it would have been easy to misinterpret parts of `0x0088` as a pointer table, a strange string structure, or just noise around translated content.

With the German comparison, it becomes possible to say something much stronger. There is a stable object shape, distinct phases, consistent value families, and a real boundary that exists in both versions.

That is a different level of understanding.

## Current bottom line

So what did this comparison actually buy us?

Quite a lot.

It confirmed that the main data formats are structurally stable. It showed that the German version uses a richer token system, especially for grammar-sensitive substitutions. It clarified several ambiguous city-data strings, including a very likely imperial-mint landmark slot and a probable fortification or garrison landmark slot. And it exposed a conserved runtime object inside at least one loader-managed module.

That makes the German edition something to keep around permanently, not as a curiosity, but as a reliable point of reference for validation, naming, token behavior, landmark semantics, and structural comparison.

## What comes next

Two directions stand out.

One is focused on the message system. The goal there is to trace how the German executable handles the inflected pronoun tokens, compare how both versions dispatch tokens at runtime, and determine whether the richer vocabulary is hardcoded or driven by data.

The other direction is focused on executable structures. That means connecting the `0x0088` object to the code that uses it, checking whether similar objects exist in other modules, and figuring out whether this is part of a broader class of runtime data structures.

There is also a smaller but very useful line of work around city semantics: determining whether the `Reichsmünzstätte` / imperial-mint slot and the fortification landmark slot were fully used by the shipped game, partially implemented, or left as semi-orphaned structures in the final data.

Either way, the German comparison has already proven its value.
