---
title: "Devlog #079 - The arrow that read the stack"
params:
  images:
    - /devlogs/079/arrow-final-frame.png
description: "A guard's missed crossbow shot at the Steyr gate led to two anomalies in the original Darklands 483.07 code: a clipping routine that reads coordinates it never wrote, and a missed arrow that ends up inside a wall."
summary: "Our reconstruction refused to guess at one line of the original projectile code. Tracing why led to a read of stale stack data, a timer interrupt writing CPU registers into map coordinates, and an arrow that stops inside a wall."
date: 2026-10-16T18:00:00+02:00
draft: false
tags: ["Darklands", "reverse engineering", "combat", "original bugs", "restoration"]
width: wide
---

A guard at the Steyr city gate raises a crossbow, fires at the party and misses. In our reconstruction, that ordinary shot led to two separate anomalies in the code MicroProse shipped as Darklands 483.07.

In the first, a clipping routine checks a point it never calculated. The point turns out to be whatever another routine left on the stack, and under the right timing a hardware interrupt can replace it. In the second, a missed arrow's search for the nearest obstacle adds a final step that it never tests, so the arrow can end up inside a wall.

Neither one is something a player would notice. Our reconstruction found both of them because of one rule it follows.

All findings here concern our pinned **483.07** executable. They are not claims about every release of Darklands.

## A reconstruction that refuses to guess

Our C# engine rebuilds the original game logic routine by routine and checks it against the original executable. Each value it uses has to have a known origin: an original instruction, a data file, or a documented decision. If a calculation needs an input whose origin we cannot establish, the engine does not fill in something plausible. It stops, with an error that names the exact original instruction it could not reproduce.

That rule also works as a bug detector. If the original code reads a value it never set, a faithful reconstruction has nothing to give it, so it stops at that line.

In ordinary guard fights at the Steyr gate, about forty ticks into combat, the engine kept stopping here:

```text
proc_0014_F284 / 0014:F34D inherited clip
```

<figure>
  <img src="/devlogs/079/steyr-gate-fight.png" alt="A guard fight at the Steyr gate in the reconstructed engine" width="960" height="600" loading="lazy" />
  <figcaption>A naturally reached guard fight at the Steyr gate, captured where the strict reconstruction stopped: one of the guards had just fired a ranged shot that missed.</figcaption>
</figure>

The stop is inside the game's missile code. Three original routines are involved:

| Original routine | What it does |
| --- | --- |
| `R18:02BE` | Decides where a missed shot ends up |
| `R14:EF3C` | Walks along the flight path and tests each wall, object or actor rectangle |
| `R14:F284` | Clipping: does this line segment intersect this rectangle? |

(Darklands loads most of its code as overlays from the end of its executable. `R14:F284` means offset `F284` in overlay record 14.)

F284 is a classic routine of the kind found in any graphics textbook. Each endpoint of the segment gets an *outcode*: one bit each for left of, right of, above and below the rectangle. If both endpoints share a bit, the segment misses. If either endpoint is inside, it hits. Otherwise the routine calculates where the segment crosses an edge and tests that point.

## A point nobody calculated

F284 begins with `ENTER 4,0`. That reserves two words on the stack for a working point (X and Y) and does not clear them. The routine then branches:

- if the segment crosses the **bottom** edge, it calculates and stores that point;
- otherwise, if it crosses the **top** edge, it calculates and stores that point;
- otherwise it goes straight on to the next instructions.

```asm
F343  push word [bp-2]   ; Y
F346  push word [bp-4]   ; X
F349  push cs
F34A  call F3E2          ; classify this point against the rectangle
```

When neither vertical test applies, nothing on that path has written those two words. The routine classifies a point that this call never calculated. If the point happens to be outside the rectangle, the code goes on to calculate the side intersection, and no harm is done. If it happens to be inside, F284 reports a hit using coordinates that have nothing to do with the line it was asked about.

In C this would be an uninitialised local variable. Our reconstruction has no honest value to supply there, so it stops.

## What is actually in those two words?

An uninitialised value is not random. On a real machine, those two stack words contain whatever was last written to them. So we went to find out what that was.

