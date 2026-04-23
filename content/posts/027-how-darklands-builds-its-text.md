---
title: "Devlog #027 - How Darklands Builds Its Text"
date: 2026-04-23T18:00:00
summary: "The runtime machinery behind the $-token system traced end to end: the recursive scanner at 0xD728, the pronoun grammar bundle that the German edition uses but English data never surfaced, the template engine at 0xD67E, and the Create New World screen owner at 0xD444."
---

Devlog #026 ended with a specific open question. The German edition revealed a richer token vocabulary than the English data suggests: `$his1` through `$his6`, `$him1`, `$him2`, `$CON`, grammar-sensitive substitutions that German players see and English players never do. But finding the vocabulary in the data is not the same as finding the machinery in the executable. How does the game actually dispatch a `$token` at runtime? Where does the pronoun grammar bundle live, and what calls into it?

This session traced that chain.

## The post-stage selector worker

The investigation anchored on what the project has been calling the resident post-stage family: the code responsible for composing and delivering text messages following state transitions. After a player completes a stage in Create New World, something builds that stage description text, resolves any variable substitutions in it, and produces the final output. That something had not been fully traced.

At `0x3679E` sits the resident post-stage selector worker. Two feeder lanes converge on it from separate directions: one from the resident post-stage feeder family rooted around `0x365B0`, one from an overlay sibling feeder at `1D2E:000A`. The worker runs two downstream paths depending on its inputs.

The primary path routes through a selector-table lookup anchored at `A895`. The table maps a selector value to a text result, and the worker delivers that result.

The fallback path is the more interesting one. When the primary lookup does not resolve, the worker drops into a pronoun-aware composition pass using a grammar bundle at `DS:521F`. That bundle is exactly where the German pronoun tokens live at runtime. The inflected possessive forms, the object forms, the `CON` alias: all of them resolve through this bundle.

This confirms something that the German data comparison only implied. The pronoun grammar bundle is not a German addition bolted onto an otherwise simpler engine. It is part of the base runtime. The English executable carries the same structure; the English content simply does not push material through those token slots in the shipped game. The capability was always there.

## 0xD806 is not the top

For several sessions, the working assumption was that `0xD806`, the resident stage dispatch entry, was the effective upper boundary for the post-stage text lane on the Create New World side. That assumption is now retired.

Two distinct wrapper functions sit above `0xD806`, each with a separate role.

**`0xD7C0` — `resident_stage_dispatch_append_builder`**: the straight-through case. It calls `0xD806` and appends the result into the caller buffer.

**`0xD728` — `resident_recursive_token_dispatch_builder`**: the scanner. This function walks its input text character by character, watching for `$`-prefixed alphanumeric sequences. Each time it completes a token, it routes that token through `0xD806` for resolution and appends the expanded result. Then it continues scanning the remaining input.

That is the `$`-token scanner. Every `$citySquare`, `$his3`, `$ChosenOneName` substitution in a Darklands text card passes through `0xD728` at runtime. The scan loop, the dispatch, and the append are all contained in this one function.

## The template engine at 0xD67E

Above the two builders sits `0xD67E`: `resident_build_selected_stage_text_from_template`. It drives both `0xD728` and `0xD7C0` depending on the nature of the input segment. Token-bearing template text goes through the recursive scanner; plain suffix text goes through the straight-through append builder.

The template engine does not select what to render. It receives a template and produces output. The selection happens one level above it.

## The screen owner at 0xD444

The function at `0xD444` is now named `resident_show_create_world_stage_screen`.

It selects the appropriate indexed template for the current Create New World stage, calls the template engine at `0xD67E`, and the rest of the chain unwinds from there. This is the top of the post-stage text pipeline for Create New World, the function we have been working toward since devlog #018 first materialized the Create New World body.

The full confirmed path:

```
0xD407 / 0xD43A   entry wrappers
      ↓
  0xD444   resident_show_create_world_stage_screen
      ↓
  0xD67E   resident_build_selected_stage_text_from_template
      ↓
0xD728 / 0xD7C0   recursive scanner / append builder
      ↓
  0xD806   resident_stage_dispatch_entry (selector gate)
      ↓
  0xDFD8   selector jump table
```

That is the Create New World text pipeline, end to end.

## Where the output goes: the pending-slot hub

The output of this chain does not go directly to the display. It feeds into a shared pending-slot worker at `0x1C850`.

Both the resident post-stage lane and the overlay sibling feeder at `1D2E:000A` converge on this hub. The worker runs in two modes driven by the caller: enqueue and flush. In enqueue mode it stores a segment reference into a 4-byte slot record. In flush mode it walks the slot table, combines each stored segment with a fixed offset `0x50C7`, calls the downstream append helper at `0xDE92`, then clears the slot.

The slot records are not arbitrary far pointers. They are segment-only descriptors: each one carries the identity of a pending overlay-chain text target through the segment word alone. The offset `0x50C7` is fixed on the flush side, not stored per slot.

The flush consumer is not unique to this hub. Byte-identical tails exist in at least four other module families, all sharing the same slot-table contract. This is a template reused across the codebase, not a one-off mechanism.

## A smaller placement: CFILE.DAT

A side result from this session placed `CFILE.DAT` inside section 138 of the EXE overlay layout, the startup and tactical controller block. It is not a standalone data file in the same sense as `ENM` or `CTY`. It belongs to overlay-resident code that sets up tactical encounters, which means understanding it properly will require tracing the section 138 load path rather than parsing the file in isolation.

## What comes next

Two questions are now in focus.

The first is the selector jump table at `0xDFD8`. This table is where each `$token` maps to its resolution: where `$his1` finds its grammar-bundle entry, where `$citySquare` finds its city-data lookup, where `$ChosenOneName` finds the active character name. Decoding the full table would turn the token vocabulary found in devlog #026 into a complete runtime map of what the game can express in text.

The second is what sits above `0xD444`. The entry wrappers at `0xD407` and `0xD43A` are confirmed, but their callers are not yet. Following that edge connects the Create New World text pipeline to the main game loop dispatch, closing the last gap in that flow.
