---
title: "Devlog #069 - Behind the sanctuary door"
date: 2026-09-07
draft: false
tags: ["gameplay", "sanctuary", "city-navigation", "reverse-engineering", "darklands"]
description: "Waiting for daylight, negotiating with the guards, and finding a way out."
summary: "Waiting for daylight, negotiating with the guards, and finding a way out."
---

The party has reached sanctuary. That settles where it is, but not what happens next.

There is still a city outside, a reputation attached to the party, and a clock moving toward daylight or darkness. Waiting, asking about the authorities, surrendering, and trying to leave are different decisions with different consequences.

Recent reconstruction has made several of those choices executable in the SDL game. More importantly, they now return through the original sequence of messages, time changes, and destination screens. Sanctuary is becoming a situation the player can work through, rather than a picture at the end of a route.

## Waiting changes the question

The two waiting choices are tied to the current part of the day. Resting until nightfall advances toward 19:00; resting until daybreak advances toward 06:00. On returning, the sanctuary menu publishes the appropriate opposite waiting choice.

That is a modest visible change with a larger requirement underneath it. The game must calculate the forward interval, run the supported calendar effects, update the controls, and rebuild the menu. Changing the displayed hour while retaining the old choices would leave the screen describing the wrong situation.

The same principle applies to shorter waits. The length of the delay is only one part of what the action does.

## Word from the captain

Asking for word from the captain of the city guard produces one of three responses according to local reputation.

The original comparisons divide the reputation range at -10 and -75. Values on either side of a boundary do not receive the same result, and equality belongs to a specific branch. Those edges now have explicit tests rather than relying on a handful of comfortable middle-of-the-range examples.

After the response is acknowledged, the action draws a delay from zero to two hours, runs the calendar service, restores the sanctuary picture, and returns to its menu.

Zero is a real possibility. We have not rounded it up to make the visit feel more substantial. Nor have we replaced a zero-hour calendar call with “do nothing”: its maintenance behavior belongs to the original service, not to an assumption about what the clock display will show.

The result is a complete selected interaction. A response can be read, dismissed, and followed by another decision in the same place.

## The picture that was not missing

Getting that return right involved correcting one of our own interpretations.

An earlier reading treated the picture argument used to restore sanctuary as empty. That sent the investigation toward a different rendering path and made the return appear blocked by an unresolved empty-picture operation.

The missing fact was in the sanctuary's entry code. It copied a picture name through an already initialized pointer before the later renderer call. Following that write changed the question from “what does the empty-picture renderer do?” to “which picture does this pointer supply?”

A controlled original-game capture supplied the answer: `MS041.PIC`. The renderer received a nonempty name and followed its ordinary picture-loading branch.

This was not a newly discovered Darklands bug. It was an error in our reconstruction of the caller's state.

Correcting it allowed the captain's response to return through the right visual path. It also prevented us from solving a more complicated problem that did not belong to this interaction in the first place.

## The party leaves together

The successful sneak-out route contains another detail worth recovering exactly: the check does not simply pick the party's finest infiltrator.

It considers the active member with the lowest signed Stealth-plus-Streetwise sum, clamps the resulting threshold to the original range, and compares the random result against it. A particularly capable character does not automatically erase a weaker companion from that calculation.

On the supported success branch, the game presents its result, accounts for the two-hour cost, and publishes the appropriate daytime or nighttime side-street state.

That is a useful piece of gameplay to have running. It is also a reminder that party-selection rules are part of the design. Replacing the weakest member with the strongest would be a plausible mechanic for a new game, but a different mechanic from this one.

## A refusal elsewhere in the city

Related work at the nighttime monastery provides a smaller contrast. Its sanctuary request is a separate interaction, and the ordinary refusal now runs through its message, event creation, and return to the nighttime church.

In the recorded graphical check, the party began at 21:00 and returned at 21:00. The clock did not move, but an event record had been created with a schedule eight hours ahead.

This gives the previous scheduler devlog a concrete example: a conversation can leave persistent state even when no time passes during the conversation itself. That record should not be replaced with an invented immediate effect, or forgotten because the next screen looks familiar.

## What remains outside

Selected sanctuary waits, the captain's reply, ordinary surrender, and successful escape now have executable routes. The failed escape's visual continuation and the more extreme reputation-dependent surrender branch still require their own work. The nighttime monastery refusal does not authorize every other monastery outcome either.

Those limits are smaller and more specific than an unexplored sanctuary controller. Inside them, the player can make a choice and reach the next meaningful decision with the original state carried along.

The door is no longer the end of the reconstruction.
