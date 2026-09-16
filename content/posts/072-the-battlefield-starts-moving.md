---
title: "Devlog #072 - The battlefield starts moving"
date: 2026-09-16
description: "From normal battlefield entry to movement, arrows, melee engagement, recovery, and the first falling guard: the latest progress in reconstructing Darklands combat."
draft: false
tags: ["combat", "gameplay", "animation", "reverse-engineering", "darklands"]
summary: "The battlefield comes alive: movement orders, arrows, melee recovery, and the first falling guard."
---

In the previous combat devlog, the goal was straightforward to describe: choose **“Draw weapons and attack the guards!”** and have the reconstructed game produce the battlefield that follows. The work was still concentrated on everything between that choice and the first image. <!-- Source: previous; https://arkana-mechanika-labs.github.io/posts/071-before-the-battlefield-appears/ -->

We have now crossed that threshold—and moved considerably beyond it.

The normal Quickstart route reaches the battlefield. Party members can receive movement orders, walk, pause, and change their destination. Supported bow attacks consume ammunition, send arrows across the scene, and inflict damage. Ordinary melee exchanges now continue into engagement, recovery, and short retreat movements. In the latest connected run, a guard becomes inactive and begins falling, using the original animation artwork. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 -->

**The battlefield is no longer just being prepared. A fight is beginning to unfold inside it.**

The entry milestone has been merged into the engine; the continuing combat work remains on the active development branch. There is still a substantial distance between these supported exchanges and a complete battle with an outcome and a return to the adventure. What has changed is how much of that journey now runs as one connected system. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 -->

*The clips below show gameplay from the controller and renderer used by our SDL host, exported as silent video. Use the player controls to pause or view fullscreen.*

## From the city gate to the battlefield

The first important result is not merely that we can display terrain and sprites. It is that the current adventure creates the encounter.

The reconstructed preparation uses the actual party, city, equipment, events, and continuing random sequence. It generates the opponents, prepares the map, places the participants, loads their resources, and builds the first battlefield image. An actual SDL run reached this point in Dresden through ordinary Quickstart and navigation choices, without restoring a captured battle or supplying a reference screenshot as the answer. <!-- Source: entry; evidence/reconstruction/darklands_483_07/combat/selec00_entry_research_20260908/clean-product-entry-release/FINDINGS.md -->

That distinction matters throughout this project. A battlefield snapshot already contains the results of many decisions. Starting from the adventure means those decisions must be made by the reconstructed code itself.

The preparation is also not hard-coded to the city used during the initial research. Within the unchanged default Quickstart-party setup, its supported inputs cover the ninety starting cities and the recovered guard-count and variant ranges. Those encounters use shared routines and their actual inputs, rather than a separate arrangement written for each demonstration. <!-- Source: entry; evidence/reconstruction/darklands_483_07/combat/selec00_entry_research_20260908/clean-product-entry-release/FINDINGS.md -->

From the player's perspective, this is the familiar transition from making a dangerous choice to facing its consequences. For us, it is the point where the earlier menu, party, resource, and encounter work finally meet.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/072/navigation.png" aria-label="Entering the guard battlefield (silent)">
    <source src="/devlogs/072/navigation.mp4" type="video/mp4">
    <a href="/devlogs/072/navigation.mp4">Watch entering the guard battlefield (MP4).</a>
  </video>
  <figcaption>From the inn through Bromberg to the city gate, then into a battlefield generated from the current party and city. This exported run is separate from the earlier Dresden desktop demonstration.</figcaption>
</figure>

## Giving an order—and then changing it

Movement is where a static battlefield first becomes an interactive place.

The current combat path supports selecting a party member, issuing a ground order, walking, pausing, selecting again, and replacing the destination. These actions operate on the same actor in the same encounter. A new command updates the existing order rather than restarting the scene. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 -->

A single walk is only the beginning of that problem. The other participants are moving too. A target can leave its original position. Another actor can obstruct a route. Reaching the end of a path can make a queued attack ready rather than simply returning the character to an idle state.

Recent work has connected more of those transitions. The movement logic can replan on the supported moved-target paths and preserve the original retry timing when planning fails. A blocked step against the path's target restores the attempted movement and runs the walk-completion behavior before publishing the next order. Other obstructions keep their own rollback and constraint handling. <!-- Source: visibility; evidence/reconstruction/darklands_483_07/combat/scheduled_clip_investigation_20260916/SCHEDULED_VISIBILITY_REVIEW.md --><!-- Source: blocked; evidence/reconstruction/darklands_483_07/combat/blocked_target_20260916/REVIEW.md -->

There is an important difference between these cases. “The character did not move” is a visible result, but it does not tell us whether the character should wait, retry, finish approaching an opponent, or prepare an attack. Recovering the decision behind that result is what allows the next update to behave correctly.

