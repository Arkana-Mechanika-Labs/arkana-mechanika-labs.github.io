---
title: "Devlog #034 - One Engine, Any Frontend"
date: 2026-05-08T09:00:00
summary: "The restoration project now has a formal host interface: six contracts a frontend must implement, and a Core that does not care which one it is talking to. This is what makes research and implementation run in parallel."
---

The central architectural question of this project is not how to render
Darklands on a modern machine. It is how to separate what the original game did
from how a modern host chooses to present it.

These are not the same question, and conflating them is what causes
reimplementation projects to calcify around a single output target. The project's
answer has been refined across dozens of implementation slices and is now
enforced by tests that fail at build time.

## What Core Owns

Core owns what the original game did.

The startup sequence, the controller logic, the resource interpretation, the
presentation intent: these are Core's domain. Core does not own how any of those
things appear on screen or come out of a speaker. It does not know what a GPU
texture looks like. It does not know the difference between SDL and Unity.

When the original game entered the party creation screen, it loaded specific
files, composited specific surfaces in a specific order, and presented a specific
controller state. Core models that as a stream of typed events: a resource was
requested, a picture was decoded, a screen model was emitted. The screen model
carries typed draw intents, each with coordinates, source data, and a fidelity
level. Core does not say "draw a 320 by 200 texture at the center of the
window." It says "here is the original indexed frame, here are the draw intents
for the command labels and the roster names, here is what is confirmed and what
is still estimated."

A host decides what to do with those facts.

## The Host Interface

A new shared project, `Darklands.Engine.Host.Shared`, defines the full contract
a host must implement. Six interfaces:

A screen presenter receives Core's screen models and renders them. A music
presenter receives Core's cue events and drives the audio hardware or software
synthesizer. An input source translates host input events into original-style
BIOS input words before Core ever sees them. An asset byte source provides raw
file bytes when Core requests a resource. A clock provides timing. A logger
receives diagnostic output.

A host that implements these six gets everything Core needs to run. It receives
Core's event stream in return, and it can render, record, replay, or inspect that
stream however it chooses. The `DarklandsHostRunner` in the shared project
handles the event loop, the startup sequence, and the intro playback. Hosts
provide the peripherals; the runner drives the engine.

## SDL as the First Host

The SDL host is currently the only concrete implementation of this interface, and
it has been reorganized to reflect that role clearly. It is divided into focused
modules: video initialization, screen presentation, audio queuing, music bridging,
input translation, platform interop.

`SdlScreenPresenter` owns SDL video lifetime, the window, the renderer, the
texture, and the letterboxed upload of Core's indexed frames. It calls the
faithful VGA renderer to convert Core's `RuntimeScreenModel` into an RGB surface,
then uploads that surface to the GPU. The SDL host has no say in which pixels
appear where on that surface. It chooses the window size, the scaling mode, and
the border. The pixel content comes entirely from Core's draw intents.

`SdlSoundModuleMusicBridge` drives the MT-32 replay and OPL register streams from
Core-emitted cue events. When Core says cue `0x0014` was dispatched, the bridge
sends the corresponding hardware command sequence to the appropriate output path.
The cue data, and the loop structure that determines when the sequence repeats,
comes from Core. The SDL host owns the audio device and the buffer queue; it does
not own the music logic.

`SdlInputSource` translates SDL key events into the BIOS-style 16-bit input words
the original game used. Core receives those words and branches on them the same
way the original controller code did. The host never decides what a keypress
means in game terms. It decides what the player pressed; Core decides what that
press does.

{{< figure src="/images/rider_reimplement1.png" caption="The C# reimplementation open in Rider. Core behavioral classes on the left, the SDL host on the right: two separate projects that share nothing except the event contract." >}}

## Research and Implementation in Parallel

This separation has a consequence beyond portability: it allows research and
implementation to proceed simultaneously without either track blocking the other.

When a runtime probe confirms a new fact about the original game, that fact lands
in Core. It might correct a Placeholder fidelity marker to Confirmed. It might
add a new draw intent to a screen model with a precisely evidenced coordinate.
It might refine the resource request order based on a traced file I/O sequence.
Core absorbs it, the test suite validates it, and every host benefits without
being touched.

The SDL host is not the source of truth for any behavior. It is a consumer of
Core's truth. This means the team can be tracing the event system and the save
format while separately extending Core's screen models and writing tests, and
neither track blocks the other. Core is stable enough to receive new facts
because the host layer is genuinely decoupled from the behavioral layer.

The formats decoded in [devlog #032](/posts/032-the-game-is-its-data/) and the
assembly-reconstruction discipline described in
[devlog #033](/posts/033-the-long-game-of-faithful-reimplementation/) both feed
into Core through exactly this boundary. A format decoder adds a new event type.
A materialized assembly function becomes a new Core behavioral sequence. Neither
change requires the SDL host to do anything beyond recompiling.

## Enforcement

The decoupling is not maintained by convention. It is enforced by architecture
tests that run at every build.

The tests scan the SDL host's source and fail if it constructs a screen model
directly, reaches into behavioral controller classes, or decodes an original
resource format. They scan Core and fail if it references SDL, OpenGL, Unity, or
any concrete file system API. They verify that typed draw intents cannot collapse
back into untyped payload fields. They require that the renderer interface
exposes the common `RuntimeScreenModel` as its entry point.

A separate category of tests covers the faithful VGA renderer: it must not
reference party controller state or COMMONSP image data directly. Its only input
is a `RuntimeScreenModel`. Its only output is pixels.

204 tests currently pass. The count is not the point. The point is that every
architectural boundary experience has shown worth defending now has a test behind
it. The boundary between Core and host is defended. The boundary between renderer
and controller state is defended. The boundary between confirmed behavior and
placeholder approximation is defended.

## A Future Host

A Unity host would implement the same six interfaces the SDL host implements.
It would receive the same Core events, map `RuntimeScreenDrawIntent` items to
Unity sprites or render textures, play the music cue stream through Unity's audio
system, translate Unity input to the same BIOS words. Core would not change.

A headless test host would implement the same interfaces with no screen output at
all, capturing Core screen models to disk for comparison against reference frames.
The same host interface that drives an interactive SDL window can drive a
frame-accurate regression test.

The architecture makes this possible by keeping a clean answer to one question:
does this belong to the original game, or does it belong to the host? Core owns
the first. Hosts own the second. The interface between them is where the
restoration project's long-term flexibility lives.
