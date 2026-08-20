---
title: "Devlog #066 - Events: Darklands' Hidden Scheduler"
date: 2026-08-20
draft: false
tags: ["events", "reverse-engineering", "runtime", "scheduler", "game-state", "darklands"]
description: "Darklands events are persistent typed records in a shared scheduler/state table, governing delayed consequences, temporary modifiers, city conditions, quests, training, alchemy, recruitment, and maintenance callbacks."
summary: "A deep look at Darklands' event system: a 300-record persistent scheduler governing delayed consequences, temporary modifiers, city conditions, quests, training, alchemy, recruitment, and maintenance callbacks."
---

In Darklands, an “event” is best understood as a persistent, typed record in a shared scheduler/state table—not necessarily an encounter or a message card.

The same mechanism represents:

- delayed consequences;
- temporary character modifiers;
- city-specific conditions;
- quest/world-state markers;
- merchant stock or service state;
- training opportunities;
- alchemy work in progress;
- recruitment state;
- records that trigger maintenance callbacks when time advances.

This is why we must preserve event kinds and fields mechanically until their consumers prove their meaning.

## The underlying event table

The original maintains a table of up to 300 pointers at `[7E30]:1B2C`. Each active pointer refers to a 48-byte (`0x30`) record. The table is loaded from `EVENTS.TMP` or restored from a save.

A fresh “Create New World” explicitly removes the previous `EVENTS.TMP`, so the initial event table is genuinely empty. Quickstart then creates its initial records through original event producers.

The principal record layout is:

| OffsetProven role |                                                              |
| ----------------- | ------------------------------------------------------------ |
| `+00`             | Kind-specific selector or identifier                         |
| `+02..+08`        | Creation hour, day, month, year                              |
| `+0A..+10`        | First scheduled date                                         |
| `+12..+18`        | Second scheduled date                                        |
| `+1A`             | Kind-specific field; often party slot, sentinel, or selector |
| `+1C`             | Frequently a location, but not universally                   |
| `+1E`             | Kind-specific value or payload                               |
| `+20`             | Kind-specific value                                          |
| `+22`             | Event kind                                                   |
| `+24`             | Maintenance flags                                            |
| `+26`             | Maintenance callback index                                   |
| `+28..+2E`        | Additional kind-specific payload                             |

The crucial point is that `+1C`, for example, must not simply be named `CityId` globally. It means that for several event families, but other kinds use it differently.


## How scheduling works

There are two independent date tuples.

### First schedule: availability or “due” predicate

Most MSG owners query the first schedule at `+0A`. A record is due when:

```
record date <= current game date
```

The comparison is signed 16-bit and ordered year → month → day → hour.

Being due does not necessarily consume the event. It merely makes the record eligible for an owner. The owner may:

- expose or disable a row;
- choose another card;
- alter an ability-check threshold;
- return a payload;
- enter a special branch;
- explicitly delete the record afterward;
- leave it in place for later queries.

Thus, “due” does not mean “automatically fires once.”

### Second schedule: expiration and maintenance

Time advancement also examines the second schedule at `+12`.

When it becomes due:

- an ordinary unarmed record is normally removed;
- kind `0008h` has special cleanup behavior involving related `0008h`/`001Ch` records;
- if maintenance flag bit 0 at `+24` is armed, the original dispatches through the callback index at `+26`.

We have recovered a 32-entry callback table. Entries 0–9 are at least partly decoded; entries 10–31 remain mostly bounded original-code owners. Some callbacks modify party fields, location data, create follow-up records, or display messages.


## Generic operations we have decoded

The original has a fairly complete event-record API, primarily in overlay 29:

