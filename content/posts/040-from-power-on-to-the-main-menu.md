---
title: "Devlog #040 - From Power-On to the Main Menu"
date: 2026-07-28T20:00:00
summary: "The reconstructed engine can now follow Darklands from its opening banner, through the complete animated introduction, to the real start screen, with synchronized music, sound, graphics, and input."
---

For a long time, the reconstruction could explain many parts of the Darklands
startup without actually performing the whole journey.

We knew how the opening banner was stored. We had decoded the PAN animation
format. We understood the digital sound files, the music driver, the start
screen picture, and several of the original routines that tied them together.
Each piece was useful, but the new engine still needed a convenient starting
point or a carefully prepared test state.

That has changed.

The C# development host can now start at the beginning and follow the original
startup all the way to the main menu. It displays the text-mode banner, plays
the seven-part introduction, mixes the music and sound effects, and arrives at
the familiar `STARTSCR.PIC` screen ready for keyboard input.

This is the first time the reconstructed project has felt like launching
Darklands rather than inspecting one part of it.

## Beginning Before the First Picture

The startup does not begin with the painted MicroProse scenes. It begins in
text mode, with a small banner assembled from `BANNER.DAT`.

That banner is easy to overlook. It appears briefly, it uses the old DOS text
screen, and it is soon replaced by graphics. It would have been tempting to
recreate it as an ordinary modern text label.

Instead, the new host uses the original banner bytes and their exact positions
on the 80 by 25 screen. It also uses a checked copy of the DOS platform font,
including the slightly wider appearance produced by the old nine-dot text
cells. The result is not merely the same sentence in roughly the same place. It
is the screen Darklands was trying to produce.

From there, the startup follows the original configuration, resource, memory,
graphics, and sound setup paths. Modern code provides files, audio devices, and
a window, but the order of operations and the decisions between them remain
those of the game.

If a required resource is missing or has the wrong identity, the route stops
and explains why. It does not replace the file, skip the step, or continue with
a lookalike.

## Seven Scenes, in Their Original Rhythm

The Darklands introduction is stored as seven PAN sequences. These are not
ordinary video files with a fixed frame rate. Each sequence contains a base
image and a stream of compact drawing commands that update parts of the screen.
The timing between those updates varies throughout the introduction.

Earlier format work taught us how to decode those commands. The newer work
answers a harder question: when should every update appear while the music and
sound effects are also playing?

We captured the timing of the complete original introduction and now preserve
all 1,170 changing intervals between its frames. The banner remains visible for
the original lead-in, each PAN update happens on the recorded schedule, and the
main menu appears a little over two minutes later at the same point in the
presentation.

The host does not try to smooth that rhythm into a modern frame rate. The small
pauses and bursts are part of how the original sequence was authored.

## One Clock for Sound and Picture

Synchronizing the introduction exposed a problem that is common in old games.
The animation, music, and digital effects all have their own data, but the
player experiences them as one performance.

If the graphics use the computer's wall clock while the audio uses a separate
playback queue, they slowly drift apart. The first scene may look fine, while a
sound effect in the last scene arrives noticeably early or late.

The new host solves this by using one audio timeline for the whole
introduction. MT-32 music and the original `OPENDARK.DGT` sound effects are
mixed into the same 48 kHz stereo stream. The amount of audio the device has
actually played then determines which animation frame should be on screen.

In other words, the soundtrack is also the clock.

This keeps the long introduction stable without constantly correcting it. It
also preserves the behavior of the original sound effects. A new effect can
replace the currently active digital voice, while the music continues
underneath it.

There was one useful trap along the way. A hardware timing value in the
Sound Blaster path looked like it might describe the audio sample rate.
Following that interpretation made the effects play almost twice as fast.
Listening to the result made the mistake obvious. The original DGT files
really are headerless, unsigned, 8-bit mono audio at 8 kHz, as the earlier
format work had established.

Reverse engineering often advances through this kind of disagreement. A
number can look persuasive in isolation. It still has to survive the whole
experience.

## Reaching the Menu Honestly

The most important part of this milestone is not the presentation itself. It
is how the engine reaches the presentation.

The faithful startup now executes one continuous route through the original
startup controller, the resident introduction code, and the original
start-screen owner. It no longer catches an unresolved call, injects a later
checkpoint, and resumes from there.

The clean C# side receives a sequence of presentation events from that route:
show the banner, prepare a PAN scene, start a sound, change a palette, and
finally present the main menu. It does not receive DOS registers, temporary
memory addresses, or instructions about how an old graphics card worked.

That separation is deliberate. The reconstructed game decides what happens and
in which order. The host decides how to put pixels on a modern display and
samples on a modern audio device.

By the time `STARTSCR.PIC` appears, the engine has reached the same original
keyboard path that handled the DOS menu. The familiar Q, C, and T choices are
not modern buttons placed over an old picture. They are the original branches,
reached from the original startup.

Only Quickstart currently continues into a playable reconstructed route. The
other choices still stop at their first unresolved original boundary. That is
intentional. A visible menu item is not evidence that everything behind it is
ready.

## Skipping the Introduction

The host also supports the way players naturally interact with an opening
sequence.

Pressing Space or Enter during the PAN presentation follows the original
pending-input path and leaves the introduction. This is separate from the
development-only `--skip-intro` command, which exists for testing.

The distinction may sound small, but it captures the larger rule behind the
project. A useful shortcut can exist in the development host without being
mistaken for game behavior. When the player uses the real controls, the
original logic remains in charge.

## A Real Beginning

The startup route now covers far more than a slideshow. It validates the
required resources, initializes the original systems, presents nineteen
ordered events, plays the full opening sequence, handles live skip input, and
lands on the start screen without a prepared checkpoint.

That gives the project a stable beginning.

It also changes the meaning of everything that follows. The next reconstructed
screen no longer has to be launched as an isolated demo. It can be reached by
starting the program, watching or skipping the introduction, and pressing Q.

The next devlog follows that key.
