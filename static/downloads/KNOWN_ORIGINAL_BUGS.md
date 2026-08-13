# Known Original-Game Bugs

This register records defects or internally inconsistent behavior that is
present in the original Darklands 483.07 executable. It is not a list of bugs
introduced by the C# rewrite.

Unverified versioned reports and investigation leads are kept separately in
`docs/research/DARKLANDS_483_07_REPORTED_BUG_CATALOGUE.md` in the engine
repository. That catalogue is research-control-only and cannot authorize
behavior or an entry in this register.

An entry requires original-byte evidence. Runtime observation, screenshots,
manuals, and the quick-reference card may corroborate the behavior but cannot
establish it by themselves. Each entry records the rewrite's explicit
disposition so that an original defect is neither reproduced accidentally nor
silently corrected.

Disposition values are:

- `replicate`: preserve the original defect for strict compatibility;
- `correct`: implement a documented intentional correction;
- `disable`: consume or omit the affected input without executing the defect;
- `pending`: no executable policy has been chosen yet.

## DL-ORIG-UI-0001: Ctrl+F leader shortcut corrupts merchant UI state

| Field | Value |
| --- | --- |
| Status | byte-confirmed original defect/quirk |
| Original units | `proc_0043_33C6`; `proc_0032_0000`; `proc_0032_0F60`; `proc_0032_076C`; `proc_0032_078E` |
| Principal instructions | `ovl_0032:15E4..1763` |
| Affected input | Ctrl+F1 through Ctrl+F5 while the Goods Merchant controller is active |
| SDL disposition | `disable` |

The generic extended-key dispatcher maps BIOS words `5E00h..6200h` to party
slots 0..4, writes the chosen leader to byte `DS:907Bh`, and repaints the party
panel. That is consistent with the quick-reference card's "define leader"
description.

The nested merchant controller intercepts the same keys. It validates the
chosen active party slot, writes `DS:907Bh`, and repaints only the party panel.
It does not call the full merchant redraw at `proc_0032_078E`, does not update
the merchant transaction target at `DS:884Eh`, and does not recompose the
displayed barterer text, inventory lists, or prices. Execution then falls
through into `ovl_0032:160F..1763`, the same block used to switch Purchase and
Sell, which flips the active list and redraws the two controls with their
enabled/disabled colors.

The separation between `DS:907Bh` and `DS:884Eh` is intentional: the former is
the leader/negotiator used by pricing helpers, while the latter is the party
member whose inventory is displayed and mutated. The dedicated "Barter for
another person" command at `ovl_0032:1384` changes `DS:884Eh`, rebuilds that
member's trade data, and redraws the relevant merchant surface. The defect is
that Ctrl+F changes the negotiator without the corresponding merchant refresh
and also toggles Purchase/Sell. On merchant exit, `proc_0032_076C` restores
`DS:907Bh` from the saved byte at `DS:884Ch`, so the apparent leader change is
not persistent either.

The SDL host therefore consumes Ctrl+F1--F5 during merchant input without
changing the leader, transaction target, active list, prices, inventory, or
visual state. It emits a diagnostic naming this entry. Normal leader selection
outside merchant-specific controllers remains a separate original mechanism.

If this entry is revisited, do not merely remove the suppression. Choose and
document one of these policies:

1. reproduce the original defective sequence exactly;
2. retain the separate negotiator and inventory target, but fully redraw the
   merchant surface after changing negotiator and do not toggle Purchase/Sell;
3. continue requiring the leader to be selected before entering the merchant.

Supporting reconstruction report:
`evidence/reconstruction/darklands_483_07/msg/msg_marke00_merchant_input_dispatch_frontier_20260812.md`.

## DL-ORIG-GAME-0001: Merchant charges for an item that a full inventory cannot accept

| Field | Value |
| --- | --- |
| Status | byte-confirmed original defect/quirk |
| Original units | `proc_0032_0F60`; `proc_0029_5090`; `proc_0031_4A04`; `proc_0032_1770` |
| Principal instructions | `ovl_0032:1032..1187`; direct inventory selector enters `ovl_0031:4B9D` |
| Affected action | Purchase with 40h occupied inventory records and no compatible stack that can accept quantity 01h |
| SDL disposition | `replicate` |

The Goods Merchant Purchase arm checks affordability, calculates its payment
price, and calls `proc_0029_5090` to subtract that price from the three-word
party purse before calling `proc_0031_4A04` to insert the item. The inventory
owner first tries to merge the item into an exact code/type/quality stack. If
no compatible stack accepts the additional quantity, it may append a new
six-byte record only while the inventory count is below `40h`.

At count `40h`, a failed merge returns the unchanged count without inserting
the purchased item. The Purchase caller does not test that return for failure
and does not refund the earlier purse subtraction; it stores the returned
count and redraws the held-item list through `proc_0032_1770`. The resulting
observable behavior is therefore:

```text
payment succeeds -> inventory insertion reports full -> money remains spent
-> no purchased item appears
```

This is narrower than merely having 64 inventory entries. A purchase can
still succeed at count `40h` when an existing compatible stack accepts the
quantity without byte overflow. Conversely, an otherwise compatible stack
whose resulting quantity would exceed `FFh` is skipped, so it does not avoid
the defect unless another compatible stack can accept the item.

The clean merchant controller deliberately preserves the original ordering
and exposes the outcome as `InventoryFullAfterCharge`. It must not silently
preflight capacity, reverse the calls, or refund the purchase unless the
project later adopts and documents an explicit `correct` compatibility
policy.

Supporting reconstruction report:
`evidence/reconstruction/darklands_483_07/msg/msg_marke00_merchant_input_dispatch_frontier_20260812.md`.

---

This website copy was published with Devlog #058 on 2026-08-13. The canonical,
maintained document is
[`docs/KNOWN_ORIGINAL_BUGS.md`](https://github.com/Arkana-Mechanika-Studios/darklands-engine/blob/main/docs/KNOWN_ORIGINAL_BUGS.md).
