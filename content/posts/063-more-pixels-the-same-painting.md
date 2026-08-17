---
title: "Devlog #063 - More Pixels, the Same Painting"
date: 2026-08-17T20:30:00+02:00
summary: "High-resolution PIC prototypes preserve Darklands' original compositions and watercolor character while exploring spring/summer, autumn, and winter variants."
width: wide
---

A Darklands message screen is more than text and a list of choices. Beside the
MSG card sits a PIC image. These pictures are small, but they carry
an enormous part of the atmosphere.

The thing is they were made for a very specific canvas, a 320×200 display, which
was ok at the time but today seems a bit outdated.

The original artists composed for that resolution. Shapes are suggested rather than 
exhaustively described. Faces may be only a few marks. Roofs, trees, reflections 
and crowds are arranged so that they read clearly through a limited palette and 
a limited number of pixels. The softness of the paintings is part necessity, part
technique but the overall tone is great and gives Darklands much of his identity.

As great as the original images are, our reimplementation is no longer bound to 
the 320x200 display resolution. It can present the same game logic, the same 
MSG resources and the same PIC identities on a modern screen. That creates 
an opportunity — but also a fidelity problem.

## Upscaling is not restoration

The easiest solution would be to resize every original picture.

Nearest-neighbour scaling preserves the pixels but turns each one into a large
block. Smoothing hides the blocks by blurring the image. More elaborate
upscalers can manufacture edges and textures, but they often treat uncertainty
as permission to invent. None of those approaches truly restores the picture.
They only magnify, soften or reinterpret the 320×200 result.

At the other extreme, we could commission or generate completely new
high-resolution scenes. They might be beautiful. They might even be historically
convincing. But they would no longer be the pictures that give Darklands its
visual identity. A newly designed medieval street is not a restoration of
Darklands' Main Street merely because both contain timbered houses.

The aim, therefore, is narrower and more demanding:

> **Restore the original painting rather than replace it.**

The original PIC remains the authority for composition, viewpoint, proportions,
architecture, figures, props, palette, lighting and mood. Higher resolution
should recover the detail that the scene implies, not redesign the scene around
detail that was never there. The result should still feel painted rather than
photographic, and it should retain the soft watercolor character that makes the
original art so distinctive.

This is not an attempt to make Darklands look like a modern game inspired by
Darklands. It is an attempt to imagine how the same picture might have looked
if its artists had been given a much larger canvas.

## The original art must remain canonical

A faithful reimplementation must always be able to display the shipped PIC
exactly as the original game did. The high-resolution work belongs in a
separate, optional presentation layer.

That distinction is important. The MSG owner still requests the same named
picture. The reconstructed gameplay does not know or care whether the frontend
shows the 320×200 source or a restored counterpart. A visual setting can choose
the original asset, while a high-resolution setting can select the restored
version. When no restored version exists, the renderer can fall back to the
original automatically.

In other words, higher-resolution art does not replace evidence. It sits above
the faithful asset path, remains reversible, and can be reviewed picture by
picture.

## Introducing seasonal variations

A higher-resolution asset system also makes another old ambition practical:
seasonal scenery.

The original developers and artists wanted the world to reflect the seasons,
but a complete set of alternate paintings would have multiplied both the art
workload and the amount of data that had to fit on early-1990s storage media.
Even one additional version of every city picture would have been expensive;
several versions would have been difficult to justify within the production
schedule and disk budget.

The reconstructed game does not have those restrictions. A restored visual layer 
can use the internal calendar state to select a corresponding scene:

```text
spring / summer  → warm-season restoration
autumn           → autumn restoration
winter           → winter restoration
```

This should not be a colour filter. Autumn is not merely a browner summer, and
winter is not the same image with white painted over the ground. Foliage,
branches, cloud cover, reflections, snow, visibility and the quality of the
light all need scene-aware treatment. At the same time, seasonal variation must
not disturb the underlying composition. The player should always recognize the
same place and the same original PIC.

For these first prototypes, spring and summer share one warm-season version.
Autumn and winter receive separate interpretations.

## Reading the Prototype Sets

Each row below contains four images:

1. the original 320×200 PIC;
2. the restored spring/summer prototype - which is the original restored as is.
3. the restored autumn prototype;
4. the restored winter prototype.

These are prototypes that were made in order to have an idea of what a restored 
high resolution image would look like. Seasonal variations were then applied.

## Seven First Experiments

### The Docks

Water is one of the hardest fidelity tests. Reflections, rigging, distant buildings and the quiet haze over the harbour all have to gain definition without becoming sharper, cleaner or more photographic than the original painting.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/DOCKDAY.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/DOCKDAY.png"
      alt="Original Darklands DOCKDAY PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/DOCKDAY_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/DOCKDAY_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands DOCKDAY PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/DOCKDAY_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/DOCKDAY_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands DOCKDAY PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/DOCKDAY_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/DOCKDAY_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands DOCKDAY PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### Main Street

Main Street tests a different kind of restraint: long perspective lines, architecture, small figures and street activity. The restored versions must make the scene readable at modern resolutions without turning its deliberately suggested details into a catalogue of newly invented objects.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/MAIN-ST.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/MAIN-ST.png"
      alt="Original Darklands MAIN-ST PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/MAIN-ST_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/MAIN-ST_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands MAIN-ST PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/MAIN-ST_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/MAIN-ST_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands MAIN-ST PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/MAIN-ST_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/MAIN-ST_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands MAIN-ST PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### The Side Street

The side-street picture depends on density and atmosphere more than on any single landmark. Here the challenge is to preserve the original visual rhythm—the balance between people, buildings and open street—while allowing the seasonal weather to change the mood.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/SID.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/SID.png"
      alt="Original Darklands SID PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/SID_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/SID_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands SID PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/SID_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/SID_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands SID PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/SID_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/SID_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands SID PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### The Grove