The same applies when a command is replaced. The position, current animation, route, and queued work all have to remain consistent. Otherwise, a character can look correct for one frame while carrying an order that belongs to a different situation.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/072/orders.png" aria-label="Selecting a character and replacing a movement order (silent)">
    <source src="/devlogs/072/orders.mp4" type="video/mp4">
    <a href="/devlogs/072/orders.mp4">Watch selecting a character and replacing a movement order (MP4).</a>
  </video>
  <figcaption>Select a party member, preview a route, walk, pause, and replace the destination during the same encounter.</figcaption>
</figure>

## Arrows that do more than cross the screen

Ranged combat has become a useful test of the whole chain between an action and its consequences.

The supported bow path now joins attack preparation, sound, projectile creation, ammunition consumption, recovery, and reload. The arrow then advances through the battlefield using the recovered movement rules and the original directional artwork. Its previous pixels are removed as it moves, rather than accumulating behind it. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md -->

When a supported impact reaches its target, the result is applied to the live combat actor. Endurance and Strength changes belong to that actor's state; the party panel displays those values instead of maintaining a separate version of the character. Damage numbers appear over the battlefield and expire later, while the underlying damage remains. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md -->

This closes a gap that a convincing animation could easily hide. A bow animation, a moving arrow, and a changing health display can be three unrelated demonstrations. Here, the output of each stage feeds the next.

One retained encounter illustrates that continuity particularly well. A party member's Endurance falls from 39 to 37 after an arrow hit. Later melee exchanges take the same character to 34 and then 32. Those are successive changes in the same developing battle, not values supplied independently to illustrate separate features. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md -->

The shot also has consequences for its attacker. Ammunition and reload state are not discarded once the projectile becomes visible. They remain part of the encounter and influence what that actor can do next. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md -->

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/072/arrow-impact.png" aria-label="Arrow flight, damage number and party-panel update (silent)">
    <source src="/devlogs/072/arrow-impact.mp4" type="video/mp4">
    <a href="/devlogs/072/arrow-impact.mp4">Watch arrow flight, damage number and party-panel update (MP4).</a>
  </video>
  <figcaption>An incoming arrow hits Gretch for 2 damage. The number appears above the character and Endurance changes from 30 to 28 in the party panel. This capture is a different encounter from the 39-to-37 example described above.</figcaption>
</figure>

## Melee is a relationship between two actors

Close combat has advanced beyond the first attack animation.

The reconstructed sequence now includes supported range checks, accuracy preparation, stance changes, ordinary hit and miss cycles, and target maintenance. It also continues into the reciprocal engagement between attacker and opponent, including the associated direction selection, hit sound, and movement. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 --><!-- Source: engagement; docs/COMBAT_MOVEMENT_PILOT.md -->

This is one of the places where the original update order becomes especially important. An attack does not change only the actor who performs it. It can change the opponent's order, motion, and relationship to the attacker during the same update.

The original scheduler can revisit an actor that it has already processed. Suppose an earlier actor in the update order is affected by an opponent processed later. Deferring every consequence until the next update would not preserve that behavior. The reconstructed engagement path now retains the same-update revisit, allowing the two sides of the interaction to remain synchronized. <!-- Source: engagement; docs/COMBAT_MOVEMENT_PILOT.md -->

The work also continues beyond engagement into recovery and the supported short retreat movement. The original conditions determine whether a partner retreats, which recovery state follows, and whether another pursuer needs a new path. An attempted retreat can be blocked; that has different consequences from a successful step. These are local combat movements, not a general implementation of fleeing the battle. <!-- Source: recovery; evidence/reconstruction/darklands_483_07/combat/engagement_recovery_20260916/REVIEW.md -->

Getting a character back into walking introduces another dependency: the correct walking resources must be restored after a combat stance. The current path handles both an already-cached walking animation and a required reload, while preserving the actor's ongoing state and the resources already allocated to it. Party recoloring and frame metadata remain part of that transition. <!-- Source: recovery; evidence/reconstruction/darklands_483_07/combat/engagement_recovery_20260916/REVIEW.md -->

What looks like a brief exchange between two figures therefore joins targeting, timing, animation, collision, pathfinding, sound, and sometimes the decisions of a third actor. The latest progress is not just another attack frame. It is more of the interaction surrounding that frame.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/072/melee-recovery.png" aria-label="Melee engagement and recovery movement (silent)">
    <source src="/devlogs/072/melee-recovery.mp4" type="video/mp4">
    <a href="/devlogs/072/melee-recovery.mp4">Watch melee engagement and recovery movement (MP4).</a>
  </video>
  <figcaption>A continuous melee exchange proceeds through supported engagement recovery and renewed movement. These are local combat movements, not a player command to flee the battle.</figcaption>
