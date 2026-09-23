---
title: "Devlog #074 - What Darklands means by difficulty"
params:
  images:
    - /devlogs/074/enemy-information-branches.png
description: "Tracing Basic, Standard and Expert through the original executable reveals hidden combat information, larger rewards, and an unresolved discrepancy in the manual."
summary: "Expert hides assessments rather than simply making enemies stronger. We followed the difficulty byte through menus, combat information, skill gains, fame, and save metadata."
date: 2026-09-23
draft: false
tags: ["Darklands", "reverse engineering", "combat", "difficulty", "restoration"]
width: wide
---

Our comparison of the combat code with the printed rules left an obvious question: could difficulty settings account for some of the differences?

Darklands offers Basic, Standard and Expert. Perhaps one of those settings changes armour effectiveness. Perhaps enemies receive more strength or better attack chances. Or perhaps the skill and damage routines we had inspected were receiving inputs already adjusted somewhere else.

There was a reason to look beyond the obvious arithmetic. We had found that higher difficulty permits larger combat skill gains. Taken alone, that sounds almost backwards. If Expert rewards the player more, what does it demand in return?

Following the setting through the original 483.07 executable gave us a more concrete answer. Part of the price is information, including information available during combat. It also led to a second question: does the game really remember a brief switch to an easier setting, as the manual claims?

## Following the switch, not just the name

The reference card lists **Alt+D** as the three-way difficulty switch. The original keyboard handler leads to three small setting routines, which write a single byte at `DS:906A`.

The values are straightforward: **0 for Basic, 1 for Standard, and 2 for Expert**. Each setter then calls the shared routine that updates the menu markers and assembles the setting-change message.

We checked the original instructions and executed all nine combinations of initial and target settings. Each produced the appropriate value, selection markers and text, such as “Difficulty is now set to Expert.” The tests stopped just before the notification was displayed.

That qualification is important. We exercised the original setting and menu-preparation code, not an entire interactive menu session. Nevertheless, it closed a real gap: we could now see what the setters actually write, rather than stopping at a dispatcher that calls an unresolved routine.

Those setter bodies do not adjust enemy statistics or record a remembered minimum difficulty. They write the selected value and prepare its presentation.

## The first cost: the game stops advising you

The manual is quite explicit about the intended help trade-off. Basic can show exact success probabilities during interactions. Standard provides qualitative advice. Expert leaves the judgement to the player.

The original-derived advice routine follows that pattern. It reads the same difficulty byte and decides how to present the evaluated result. One branch formats a number; another selects a verbal band; the Expert branch returns before the normal advice-rendering path.

This changes what the player knows about a choice, not the evaluated score inside that display routine. A dangerous attempt does not need to become statistically worse for it to become harder to judge without the number beside it.

The manual also describes clues about unavailable potions and unknown saints at easier settings. Those descriptions help explain the broader design, although they are not all newly verified mechanisms from this investigation. The important discovery here is that difficulty-dependent information is not confined to the interaction menus.

## The second cost: less knowledge of your opponents

Inside the original enemy-information routine, `0021:03FE`, four branches explicitly check for Expert.

They skip supplemental assessments associated with the enemy's melee weapon, ranged weapon, natural armour and natural weapon. In the ordinary weapon paths, the code reads a skill value, converts it into a verbal rating, and draws the additional assessment. The original descriptor table runs from “very poor” through intermediate ratings to “excellent” and “superb.”

Basic and Standard retain the applicable assessment lines. Expert skips them.

**The enemy-information screen itself does not disappear.** Names and equipment descriptions have their own paths. What disappears is some of the extra assistance in interpreting how capable or well-protected that opponent is.

This is a direct combat-related effect of difficulty, but it is not an enemy buff. The inspected branches change what is displayed, not the underlying capabilities being described.

That makes the reference card's **Enemy Info** command, `e`, more significant for the restoration than a simple list of names and equipment. Reproducing the screen faithfully means reproducing what each setting withholds as well as what it shows.

The finding comes from original instructions and fresh focused Ghidra inspection. We have not yet captured a new matched pair of complete enemy-information screens, and discovering these branches does not mean the reconstructed interface already exposes the whole feature.

![Original enemy information branch map for Standard and Expert](/devlogs/074/enemy-information-branches.png)

*Evidence diagram of the inspected enemy-information branches. It records which supplemental assessments the original instructions skip at Expert; it is not a matched capture of complete game screens.*

## What the player receives in exchange

The larger rewards are not an illusion or a mistaken label in our C#.

The original combat skill-award routine first decides whether an improvement occurs. Only after that initial roll succeeds does it read difficulty and select the possible size of the improvement.

| Setting | Possible successful skill increase, before the ordinary cap |
|---|---:|
| Basic | +1 to +3 |
| Standard | +1 to +4 |
| Expert | +1 to +5 |

The setting does not alter the initial improvement roll inside this routine. Nor does the table promise an increase after every battle. It describes the amount awarded when the relevant improvement succeeds.

We reran the existing **582-case original-instruction corpus**, which includes all three settings and other input variations. Every regenerated case matched its retained result. This was an original-side verification, not a fresh run of the C# suite.

Fame has an equally concrete rule. The native helper at `0039:1E06` selects a base award, then gives **two-thirds on Basic, the unmodified amount on Standard, or one-and-a-half times the amount on Expert**, discarding fractional parts.

