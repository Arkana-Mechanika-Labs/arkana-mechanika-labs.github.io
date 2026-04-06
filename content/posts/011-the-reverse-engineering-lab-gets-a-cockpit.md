---
title: "Devlog #011 â€” The Reverse-Engineering Lab Gets a Cockpit"
date: 2026-04-06
draft: false
tags: ["workflow", "frontend", "runtime", "codex", "claude", "dosbox-x", "ghidra", "automation"]
description: "The Darklands Restoration Project now has a unified Claude/Codex workflow, artifact-driven handoffs, and a guided runtime cockpit that turns hybrid DOS reversing into a repeatable system."
summary: "The Darklands Restoration Project now has a unified Claude/Codex workflow, artifact-driven handoffs, and a guided runtime cockpit that turns hybrid DOS reversing into a repeatable system."
---

_Published April 6, 2026_

This week was less about one isolated reverse-engineering breakthrough and more about something
arguably more valuable: building a real operating system for the work itself.

The Darklands Restoration Project is no longer just "an agent in Ghidra" plus whatever notes
survive the end of a session. It now has a resilient, multi-provider workflow that can carry
static analysis into runtime validation and back again without losing context, duplicating work,
or depending on one fragile chat thread staying alive forever.

That sounds abstract. It is not. It means the project can now move faster, waste fewer credits,
recover more cleanly from interruptions, and turn each session into durable progress instead of
ephemeral conversation.

---

## Why this matters

Reverse engineering a 16-bit DOS game is not a straight line.

One session is pure static analysis in Ghidra. The next needs a live DOSBox-X trace. Then the
result has to come back into static reasoning, be recorded in the knowledge base, and feed the
next question. If that handoff is sloppy, you lose time. If it depends on one model, one window,
or one memory buffer, you lose momentum. And if it burns too many credits, you lose the ability
to keep iterating at all.

So this sprint focused on the bottleneck behind the bottlenecks: the workflow.

---

## The big upgrade: one workflow, two providers

The reverse-engineering pipeline now supports both Claude Code and Codex through the same
frontend and the same project artifacts.

That means:

- the same bounded session goals
- the same compact resume context
- the same findings pipeline
- the same runtime request / runtime evidence loop
- the same session reports and handoff files

In practical terms, if one provider becomes expensive, constrained, or temporarily unavailable,
the project does not stall. A clean session boundary is now a true switching point.

That is a big deal for a sponsor-facing project, because it means the work is becoming
operationally resilient, not just technically interesting.

---

## The frontend is now a real command center

The project dashboard used to be informative. It is now becoming actionable.

It can now:

- show live session state, turns, tokens, duration, and boundary status
- tell the operator whether it is safe to switch providers
- recommend whether the next action should be `Run` or `Resume`
- expose a session handoff and a curation handoff after the reverse-engineering pass ends

The important shift is philosophical as much as technical: the UI is no longer a thin wrapper
around an agent. It is becoming the place where the whole workflow becomes visible, inspectable,
and repeatable.

That matters because reverse engineering is hard enough. The tooling around it should not be
mysterious too.

---

## Runtime work is no longer a side quest

This is the part I am happiest about.

Darklands keeps forcing an uncomfortable truth: some of the most important answers do not exist in
the static image alone. Overlay dispatch, live state changes, real execution targets, and menu-
driven transitions often need to be observed in motion. The old way to handle that was effective,
but fragile: run a separate Codex session, talk through the runtime steps manually, then hope the
important conclusions get handed back cleanly.

The new runtime cockpit inside the frontend is designed to make that loop much more robust.

It can now:

- launch the patched DOSBox-X plus Darklands session on the host
- switch the runtime workflow onto Codex automatically as a safeguard
- show the active runtime request and its capture requirements
- guide a human operator through the live session
- set breakpoints, continue, wait for events, read registers, capture screenshots
- check whether the requested evidence is actually complete before allowing a save
- run a bounded Codex summarizer on the capture
- write structured `runtime_evidence.json`
- append a narrative note to the cross-provider `handoffs.md`

That is the key innovation here: runtime validation is now treated as a first-class phase of the
pipeline, not an awkward detour.

---

## A hybrid model that actually respects what humans are good at

One of the most promising things about this workflow is that it does not pretend the human should
disappear.

In these runtime sessions, the human pilot is still the best part of the system for:

- navigating DOS-era menus
- recognizing whether the game is on the right screen
- reacting to weird edge cases in real time

The agent is better at:

- planning the probe
- choosing the breakpoint target
- deciding what to capture
- turning the results into a reusable answer

So the workflow now leans into that hybrid model instead of fighting it. The runtime coach can ask
for checkpoints like "tell me when you are on the world map," react to what the operator reports,
and then turn the resulting trace into a structured handoff for the next static session.

This is the part that feels genuinely new: not just AI-assisted reversing, but a coordinated
human plus agent plus emulator loop designed specifically for old software archaeology.

---

## Why sponsors should care

There are two kinds of progress in a project like this.

The first is visible progress: more functions named, more structures understood, more subsystems
mapped. That is still happening, and it will keep happening.

The second is infrastructure progress: making the process itself faster, more resilient, more
reproducible, and less dependent on one lucky session going well.

That is what this sprint accomplished.

Sponsorship is not just buying another hour of reverse engineering. It is helping build a toolchain
that makes every future hour more productive:

- less credit waste
- fewer dead-end sessions
- cleaner handoffs
- better reuse of runtime evidence
- stronger continuity across providers and across days

For a restoration project built on deep technical archaeology, that kind of leverage matters.

---

## What comes next

The immediate next step is straightforward: use the new runtime workflow to resolve the
`rtlink_load_char` path cleanly, map the real implementation back into the static overlay layout,
and keep pushing on the `party_add_member` family.

But the more important story is broader.

The project is no longer just uncovering Darklands. It is also building a reusable workflow for
how AI-assisted reverse engineering of old games can actually work in practice: bounded,
inspectable, cross-provider, hybrid, and durable.

That is the sort of infrastructure that makes a restoration effort feel less like a heroic one-off
and more like the foundation of a real lab.

If that vision resonates, you can help keep the work moving:

[Sponsor the project](https://github.com/sponsors/Arkana-Mechanika-Studios)
