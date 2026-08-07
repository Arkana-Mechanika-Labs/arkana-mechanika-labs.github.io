---
title: "Devlog #044 - When Evidence Became Reusable"
date: 2026-08-03T09:30:00
summary: "Darklays now indexes current evidence, matches exact helper contracts, and builds selected-path releases without making researchers rediscover the same RNG, calendar, input, and dispatch machinery for every owner."
---

Reverse engineering is supposed to get faster as the program becomes less
mysterious.

For a while, our decoding did get faster—but the complete reconstruction cycle
did not.

A new city action might use an RNG helper we already understood, a calendar
path we had already certified, the same generic MSG input routine, and the same
central state dispatcher. Reading its local instructions could take minutes.
Proving that every dependency was still current could take much longer.

The facts were present, but they lived in different places:

```text
Darklays packets
promoted facts
annotations
StateEffect certificates
Ghidra and Reko intakes
runtime observations
the raw-state atlas
the decision census
C# implementations
tests and release receipts
```

The project needed more than a larger archive. It needed a way to ask the
archive a precise question.

That work changed Darklays again.

## The Cost of Knowing Something Twice

Consider a routine that makes one random roll, advances the calendar on one
branch, reads the resulting hour, and publishes a new raw state.

By this point, none of those pieces is exotic. The project already has
byte-faithful implementations and certificates for the original RNG, selected
calendar paths, hour classification, event maintenance, and central
redispatch.

Yet a new caller could still trigger a long manual search:

```text
Which calendar certificate covers literal 0001h?
Does it return the live data segment the caller needs?
Which packet is current?
Is the helper whole-owner authority or selected-path authority?
Did its evidence move into a durable bundle?
Does the parent require a register or memory effect that the helper
certificate does not expose?
```

A wrong answer is dangerous. Reopening every helper is wasteful.

The solution was not to weaken the rules. It was to make the existing rules
queryable.

## A Content-Addressed Evidence Index

Darklays can now build a derived MSG evidence index.

The index is keyed by the identities that matter during reconstruction:

- raw state and raw owner ordinal;
- canonical owner and call site;
- current packet and certificate;
- entry predicate and observation boundary;
- helper dependencies;
- implementation and test files;
- atlas and census relations;
- Ghidra, Reko, and runtime evidence;
- exact artifact hashes.

A lookup such as:

```text
msg-lookup --state 0013 --ordinal 0007
```

does not authorize anything. It returns the current map of what the project
already knows.

The result can say:

```text
canonical action owner: proc_0048_2BAE
C# candidate: present, focused-tested, not yet wired
current RNG authority: found
calendar literal-0 authority: found
calendar literal-1 authority: found
hour-classifier authority: found
parent suffix: already certified
missing dependency: none
```

That is a much better starting point than searching filenames and remembering
which report superseded which older report.

The index itself is disposable and non-authorizing. Its source key is built
from the hashes of the authoritative artifacts. When those change, the index is
rebuilt. The original bytes, packets, certificates, and promoted facts remain
the evidence.

## Matching Contracts Without Guessing

Finding a helper is only half of the problem. The caller still has to prove
that it is allowed to reuse the helper's existing contract.

Darklays now has a restricted helper-contract matcher.

It does not understand friendly names. It does not decide that two routines are
“basically calendar code.” It only proves small mechanical relations:

```text
exact argument equality
finite-set inclusion
signed or unsigned range inclusion
exact alias conditions
exact observation-boundary coverage
exact authority and freshness hashes
```

Its answers are deliberately limited:

```text
proven
rejected
unknown_requires_review
```

There is no “closest match.”

This mattered immediately for `proc_0048_2BAE`. The local action had already
been translated into C#. It makes one range-100 random draw, compares it with a
raw threshold, and selects one of two previously certified calendar paths. On
one arm it also calls the current hour classifier. The action then publishes
state `0001h`, `0006h`, or `0008h`.

The matcher found and pinned the exact existing contracts. No helper packet was
regenerated. No calendar behavior was generalized beyond the literal paths
already proved. The action could be promoted as a selected canonical-entry
composition and wired into its parent without pretending that its whole owner
or every calendar route was complete.

That pilot demonstrated the purpose of the tool: not discovering new game
logic, but allowing accumulated knowledge to compound.

## From Whole Owners to Observable Transactions

Darklays still supports complete Certified Original Owner Services. Small,
bounded, reusable routines are excellent candidates for whole-owner
certification.

Large game controllers are different.

A city owner may contain many rows, several event branches, alternate selection
tables, callbacks, card loops, and rare outcomes. Waiting for every branch to be
understood would block useful gameplay for months. Treating an interior block
as a new public function would be equally misleading.

The project now uses a stricter transaction model.

For one canonical entry under a precise predicate, we choose a meaningful
observation boundary and record everything that remains visible there:

```text
E = exact entry predicate
B = next stable game-visible boundary
O = control result, live state, persistent writes, ordered effects,
    and timing that later logic can observe
```

If the reconstructed path matches the original over `O`, the selected path may
be executable. Every other route fails at its first unresolved original
address.

This is how large owners can grow one honest transaction at a time without
leaking path-specific knowledge into whole-owner claims.

## One Release, Not a Trail of Half-Releases

Evidence work used to leave a long wake of packet attempts, temporary exports,
manually copied hashes, and metadata edits.

The current release path is much more deliberate.

A StateEffect batch stages:

- the semantic claim;
- the selected certificate;
- promoted-fact and annotation fragments;
- metrics updates;
- durable artifact inventory;
- evidence-index lookup receipt;
- helper-match receipts;
- focused validation;
- Ghidra and Reko feedback or an exact zero-work disposition.

The candidate is validated before it touches the global promoted facts. The
final release checks the exact expected postimage, runs the full test suites
once, generates the feedback ledger, commits, pushes, and verifies the remote
heads.

Re-running the same preparation is deterministic. A changed helper, parent
predicate, packet, or observation boundary invalidates the appropriate receipt.
A comment or output directory does not.

This does not make the ceremony free. It makes it predictable—and, more
importantly, it prevents clerical work from masquerading as new reverse
engineering.

## The Tool Is Still Allowed to Refuse

The new index and matcher are accelerators, not escape hatches.

They cannot prove an unusual stack alias. They cannot turn a runtime address
into a canonical owner without valid normalization. They cannot close an
indirect callback whose frame is unknown. They cannot infer a persistent effect
from a similar sibling.

When the caller asks for more than the selected helper contract provides, the
match is rejected. When the implication is too complicated, the result is
`unknown_requires_review`.

That refusal keeps the speedup honest.

## A Healthier Kind of Scale

The engine now carries well over two thousand tests. Darklays carries more than
a thousand of its own. Hundreds of promoted facts are checked for current
packets, hashes, certificate roles, ownership, and freshness.

The raw numbers are not the goal. The useful change is that new ordinary city
edges increasingly reuse existing evidence instead of creating another
analysis island.

A sibling owner can now begin with one lookup, one focused decompiler review,
one small owner-specific delta, one selected E-to-B composition, and one
coherent release.

Novel mechanisms are still difficult. Shared tails, indirect callbacks,
mini-games, and new subsystems still require careful work.

But familiar mechanisms have started to feel familiar.

That is how a reverse-engineering project begins to accelerate: not by lowering
the standard, but by paying for each hard-won fact only once.
