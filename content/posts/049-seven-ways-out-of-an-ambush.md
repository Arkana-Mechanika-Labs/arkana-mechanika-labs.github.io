---
title: "Devlog #049 - Seven Ways Out of an Ambush"
date: 2026-08-09T07:00:00+02:00
summary: "The seven actions on $CITYT00 are becoming real gameplay: prayer, potions, arms, grovelling, fleeing, and combat are now separated into exact owner consequences instead of guessed menu routes."
---

`$CITYT00.MSG` is a compact test of almost every rule that makes Darklands hard
to reconstruct.

It is an encounter card reached through nighttime Streetwise and Stealth
checks. Its rows include ordinary choices, conditional choices, saint and
potion popups, random tests, inventory mutation, calendar effects, equipment
recalculation, and combat handoffs.

Finishing it does not mean writing seven routes in a switch statement. Each
visible row returns an owner ordinal to record 53, and each owner performs a
different transaction. Over the last day we closed most of that transaction
table.

## Testing Your Arms

The “test your arms” owner selects a party member and computes the maximum of
seven signed current attributes. It then performs the original outcome RNG and
calls the no-improvement helper.

On the certified success arm, the owner displays card 6 over
`PICS\XCHASE.PIC` and returns to the deferred city state. It does not advance
the calendar.

The investigation also recovered the owner's exact eight weapon-definition
pointers into `DARKLAND.LST`:

- Hand Axe;
- Throwing Knife;
- Two-hand Sword;
- Long Sword;
- Falchion;
- Short Sword;
- Poniard;
- Dagger.

Inventory resolution retains exact item type and quality, falls back to the
same type when required, and finally uses the original Dagger fallback. The
attribute-improvement and combat-failure arms remain separate boundaries.

## Offering Possessions and Grovelling

The grovel route is much more destructive than its row text suggests.

The original owner clears the party's money. It then walks active party slots,
calculates signed averages and probability classes, consumes RNG in exact item
order, and removes inventory records while preserving the original compacting
behavior. Because deletion shifts later records down, the scan retains the
same index after a removal.

We reconstructed the exact six-byte inventory compactor, including the trailing
inactive record and live count decrement. Equipped items are invalidated in the
same categories as the original: weapon, vital armor, leg armor, shield, and
missile weapon.

Equipment load is recomputed from item-definition byte `+25h`. A live runtime
capture closed a linked helper that had previously been ambiguous: it is a
signed three-way clamp. In this route it clamps the recomputed value to
`0..500`.

After the loss pass, the owner grants item code `000Fh`, the Club, using the
original stack, overflow, capacity, and append rules. The clean C# projection
materializes the original-shaped data, executes those owners, and imports the
result back into the gameplay model before returning to the deferred state.

## Fleeing: Three Different Outcomes

The flee owner begins with a shared five-party predicate.

It scans every active party record and calls the item query with definition
word-20 mask `2000h`. If every active member satisfies the predicate, the owner
bypasses both RNG and elapsed time, presents card 10, and returns.

The project owner's original-game observation supplies an important gameplay
correlation: this card-10 bypass occurs when the party has horses. **Horses are
therefore the leading interpretation of flag `2000h`.** The byte evidence proves
the mask, five-party scan, and bypass; it does not yet name the item class. The
code and certificates deliberately keep the raw name until a direct original
data relation confirms the semantic label.

If the predicate is false, the owner computes a threshold from each active
member's Endurance, Strength, Agility, and encoded equipment load. It takes the
original unsigned minimum, adds five, and compares a signed `RNG(100)` result.

An ordinary success advances one hour, shows card 11, and returns to the deferred
state. A failure advances one hour, shows card 12, and hands control to combat.
The hour-23 day rollover and failure combat continuation remain fail-closed
because each crosses a separate original boundary.

This split prevents a common reconstruction mistake: “flee” is not one action
with cosmetic result text. It has a horse-related no-time bypass, an ordinary
one-hour success, and a one-hour combat failure.

## Direct Attack Is Deliberately Small

The direct-attack owner turned out to be only ten bytes.

It pushes zero, calls the shared combat controller, cleans the argument, and
returns. There is no hidden MSG composition, calendar advance, inventory
mutation, or additional skill check in that owner.

That finding is useful precisely because we did not descend into combat merely
to make the encounter table look complete. The owner is classified correctly
and remains stopped at the combat subsystem.

## Why This Matters Beyond One Encounter

The `$CITYT00` work exercised the architecture we need for the wider game:

- visible rows map to raw owner ordinals, not compact screen positions;
- checks, RNG, side effects, pictures, cards, and returns remain ordered;
- shared services are implemented once but caller-owned consequences stay with
  their owner;
- clean state is projected through original-shaped compatibility boundaries;
- unsupported branches stop before mutation instead of taking a plausible
  neighbor route.

The implementation is no longer merely displaying this ambush. It can execute
substantial parts of its original gameplay.

## What Is Actually Implemented

The SDL route can now exercise the encounter's conditional row publication,
street-sense result cards, saint and potion popups, the certified potion
outcome, Saint Apollinarius, arms success, complete grovel mutation, the
flag-`2000h` card-10 flee bypass, and ordinary card-11 flee success.

Direct attack, flee failure, the arms combat arm, day rollover at hour 23, and
uncertified item/saint effects remain explicit boundaries. That is not missing
error handling; it is the line between reconstructed behavior and behavior we
have not yet proved.