</figure>

## The first guard begins to fall

The latest visible milestone follows naturally from those exchanges: an actor becomes inactive, and the game has to do something other than continue its normal combat animation.

The current path now handles the supported melee-collapse and cancellation transitions, updates the relevant state and panels, and continues into inactive-actor animation. In the reported encounter, a guard reaches the original `E02dy` falling sprite and is drawn in its first falling frame. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md --><!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

That required more than setting a “dead” flag or replacing a sprite name.

The falling resource follows its own loading rules. Its name has no weapon suffix. Party and enemy appearances use their established resource capacities and metadata, and party recoloring still applies where required. The loader must also preserve existing hit-sequence data that this kind of resource does not replace. <!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

There is a corresponding change on the rendering side. Inactive actors are submitted through the original alternate actor-record buffer rather than treated as ordinary active combatants. Their bounds, clipping, and dirty regions still have to participate correctly in drawing the battlefield. That connection is now in place for the supported falling path. <!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

The result is a completed image showing the guard beginning to fall—not merely an internal state change that the renderer cannot yet display.

The next update reaches the remaining terminal handling for removal, loot, sound, and terrain effects. That is the present limit of this particular sequence. **Seeing the fall begin does not yet mean that the complete aftermath of defeating an opponent is implemented.** <!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

Nevertheless, this is a substantial change from the opening battlefield. The same generated encounter now carries actors through movement, attacks, damage, engagement, and the beginning of a fall.

<figure class="devlog-gameplay">
  <video controls loop muted playsinline preload="metadata" width="960" height="600" poster="/devlogs/072/first-falling-guard.png" aria-label="The first guard begins to fall (silent)">
    <source src="/devlogs/072/first-falling-guard.mp4" type="video/mp4">
    <a href="/devlogs/072/first-falling-guard.mp4">Watch the first guard begins to fall (MP4).</a>
  </video>
  <figcaption>The first guard begins falling in consecutive completed frames. Only the first falling pose is available: the clip ends before the unsupported removal and loot update.</figcaption>
</figure>

[View the full-size screenshot of the first falling guard](/devlogs/072/first-falling-guard.png).

## Why one encounter could stop while another continued

One recent challenge came directly from an ordinary reported play session.

The encounter stopped during an early scheduled visibility check, even though other regression encounters were already reaching melee. This was a useful reminder that a longer demonstration does not automatically cover every earlier decision another battle might require. The reported route was reproduced from its normal Quickstart inputs, preserving the state leading up to the stop. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md -->

The subsequent work resolved that scheduled visibility case, connected the newly reached moved-target behavior, and removed an overly conservative invalidation in a later visibility calculation. The character could then finish the walk, and the encounter continued into the later combat interactions. That same reported route is now the one that reaches the falling guard. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md --><!-- Source: visibility; evidence/reconstruction/darklands_483_07/combat/scheduled_clip_investigation_20260916/SCHEDULED_VISIBILITY_REVIEW.md -->

The investigation also exposed a concrete directional-visibility mistake: one lookup used the actor's appearance group where the original reads a secondary facing value. Appearance and direction can both be represented by small integers, so the error need not announce itself with an invalid value. It changes the meaning of the lookup instead. The original comparisons now cover the corrected operand. <!-- Source: visibility; evidence/reconstruction/darklands_483_07/combat/scheduled_clip_investigation_20260916/SCHEDULED_VISIBILITY_REVIEW.md -->

We have not turned this into a special rule for one city or random seed. The reported encounter remains a regression example: a reproducible journey that must continue to work as the shared implementation changes. At that checkpoint, other inputs still exposed unfinished branches, including a blocked ranged-sight response. The later revision used for the clips above also handles that response; both longer encounters now reach the end-of-fall boundary. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 --><!-- Source: visibility; evidence/reconstruction/darklands_483_07/combat/scheduled_clip_investigation_20260916/SCHEDULED_VISIBILITY_REVIEW.md -->

This is one of the benefits of working with connected encounters. They reveal not only that something is missing, but the precise situation in which it becomes necessary.

## Small details that change the next action

Not every significant discovery has been a large new subsystem. Two smaller examples show the level at which apparently reasonable code can diverge from the original.

A walk-completion helper was clearing the wrong flag. The original clears `0x0010`; our implementation had been clearing `0x1000`. Both are valid bit operations, but they affect different parts of the actor's state. A new comparison against the original instructions failed before the correction and passed afterward. An older hand-written test had agreed with the incorrect implementation and needed correction too. <!-- Source: blocked; evidence/reconstruction/darklands_483_07/combat/blocked_target_20260916/REVIEW.md -->

