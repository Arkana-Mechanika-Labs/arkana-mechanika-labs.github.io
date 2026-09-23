---
title: Darklands Restoration Project
description: A faithful native C# reconstruction of MicroProse's 1992 RPG, rebuilt from original code and data with evidence-backed verification.
toc: false
width: wide
---

<div class="drp-hero">
  <div class="drp-hero-copy">
    <div class="drp-hero-eyebrow">Arkana Mechanika Studios</div>
    <p class="drp-hero-tagline">Rebuilding the classic 1992 DOS RPG for modern systems</p>
    <p class="drp-hero-subtitle">A faithful C# reconstruction bringing Darklands to modern systems while preserving the gameplay, data, and atmosphere of the 1992 original.</p>
    <div class="drp-hero-buttons">
      <a href="https://discord.gg/HjzWvmHhqZ" class="drp-btn drp-btn-primary" target="_blank" rel="noopener noreferrer">Join the Discord ↗</a>
      <a href="#showcase" class="drp-btn drp-btn-outline">Watch the Showcase</a>
      <a href="/posts/" class="drp-btn drp-btn-outline">Read the Devlogs</a>
    </div>
  </div>
  <div class="drp-hero-art">
    <div class="drp-hero-cover-frame">
      <img
        src="/images/darklands-cover.jpg"
        alt="Darklands original box cover"
        class="drp-hero-cover"
      />
    </div>
  </div>
</div>

---

## The Project

Darklands is MicroProse's ambitious 1992 role-playing game set in a grounded, folkloric medieval Germany: robber knights, saints, alchemy, political intrigue, and danger on every road. The original release was built for 16-bit DOS and today is normally played through emulation.

Darklands is gradually coming back to life. We're restoring the places, encounters, and choices that made the original adventure distinctive, while bringing it to modern systems. [Follow the devlogs](/posts/) to see what has returned and what comes next.

<div class="drp-current-note">
  <strong>Project status</strong>
  <p>The restoration is still in development. Some places and encounters are unfinished, and running the development version requires your own copy of the original Darklands game data.</p>
</div>

<section id="showcase" class="drp-showcase" aria-labelledby="showcase-title">
  <div class="drp-section-kicker">Presentation #01</div>
  <h2 id="showcase-title">See the reconstructed engine in motion</h2>
  <p>This presentation follows the restoration from the original opening into the native development host. The <a href="/posts/">devlogs</a> show later gameplay milestones.</p>
  <div class="drp-video-frame">
    <iframe
      src="https://www.youtube-nocookie.com/embed/CrwcEszBJcc"
      title="Darklands Restoration Project - Presentation #01"
      loading="lazy"
      allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
      referrerpolicy="strict-origin-when-cross-origin"
      allowfullscreen>
    </iframe>
  </div>
  <p class="drp-video-link"><a href="https://youtu.be/CrwcEszBJcc" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></p>
</section>

---

## Where the Restoration Stands

<div class="drp-progress-grid">
  <article class="drp-progress-card">
    <span class="drp-progress-label">Startup and city</span>
    <h3>From the opening into city life</h3>
    <p>The .NET 10 development host reproduces the opening, executes Quickstart, and reaches supported city streets and destinations, including merchants, churches, docks, groves, and party screens. Coverage remains route-by-route.</p>
  </article>
  <article class="drp-progress-card">
    <span class="drp-progress-label">Combat gameplay</span>
    <h3>A fight is unfolding</h3>
    <p>The published guard-encounter milestone connects battlefield entry, movement orders, arrows, melee exchanges, damage, and the first falling guard. <a href="/posts/072-the-battlefield-starts-moving/">See the captured gameplay.</a> Complete battle outcomes remain unfinished.</p>
  </article>
  <article class="drp-progress-card">
    <span class="drp-progress-label">Presentation</span>
    <h3>Classic and Enhanced Faithful</h3>
    <p>Classic preserves the exact indexed presentation at modern window sizes. The bounded Enhanced Faithful path can combine restored high-resolution scenery with the original interactive card, text, choices, and party panel, falling back atomically when a scene is unsupported.</p>
  </article>
  <article class="drp-progress-card">
    <span class="drp-progress-label">Preservation</span>
    <h3>Knowledge becomes durable evidence</h3>
    <p>Original code units, data formats, state effects, oddities, and unresolved boundaries are recorded and tested. The project has decoded graphics, animation, audio, text, saves, world data, events, and many of the mechanisms that connect them.</p>
  </article>