- Find a free slot; return `FFFFh` if all 300 are occupied.
- Initialize all 48 bytes and stamp the creation date.
- Search by kind.
- Test whether a kind exists.
- Test whether a matching record is due.
- Count records or due records.
- Return a matched record’s `+1E` payload.
- Search with wildcard filters over `+00`, `+1A`, `+1C`, `+28`, and `+2A`.
- Create a new record.
- Reuse an existing matching record and reschedule it.
- Mutate a record’s `+1E` payload.
- Delete one record or all matching records.
- Convert kind `0008h` source records into kind `0024h` follow-ups.
- Run due-record maintenance callbacks.

The original uses `FFFFh` as a wildcard in several filtered searches. `270Fh` is a special schedule argument which suppresses ordinary schedule calculation or installs a far-future sentinel, depending on the producer.


## Event kinds with relatively strong gameplay meaning

| KindCurrent understanding |                                                                                                                                                                                                                 |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0007h`                   | Marketplace/service state. Goods Merchant, Foreign Trader, and Pharmacist owners create or reuse these records. Exact fields distinguish provider, city, and service/stock state.                               |
| `000Ah`                   | A failed city-gate persuasion attempt creates this current-city consequence, scheduled 12 hours ahead.                                                                                                          |
| `000Bh`                   | A failed city-gate sneaking attempt creates this current-city consequence, also scheduled 12 hours ahead.                                                                                                       |
| `000Ch`                   | Failed daytime city-gate fame/reason attempts. The decoded paths schedule it 12 or 13 hours ahead.                                                                                                              |
| `000Eh`                   | One of the two consequences of a failed alchemical tactic at a city gate; scheduled 30 hours ahead.                                                                                                             |
| `0011h`                   | The longer city-gate alchemy consequence, scheduled 240 hours ahead. It also affects later persuasion/sneaking behavior.                                                                                        |
| `001Dh`                   | Residence alchemy work in progress. `+00` is the formula record, `+1A` the character slot, and `+20` the batch count. Cancelling or leaving the activity restores ingredients and deletes the matching records. |
| `0028h`                   | Current-city training offers. The fields identify the skill, cost, and training scale. Residence “Train or study” enumerates due records, charges the cost, and attempts improvement from their payload.        |
| `0048h`                   | Party-slot/field temporary modifier family whose active value is the maximum positive matching `+1E`.                                                                                                           |
| `0049h`                   | Party-slot/field modifier family whose matching `+1E` values are summed. Several saint effects produce these.                                                                                                   |
| `004Ah`                   | Related party-slot/field/value modifier producer. Production is proven, but its complete consumer/expiration behavior is not yet closed.                                                                        |
| `004Ch`                   | Recruitment-roster event. The Add path creates it for a roster ID and location with a schedule exactly 168 hours—seven days—ahead. The exact due tuple is later used by recruitment membership logic.           |
| `004Dh`                   | City-square prison-related availability. A due current-city record exposes the prison row; later prison paths find and delete it.                                                                               |
| `0051h`                   | Due current-city residence alchemy-disaster event. With the certified field shape, it triggers the inn explosion branch, including Pay/Flee choices and their virtue/reputation/fugitive effects.               |


## Broad or only partly interpreted families

These have proven consumers or producers, but we should retain their raw names until more owners are decoded.

| Kind(s)What is proven     |                                                                                                                                                                                                                                         |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0003h`                   | Recognized by a Pharmacist existing-stock branch. Its complete producer/lifecycle is not yet promoted.                                                                                                                                  |
| `0008h`                   | Large generic quest/world/service record family. Many helpers filter it by `+28`, location, selector fields, and schedule. It can generate `0024h` follow-ups.                                                                          |
| `001Ch`                   | Closely related region/event family. Some generic scans requesting `001Ch` deliberately accept stored `0008h` records as aliases. Quickstart creates `001Ch` records.                                                                   |
| `0024h`                   | Follow-up records produced from `0008h`; used by marketplace and pharmacist stock gates. The record mechanics are known, but no universal gameplay label is justified.                                                                  |
| `0012h`, `0013h`, `0014h` | Current-city conditions used by night-side-street and guard calculations. `0012h` contributes 2 and `0013h` contributes 1 to a classifier; `0014h` supplies another publication/penalty flag. Their narrative origin is not yet proven. |
| `0017h`, `0019h`, `001Ah` | Due-record conditions that alter $MARKE01 row availability/classification. Their complete origin and narrative meaning remain open.                                                                                                     |
| `001Eh`                   | Changes one $CITYE00 approach owner’s classification.                                                                                                                                                                                   |
| `002Fh`                   | A current-city marker created by the certified $SHELL00 alternate. Its exact gameplay name is deliberately unresolved.                                                                                                                  |
| `0039h`                   | Alters $DOCKS00 presentation arguments.                                                                                                                                                                                                 |
| `003Ah`                   | Current-location override used by $COUNC00 publication.                                                                                                                                                                                 |
| `003Eh`                   | A conditional marketplace/merchant routing gate.                                                                                                                                                                                        |
| `0042h`                   | Due location-record predicate involved in $CITYN00 “Empire affairs” result selection.                                                                                                                                                   |
| `0043h`                   | Party/roster lifecycle and exclusion family. It can reject recruitment candidates, and calendar maintenance recognizes a special empty-party-slot case. The complete system is not closed.                                              |
| `0047h`                   | A maintenance callback body is partly decoded and gated through party-state storage; its higher-level meaning is unresolved.                                                                                                            |
| `004Bh`                   | A maintenance callback can allocate this kind, but the complete gameplay interpretation is unresolved.                                                                                                                                  |
| `0060h`                   | A due record clears a five-slot accumulated value; otherwise a raw assignment-based accumulator is updated. The gameplay label is not yet proven.                                                                                       |
| `0063h`                   | Produced by startup and saint message/effect vectors. Production is proven, but it does not yet have one safe universal gameplay name.                                                                                                  |

