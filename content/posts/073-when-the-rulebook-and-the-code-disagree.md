---
title: "Devlog #073 - When the rulebook and the code disagree"
params:
  images:
    - /devlogs/073/armour-equality.png
description: "Checking Darklands' combat calculations against the manual, the clue book, and the original 483.07 executable."
summary: "A division by two where the clue book says three led us into a wider comparison of armour, equipment quality, tactics, and attack timing."
date: 2026-09-23
draft: false
tags: ["Darklands", "reverse engineering", "combat", "restoration"]
width: wide
---

According to the Darklands clue book, a weapon whose penetration exactly matches the target's armour should have its damage value divided by three. With a starting value of 12, that leaves 4.

In the executable we are restoring, it leaves 6.

This is not a critical hit, an unusually strong attacker, or a hidden equipment bonus. It is a different operation: the original code divides by two.

Comparing our reconstructed combat calculations with the manual and clue book has revealed several disagreements of this kind. Some are precise numerical contradictions. Others are differences between a useful explanation for players and the more complicated machinery needed to reproduce the game. Together, they illustrate why rebuilding Darklands cannot mean simply turning its printed rules into C#.

All the executable findings discussed here concern our pinned **483.07** version. They are not claims about every release of Darklands.

## The hit that should have been weaker

The clue book's printed page 40 describes three outcomes when weapon penetration meets armour. Penetration below the armour thickness divides the damage value by eight. Equal penetration divides it by three. Penetration above the armour leaves the value unchanged.

Our reconstruction agreed with the first and third cases, but not the middle one. Rather than change the C# to match the book, we set up a small experiment using the original machine instructions.

The attacker had a base damage value of 12 and penetration of 3. Strength was inside the weapon's normal range. Weapon and armour quality were equal. We excluded vulnerable-spot and glancing-hit adjustments, then changed only the target's armour thickness.

| Armour thickness | Clue book's predicted damage potential | Original executable's damage potential |
|---|---:|---:|
| 2: the weapon penetrates | 12 | 12 |
| 3: penetration exactly matches | **4** | **6** |
| 4: penetration is insufficient | 1 | 1 |

These are **damage potentials passed to the subsequent random damage calculation**, not promises about the number displayed above a character's head. That distinction matters because the game still has more work to do before determining endurance and strength losses.

The equality case was unambiguous. At original offset `0014:ACB7`, the instructions perform signed integer halving:

```asm
mov ax, [bp-2]
cwd
sub ax, dx
sar ax, 1
```

The surrounding instructions handle signed values, but the key operation is the final shift: this branch halves the number. The controlled execution passed 6 to the next damage routine, exactly as our C# calculation does.

At this stage of the calculation, 6 is 50% more than the book's predicted 4. That does not imply 50% more final damage in every fight, but it is plainly more than a cosmetic discrepancy.

![Evidence comparison of the armour equality rule and the original instruction result](/devlogs/073/armour-equality.png)

*The printed rule predicts 4 from a damage potential of 12; the original 483.07 instruction test produces 6. The graphic transcribes the rule and test result; it is not a screenshot of the printed book.*

## Why passing our own tests would not be enough

There is an obvious trap here. We could write a damage formula, write tests that expect that formula, and then congratulate ourselves when everything passes. That would tell us very little about the original game.

The relevant reference cases do something different. They execute the original instruction bytes in a controlled 16-bit CPU environment. The original damage routines and random-number helpers produce the expected results. Our reconstructed formula is not used to manufacture its own answer sheet.

During the verification, all **4,034 original-side cases** were regenerated and matched their retained results. The comparisons include returned results or faults, calls, ordered memory writes, and the final data-segment hash. Existing C# tests consume **3,884 applicable cases** from that corpus for the clean implementation's allocated-actor domain.

Those are two separate facts. The fresh run reproduced the original reference results; it was not a fresh run of the entire C# suite. Nor do thousands of local comparisons prove that every complete battle is correct. A faithful damage helper can still receive the wrong armour value from its caller.

For the narrow question at hand, however, we have both a readable instruction sequence and controlled original execution. The clue book's division-by-three statement does not describe this executable's equality branch.

## Equipment quality changes a different part of the calculation

Another disagreement concerns a rule that can look almost interchangeable in prose.

On printed page 74, the manual describes every ten points of equipment-quality difference as changing penetration or protection by one level. That suggests a better weapon might cross an armour threshold that an ordinary weapon cannot.

The clue book's pages 40–41 describe something else: compare penetration and armour first, adjust the damage value, and then apply the quality difference to that damage value.

The inspected original-backed damage calculation follows the latter sequence. The ordinary quality adjustment adds or subtracts damage after the penetration comparison; it does not move that comparison into a different category.

This matters because Darklands treats failing to penetrate, matching the armour, and fully penetrating as distinct cases. Changing which case applies is not equivalent to adding a point after that decision. In particular, the penetration relationship also determines the range used when calculating strength loss.

A superior weapon can therefore make an otherwise weak hit more painful without turning it into a fully penetrating hit. Conversely, superior armour quality can reduce the damage without changing the armour-thickness comparison itself.

