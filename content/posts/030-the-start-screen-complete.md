---
title: "Devlog #030 - The Start Screen, Complete"
date: 2026-04-27T09:00:00
summary: "The 2649 start-screen controller fully mapped: BIOS keyboard polling, exact button coordinates, confirmed dispatch for Q/C/T, and a fourth button that loads and draws but never fires in v483.07. Also: eight bytes that configure a sound card, and a voice clip that says 'Welcome to Darklands'."
---

After the intro sequence ends, `OPENING9.PAN` completes its post-intro branch and the engine
transfers through `0BC4:0291` and `11E3:18DD` into the start-screen controller at `2649:0084`.
This is where the player makes their first choice: Quickstart, Create New World, or The Story
Continues.

The `2649` controller is now fully mapped. Everything it does is accounted for, including one
thing that turned out to be more interesting than expected.

## How it reads input

The start screen does not use any game-layer input abstraction. It goes directly to the BIOS.

Keyboard polling is two calls: `INT 16h` with `AH=01h` to check whether a key is waiting, and
`AH=00h` to read the scan code when one is. The result is a 16-bit word with the scan code in
the high byte and the ASCII character in the low byte. The controller branches on those words
directly.

Pointer input works through three shared globals: `[6EF0]` holds the current button pressed
state, `[6EEC]` holds the X coordinate, and `[6EEE]` holds the Y coordinate. These are the same
globals used by every other controller that handles mouse input. The pointer zones on the start
screen map regions of the 320x200 display back to the keyboard words for Q, C, and T, so the
pointer and keyboard paths converge at the same dispatch point.

## The three buttons

The controller loads five PIC files: `STARTSCR.PIC` for the background, and `BUTTON1.PIC`
through `BUTTON4.PIC` for the action buttons. The confirmed draw coordinates for the four button
positions:

```
BUTTON1 / Quickstart          (81, 55,  158, 16)
BUTTON2 / Create New World    (81, 87,  158, 16)
BUTTON3 / The Story Continues (81, 120, 158, 16)
BUTTON4 / Heroes of Darklands (81, 167, 158, 16)
```

Each is 158 pixels wide, 16 pixels tall, at X position 81. The three active buttons dispatch as
follows:

- `Q` (Quickstart) calls into `1C85:4184` and returns `011B`.
- `C` (Create New World) calls into `1C85:0000`, which is the party creation controller
  identified in [devlog #029](/posts/029-digging-up-overlays/), and returns `011B`.
- `T` (The Story Continues) calls into `24A0:0002` and returns `011B`.

The `011B` return value is the BIOS word for the Escape key. Returning it is how the controller
signals to the caller that the current screen is done and the next phase should begin.

## BUTTON4

The fourth button is the interesting one.

`BUTTON4.PIC` is loaded. Its draw coordinates are confirmed. The `H` key reaches the dispatcher
in the current v483.07 build. And then nothing happens. The key is handled, logged internally,
and the screen does not change. No call to the shared PIC blit helper. No modification of
`A000`.

In the release build of the game, the fourth button is a dead branch. The
image is there, the input path is there, but the action was never wired up or was removed before
shipping.

The most likely explanation is a cut feature. The fourth button's position and shape matches the
others exactly, so it was clearly part of the original design. The Darklands manual mentions a "Heroes of Darklands" feature and it's clearly linked to that BUTTON4.PIC.

This is the kind of thing that only becomes visible once you are reading the exact branch table
rather than just watching the game run.

## Eight bytes that configure a sound card

`CONFIG.DRK` was mentioned in [devlog #021](/posts/021-boot-sequence-decoded/) as part of the
startup sequence. This session decoded it precisely.

The file is eight bytes. The current 483.07 install contains:

```
04 00 20 02 05 00 01 00
```

Read as four little-endian words:

```
word 0: 0x0004   device/config mode
word 1: 0x0220   base I/O port
word 2: 0x0005   IRQ 5
word 3: 0x0001   DMA channel 1
```

The selected sound driver (in this install, `psound.dlc`) reads these words at init time and
stores them to internal driver state. Device mode `0x0004` puts the driver in a
Sound-Blaster-DSP-shaped branch that uses the base port, DMA, and IRQ for sampled audio output.
Port `0x0220` is the standard Sound Blaster base address.

The game ships with three `.DLC` sound modules: `ASOUND.DLC`, `PSOUND.DLC`, and `RSOUND.DLC`.
`README.SND` labels them as different driver types (OPL-3, Roland, and so on). In the current
local install all three files are byte-identical, which means the driver selection comes
entirely from the config words, not from the module name. The faithful implementation preserves
the selected filename and the four config words as separate facts and does not infer hardware
backend from the filename alone.

## Welcome to Darklands

`OPENDARK.DGT` is a 61,754-sample, 8000 Hz, unsigned 8-bit mono PCM file. The [DGT format](/posts/020-the-sound-of-1992/)
was documented in devlog #020. What that devlog did not mention is what the file actually says.

It says "Welcome to Darklands." It is a digitized voice clip that plays at some point during the
`OPENING8` portion of the intro sequence. Users who have played the original game will likely
remember it.

The file is opened and preloaded at the start of the normal presentation path. The exact
instruction that triggers playback is not yet captured. The audio layer inside `psound.dlc` has
a candidate DSP command sequence at `4E34:1871` that reaches port `022C` (the Sound Blaster DSP
write port for the current base address `0x0220`), but connecting that to the exact moment the
voice plays requires a runtime probe during `OPENING8` that has not been run yet.

The intro also has a sustained music layer that runs through the entire `OPENING2` through
`OPENING8` sequence. That layer is separate from `OPENDARK.DGT`. The music is driven by the
selected `.DLC` module through an internal sequencer; `OPENDARK.DGT` is a one-shot sampled clip
layered on top. Both of these facts are evidenced, but neither playback trigger is pinned to a
specific runtime address yet.

## What this closes

The start screen was one of the last unsettled pieces of the intro layer. The input mechanism,
the resource list, the button coordinates, and the three dispatch branches are all confirmed.

The fourth button is explicitly open: it is tracked in the implementation as an unhandled action
rather than as dead code that can be silently discarded. If a later probe or a different game
build shows it wiring up to something, that fact has a place to land.

The sound configuration and audio layers are modeled in the engine as structured events with the
confirmed config words attached. Audio host implementation is later work, but the data contract
is in place.

The intro layer is done. The next layer is the game itself.