We ran the original game under DOSBox-X in a guard fight and placed memory watches on those exact stack addresses, then followed the bytes back to their origin. Just before the clipping call, the parent routine EF3C had used the same stack slots for its own variables: the smallest cell X (19) and the largest cell Y (8) of the area it was scanning. F284 then read those words back in swapped order as the point **(8, 19)**.

The projectile code was clipping against a point made of another routine's leftover loop bounds. In the observed case, (8, 19) was far outside the wall rectangle near X = 702, so the result was correct by luck.

## The timer interrupt gets a vote

The game draws frames between the scan and the clipping call, so we measured the stack inside the original graphics routine. At one instruction it sits at exactly the depth where an incoming hardware interrupt would make the CPU save its FLAGS register over the Y word and its code segment over the X word. That stretch of code never disables interrupts.

At first that was only a prediction from the instructions. Next we checked whether it happens in practice. We reloaded the same saved checkpoint of the original game several times, changing only the emulator's CPU speed. At one setting, a timer interrupt arrived at the vulnerable instruction:

| Event | Observation |
| --- | --- |
| Timer interrupt arrives in the graphics routine | The CPU writes FLAGS `7217h` over Y = 19 |
| Same interrupt | The CPU writes code segment `4A65h` over X = 8 |
| The handler runs and returns | Those two words are left as they are |
| F284 reads its "point" | **X = 4A65h, Y = 7217h** |

A code segment address and the CPU flags were being used as map coordinates. Continuous watches showed that nothing else wrote to those words in between. The result reproduced in a fresh emulator process and again after a reload.

The scope of what this shows needs stating precisely. In that run the corrupted point was still outside the rectangle, so the arrow landed in the same place, `(754,133)`. Only an intermediate value changed. Earlier controlled experiments had shown what an inside point does: placing `(703,40)` in those two words changes F284's answer and sends the same projectile to `(680,91)` instead.

We have **not** seen a real game in which an interrupt moved an arrow. What we have shown is the mechanism. In the original executable, the result of a projectile calculation depends on stale stack data, and a timer interrupt can overwrite that data, depending on CPU timing. Whether it ever affected a fight on a 1993 PC is something the evidence cannot tell us.

## Bug, or a convention we don't understand?

Before calling this a bug, we tried to argue the opposite case.

EF3C calls F284 from six places, and none of them passes a point. In all six, F284's frame sits at the same stack depth, so its working point always occupies the same two words. That allows one theory: the point might be meant to carry over from one rectangle to the next within a single scan. We built a small example in exact arithmetic where this "carried point" reading gives a different, still geometrically valid answer than calculating a fresh one.

The evidence against that theory is strong:

- no caller ever sets a valid starting point;
- the value can be replaced by an interrupt, and a convention that breaks whenever the timer fires at the wrong moment is not a workable design;
- nothing else in the code indicates when the point is valid or which query it belongs to.

We also checked whether MicroProse ever touched it. Our local 483.06 executable, run through the original 6-to-7 updater, comes out **byte-identical** to the 483.07 we use as our reference. Both contain the same unwritten read. The routine did change between those versions, since its vertical calculation was rewritten, but the gap remained. The update's notes describe broad logic, art and memory-corruption repairs, with nothing about missile clipping.

Our classification is **high-confidence defect**. We stop short of "confirmed" because we do not have the original programmer's intent. Without source code or symbols, it is almost certainly a mistake, but we cannot prove it.

## Correcting it without inventing anything

Because the original is ambiguous, any correction is our own engineering decision, and we label it that way. We tried three options: seeding the point from a known endpoint, carrying a point through each scan, and a third that we chose because it changes the least.

Our chosen correction does one thing. When no vertical intersection has been calculated, it calculates the side intersection directly and then classifies that point. Everything else stays as it was: each early exit, the bottom-before-top and right-before-left order, and the original 16-bit arithmetic, including its wrapping, its signed multiply and its truncating divide.

We then tested it in three ways:

