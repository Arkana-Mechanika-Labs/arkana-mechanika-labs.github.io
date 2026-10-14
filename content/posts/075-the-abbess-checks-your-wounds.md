---
title: "Devlog #075 - The abbess checks your wounds"
params:
  images:
    - /devlogs/075/monastery-healing.png
description: "Asking the Steyr monastery for healing costs an hour and passes through a quiet check of the whole party's Strength and Virtue before the abbess answers."
summary: "A polite refusal at the Kloster turned out to be a real calculation: who is badly hurt, how virtuous the party is, and one roll that almost never succeeds for a healthy party."
date: 2026-10-15T00:00:00+02:00
draft: false
tags: ["Darklands", "reverse engineering", "cities", "church", "restoration"]
width: wide
---

In [Presentation #02](https://youtu.be/wnP9VwCIHuo), the party walks from Main Street to the great churches of Steyr and on to the Kloster. An elderly monk asks their business, the party asks for healing, and after a short wait the answer comes back: the abbess only helps the truly virtuous and those with serious wounds. Visit the city physician instead.

It looks like flavour text. It is not. Behind that refusal is a small but complete decision that reads the whole party, and the reconstruction now follows it.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/075/monastery-healing.png" aria-label="The Steyr monastery menu, a healing request, the wait and the refusal (silent)">
    <source src="/devlogs/075/monastery-healing.mp4" type="video/mp4">
    <a href="/devlogs/075/monastery-healing.mp4">Watch the monastery healing request (MP4).</a>
  </video>
  <figcaption>The daytime Kloster menu, a healing request, the monk's errand, and the abbess's answer. Recorded from an ordinary Quickstart in Steyr.</figcaption>
</figure>

## Getting through the door

The monastery is not open to everyone. Before the first card appears, the original owner checks two things: local reputation must be above −40, and the party's best value in one skill field plus a twentieth of its fame must be above 15. Fail either and the route stops; pass both and the first visit publishes the welcome card and records an event, while later visits receive a shorter greeting.

The church row that leads here goes straight to the monastery after a zero-hour calendar call. We have not found an hour test on that path, so we do not claim one.

## Why the donation row is grey

The first row offers a florin for prayers. In the video it is disabled, and there are two independent reasons the original can disable it:

- a recent donation at this location is still on the event schedule, or
- the purse holds less than 60 pfennigs per active party member, which for four members is exactly one florin.

Our Quickstart party is in the second situation. It is the same purse test that disables the paid row at the convent.

## The abbess's question

Choosing *seek aid in healing your wounds* shows the monk leaving to ask. Acknowledging that card advances the calendar by one hour, and only then is the answer decided.

The check looks at every active party member, not just the leader:

1. **Is anyone seriously hurt?** A member counts if their current Strength is at most nine tenths of their maximum.
2. **If so,** the threshold is the party's average Virtue plus 20, clamped to 0–100.
3. **If nobody qualifies,** the threshold is **0**.
4. One draw from 0–99 decides: the request succeeds if the roll is at most the threshold.

That last case is the interesting one. A threshold of zero still succeeds on a roll of exactly zero, so a healthy party has roughly a one-in-a-hundred chance of being taken in anyway. It is not an unconditional refusal, and our tests keep that rare success path alive rather than simplifying it away.

There are also two different refusals. A party with nobody badly hurt gets the card we saw, sending them to the physician. A wounded party whose roll fails gets a different card. The text the player sees therefore already tells them which half of the check they failed.

## When the answer is yes

Acceptance records a cooldown for this location, which is also what disables the healing row on a return visit, and hands the party to the convent. There, two hours pass while every active member recovers up to two points of Strength, and one of three cards is chosen at random to continue the stay.

The convent's own menu, with paid care and the charity request, was the subject of [Devlog #067](/posts/067-the-price-of-recovery/). For filming we reached it with a development shortcut rather than by getting the party badly hurt first:

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/075/convent-charity.png" aria-label="The convent care menu and an accepted charity request (silent)">
    <source src="/devlogs/075/convent-charity.mp4" type="video/mp4">
    <a href="/devlogs/075/convent-charity.mp4">Watch the convent charity request (MP4).</a>
  </video>
  <figcaption>The convent card staged with the developer console (note the DEV MUTATED marker). The paid row is disabled by the purse; the charity request is accepted.</figcaption>
</figure>

## And sanctuary at noon

The same menu offers sanctuary. In daylight, the monk simply shakes his head: there is no tradition of holy sanctuary here, try the Pfarrkirche around the corner. That card changes nothing: no time passes, no roll is made, no event is written, and acknowledging it returns the party to the church. The night monastery's refusal, which does cost an event record, was covered in [Devlog #069](/posts/069-behind-the-sanctuary-door/).

## What remains closed

- Paid care and the charity request currently require exactly four active members, matching the cases we have verified.
- A stay that would cross into a new month stops at its boundary rather than guessing how the calendar rolls over.
- If the event table is full when the cooldown or donation record must be written, the route stops instead of dropping the record.
- How the night church naturally reaches the night monastery is still open; we only claim the day route shown here.

A monk's polite refusal turned out to read Strength, Virtue, the calendar and the event table. That is Darklands in miniature: very little on screen, a surprising amount underneath.
