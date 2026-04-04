---
title: "Devlog #008 — The Runtime Side Starts to Click"
date: 2026-04-03
tags: ["devlog", "reverse-engineering", "darklands", "dosbox-x", "runtime", "tooling", "world-map"]
description: "The custom DOSBox-X workflow matures into a real collaboration layer: the agent asks better questions, the human handles the fiddly bits, and the world map finally gives up its first confirmed runtime hook."
summary: "The custom DOSBox-X workflow matures into a real collaboration layer: the agent asks better questions, the human handles the fiddly bits, and the world map finally gives up its first confirmed runtime hook."
---

Yesterday felt like an important turning point for the project.

Up to now, a lot of the reverse-engineering work has lived on the static-analysis side: opening the game in Ghidra, naming functions, following references, building up the game's internal logic piece by piece. That work has paid off, and it got us a long way. But some questions cannot be answered from static analysis alone. Eventually you need to look at the game while it is actually running.

That is where the custom DOSBox-X workflow comes in.

The important thing is that we are not just using DOSBox-X as-is. We have been tailoring it to the needs of this project. That includes adding ways to drive it automatically, set up runtime breakpoints without manually poking around in the debugger, collect logs and screenshots, and even queue mouse and keyboard input from the outside.

In theory, that means the tooling can help pilot the game automatically. In practice, Darklands is a very menu-driven, visual, slightly awkward game to navigate in a fully reliable way. So the most useful outcome was not "full automation solved." It was realising that the right workflow is a hybrid one.

The system now works more like a small team than a single tool:

- the agent prepares the investigation and asks the runtime questions
- the DOSBox-X tooling sets breakpoints, captures evidence, and can assist with automated inputs
- the human pilot handles the fiddly menu navigation and visual decisions that are still easier for a person than a script

That has turned out to be a much better fit for the game. We get the benefits of automation where it is strong, without pretending every menu and map transition should be fully scripted.

Yesterday's work pushed that idea much further. The DOSBox-X adapter became more solid, the session flow became clearer, and the whole runtime side started feeling less like an experiment and more like an actual operating model.

One especially useful part of this is the growing interaction between the agent and the runtime workflow. The agent can now stop cleanly when it reaches a question that really needs live confirmation, instead of guessing or overextending static analysis. It can ask for runtime evidence, describe what it needs to know, and hand that question over to a guided DOSBox-X session. That evidence can then be brought back into the next analysis pass.

That sounds simple, but it changes the rhythm of the work in a big way. Instead of one agent trying to do everything, we now have a clearer division of labour: static reasoning, runtime probing, and human guidance all feeding into each other. It is beginning to feel less like a lone RE session and more like the workflow of a small research team.

There was also a concrete payoff from all of this: the world map is no longer a blind spot. Earlier static leads pointed us toward the old overlay-management side of the executable, but real runtime probes showed that those were not the hooks we actually needed. After improving the custom DOSBox-X path, we were able to break into a live world-map session and confirm a recurring runtime hook there. That does not solve the whole world-map problem overnight, but it gives us a real foothold where previously we had only educated guesses.

So the headline for yesterday is not just "we did more emulator work." It is that the custom DOSBox-X workflow is maturing into a practical collaboration layer for the project.

We now have a setup where the emulator can be steered for our needs, the agent can ask better questions, the human operator can step in where that is still the most reliable option, and the results can flow back into the analysis in a structured way.

That is the kind of progress that makes future breakthroughs much more likely.
