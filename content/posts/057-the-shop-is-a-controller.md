---
title: "Devlog #057 - The Shop Is a Controller"
date: 2026-08-13T12:00:00+02:00
summary: "The Goods Merchant is now a live original-shaped controller with generated stock, exact prices, scrolling, selection, purchase, sale, barter targeting, and keyboard commands."
---

The marketplace's first choice is not the weaponsmith. It is the merchant who
sells everyday goods, and its screen is one of the densest non-combat
controllers we have reconstructed so far.

It is also not an MSG card. `$MARKE00` hands control to `proc_0032_0000`,
which saves global state, builds a trading surface over `BUYSELL.PIC`, polls
its own input loop, performs transactions, and restores the caller's state on
exit.

## Reconstructing the Screen from Bytes

The complete redraw owner publishes:

- the party purse in florins, groschen, and pfennigs;
- the negotiator and merchant description;
- Purchase, Sell, Barter, and Leave commands;
- four visible merchant offers;
- four visible items from the selected party member;
- independent cursors and scroll origins for the two lists.

The original uses font selector 1 here. Using the larger general text font
made capitals and numbers visibly wrong, so the SDL renderer was corrected
from the byte-level selector rather than tuned against a screenshot.

The initial merchant item is selected when the controller opens. Items do not
highlight merely because the pointer passes over them; selection changes on
click. Selecting an offer enables Purchase and disables Sell. Selecting a held
item does the reverse, and disabled commands cannot be highlighted or
activated.

The red initial letters in Purchase, Sell, Barter, and Leave are real command
mnemonics. SDL accepts the matching keys and the original mouse slots.

## Stock Is Generated, Not Stored as Four Rows

The offer list is built by scanning all 200 real `DARKLAND.LST` definitions.
The original visibility predicate uses item-definition fields, merchant type,
city data, and conditional RNG. Quality and price are computed values; they
are not arbitrary constants attached to the renderer.

Held items come from exact six-byte character inventory records. The selected
party leader negotiates prices, while a separate transaction target controls
whose inventory is displayed and mutated. The two lists retain separate
origins and cursors, and both scroll through their original four-row windows.

## Purchasing in the Original Order

Purchase resolves the selected offer and performs two separate price
calculations.

The first is normalized and compared against the party purse. If it is
unaffordable, nothing mutates. The original then constructs a quantity-one
inventory record and computes the price again. A city flag can add an RNG
term, so the two results can genuinely differ.

Only then does the game subtract the second price using its exact
radix-12/radix-20 money owner and call the inventory insertion owner. Existing
compatible stacks are tried first; otherwise a new six-byte record is
appended. Merchant stock is not consumed by the purchase.

Afterward, only the party inventory list is redrawn.

## Selling and Bartering

Sell uses its own owner, not Purchase in reverse. It rejects definitions with
the original unsellable flag, computes one sale value, adds it through the
three-denomination money owner, and removes the complete six-byte inventory
record. It does not decrement a quantity field. Cursor and origin are then
corrected if the removed record was at the end of the list.

“Barter for another person” is not a leader-selection popup. It rotates the
transaction target through active party slots and performs the complete
merchant redraw. The negotiator remains the leader and still owns the price
calculations; the new target owns the shown and mutated inventory. Per-target
list mode, held cursor, and held origin are preserved.

## What Is Implemented

The SDL Goods Merchant now supports original-shaped stock generation,
computed qualities and prices, both scrollable lists, click selection,
Purchase, Sell, Barter target rotation, Leave, and the corresponding keyboard
mnemonics. Money and inventory mutations use certified original owners rather
than modernized arithmetic.

The reconstruction is still deliberately scoped to the everyday-goods
merchant path. Other merchant families have their own catalogue predicates,
resources, and owner consequences and are not treated as cosmetic variants.
