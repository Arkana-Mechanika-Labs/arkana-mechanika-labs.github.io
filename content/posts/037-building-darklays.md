---
title: "Devlog #037 - Building Darklays"
date: 2026-07-19T08:15:00
summary: "Darklands moves much of its code through a custom overlay loader. We built Darklays to reconnect the executable on disk, the code running in DOSBox, the analysis in Ghidra and Reko, and the C# reconstruction."
---

There is a particular kind of address that shows up constantly while reverse
engineering Darklands. It looks like this:

```text
211F:04A2
```

At first glance, that seems wonderfully precise. Segment, offset, one exact
place in memory. Put a breakpoint there, click a row in the city, and the
debugger stops on the instruction that handles it.

The trouble is that `211F` is not a permanent home.

It is a segment DOS happened to allocate during that session. A few moments
later, the game may load different code into the same memory. The address that
held a city handler can become an inn, a church, or an entirely unrelated
service. If we inspect it after the transition, we may be looking at the code
for the destination rather than the code that got us there.

This is the central difficulty of working with Darklands. Much of the game is
not sitting neatly inside the visible executable, waiting for a disassembler to
find it. It moves through a custom overlay system built from resolver records,
source descriptors, relocation tables, loader stubs, and chains of small
dispatch routines.

We needed a way to connect all of those views without guessing. That need
became Darklays.

## The Executable Is Only the Beginning

Darklands starts with a normal DOS MZ executable, but the normal part is not the
whole file. Beyond the resident program image is a large body of code and data
managed by the game's own loader.

The loader describes that material through compact 18-byte records. Each record
contains enough information for the game to find a source payload, allocate
memory, apply relocation fixups, and make the result callable. Unfortunately,
"enough information for the original loader" is not quite the same as "obvious
to a modern analysis tool."

The first version of Darklays was built to solve that problem. It reads the MZ
header without throwing away the bytes beyond the resident image. It parses the
resolver records and their source descriptors. It finds the payload and fixup
tables, reconstructs the zero-filled tail the game allocates at runtime, and
produces an analysis image with the relocations applied.

Even that process cannot be reduced to one hard-coded layout. Most records
follow the same broad pattern, but some are incomplete, unusual, or simply not
understood yet. Darklays therefore tests several plausible layouts for each
record and records why one was selected or rejected.

If two candidates are too close to call, the record remains ambiguous. If a
payload extends outside the file, the record remains out of bounds. If a source
descriptor cannot be resolved, the record remains visible as an unresolved
record rather than quietly disappearing from the project.

That behavior became an important design principle: a bad record should not
destroy the analysis, but it should never be made to look good either.

## Finding the Loader's Doorways

The next problem was finding every place the resident executable can ask for
one of those overlays.

Darklands uses small ten-byte thunk records. Each thunk contains a far target,
a resolver-record identifier, and a relative call into the resident loader. An
older description of the executable documented a small, useful window of these
stubs. Darklays scanned the full file instead.

The result was a single strong run containing 751 thunk entries and 134 distinct
resolver identifiers. That is slightly larger than the older published count.

It would have been easy to trim the result until the numbers matched. Darklays
does the opposite. It keeps both the observed result and the older expectation,
then reports the disagreement as something to validate. Matching a familiar
number is not evidence that the parser is right.

Once those thunks and resolver chains were mapped, the moving parts of the
executable started to acquire stable identities. A routine could be described
as `proc_0045_10E2` instead of "whatever happens to be at `211F:04A2` in this
run." The former refers to original code. The latter refers to a temporary
place where that code happened to live.

## One Map for Several Tools

Materializing the overlays solved the byte problem, but it created another
question: which tool should own the analysis?

Ghidra is excellent at building a long-lived workspace of functions,
references, labels, comments, and data types. Reko provides a second view of
the control flow and can expose useful decompiler candidates. A focused custom
scanner is often faster at answering Darklands-specific questions about thunk
shapes, far-pointer tables, or compact 16-bit dispatch patterns.

We did not want three tools producing three subtly different versions of the
game.

Darklays therefore generates the shared map they all consume. It creates a
deterministic project manifest, assigns each materialized overlay an analysis
address, and exports the same bytes, procedure seeds, names, references, and
validation state to both Ghidra and Reko.

The Ghidra side is deliberately round-trip tested. Darklays builds an import
package and verifies it before Ghidra opens it. After the generated importer has
created the overlay blocks and annotations, a second script reads the project
back and checks that the expected functions, references, comments, and
bookmarks survived.

The Reko side follows a similar pattern. Darklays creates the workspace and
procedure seeds, runs the external tool, then harvests the useful results back
into a review package. Generic fallback names are kept separate from meaningful
discoveries so that a decompiler's confidence does not become our confidence by
accident.