- **Against the original.** In 1,488 cases executed with the original F284 instruction bytes, the correction gives the same answer every time. All 128 cases on the affected path happened to inherit points outside the rectangle, so this shows agreement but says nothing about intent.
- **Against geometry.** In 26,244 small-coordinate cases, checked against an exact-arithmetic segment/rectangle solver that shares no code with F284, the corrected path had no mismatches. The *original* vertical paths do produce 884 false hits from integer rounding. We deliberately leave those alone. Correcting the game's arithmetic would be a separate decision.
- **Against the real call chain.** We ran the existing publication, visibility and projectile code on controlled battlefields.

The last test was a real game.

## The real shot

With the correction enabled in an experimental build, we played ordinary guard fights at the Steyr gate: normal startup, normal clicks, nothing forced. Everything the projectile code reads was captured, including the full 13,308-byte battlefield floor, every actor and object table, and all 17 projectile slots.

About 640 ticks into one fight, a guard at `(632,60)` fired at a party member and missed. In Darklands a missed shot does not stop at its target. The code extends the flight beyond the target and searches for where the shot would strike something. During that search the corrected path was used eight times. All **52** rectangle tests matched exact geometry. The arrow was published, crossed the screen and was removed. This was the first complete corrected projectile flight in naturally reached play.

The captured coordinates, however, showed the arrow ending up inside a wall.

<figure>
  <img src="/devlogs/079/missed-arrow-flight.gif" alt="Animated frames of the missed arrow crossing the battlefield towards the east wall" width="784" height="491" loading="lazy" />
  <figcaption>Actual frames of the missed arrow from the experimental build, slowed to 350 ms per frame for inspection. This is our reconstruction running original logic with the clipping correction enabled. It is not footage of the original DOS executable, and it is not game-speed timing.</figcaption>
</figure>

## The second anomaly

F284 had answered every question correctly, so the problem had to be in what its caller did with those answers. That led to `R18:02BE`, the routine that decides where a miss ends up.

It works roughly like this:

1. Start at the target, with a step equal to the distance from shooter to target.
2. **Probe:** while the end point is clear, add another full step and test again, up to seven times.
3. **Refine:** after the first blocked answer, halve the step and move back. Keep halving: move back when blocked and forward when clear.
4. Store the end point.

Our arrow's search:

| Test | End point | Answer | What the routine does next |
| --- | --- | --- | --- |
| 1 | (896,94) | Clear | Add (264,34) |
| 2 | (1160,128) | Blocked | Start refining; subtract (132,17) |
| 3 | (1028,111) | Blocked | Subtract (66,8) |
| 4 | (962,103) | Clear | **Add (33,4), then stop** |

The last row is the problem. On a clear answer during refinement, the routine adds the next half-step and only *then* checks whether it should stop. It stops without testing where it ended up. The original bytes show it clearly:

```asm
0341  add [bp-8], ax      ; end point X += step X
034A  add [bp-0Ah], ax    ; end point Y += step Y
034D  cmp word [bp-2], 16 ; refining?
0351  jne 0380            ; no: test again
0353  jmp 038B            ; yes: store the end point, without another test
```

(The shift that halves each step sits between these lines and is omitted for readability.)

The last tested point, `(962,103)`, was clear. The stored point, `(995,107)`, was never tested. The east wall in that floor cell occupies `[990,992] × [95,112]`, so the arrow's end point lies **3 units past the far side of the wall**.

```text
   guard                             last clear      wall      stored
  (632,60) ------------------------> (962,103) ----> |##| ---> (995,107)
                                                     990 992
```

This is not an error in our translation. Native disassembly of the unchanged 483.07 bytes shows the original doing exactly the same thing. The movement code has no wall check of its own. It flies the arrow to wherever this routine said, marks it as a finished miss, draws an ordinary arrow and removes it.

<figure>
  <img src="/devlogs/079/arrow-final-frame.png" alt="The final frame of the missed arrow at its stored end point" width="784" height="491" loading="lazy" />
  <figcaption>The last frame before removal: the arrow drawn at its stored end point. At this resolution the wall artwork cannot settle collision on its own; the crossing is established from the logged world coordinates and the captured wall geometry.</figcaption>
</figure>