</div>

<div class="drp-screenshots drp-screenshots-current">
  <figure class="drp-screenshot">
    <a href="/images/classic-mainst.png" target="_blank" rel="noopener noreferrer">
      <img src="/images/classic-mainst.png" alt="Classic Darklands presentation showing the original indexed Main Street scene in Magdeburg" loading="lazy" />
    </a>
    <figcaption><strong>Classic:</strong> the exact original indexed surface, including its picture, message card, text, choices, and party panel, presented by the native SDL development host.</figcaption>
  </figure>
  <figure class="drp-screenshot">
    <a href="/images/devlogs/064/MainStreet.png" target="_blank" rel="noopener noreferrer">
      <img src="/images/devlogs/064/MainStreet.png" alt="Enhanced Faithful Darklands Main Street with restored high-resolution scenery and the original interactive interface" loading="lazy" />
    </a>
    <figcaption><strong>Enhanced Faithful:</strong> restored high-resolution scenery behind the original message card, choices, and party panel. It is an optional presentation path with complete Classic fallback.</figcaption>
  </figure>
</div>

---

## How Reconstruction Works

<ol class="drp-pipeline">
  <li><span>01</span><div><strong>Start with the original</strong><p>Original version 483.07 bytes, assembly, resources, and observed machine state define the behaviour to recover.</p></div></li>
  <li><span>02</span><div><strong>Review structure and data flow</strong><p>Focused Ghidra analysis is checked against an independent Reko decompilation so disagreements are visible before implementation.</p></div></li>
  <li><span>03</span><div><strong>Certify the exact unit</strong><p>Darklays binds ownership, call targets, branches, memory effects, and evidence freshness to the specific original routine or selected path.</p></div></li>
  <li><span>04</span><div><strong>Rebuild the whole observable path</strong><p>The C# implementation preserves controllers, handlers, helpers, state effects, presentation, audio, time, acknowledgement, and destination settling—not only the endpoint.</p></div></li>
  <li><span>05</span><div><strong>Verify against the running game</strong><p>Autoprobe and the patched DOSBox-X runtime compare the reconstructed route with the original executable at focused observation boundaries.</p></div></li>
</ol>

<p class="drp-toolchain"><strong>Current toolchain:</strong> original Darklands 483.07 bytes and data &nbsp;·&nbsp; Ghidra &nbsp;·&nbsp; Reko &nbsp;·&nbsp; Darklays &nbsp;·&nbsp; patched DOSBox-X and Autoprobe &nbsp;·&nbsp; C# / .NET 10 &nbsp;·&nbsp; SDL2</p>

---

## What the Project Is Building

<div class="drp-goals">
  <div class="drp-goal">
    <h3>A Faithful Native Engine</h3>
    <p>Reconstruct original Darklands behaviour in readable, testable C# while preserving its decisions, data, timing, presentation, and known oddities.</p>
  </div>
  <div class="drp-goal">
    <h3>A Permanent Classic Reference</h3>
    <p>Keep the original 320×200 indexed look available as the exact reference presentation, scaled cleanly on modern displays.</p>
  </div>
  <div class="drp-goal">
    <h3>Optional Modern Presentation</h3>
    <p>Allow frontends and restored artwork to improve presentation without moving gameplay authority out of the reconstructed engine.</p>
  </div>
  <div class="drp-goal">
    <h3>Open Technical Documentation</h3>
    <p>Publish practical knowledge of file formats, algorithms, data structures, original bugs, and reconstruction methods for preservation and research.</p>
  </div>
</div>

---

## Follow the Work

The devlogs document the restoration as it happens, including both visible milestones and the less glamorous evidence work that makes those milestones trustworthy.

<div class="drp-follow-actions">
  <a href="https://discord.gg/HjzWvmHhqZ" class="drp-btn drp-btn-primary" target="_blank" rel="noopener noreferrer">Join the Discord ↗</a>
  <a href="/posts/" class="drp-btn drp-btn-outline">Browse the Devlogs</a>
  <a href="/tools/" class="drp-btn drp-btn-outline">Project Tools</a>
  <a href="/faq/" class="drp-btn drp-btn-outline">Read the FAQ</a>
</div>

<div class="drp-cta">
  <p class="drp-contact">Questions or contributions: <a href="mailto:arkana.mechanika.studios@gmail.com">arkana.mechanika.studios@gmail.com</a></p>
</div>