## Save-observed kinds

The save corpus also contains kinds for which we have not promoted an original producer or consumer:

```
0026 002A 002B 0031 0034 0037 003D
005B 005C 0061 0064 0065
```

These prove that the kinds exist in real saves, but nothing more. We must not implement behavior based only on their presence.

`0064h` deserves particular caution: some producers write `0064h` to record field `+1E`. That does not mean they are producing event kind `0064h`, because the kind is at `+22`.

## Important behavioral conclusions

Several rules now appear stable:

1. Events are persistent state, not immediate calls. A routine may create a record now so an unrelated MSG owner notices it days later.
2. Location is usually part of the key. Many events are meaningful only when `+1C` matches the current city. Our explosion test used Steyr only because the developer fixture was created for the current city—not because the original explosion logic is hardcoded to Steyr.
3. Repeated actions may reuse records. The generic producers often search first, then update and reschedule an existing record instead of producing duplicates.
4. Different kinds can cooperate. The clearest example is the `0008h → 0024h` follow-up mechanism and the special `0008h`/`001Ch` aliasing.
5. Expiration can have effects. Some records simply disappear at their second scheduled date; others call a maintenance callback that can modify characters, locations, or produce more events.
6. Event presence, due status, and consumption are distinct. A record can exist but not yet be due, be due and repeatedly queried, or be consumed only by one specific owner.
7. Full-table failure is observable. Producers return `FFFFh` when no slot is free. We preserve that as a typed boundary rather than silently dropping an event.

## Where the reconstruction still falls short

We have a strong generic record model and many certified owner-specific uses, but not yet a complete universal event engine.

The largest remaining gaps are:

- most armed maintenance callbacks 10–31;
- the complete semantic map for `0008h`/`001Ch` quest and world records;
- origins of several city and marketplace condition kinds;
- full save-load/runtime execution for every save-observed kind;
- exact relationships between some temporary modifiers and their expiration messages;
- complete producer/consumer closure for `0043h`, `0047h`, `004Ah`, `004Bh`, and `0063h`.

So the safe summary is: **we understand the data structure and its generic operations quite well; we understand several important event families end-to-end; but the event-kind namespace as a whole is still only partially decoded.**