Neither tool is treated as the final authority. They are independent witnesses
looking at the same original bytes.

## Connecting Runtime Back to the File

Static analysis still cannot tell us which overlay occupied a DOS segment at a
particular moment. That bridge requires runtime evidence from the same session
and, ideally, from the same event.

Darklays builds session-scoped segment maps. These maps can come from runtime
dumps, loader observations, Autoprobe captures, or carefully recorded manual
evidence. A runtime address is resolved through that map to a resolver record
and materialized offset, and only then to an owning procedure.

The distinction matters enough that Darklays has three resolution modes.

`strict` accepts confirmed mappings. `balanced` may identify one strong
hypothesis, but labels it as requiring runtime confirmation. `exploratory`
shows plausible candidates for investigation. Only the first can participate
in implementation authority.

Event-time code windows add another safeguard. When Autoprobe catches a
selected handler, it records bytes from the moment that handler is executing.
Darklays compares those bytes against the materialized overlays. Relocated
segment words in far calls and jumps may legitimately differ; opcodes and
ordinary data may not.

If the bytes match one original location, we have a strong bridge. If they
match several, the result is ambiguous. If they match none, Darklays preserves
the captured window as a recovery clue. It does not silently reinterpret the
address until something fits.

This solved one of the most dangerous failure modes in the project: using code
read after a transition to certify the code that caused the transition.

## From a Location to an Original Unit

Finding the correct bytes is necessary, but it is still not enough to rewrite a
routine.

A selected handler may begin in the middle of a larger owner. It may call five
helpers, write through a caller-owned pointer, branch on signed arithmetic, or
jump through a table whose targets are only partly known. A clean disassembly
of the first twenty instructions does not explain the complete behavior.

This is why Darklays grew an Original Code Unit Workbench.

For one proposed unit, the workbench assembles an implementation packet. The
packet brings together:

- original byte identity and procedure ownership;
- instruction boundaries checked by an independent 8086 disassembler;
- direct and indirect control flow;
- branch predicates and observed branch coverage;
- memory reads, writes, and caller-buffer effects;
- helper calls and the state of every helper contract;
- recovered tables and dispatch targets;
- Ghidra and Reko findings;
- runtime evidence, remaining blockers, and a verification plan.

The result is not a general confidence score. It is a decision with reasons.

An investigation packet can say, "this is probably the routine." An
implementation candidate can say, "the routine is owned and most of its shape
is known, but these effects remain unresolved." An implementation-grade packet
can authorize the whole original owner only when its bytes, branches, effects,
and reachable helpers are covered.

There is also a narrower path certificate. It can authorize one exact route
from a canonical owner entry while every unselected branch fails at its first
unresolved original address. It cannot turn an interior instruction into a new
public function, and it cannot promote the whole owner by implication.

That distinction is what allowed the city reconstruction to move forward
without pretending that enormous controllers were already complete.

## A Tool That Is Allowed to Say No

Darklays became useful when it stopped trying to make every packet succeed.

Unknown ownership is a blocker. A runtime mapping based only on a likely
relocation delta is a blocker. A disagreement over instruction boundaries is a
blocker. An unknown helper effect, indirect target, write destination, or
branch is a blocker.

Just as importantly, a packet can become stale. Every promoted result is tied
to hashes of the original bytes, its analysis revision, its helper packets,
and the feedback exported to Ghidra and Reko. If a child packet is regenerated
or a dependency disappears during cleanup, the parent no longer gets to call
itself current.

The freshness audit identifies the smallest set that must be repaired and the
order in which to rebuild it. The engine then checks the promoted facts before
allowing reconstructed behavior to remain executable.

This may sound severe, but it is much cheaper than discovering months later
that a comfortable C# abstraction was based on the wrong overlay or a single
runtime sample.

## What Darklays Changed

Darklays began on June 30 as an overlay materializer. Over 230 commits, it grew
into the bridge between the original executable, the live DOS runtime, two
external analysis tools, and the new engine. Its current test suite contains
774 passing tests.

The more important numbers are on the other side of that bridge. The engine now
contains 26 complete original owners that have passed the strict service gate,
plus ten promoted canonical-entry path compositions through larger blocked
owners. The complete 366-entry state-dispatch table has been recovered from the
original executable. The city presentation, input, clock, and state-transition
paths described in the next devlogs were built from these packets.

Darklays is not a generic DOS unpacker. It is not an emulator, and it does not
produce a modified playable executable. It does not contain or distribute the
game's original files. It is a workbench built specifically around the strange
way Darklands stores, loads, and reuses its code.

Most of all, it gives us a defensible answer to a question that used to be
surprisingly hard:

```text
What original code ran here, what did it actually do,
and are we ready to rewrite it?
```

Sometimes the answer is yes. Often the answer is not yet.

Both answers are progress.
