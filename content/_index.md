---
title: Darklands Restoration Project
description: MicroProse's 1992 role-playing game Darklands, rebuilt in C# to run on today's Windows and to play exactly like the original. Version 0.9.0 is out.
toc: false
width: wide
params:
  images:
    - /images/0.9.0/city.png
---

<div class="drp-hero">
  <div class="drp-hero-copy">
    <div class="drp-hero-eyebrow">Arkana Mechanika Studios</div>
    <p class="drp-hero-tagline">Darklands, rebuilt for today's Windows</p>
    <p class="drp-hero-subtitle">MicroProse's 1992 role-playing game of saints, alchemy, witches and robber knights, running without DOSBox and playing exactly like the original. Version 0.9.0 is out.</p>
    <div class="drp-hero-buttons">
      <a href="/download/" class="drp-btn drp-btn-primary">Download 0.9.0</a>
      <a href="https://discord.gg/HjzWvmHhqZ" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">Join the Discord ↗</a>
      <a href="https://github.com/Arkana-Mechanika-Studios/darklands-restoration" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">Source code ↗</a>
    </div>
  </div>
  <div class="drp-hero-art">
    <figure class="drp-hero-game-frame">
      <img src="/images/0.9.0/city.png" alt="An evening in a Gasthaus in Strassburg, the party swearing its oath" class="drp-hero-game" />
      <figcaption>Version 0.9.0: a Gasthaus in Strassburg</figcaption>
    </figure>
    <img src="/images/darklands-cover.jpg" alt="Original Darklands box art" class="drp-hero-box-art" />
  </div>
</div>

<section class="drp-showcase" id="release-video">
  <span class="drp-section-kicker">Release video</span>
  <h2>Darklands Restoration Project 0.9.0</h2>
  <p>Four and a half minutes of version 0.9.0: character creation, the cities, a night ambush and a real-time battle, the world map and the camp, and what comes next.</p>
  <div class="drp-video-frame">
    <iframe src="https://www.youtube-nocookie.com/embed/jaFP2INDo88" title="Darklands Restoration Project 0.9.0" loading="lazy" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
  </div>
  <p class="drp-video-link"><a href="https://youtu.be/jaFP2INDo88" target="_blank" rel="noopener noreferrer">Watch on YouTube ↗</a></p>
</section>

---

## The Project

Darklands is MicroProse's ambitious 1992 role-playing game set in a grounded, folkloric medieval Germany: robber knights, saints, alchemy, political intrigue, and danger on every road. It was made for 16-bit DOS and is normally played through emulation today.

The Darklands Restoration Project brings it back as a native program. This is not a remake and not an emulator: every rule of the original — combat, prices, saints, alchemy, the cards of every city and encounter, the generators of castles, mines and battlefields — has been rewritten from the original program and checked against it. The screens, the music and the sound are the original's, drawn and played from your own copy of the game.

<div class="drp-current-note">
  <strong>Version 0.9.0 is out</strong>
  <p>The whole game plays: character creation, cities, inns and shops, guilds, banks and churches, the world map and its encounters, battles, camping, saints and alchemy, saving and loading. You need your own copy of Darklands (GOG or Steam). Version 1.0 will follow once the remaining faithfulness checks are finished. <a href="/download/">Get it →</a></p>
</div>

## Version 0.9.0

<div class="drp-story-grid">
  <figure class="drp-story-card"><img src="/images/0.9.0/start-screen.png" alt="The start screen" loading="lazy" /><span class="drp-section-kicker">Start</span><strong>The original start screen</strong><span>Quickstart, a new world, or a saved game.</span></figure>
  <figure class="drp-story-card"><img src="/images/0.9.0/world-map.png" alt="The world map" loading="lazy" /><span class="drp-section-kicker">Travel</span><strong>The world map</strong><span>Roads, towns, castles and what waits on the way.</span></figure>
  <figure class="drp-story-card"><img src="/images/0.9.0/battle.png" alt="A battle" loading="lazy" /><span class="drp-section-kicker">Combat</span><strong>Real-time battles</strong><span>Pause, give orders, and watch the fight unfold.</span></figure>
  <figure class="drp-story-card"><img src="/images/0.9.0/character-sheet.png" alt="A character sheet" loading="lazy" /><span class="drp-section-kicker">Party</span><strong>Characters and their gear</strong><span>Attributes, skills, saints and formulas.</span></figure>
  <figure class="drp-story-card"><img src="/images/0.9.0/inn.png" alt="An inn's choices" loading="lazy" /><span class="drp-section-kicker">Cities</span><strong>Inns, guilds and streets</strong><span>Every card of every city, as the original wrote it.</span></figure>
  <figure class="drp-story-card"><img src="/images/0.9.0/camp.png" alt="Camping in the wild" loading="lazy" /><span class="drp-section-kicker">Time</span><strong>Camping and the hourglass</strong><span>Rest, pray, brew potions, and watch the days pass.</span></figure>
</div>

---

## How it is made

The game logic is a C# reimplementation of the original program, kept apart from graphics, sound and input. Each piece cites the place in the original it reproduces, and the rules are checked by running the original's own functions next to the C#: tens of thousands of cases, and every card of the game. What is knowingly different from the original, and which of its bugs are kept on purpose, is listed openly. <a href="/method/">Read how it is made →</a>

The original's surprising rules and genuine defects are collected in [Bugs & Oddities](/formats/original-bugs-and-oddities/).

---

## Follow the Work

News about releases goes to the [news](/news/). The devlogs and the presentation videos of the earlier development are kept in the [archives](/archives/).

<div class="drp-follow-actions">
  <a href="/download/" class="drp-btn drp-btn-primary">Download 0.9.0</a>
  <a href="https://discord.gg/HjzWvmHhqZ" class="drp-btn drp-btn-outline" target="_blank" rel="noopener noreferrer">Join the Discord ↗</a>
  <a href="/news/" class="drp-btn drp-btn-outline">News</a>
  <a href="/faq/" class="drp-btn drp-btn-outline">Read the FAQ</a>
</div>

<div class="drp-cta">
  <p class="drp-contact">Questions or contributions: <a href="mailto:arkana.mechanika.studios@gmail.com">arkana.mechanika.studios@gmail.com</a></p>
</div>