The overshoot is not a fixed tolerance. Its size depends on the shot's length and the course of the search. In a constructed case with a nearby wall, the same logic overshoots by **11** units. Neither the arrow sprite's 7 × 7 drawing area nor the separate impact offset explains it, since nothing in the code connects either one to this last half-step.

We have entered this in our original-bug register as **confirmed original behaviour and a possible gameplay defect**. The routine clearly searches for obstacles, which suggests the end point is meant to be clear. But "roughly the right distance" is a plausible goal for a 1992 game too. A miss that lands a few units inside a wall causes no damage here and is invisible at 320 × 200. The bytes show what happens. They cannot tell us whether anyone cared.

## Our correction exposed the second anomaly

In strict mode the reconstruction never reached this end point, because the first anomaly stopped it earlier. Correcting the first one is what let us see the second.

It would have been easy to treat the successful flight as a win and move on. Our records say plainly that correct visibility answers do not by themselves make the end point wall-safe.

So we compared three possible end-point rules on the same captured battlefield:

| Rule | End point | Visibility tests | Result |
| --- | --- | ---: | --- |
| Original routine | (995,107) | 4 | Crosses the wall |
| Use the last clear point | (962,103) | 4 | Clear, 28 units short of the wall |
| Test the final step; if blocked, use the last clear point | (962,103) | 5 | Clear |
| Step through the path to the first obstruction | (989,106) | 362 | Clear, 1 unit short |

The first alternative is the simplest, but it also shortens shots that had nothing in their way. The last is the most precise and costs about ninety times as many tests. The middle option adds a single test, keeps each final step that really is clear, and otherwise falls back to a point already known to be clear. Of the three, it was the one we preferred.

That is a design decision for the project. It is not something we recovered from the original. Any of these rules can change when an arrow arrives, and with it later random draws and outcomes. For now we have decided **not** to adopt any of them: the original final step is deliberately kept, and the question is tracked as an open issue to revisit when projectile visuals and combat are polished.

## What this says about the method

[Devlog #058](/posts/058-when-faithfulness-includes-bugs/) described our policy for original bugs: preserve the original behaviour in the certified original-code layer, document every defect, and choose an explicit disposition (`replicate`, `correct`, `disable` or `pending`) for the playable game. This investigation shows that policy applied to a harder case.

- **Each claim has a confidence level.** Every finding is recorded as one of three things: confirmed fact (bytes and traces), strong inference (an accidental stale read) or unresolved (the programmer's intent). Where we did not know, we wrote that down.
- **Each experiment answered one question.** One showed that an interrupt *could* reach those stack words. Another showed that it *did*, and that the values survived until they were read. A third asked whether it changed the outcome. It did not, and we reported that.
- **Evidence is pinned.** The executable, disassembly database, emulator build, save states and captured event streams are identified by SHA-256 hashes, and independent reviewers checked each stage. Anyone repeating the geometry check against the same capture should get the same exact fractions.
- **Bugs are recorded, not quietly fixed.** Neither anomaly has been silently repaired. The correction we adopted is limited to one documented call path, the anomaly we kept is documented as kept, and the original-code comparisons remain strict.

## Where things stand

- **The stale clipping read:** high-confidence defect. Our correction is now **enabled** in restoration gameplay, but only for this missed-projectile path. Every other caller of the clipping routine, and every comparison against the original code, stays strict. The full engine test suite (12,215 tests) passes with it. We have not yet recorded a fresh natural missed shot with the integrated build.
- **The untested final step:** confirmed original behaviour and a possible defect. It is **deliberately kept as the original does it** for now, so a missed arrow can still finish a few units inside a wall. Testing the final step with a last-clear fallback remains our preferred fix if we change that.
- **Still open:** the original intent behind both routines, a related stale read on a different ranged-attack path, and another strict stop that occurs later in the same fight.

Both anomalies are listed on our [Original Bugs & Oddities](/formats/original-bugs-and-oddities/) page as `DL-ORIG-GAME-0036` and `DL-ORIG-GAME-0037`.

We chose the clipping correction on its own and kept the overshoot visible, rather than letting one fix carry the other along with it.