A base award of 10 becomes 6, 10 or 15. A base award of 25 becomes 16, 25 or 37. The clue book even lists a 6/10/15 fame reward on printed page 84, consistent with the base-10 result.

A later focused audit expanded this to **63 standalone fame cases**, covering seven category inputs, three initial fame values and all three settings. Every case produced the expected stored fame. These experiments executed the original getter and setter too; they did not merely stop after calculating a prospective award. They establish this helper's behaviour, not that every fame-producing event has been traced to it.

Taken together, the verified rules support the manual's central bargain: less assistance, larger rewards. For a player who already knows the encounters, that bargain may be more advantageous than challenging. That is a reasonable interpretation of the design, not evidence that a hidden damage multiplier must exist.

## The penalty that did not survive our test

The manual adds a safeguard to this bargain. On printed page 19, it says that advancement and rewards depend on the easiest setting selected during a preceding period. Even a brief look at an easier level is supposed to carry a penalty after switching back.

That gives us a testable expectation. Returning to Expert immediately after selecting Basic should not behave exactly like remaining on Expert, at least where that historical rule governs the award.

But the inspected setters record the current setting, and the skill and fame readers we traced consult that current byte. We did not find a remembered-minimum input in those readers.

We therefore ran sequences of the original setters followed by the original fame helper. The same emulated data memory was preserved between calls. The later audit used a category with a base award of 64 and tested six sequences:

| Sequence of original setting calls | Award |
|---|---:|
| Basic | 42 |
| Standard | 64 |
| Expert | 96 |
| Expert → Basic → Expert | 96 |
| Expert → Standard → Expert | 96 |
| Standard → Basic → Standard | 64 |

Both returns to Expert received its 96-point award. The return to Standard received its 64-point award. In this isolated composition, the easier-setting detour left no penalty that affected the subsequent award.

This is stronger than simply failing to locate a variable. It is an observed result from relevant original code. It is also narrower than proving an exploit in every situation in the running game.

The setting calls stopped before the notification routine, and each later call began with a fresh call frame while retaining data memory. The experiment did not include the complete notification/input loop, passage of game time, quest transitions or save/load sequence. We therefore cannot claim that every possible historical mechanism elsewhere has been excluded.

The finding remains worth reporting: **the manual's remembered-easiest rule is contradicted by the isolated setter/reward composition we tested.** We should not invent that bookkeeping in the restoration solely because the book describes it.

![Awards after isolated original setting sequences](/devlogs/074/setting-sequences.png)

*Captured results from the bounded original setter/reward execution. This is not a full-game exploit test.*

## A suspicious bit with a different job

There was one tempting clue that could easily have sent us in the wrong direction. The difficulty-label code masks its byte with `0x7F`. Why reserve the remaining high bit? Could it represent a previous setting or some hidden penalty state?

The examined save/load instructions provide a more concrete explanation. During an inspected save-context path, the game sets that high bit. On loading, it transfers the condition into another flag and clears the bit from the difficulty value before presenting the setting.

Here, difficulty and save-context metadata share a byte. The high bit is not evidence for a remembered easier setting.

This was a static save/load finding, not a newly completed save/load replay. It nevertheless prevents an attractive but unsupported interpretation from becoming part of our model of the game.

## So where are the stronger enemies?

We also inspected direct references to the difficulty byte throughout the executable. After rejecting two coincidental byte patterns, the census contained 36 real references or address arguments, covering settings, presentation, rewards and save/load handling.

No direct reference appeared in the main combat overlay `0014`. The inspected guard preparation and ordinary hit/damage calculations likewise supplied no identified difficulty-dependent enemy buff. In particular, the armour-equality division discussed in the previous devlog does not select its divisor from a difficulty setting.

That is useful negative evidence, but it is not exhaustive data-flow analysis. Computed pointers, copied state and upstream inputs can escape a literal-address search. The justified conclusion is that **we have not identified a difficulty-based increase to enemy statistics or ordinary damage in the examined paths**, not that every possible effect in every encounter has been disproved.

The concrete progress is elsewhere. We can now connect the menu setting to original help branches, combat-information restrictions and reward calculations. We also have a specific experiment challenging a documented rule, with a clear boundary for what still needs checking.

For the restoration, that means difficulty is not just another number to feed into the damage formula. It also determines which facts the player is allowed to see. Rebuilding those omissions matters just as much as rebuilding the information around them.

---

### Research notes

Printed sources: *Darklands* manual, pp. 18–19, 28, 44, 46 and 48; *Darklands Clue Book*, p. 84; reference card, general commands on page 1 and Enemy Info on page 2. Page numbers refer to printed pagination where applicable.

Code and experiment basis: pinned original 483.07 executable; earlier engine snapshot `a0f60ae7fe3b8772487017ec51564ec13be44602`; original setters `0000:1408/1418/1428`, menu routine `0000:1438`, advice routine `0043:27E6`, enemy information `0021:03FE`, skill award `0021:0000`, fame helper `0039:1E06`, and selected save/load instructions in `0037`. The earlier investigation recorded nine setting tests and the 582-case original skill-corpus rerun. A subsequent focused audit added 63 standalone fame cases, six setting sequences, and bounded Ghidra and Reko analysis. Original bytes, focused decompiler output and controlled original execution support the findings. No fresh C# suite run was performed for this article. Neither investigation changed gameplay implementation. The later audit remains a local research bundle outside the repository. This is not a whole-game equivalence claim.
