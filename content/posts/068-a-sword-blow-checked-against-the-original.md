---
title: "Devlog #068 - A sword blow, checked against the original"
date: 2026-09-05
draft: false
tags: ["combat", "verification", "reverse-engineering", "darklands"]
description: "Plausible combat numbers are not enough. The original instructions give us something stricter to compare."
summary: "Plausible combat numbers are not enough. The original instructions give us something stricter to compare."
---

A combat calculation can be wrong without looking wrong.

It can produce a reasonable chance to hit, a believable amount of damage, and a fight that ends with the expected winner. None of those observations tells us whether it follows Darklands' actual rules. They tell us that it behaves like a plausible combat system.

For this project, that is a starting point, not an acceptance test.

Recent work has moved further inside the calculation itself. The original to-hit routine is now reconstructed as an internal C# component, alongside the damage driver and the missing routines needed to prepare pending damage. Independent comparisons with Bruce's combat reconstruction have also supplied concrete corrections and useful confirmation.

The important change is that we can ask the old instructions and the reconstructed code the same carefully bounded questions.

## Putting the original on the test bench

The comparison does not require playing thousands of complete fights. We can execute selected, identity-checked original machine-code routines with controlled inputs, record their results, and compare those results with the reconstruction.

This is differential testing: the original implementation supplies the reference behavior.

The inputs are deliberately varied. Ordinary values matter, but so do signs, limits, preserved fields, and cases that take a different branch. Some are research probes rather than states we have established as naturally reachable during play. That distinction stays attached to the results.

An early strike-comparison corpus contained 99,352 cases. It exposed six differences involving signed operands, limits, cached values, and whether a particular output should be overwritten. After correction, the candidate matched the entire retained corpus.

That does not mean 99,352 battles were reproduced. It means those specific calculations agreed across those specific tests. It is a narrower statement, and a much more useful one.

## When the same byte means something else

One later investigation offers a compact example of the problem.

A byte containing hexadecimal `80` can be read as 128 or as -128. The stored bits are identical. Which value matters depends on how the original instructions extend and use that byte.

In a controlled skill-threshold experiment, the original routine returned 90 while the candidate returned 26. Reading a signed skill byte as an unsigned number was enough to send the calculation in a different direction.

The correction removed the differences across the selected no-obstacle comparison set. It did not establish every obstacle-dependent path, and the deliberately chosen input should not be mistaken for an ordinary character's skill value.

For a reverse-engineer, the lesson is familiar but unforgiving: an expression that looks cleaner in modern code may have changed meaning on the way out of the decompiler. A cast, a truncation, or the position of a clamp can be part of the rule.

## Damage has a before and an after

Another important distinction is between calculating damage and applying it to a character.

The reconstructed damage driver prepares pending Endurance and Strength damage. It does not, by that fact alone, implement the complete sequence of a fighter attacking, the target reacting, the visible statistics changing, and the scheduler continuing.

Those surrounding steps are separate work. Combining them under a friendly name such as `Attack()` would not make their missing behavior disappear.

For the integrated damage work, 4,034 independent original-instruction cases compared more than a final number. They checked returned results or faults, ordered memory writes, and the complete 64 KiB data area used by that test contract. All sixteen reachable new conditional sites were exercised both ways.

The order is significant. In one deliberately constructed overlap case, a pending-damage write reaches storage also used by the random seed and changes a later draw. It is not evidence that ordinary fights routinely arrange memory that way. It is evidence that a returned damage value alone does not describe everything the routine can expose under the tested contract.

## Independent work that can challenge itself

Bruce's reconstruction is valuable precisely because it provides another implementation to compare, rather than a second description copied from our own assumptions.

A disagreement gives us somewhere specific to look. An agreement is useful too, provided we can say what inputs were compared and what was observed. The result is an exchange of reproducible findings: a routine, an input, an original result, and a correction that can be checked independently.

This is also why the test runner stays outside the finished game's execution path. Executing original instructions is a research technique. The engine's job is to implement the recovered behavior in C#.

## What this adds to the game

We now have more of the machinery needed to calculate a hit and prepare its damage, with concrete comparisons behind it. We also have regression cases that prevent several subtle mistakes from quietly returning.

A complete combat replay is still a larger milestone. Animation, scheduling, damage application, movement, and the surrounding controllers must cooperate before a sword blow becomes something the player can actually watch.

But the work underneath that future animation is no longer merely plausible mathematics. We can inspect a disagreement, reproduce it against the original, and show exactly why the corrected result belongs.