The grove makes the seasonal idea immediately visible. Leaves, bare branches, ground cover, snow and the colour of the light can change while the composition and the identity of the location remain fixed.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XGROVE1.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/XGROVE1.png"
      alt="Original Darklands XGROVE1 PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XGROVE1_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/XGROVE1_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands XGROVE1 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XGROVE1_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/XGROVE1_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands XGROVE1 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XGROVE1_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/XGROVE1_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands XGROVE1 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### XMS036 - The City Gate

XMS036 provides another useful test of the method. The aim is not to use the low-resolution source as a loose prompt, but as the governing composition: the same view, the same visual hierarchy and the same restrained watercolor treatment.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XMS036.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/XMS036.png"
      alt="Original Darklands XMS036 PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XMS036_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/XMS036_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands XMS036 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XMS036_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/XMS036_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands XMS036 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XMS036_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/XMS036_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands XMS036 PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### XTHANKS - The Marketplace

XTHANKS is a good measure of whether added detail remains subordinate to the scene. A restoration succeeds only when the eye still reads the picture in the same order as it did at 320×200.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTHANKS.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/XTHANKS.png"
      alt="Original Darklands XTHANKS PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTHANKS_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/XTHANKS_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands XTHANKS PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTHANKS_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/XTHANKS_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands XTHANKS PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTHANKS_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/XTHANKS_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands XTHANKS PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>


### XTOWN - The City Square

The city square view brings the whole problem together: architecture, landscape, sky, distance and human scale. Each season should feel materially different, yet all three restorations must unmistakably remain the same Darklands picture.

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 1rem; align-items: start; margin: 1.25rem 0 2.5rem;">
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTOWN.png" target="_blank" rel="noopener" title="Open original — 320×200 at full size">
    <img
      src="/images/devlogs/063/XTOWN.png"
      alt="Original Darklands XTOWN PIC at 320 by 200 resolution"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Original — 320×200
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTOWN_A_D_S.png" target="_blank" rel="noopener" title="Open restored — spring/summer at full size">
    <img
      src="/images/devlogs/063/XTOWN_A_D_S.png"
      alt="High-resolution spring and summer restoration prototype for the Darklands XTOWN PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — spring/summer
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTOWN_A_D_A.png" target="_blank" rel="noopener" title="Open restored — autumn at full size">
    <img
      src="/images/devlogs/063/XTOWN_A_D_A.png"
      alt="High-resolution autumn restoration prototype for the Darklands XTOWN PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — autumn
  </figcaption>
</figure>
<figure style="margin: 0; min-width: 0;">
  <a href="/images/devlogs/063/XTOWN_A_D_W.png" target="_blank" rel="noopener" title="Open restored — winter at full size">
    <img
      src="/images/devlogs/063/XTOWN_A_D_W.png"
      alt="High-resolution winter restoration prototype for the Darklands XTOWN PIC"
      loading="lazy"
      decoding="async"
      style="display: block; width: 100%; height: auto; border-radius: 0.5rem; box-shadow: 0 0 0 1px rgba(127,127,127,0.28);"
    >
  </a>
  <figcaption style="margin-top: 0.5rem; text-align: center; font-size: 0.9rem;">
    Restored — winter
  </figcaption>
</figure>
</div>

## What these prototypes are testing

These images are not a declaration that the visual work is finished. They are
tests of a direction.

The most important question is not whether a single enlarged picture looks
impressive in isolation. It is whether a complete set can obey the same rules.
A restoration pipeline will need consistency in brushwork, architecture,
figures, perspective, palette and the amount of recovered detail. It will also
need a disciplined review process in which the original picture is always
visible beside the proposed restoration.

The seasonal versions add another requirement: the transformations must be
credible across many kinds of scene. A winter grove, a winter harbour and a
winter city street cannot all be produced by the same superficial effect. Each
one has different vegetation, surfaces, weather, reflections and human
activity. Yet they must still belong to one coherent visual system.

These prototypes therefore help us define future acceptance questions:

- Does the composition still match the original at a glance?
- Have important silhouettes, objects or relationships moved?
- Has the scene become too sharp, too photographic or too busy?
- Does added detail clarify what was implied, or invent a different place?
- Does the seasonal version change the environment without changing the
  identity of the scene?
- And the most important of all: Does the complete set still look like Darklands?

## A possible future runtime

The implementation itself can remain simple because the game's original
resource identity already provides the key.

```text
MSG owner requests PIC name
        ↓
visual mode selects original or restored family
        ↓
day/night and season select an available variant
        ↓
missing variant falls back to the original PIC
```

The faithful mode would always use the shipped images. The restored mode could
choose seasonal counterparts from the current in-game date. This keeps visual
restoration separate from gameplay reconstruction and prevents an artistic
experiment from silently becoming part of the historical compatibility layer.

The same structure also leaves room for later work—additional day and night
variants, improved restorations, or alternative curated sets—without changing
the decoded MSG and state machinery underneath.

## More pixels, the same painting

Darklands' art does not need to be escaped from. Its low resolution conceals
detail, but it also contains remarkable composition, colour and atmosphere.
The challenge is to reveal more of that work without painting over it.

That is the principle behind these prototypes: preserve the original scene,
preserve its watercolor beauty, and let modern resolution serve the painting
rather than replace it.

Seasonal variation goes one step further. It uses freedom that the original
production did not have, but applies it within the visual language the original
artists established. If we eventually introduce it, it will be clearly
identified as restored content, built on top of a mode that continues to show
Darklands exactly as it was shipped.

More pixels are easy. Keeping the same painting is the real work.
