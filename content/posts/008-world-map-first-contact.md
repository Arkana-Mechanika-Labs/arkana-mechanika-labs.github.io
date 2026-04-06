---
title: "Devlog #008 - The Runtime Side Starts to Click"
date: 2026-04-03
tags: ["devlog", "reverse-engineering", "darklands", "dosbox-x", "runtime", "tooling", "world-map"]
description: "The custom DOSBox-X workflow matures into a real collaboration layer: the agent asks better questions, the human handles the fiddly bits, and the world map finally gives up its first confirmed runtime hook."
summary: "The custom DOSBox-X workflow matures into a real collaboration layer: the agent asks better questions, the human handles the fiddly bits, and the world map finally gives up its first confirmed runtime hook."
---

_Published April 3, 2026_

This session felt like an important turning point for the project.

Up to now, a lot of the reverse-engineering work has lived on the static-analysis side: opening the game in Ghidra, naming functions, following references, building up the game's internal logic piece by piece. That work has paid off, and it got us a long way. But some questions cannot be answered from static analysis alone. Eventually you need to look at the game while it is actually running.

That is where the custom DOSBox-X workflow comes in.

The important thing is that we are not just using DOSBox-X as-is. We have been tailoring it to the needs of this project. That includes adding ways to drive it automatically, set up runtime breakpoints without manually poking around in the debugger, collect logs and screenshots, and even queue mouse and keyboard input from the outside.

In theory, that means the tooling can help pilot the game automatically. In practice, Darklands is a very menu-driven, visual, slightly awkward game to navigate in a fully reliable way. So the most useful outcome was not "full automation solved." It was realizing that the right workflow is a hybrid one: the agent prepares the investigation and asks the runtime questions, the DOSBox-X tooling sets breakpoints and captures evidence, and a human pilot handles the menu navigation and visual decisions that are still easier for a person than a script.

This session pushed that idea much further. The DOSBox-X adapter became more solid, the session flow became clearer, and one particularly useful addition changed the rhythm of the work in a concrete way: the agent can now stop cleanly when it reaches a question that really needs live confirmation, instead of guessing or overextending static analysis. It emits a structured runtime request, what address to probe, what to observe, what each possible answer would unlock, and hands that question off to a guided DOSBox-X session. The evidence comes back into the next analysis pass.

There was also a concrete payoff from all of this: the world map is no longer a blind spot. Earlier static leads pointed us toward the old overlay-management side of the executable, but real runtime probes showed that those were not the hooks we actually needed. After improving the custom DOSBox-X path, we were able to break into a live world-map session and confirm a recurring runtime hook there. That does not solve the whole world-map problem overnight, but it gives us a real foothold where previously we had only educated guesses.

So the headline for this session is not "we did more emulator work." It is that the runtime side of the project is maturing into an actual operating model, one where static reasoning, runtime probing, and human judgment each do what they are best at, and the results feed into each other in a structured way.

The immediate next step is to use that model on the hardest open question: the dispatch table. The state machine is confirmed, but its targets are in dynamically loaded overlay segments that Ghidra cannot see. Reading them requires a live process. The agent now has a clean way to ask for exactly that, and there is a confirmed world-map hook waiting to serve as the first anchor when it does.
