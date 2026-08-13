---
title: "Devlog #058 - When Faithfulness Includes Bugs"
date: 2026-08-13T13:00:00+02:00
summary: "Two merchant defects forced us to define a versioned bug policy: preserve original bytes in COAB, document every defect, and choose an explicit SDL disposition."
---

Faithful reimplementation eventually reaches an uncomfortable question: what
happens when the original code is wrong?

The Goods Merchant gave us two concrete examples in Darklands 483.07. One is
a broken leader shortcut. The other can take the party's money without giving
it the purchased item.

Neither can be handled by quietly “improving” the reconstructed owner.

## The Ctrl+F Leader Defect

The quick-reference card says Ctrl+F1 through Ctrl+F5 define the party leader.
The generic input dispatcher does exactly that. The nested merchant controller
intercepts the same keys, but its implementation is incomplete in a dangerous
way.

Inside the merchant it changes the leader byte and repaints only the party
panel. It does not update the separate transaction target, recompute the
barterer text, rebuild the inventories, or recalculate displayed prices.
Execution then falls through into the Purchase/Sell list-toggle block and can
change which command appears active.

On leaving the merchant, the saved leader byte is restored, so even the
apparent leader change is temporary.

This is now catalogued as `DL-ORIG-UI-0001`. SDL deliberately consumes the
shortcut without mutation while the merchant controller is active. Leader
selection elsewhere remains a separate original mechanism.

That is a conscious `disable` policy, not a failure to implement keyboard
support.

## Charged, but the Inventory Is Full

The second defect is more severe and is confirmed directly by instruction
ordering.

Purchase subtracts money before attempting inventory insertion. The inventory
owner tries compatible stacks, then appends a new record only when fewer than
64 records are occupied. If all records are occupied and no compatible stack
can accept the extra quantity, insertion returns the unchanged count.

The caller does not interpret that as failure. It does not refund the price.
It simply redraws the inventory.

The observable sequence is:

```text
payment succeeds -> insertion cannot add the item -> money remains spent
-> purchased item is absent
```

This is narrower than “a full inventory always loses purchases.” A compatible
existing stack can still accept the item, provided the quantity does not
overflow `FFh`.

The clean controller exposes the result explicitly as
`InventoryFullAfterCharge`. For now its SDL disposition is `replicate`,
because reversing the operations or adding a preflight check would claim a
behavior that is not in the original 483.07 owner.

## Two Registers, Not One Rumor List

These discoveries led to a formal bug catalogue.

`KNOWN_ORIGINAL_BUGS.md` contains byte-confirmed defects, the exact original
units and instruction ranges, and the chosen reimplementation disposition:

- `replicate` for strict compatibility;
- `correct` for an explicit project fix;
- `disable` when executing the original defect is unsafe or confusing;
- `pending` while policy is undecided.

A separate research catalogue holds community reports from manuals, old
forums, Yahoo/Groups.io archives, and earlier versions. Reports fixed before
483.07 remain historical. Reports allegedly affecting 483.07 are leads for
testing, not implementation authority.

This distinction matters because Darklands circulated in several patched
versions. Reimplementing a famous 1992 bug that was fixed in 483.07 would be
just as inaccurate as silently fixing a defect that remains in 483.07.

## COAB Still Follows the Original

The Certified Original-Code Boundary layer does not “repair” either defect.
It preserves the original segment/offset owner, reads, writes, call order, and
return behavior. That raw relation is our executable historical record.

Policy belongs above it. The clean gameplay or SDL layer may reproduce,
correct, or suppress a defect, but only with a documented decision. Tests pin
both the original relation and the chosen product behavior.

That separation lets the project be faithful without being careless. Bugs
are not erased, accidentally amplified, or allowed to drift into folklore.
