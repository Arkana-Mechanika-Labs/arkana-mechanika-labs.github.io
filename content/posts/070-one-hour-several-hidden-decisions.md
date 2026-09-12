---
title: "Devlog #070 - One hour, several hidden decisions"
date: 2026-09-08
draft: false
tags: ["events", "calendar", "verification", "reverse-engineering", "darklands"]
description: "Why reproducing the clock is not enough to reproduce the game."
summary: "Why reproducing the clock is not enough to reproduce the game."
---

A small instruction in a reconstruction can hide a very large assumption:

```text
Advance time by one hour.
```

It sounds precise. The number is known, the unit is known, and the clock provides an obvious thing to check afterward.

But a Darklands action can arrive at the correct hour with the wrong party state, the wrong event records, or a random sequence that has already drifted away from the original. The clock is an output of the operation. It is not the operation's entire result.

A recent investigation of the nighttime monastery made that distinction concrete. It also gave us a useful test of the project's AI-assisted research process: could a second investigation recover the same behavior without first being told what to expect?

## Asking for help takes more than a roll

The monastery action we followed displays an initial message, waits for acknowledgement, advances time by one hour, and then makes its own random check. The outcome determines which response and destination follow.

A quick description could reduce that to a message, a clock increment, and a success roll.

The original calls something larger. Its time-advancement service also maintains party and event state. At a midnight crossing, the inspected path can consume an additional bounded random draw and further draws for each surviving active character before control returns to the monastery's own check.

That means the visible success roll is not necessarily the next draw after the player clicks.

Skipping the maintenance would not merely remove background bookkeeping. It could change the state and random inputs used by what happens next. Both implementations might still display one o'clock, and both might even select the same response on a particular run. That apparent agreement would leave the missing work undetected.

## Following the whole action

The useful unit of investigation is therefore the path from a player's choice to the next stable result:

```text
Initial message and acknowledgement
    -> original time-maintenance service
    -> action's own random check
    -> result message and acknowledgement
    -> destination controller and its first stable screen
```

Each step has its own effects. The successful monastery inquiry, for example, routes the party toward convent care. The inquiry itself does not perform the later convent recovery. Putting healing into the inquiry because its text sounds helpful would give the correct general impression while placing the effect in the wrong operation.

That distinction matters when the same destination has several ways in, or when an acknowledgement separates what has happened from what is still pending.

## An investigation kept blind

For this experiment, a Scout first explored the relevant monastery code and prepared a dossier of likely routes, calculations, and dependencies. That dossier was a research aid, not permission to implement its conclusions.

A separate validation pass then worked from the original executable and resources without opening the Scout's account. Its report was frozen before the two were compared.

The broad routing agreed. That was useful confirmation, but the differences were the more valuable part of the exercise.

One concerned a picture restored after a result card. Another concerned the distinction between an event record and a city-record word. A failure branch with an existing event modified the city record; it did not reschedule or rewrite that event merely because the event had selected the branch.

Another concerned an arithmetic helper that kept only the low byte of a result and then widened that byte again. Describing it as an ordinary signed average lost a transformation present in the original instructions.

These are not dramatic-looking mistakes. They are exactly the sort that can survive a readable summary and become permanent when that summary is turned into code.

## The difference between discovery and acceptance

AI assistance is especially useful when there are many possible places to look. A broad pass can identify a controller, follow its callbacks, propose the meaning of a field, and point toward a promising experiment.

The danger is treating that useful account as settled behavior. Once an interpretation has a good name and a coherent story, the next pass can unconsciously inherit it.

The blind comparison gave us a way to challenge that. Agreement on the main route did not conceal disagreement over its effects, because the second account had already committed to what it independently found.

Nor did the disagreements send us back to indiscriminate exploration. They identified specific work: preserve a picture restoration, distinguish two different records, retain the byte conversion, and follow the time helper far enough to account for its consequences.

## What reached the engine

The subsequent selected monastery implementation incorporated those findings. It preserves the recovered message and acknowledgement order, uses the supported original calendar relation, makes the action's own check afterward, and keeps the destination's later effects with that destination.

Unsupported month-end and event-maintenance alternatives remain explicit stopping points. We have not turned one verified one-hour route into a claim that every possible calendar transition is complete.

This is real progress even though the most revealing screenshot might contain an entirely ordinary clock. The change is in what the engine now does before that clock settles, and in the mistakes its tests prevent.

Reconstructing an hour means recovering what Darklands does with the hour—not merely writing a later number on the screen.
