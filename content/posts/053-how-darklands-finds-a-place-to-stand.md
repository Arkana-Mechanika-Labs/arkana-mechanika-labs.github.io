---
title: "Devlog #053 - How Darklands Finds a Place to Stand"
date: 2026-08-12T09:28:00+02:00
summary: "The combat placement corridor is now executable from its sixteen-word mask through clipping, packed-record tests, exact RNG retries, and final battlefield writes."
---

[The previous combat devlog](/posts/052-fifteen-pieces-of-combat/) ended with
an unusually specific promise: do not draw a battle screen around the gaps;
close the placement leaves and reconnect their parent first.

That work is now done.

The result is not yet a playable fight, but one of combat's largest internal
corridors has changed status. We no longer merely have notes describing how
Darklands searches for positions. The original mask producer, geometry chain,
packed-record predicate, and complete placement owner now execute as certified
raw C# owners, preserving the memory and RNG contract of the DOS program.

## Sixteen Words Decide Whether a Position Survives

The centre of the first dependency group is `proc_0014_5ECA`.

It begins by clearing sixteen words at `DS:E11C`. It then constructs a raw
geometry snapshot, conditionally composes four independently certified leaf
procedures, and OR-reduces the sixteen words. The final union is written to
`DS:D708` and returned in `AX`.

Those leaves do not return friendly booleans. They publish raw bits and words
into the shared mask:

- `proc_0014_63CC`, the leaf completed before the last devlog, can publish
  `4000h` at `E138` after one of 48 ordered predicates rejects a candidate;
- `proc_0014_60B0` has twelve more low-nibble-controlled rejection gates and
  can publish the same `4000h` bit;
- `proc_0014_66FE` scans nine packed four-byte entries, preserves signed table
  lookups and boundary tests, and can publish `2000h` at `E136`;
- `proc_0014_6600` scans thirteen records and conditionally copies indexed
  words into `E11C..E134`.

The parent does not replace those procedures with a simplified collision
test. It calls the original raw owners in the original order. It also preserves
an early route where the high word of the *centre* snapshot entry is tested,
`AX=FFFFh` is returned, and the previous `D708` value is left untouched.

That detail is easy to lose in a clean rewrite. It is also observable original
behaviour.

## The Rectangle Test Is a Small Pipeline of Its Own

Another dependency chain starts with `proc_0014_F3E2`. Given a point and four
signed bounds, it assembles a four-bit outcode: left, right, below, and above.
Equality is inside. The order of the bits and signed comparisons is exact.

`proc_0014_F284` calls that helper four times while testing a segment against
the rectangle. It preserves shared-outcode rejection, immediate acceptance
routes, wrapping 16-bit products, and signed 32-bit division at the conditional
intersection points.

Then we found the awkward part.

`F284` allocates two local stack words, but two reachable paths can read them
before that invocation initializes them. Initializing them to zero in C# would
make the code tidier and change the program.

The caller, `proc_0014_EF3C`, revealed the real contract. It invokes `F284` six
times, and each call reuses the same two physical words below the caller's
stack pointer. Conditional writes made by one child call are live inputs to the
next. The raw C# owners therefore pass this stack-shaped state explicitly from
call to call. It remains opaque because the original consumers have not earned
a gameplay name for it.

This is exactly the kind of behaviour a decompiler-shaped rewrite tends to
erase. Here, it became a first-class part of the certified ABI.

## Five Fixed Tries, Then 1,002 Chances

With those dependencies closed, we could certify the complete placement owner,
`proc_0014_4188`.

It first handles the no-coordinate sentinel: when both supplied coordinate
words are `FFFFh`, it returns without reading or writing memory.

Otherwise it publishes working coordinates, selects one of four certified
five-coordinate patterns, and tries that pattern's five coordinates. Each
candidate flows through the mask producer and the packed-record predicate
rather than through a modern approximation.

If the fixed patterns fail, the original randomized search begins. Every
attempt consumes exactly two bounded RNG calls, in this order:

```text
bounded RNG with 0030h
bounded RNG with 0018h
```

There are 501 attempts, one owner-wide relaxation transition, and then another
501-attempt budget. Only after both budgets fail does the owner skip the
record. A successful route eventually performs nine ordered low-nibble writes
through the live battlefield-grid segment.

The retry flag at `DS:E0A2` is also original state: it becomes one when the
retry phase begins and returns to zero at normal completion.

Changing 501 to a round 500, drawing the two random values in the opposite
order, or caching a repeated read would all produce a plausible placement
algorithm. None would reproduce Darklands.

## From a Research Description to Executable Authority

[Devlog #051](/posts/051-combat-is-a-pipeline/) described the broad placement
search from the research branch. The important change now is that the entire
selected owner and its dependency chain have crossed the project's authority
boundary:

```text
original bytes
    -> reconciled instructions and current certificates
    -> raw Segments owners
    -> sentinel-backed memory and RNG tests
```

At the placement integration point, nine focused tests passed, the full Engine
Release suite passed 3,729 tests, and Darklays passed 1,057 tests. No clean
combat service or SDL route was added.

The placement owner is complete. Its callers are not. The three reviewed
callers at `D882h`, `D966h`, and `DA18h`, along with the larger combat owner at
`0DEEh`, still fail closed.

That boundary is narrower than it was yesterday. More importantly, it is now
on the far side of a real, faithful battlefield-placement implementation.