Here the clue book is the better description. That is worth stressing: this investigation is not a contest in which one document is always right and the other always wrong. Different passages have to be checked against the particular operation they describe.

## Tactics do not fit one tidy printed explanation

The Vulnerable tactic provides a simple example of the books disagreeing with each other. The manual's page 38 says that aiming at weak points slows attacks and improves penetration without changing the chance of hitting. The clue book's page 42 includes a **−5 situational modifier** instead.

The reconstructed melee-threshold routine contains that −5 term. At this stage, the clue book agrees with the code and the manual's description leaves out a penalty.

Berserk produces a more striking comparison. The manual describes faster attacks with an increased chance of hitting. The clue book's numerical explanation instead describes a subtraction for the attacking character's all-out tactic.

In the original-backed threshold calculation, the attacker's own Berserk term is positive: at least 10, increasing with a quarter of the relevant weapon skill. With skill 60, that contribution is **+15**, not a subtraction. Against an ordinary defender, this agrees with the direction described by the manual rather than the clue book's formula.

It would be premature to turn that into a universal recommendation to go Berserk. This is a contribution to one calculation, not a complete comparison of tactics. The defender's action can change the modifier, surrounding combatants matter, and attack preparation has additional stages.

Some branches are stranger still. When the defender is Berserk, the inspected original routine reads the **attacker's** skill and replaces an earlier modifier. That is exactly the kind of detail a reconstruction could accidentally “correct” into something more intuitive.

The retained melee research checks **513 original threshold cases** covering tactics, shields, engagement counts and other input variations. Those cases let us preserve a surprising operation because there is evidence for it, rather than because it looks like sensible game design.

## A weapon's speed number is not a complete timer

The clue book gives useful advice about attack speed: slow weapons, cumbersome equipment and vulnerable-spot attacks can combine into a character who appears busy but rarely connects. It also supplies additive penalties for tactics and encumbrance.

The reconstructed preparation helper contains more structure. Its calculation uses weapon skill and agility as well as weapon speed, tactic and load. It derives a cached value from an integer division, and that value participates in a later attack-selection gate.

This is where we have to resist labelling every extra detail a documentation error. A helper's intermediate value is not automatically a complete attack interval measured in seconds. The printed account may compress several stages into one explanation.

What we can say is that implementing a simple cooldown from the printed additions alone would not reproduce the helper we have recovered. The existing comparison covers **515 applicable original cases**, including the original division-fault behaviour.

There are smaller numerical differences in the damage roll, too. With the original tables, a zero damage potential produces one point of endurance loss in the inspected routine, rather than the clue book's stated possibility of zero or one. At potentials of 21 or more, the reconstructed two-draw calculation spans **potential minus eight to potential plus two**, rather than minus nine to plus two.

These differences are much less dramatic than the armour divisor. They still belong in the record, because preserving the game means preserving its integer arithmetic and random draws, not just producing a similar-looking average.

![Captured combat scene with a visible damage number](/devlogs/072/arrow-impact.png)

*Captured reconstructed combat from the previous devlog: a visible 2-point hit. This frame illustrates the later presentation stage; it is a different encounter from the controlled armour-equality test above, and the visible number must not be read as that test’s damage potential.*

## Which Darklands are we restoring?

None of this makes the books disposable. The clue book's own introduction warns that unexpected code paths and late changes can leave inaccuracies. Its combat chapter also says that the explanation does not cover every detail and exception.

There is a version question as well. The clue book's version-history table ends at 483.06; our target is 483.07. That leaves several possible explanations for a disagreement: a printing error, a rule changed during development, a later revision, or a bug in the executable relative to the intended design. We have not established which explanation applies to each case.

What we can establish is narrower and more useful to the restoration: **given these inputs, this executable performs this operation**.

That is why we are retaining the original-backed division by two rather than replacing it with the book's division by three. It is why quality remains in the damage stage where we found it. And it is why counterintuitive tactic branches deserve evidence and regression tests instead of an intuitive rewrite.

A faithful restoration has to preserve the rules the game actually ran, even when they disagree with the rules that came in its box.

---

### Research notes

Printed sources: *Darklands* manual, pp. 38 and 74; *Darklands Clue Book*, pp. 5, 39–43 and 121. Page numbers refer to the printed books rather than PDF page indices.

Code and experiment basis: original 483.07 damage routines `0014:AC08` and `0014:AD5A`; melee threshold `0014:AA22`; attack preparation `0014:A492`. The reconstruction was inspected at engine commit `74b72f3b24f1b454fc27972a9cb6889eac03b013`. The armour-equality experiment and 4,034-case original-side rerun are recorded in the combat discrepancy verification note. Other comparisons draw on the retained damage and melee evidence, not a new whole-game replay. Since that snapshot, connected combat has progressed through movement, arrows and melee exchanges, but these local arithmetic checks still do not certify complete combat or establish the designers' intent. See [the battlefield progress report](/posts/072-the-battlefield-starts-moving/) for the current connected-play scope.
