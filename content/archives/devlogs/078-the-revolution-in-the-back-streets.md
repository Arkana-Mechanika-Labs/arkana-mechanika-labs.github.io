---
title: "Devlog #078 - The revolution in the back streets"
params:
  images:
    - /devlogs/078/back-streets.png
description: "Darklands 483.07 ships a nineteen-file political quest about rebels, handbills, marches and sieges. We traced how much of it the shipped game can still reach, and where the trail goes cold."
summary: "A Discord member remembered stumbling once into a political campaign in a city's back streets. The game still contains it: 230 cards of revolution and counter-revolution, a working doorway, and a trail that goes cold after the planning stage."
date: 2026-10-15T00:30:00+02:00
draft: false
tags: ["Darklands", "reverse engineering", "cities", "hidden content", "quests", "restoration"]
width: wide
aliases: ["/posts/078-the-revolution-in-the-back-streets/"]
---

{{< callout type="info" >}}
**Archived devlog.** Written during the earlier development of the restoration; later findings may supersede it. The current version is [Darklands Restoration Project 0.9.0](/download/).
{{< /callout >}}

A member of our Discord recently shared a memory from years ago: once, and only once, while wandering a city's side streets towards some unknown destination, their party was drawn into a kind of political campaign. It never seemed to lead anywhere, and they never saw it again.

That memory is almost certainly real. Darklands 483.07 still ships an entire political storyline, and part of the route into it is still present in the original code. This post sets out what we know, what we can prove, and where the trail currently goes cold.

## Nineteen files of revolution

The game's message files include nineteen consecutive resources, `$REVOL00` to `$REVOL18`, with 230 cards between them. Read in order, the prose describes a complete two-sided quest:

| Stage | What the cards describe |
| --- | --- |
| The approach | arriving at the house of a political organiser by day or by night |
| The offer | an interview and a dangerous job: carrying handbills for the cause |
| Planning | faction attitudes, where to post handbills, influence, secrets, raids |
| Investigation | sounding out the guilds, merchants, clergy and common people |
| Crisis | an arrested organiser to rescue or abandon; a government warning that rebels are marching |
| Confrontation | headquarters surrounded, a rally, escorting prisoners through a hostile crowd, a march met by the city guard |
| Siege | the rebels besieging the fortress or the council hall, and knights arriving from the countryside to break the siege |
| Endings | a government victory with the leaders delivered to the dungeon, or a rebel victory, a new council and a celebration |

The planning card alone lets the party discuss marching on the council hall or the fortress *to replace the government*, or *arresting the rebels for treason*. You could serve either side.

This table describes the **text**. A card's prose tells us what the designers wrote; only the code that displays it and acts on the choices tells us what the shipped game can actually do.

## The doorway is still there

Steyr's side streets offer *other locations you remember*. That leads to a card we can now show in the reconstructed engine, reached from an ordinary Quickstart in Steyr:

<figure>
  <img src="/devlogs/078/back-streets.png" alt="The back streets card: Trudging along back streets and alleys, you head for the main street or another side street" width="960" height="600" loading="lazy" />
  <figcaption>The back-streets card in Steyr. In the shipped data it can also offer “the home of …” two named people, but only when particular events are active. Here they are not.</figcaption>
</figure>

The card's encoded text has two more options: *the home of $NamedOneName* and *the home of $NamedTwoName*. The names are generated at random from the game's own name tables, 88 female and 108 male first names plus a surname. That fits our community member's memory of heading somewhere unknown.

Those two rows only appear while specific events for the current city are on the schedule. We know exactly which event records the original tests for. We do not yet know which part of the game creates them. That is the most likely reason the scene is so rare, and it is also the first open question.

The same card also encodes six more destinations whose text is just the numbers 2 to 7. The original never offers them. They are placeholders.

## From the door to the plan

Following a named house leads into the revolt files. This much of the chain is proven from the original code:

1. **The approach.** By day, the party can ask around on the street, request an interview, boast and ask for work, pick a lock, use an alchemical distraction, or leave. By night there is a different version of the same house.
2. **The interview.** A successful approach can open with the organiser's greeting: *“Ah, bold heroes at last!”*
3. **The offer.** The organiser explains that people have been beaten and killed for carrying handbills, and asks why you want the job. You can say you need the money, that the city needs new leadership, that the government must be protected, that holy inspiration led you here, or pray for guidance. Only one of the two political answers is offered, depending on a value that appears to record which side the organiser is on.
4. **Accepting.** If you take the money, an hour passes and one roll is made against a threshold that the original computes from the current state of the game: ratios of active event records combined with party values. We have not yet established what those ratios mean in the story. On a failure the organiser declines. On success the game records a quest event and moves on to the planning card.

So the shipped game can carry a party from the back streets to the revolution's planning table. Beyond that point we have not yet decoded how the later stages are reached. The text exists for all of them, but text alone is not evidence that play can get there.

## What is provably hidden

Some options are definitely never offered by the code that shows these cards:

- by day, *draw weapons, kick down the door, and charge inside*. Its night-time counterpart is different: there, an event can make the forced entry available, so it is conditional rather than hidden. That is the same trap described in [Devlog #062](/archives/devlogs/062-the-street-only-thirty-two-cities-have/), where a street that looked hidden turned out to depend on the city;
- several rows on the approach cards and two on the offer card whose text is just a number.

They join the other dormant branches we have catalogued, such as Soldier's Road in [Devlog #061](/archives/devlogs/061-the-road-darklands-refuses-to-show/), which the original also never shows even though its cards and merchant still work when forced. We keep these hidden in the restoration, as the original does. We document them because they say something about how the quest was built: it had more options than the shipped version offers.

## Where the trail goes cold

The investigation is parked at the money option of the offer card. Its threshold can be computed in two ways; one is fully verified, and the other leads into a short routine whose exact boundaries our two decompilers do not agree on. We tried to settle it by observing the original game running, and the emulator crashed three times in a row. We stopped there. The next step is to establish that routine from the original bytes alone, without forcing anything at runtime.

Beyond that lie the questions that matter most:

- what creates the events that make the named houses appear;
- how the planning stage connects to investigation, crisis, confrontation and the sieges;
- whether an unmodified game can reach any of the later files at all.

## Was it more complete in an earlier version?

It is tempting to conclude that the quest worked in an earlier release and was disconnected later. Some things point that way: the size and coherence of the text, choice tables kept intact for options that are never offered, and stages that depend on timed events. We keep that idea as a **hypothesis**, not a finding. All the analysis in this post uses the final 483.07 release. Testing the idea means comparing the revolt code and its `MSGFILES` against earlier versions of the game, and that comparison has not been done yet.

## What this means for the restoration

Our rule does not change: the restored game behaves the way the original can be shown to behave. The doorway, the approach, the offer and the planning card will be restored as the code allows, under the same conditions. Content the original never offers stays hidden. As discussed in [Devlog #061](/archives/devlogs/061-the-road-darklands-refuses-to-show/), any future option to explore dormant content would be separate and clearly labelled, never the default. Anything we have not yet decoded stops at a clear boundary rather than being filled in with a guess.

What a faithful reconstruction can do is show how much of the revolution exists, which parts the shipped game can still reach, and where its trail ends. One player's memory of a single strange afternoon in a side street is a good reason to keep looking.
