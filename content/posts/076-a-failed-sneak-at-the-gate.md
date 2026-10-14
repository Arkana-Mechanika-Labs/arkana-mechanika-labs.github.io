---
title: "Devlog #076 - A failed sneak at the gate"
params:
  images:
    - /devlogs/076/gate-sneak-challenge.png
description: "Returning to Steyr from the world map: the guarded gate card, a party-wide sneak roll, the guard challenge, the chase, what surrender takes, and a visit from the priest."
summary: "One bad roll at the city gate leads through a challenge, a chase, a confiscation and a prison cell. Every step reads party state, and one of them taught us something even in failure."
date: 2026-10-15T00:00:00+02:00
draft: false
tags: ["Darklands", "reverse engineering", "cities", "world map", "prison", "restoration"]
width: wide
---

[Devlog #056](/posts/056-from-the-city-guard-to-a-cell/) followed the chain from a guard challenge into a cell. Since then the world map has arrived, and with it a new way to reach that chain: walking back to a city whose guards remember you.

In [Presentation #02](https://youtu.be/wnP9VwCIHuo), the party returns to Steyr from the countryside, approaches the walls and tries to slip past the gate. It goes badly. This post follows each step and what the original actually decides along the way.

One qualification first: this run begins from a controlled post-battle starting point, used to open the world map, rather than from a single natural playthrough. Everything after it is ordinary keyboard and mouse input through the reconstructed routes.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/076/gate-sneak-challenge.png" aria-label="Approaching Steyr, the guarded gate card, a failed sneak and the guard challenge (silent)">
    <source src="/devlogs/076/gate-sneak-challenge.mp4" type="video/mp4">
    <a href="/devlogs/076/gate-sneak-challenge.mp4">Watch the gate approach and failed sneak (MP4).</a>
  </video>
  <figcaption>The guarded gate of Steyr. Persuasion and the saint row are unavailable; the sneak attempt fails and the guards recognise the party.</figcaption>
</figure>

## The right card, finally

Arriving at a city first shows the approach, and entering the gate shows one of several gate cards. When the guards are on alert, the original selects card 18: *the guards at the gate are numerous and nervous*, with a toll, persuasion, a sneak attempt, an alchemical distraction, a saint, an attack, or reconsidering.

Our first implementation showed the wrong card. The original pushes the card number as the byte `12h`, which is decimal 18; we had written decimal 12. Card 12 is the failed-saint card, which contains a pronoun token, so the mistake surfaced as an apparently missing pronoun binding rather than as an obviously wrong number. The fix was a single constant. The investigation that confirmed it replayed the original selection bytes and checked both cards in the original message files.

It is a good reminder of why we keep original addresses and values next to the code: a plausible-looking failure pointed somewhere else entirely.

## Why two rows are grey

The guards are on alert because an earlier fight at this gate left an event on the schedule. While that event is due, the original disables the persuasion row and, as we will see, makes sneaking harder. The saint row is unavailable because the party does not currently qualify for it.

The local reputation in this run is −31, which the game calls *suspected*. Reputation is not what routes the party here; the event state is.

## A sneak roll for the whole party

*Sneak in, relying on your agility and streetwise* is not a roll for the leader. The original averages over every active member:

1. Each member's Agility is adjusted for encumbrance: unchanged when lightly loaded, reduced to two thirds, then a third, and finally to 1 as the load grows relative to Endurance plus Strength.
2. The threshold is the party's average adjusted Agility plus its average Streetwise, divided by two.
3. While the guards' alert event is due, the threshold is **halved**, then clamped to 1–99.
4. One draw from 0–99 succeeds if it is at most the threshold.

In our run the roll was 69, and the halved threshold was lower. (The run records the roll, not the threshold.)

Failure writes an event that disables sneaking at this gate for a while. Because the guards are already on alert, the original then runs a party-wide Streetwise improvement step in its *failure* mode before the challenge. In our run Gretchen's Streetwise went from 11 to 14, so even failing at the gate taught her something. An hour passes, and the guard challenge begins.

## Recognised, and running

The guard's line, *I recognize them! They're wanted here, arrest them all!*, is the challenge card's fixed text. Its rows depend on the situation: bribery is only offered when the party arrived from particular earlier states, and the bomb and saint options depend on items and known saints.

Running involves no roll at all. It costs an hour and starts the chase through the streets.

## What surrender takes

Surrendering during the chase leads, after three hours, into the prison owner, which begins with the original all-party loss routine:

- **All money is lost.**
- For every active member, each item gets a score from two bytes of its item record. High-scoring items are always taken. Others are taken depending on a roll against the member's average of Agility and Stealth, so nimble, stealthy characters keep more of their belongings.
- Taken items are also removed from any equipped slot, and load is recomputed.

In our run the purse went to zero, two members lost two items each, including Gunther's club, and two kept everything.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/076/surrender-cell-priest.png" aria-label="The chase, surrender, confiscation, the prison cell and the priest (silent)">
    <source src="/devlogs/076/surrender-cell-priest.mp4" type="video/mp4">
    <a href="/devlogs/076/surrender-cell-priest.mp4">Watch the surrender, cell and priest (MP4).</a>
  </video>
  <figcaption>Surrender, confiscation, the cell, a visit from the priest, and back to the cell.</figcaption>
</figure>

## A priest, and a second search

The cell offers nine possibilities, from picking the lock to waiting for the magistrate; some depend on items or on the party's composition. Asking for a priest costs three hours and opens a new card: confess, ask for help escaping, ask for a good word with the magistrate, or leave him alone.

Leaving him alone returns to the prison owner through its normal entry, and that entry runs the loss routine again. In our run another member lost an item on the way back to the same cell. A shortcut that simply redrew the cell would have looked identical and been wrong.

## What remains closed

- At the gate: attacking the guard, a rejected toll, and the persuasion path into the challenge.
- In the challenge and chase: fighting, talking, bribing, bombs and saints, and capture into combat.
- In the cell: everything except the priest's visit and returning to the cell, including waiting for the magistrate and every escape attempt.
- Entering the city after the gate. The city interior on this route is still ahead of us.

A failed sneak, a short run and a surrender took one bad roll, three owners and a confiscation routine. The reconstructed engine now walks all of it from the world map, and stops honestly where the original's remaining branches are still unexplored.