Unarmed attack preparation supplied another surprise. Its weapon key is `-1`, and the original calculation uses that signed value to read the initialized byte immediately before its category table. A separate equipment routine has a convenient unarmed mapping, but this attack calculation does not use it. <!-- Source: unarmed; evidence/reconstruction/darklands_483_07/combat/unarmed_melee_20260916/REVIEW.md -->

The reconstructed table data now retains the actual preceding byte. Tests deliberately change that value and the alternative equipment-category value independently, so they can distinguish the correct lookup from either a hard-coded answer or the wrong mapping. This allowed the unarmed party member to complete attack preparation and reach the subsequent engagement. <!-- Source: unarmed; evidence/reconstruction/darklands_483_07/combat/unarmed_melee_20260916/REVIEW.md -->

Neither change makes an impressive screenshot on its own. Both affect what happens after the screenshot. That is why the investigation has to follow the decisions as well as the visible result.

## Checking the behavior behind the pictures

The original instructions remain the reference for the rules we reconstruct. Focused disassembly and decompiler views help identify the decisions and their dependencies; controlled execution of the original code supplies independent results to compare with the C# implementation. Existing evidence is reused when the next task reaches an already-understood helper. <!-- Source: recovery; evidence/reconstruction/darklands_483_07/combat/engagement_recovery_20260916/REVIEW.md --><!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

The newest falling-animation work, for example, includes 258 original animation cases, 56 comparisons using the actual shipped stance resources, and 36 alternate-render-record cases. Those checks exercise distinctions that a single successful fall would not reveal: actor side, frame limits, cached and newly loaded resources, clipping, and buffer capacity. <!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

The connected session tests answer a different question: do the individually checked operations work together when they inherit one another's results? Earlier milestones remain checked as the encounter advances. A later fix must not quietly change the party, random state, or movement that brought the fight to that point. <!-- Source: pilot; docs/COMBAT_MOVEMENT_PILOT.md --><!-- Source: recovery; evidence/reconstruction/darklands_483_07/combat/engagement_recovery_20260916/REVIEW.md -->

At the falling-animation checkpoint, the full Release regression run passed **9,037 tests, with no failures or skips**. That is the wider test suite, not 9,037 battles, and it is not a percentage of combat completion. <!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

There is also a distinction between the different images we can show. Battlefield entry has been exercised in the desktop SDL application, and the accepted initial reference includes state-and-pixel comparisons with the original. The newest combat milestones are retained outputs from connected C# gameplay and rendering runs. They establish visible progress in that implementation, but they do not yet constitute a complete original-versus-reconstruction battle replay. <!-- Source: entry; evidence/reconstruction/darklands_483_07/combat/selec00_entry_research_20260908/clean-product-entry-release/FINDINGS.md --><!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

A screenshot demonstrates what was drawn. The surrounding checks tell us more about why it was drawn and what state the next action will inherit.

## What comes after the fall

The immediate next piece of work is the terminal handling reached after the falling animation: the original removal and aftermath effects must be completed rather than replaced with a generic disappearance. The blocked ranged-sight response that stopped another encounter has since been connected in the revision used for these captures. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 --><!-- Source: fall; evidence/reconstruction/darklands_483_07/combat/inactive_animation_20260916/REVIEW.md -->

Beyond those lie further targeting and special-action cases, additional effect and encounter families, and the decisions that end a battle. Returning the resulting party state to the adventure—and eventually restoring arbitrary saved battles—remains work of its own. The present development slice is centered on the fresh Quickstart guard encounter, not every battle Darklands can generate. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 -->

The direction is to keep extending these connected fights, using each newly reached situation to identify the next missing behavior. That gives us something more useful than a growing list of isolated routines: a sequence of actions whose consequences are carried forward.

We began this stage trying to make the battlefield appear. It now accepts orders, supports shots and melee exchanges, updates injured characters, and reaches the first falling guard. <!-- Source: status; https://github.com/Arkana-Mechanika-Studios/darklands-engine/pull/46 -->

There is still a battle to finish. But the work now takes place inside a fight that has already begun.

<!-- Publication provenance: article research snapshot 2026-09-16, baseline
0ace4a4389463e4f3b6f9c123804184c69f8d2e4. Repository paths in source comments
refer to that research snapshot. Media and the noted blocked-ranged continuation
use committed revision bd3b8da2a8913563419163a39afc8f0e1fc89a63.
Media: silent engine-frame exports; 60 Hz export-host presentation samples;
engine-owned elapsed-time scheduling, no clock-to-frame conversion, no interpolation.
Navigation has scripted 1.5-second input dwell; all other clips preserve their
continuous sample intervals. Fall ends before partial clock1320/0014:23AE.
The historical 9,037-test figure is the reported falling-animation suite, not
new testing for publication. -->
