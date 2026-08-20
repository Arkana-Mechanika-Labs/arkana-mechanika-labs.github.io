---
title: "Devlog #065 - Preparing for localisation"
date: 2026-08-20T09:00:00+02:00
summary: "Stable text identities, pre-layout message plans, and a separate display layout now prepare Darklands for future translations without allowing localized wording or geometry to alter the original gameplay."
width: wide
---

Darklands contains an enormous amount of text. Cities, encounters, prayers,
rumours, merchants, character screens and travel decisions all depend on words,
and many of those words are assembled dynamically from the current party and
world state.

That makes localization look, at first, like a simple future task: extract the
English text, translate it, and display another string.

Unfortunately, it is not that simple.

In Darklands, text is part of a larger presentation machine. The game selects a
MSG document and a card, expands tokens such as place names or character names,
wraps the resulting text with the original bitmap font, calculates the
rectangles occupied by each option, highlights the row under the pointer and
finally converts the selected visible row back into an original owner ordinal.

A translation can be longer than the English sentence. It can wrap onto another
line. That pushes the following rows down. Their clickable areas must move with
them. At the same time, the translation must not be allowed to change which
original choice the row represents.

The problem we have addressed in this development slice is therefore not
translation itself, but rather preparing the architecture for it.

The answer required two small architectural phases, L0 and L0.5. Together they
lay the groundwork for future localization without turning translated text into
a second source of gameplay behavior.

## The dangerous shortcut

A fragile localization layer would work on the final English screen.

The original text would first be expanded, wrapped and placed. The localization
system would then replace the visible English sentence with a translated one.
That approach can appear to work for short labels, but it immediately breaks
down on a real MSG card.

Consider an English option that occupies one line. Its French equivalent may
occupy two. If the renderer keeps the English rectangle, the second line may
overlap the next choice. The pointer may highlight one row while the player is
visually pointing at another. A click on the new second line may fall outside
the old hit area entirely.

The wrong pipeline would be:

```text
English text
    -> English word wrapping
    -> English row rectangles
    -> replace the visible words
```

The correct pipeline must instead be:

```text
choose the text for the active language
    -> insert the dynamic values
    -> encode or shape the resulting characters
    -> calculate word wrapping
    -> publish the displayed row rectangles
```

There is a second, more serious danger. A translation must never become the
identity of a gameplay choice.

Looking up a row by its English sentence would be unstable: punctuation,
spelling or editorial corrections would change the key. Looking it up by its
translated sentence would be worse. The behavior of the game would then depend
on language content that belongs only to presentation.

The central rule of the new architecture is therefore:

> **Text and geometry may change. Canonical choice identity must not.**

## Stable identities that are not sentences

The first phase introduced stable, language-neutral identities for
user-visible text slots.

A generic MSG heading receives an identity such as:

```text
msg/$CITYS00.MSG/card/0/heading
```

A source row receives an identity based on the exact document, card and original
owner ordinal:

```text
msg/$CITYS00.MSG/card/0/row/0005
msg/$PARTY02.MSG/card/6/row/0002
```

The key does not contain the English sentence. It does not contain its current
coordinates. It does not contain the destination state. It does not even use
the compact visible-row index.

That last distinction matters. Darklands cards can contain hidden rows,
display-only rows and selectable rows. When hidden rows are removed from the
visible list, the visible indices are compacted. The original source-row owner
ordinal remains the durable identity.

In other words, a localization key answers:

> Which text slot in the original game is this?

It does not answer:

> What does this text currently say?

Typed interfaces receive the same treatment. The main-menu actions, for
example, have explicit identities:

```text
ui/main-menu/quickstart/label
ui/main-menu/create-new-world/label
ui/main-menu/the-story-continues/label
```

Those IDs are not derived from C# enum names or from pixels in `STARTSCR.PIC`.
They identify future label slots without changing the existing picture-backed
main menu.

An immutable catalog contract can now associate one of these IDs with an
optional translated value. Missing entries do not invent substitutes. They
simply fall back to the canonical English presentation.

## Saving the card before English becomes pixels

Stable keys tell us where translated text belongs, but they are not enough by
themselves.

The old canonical pipeline expanded `$Token` values directly into an English
byte stream. By the time the screen had been laid out, information about the
source template had disappeared. We could see the final name, amount or place,
but no longer knew which part of the sentence had been literal text and which
part had come from a token.

That would force a later localization pass to reverse-engineer our own resolved
English output.

Every production generic MSG presentation now carries an immutable
`MessageTextPlan`.

The plan preserves the card before it becomes a final rendered layout. It
records:

- the exact MSG document and card;
- the heading or body template;
- every encoded source row, including hidden rows;
- each raw row marker and its classification;
- the original owner publication state;
- the stable localization ID for every text slot;
- every token referenced by a published slot;
- the immutable argument values captured during canonical resolution.

Hidden rows are preserved deliberately. A hidden row is still part of the
original card structure, even when the current owner state prevents it from
being displayed. Removing it from the plan would change the relationship
between source rows and owner ordinals.

The captured arguments are intentionally conservative. At present they are
classified only as `ProperName` or `OpaqueCanonicalText`.

That restraint is important. A character name is safely recognizable as a
proper name. An arbitrary token string is not automatically a noun with known
gender, number or case. We do not want to invent grammatical semantics merely
because a future translator may eventually need them.

Later phases may add richer, evidenced kinds for values such as money,
quantities or world terms. The current plan already gives those phases a stable
place to attach that information without changing the canonical resolver.

## One canonical presentation, one active display layout

The next separation is the most important one.

`MessagePresentation` remains the canonical presentation selected by the
reconstructed game. It owns the original document and card identity, the visual
source, the published rows and the canonical relationship to gameplay.

A new `MessageDisplayLayout` owns only what is actually displayed:

- resolved display text;
- searchable display text;
- displayed rows;
- selectable rows;
- row positions and sizes.

This is not a second MSG controller and not a second account of gameplay. It is
a presentation treatment.

The relationship is now:

```text
original bytes and resources
    -> certified original owner
    -> canonical MessagePresentation
    -> compatible MessageDisplayLayout
    -> renderer and pointer hit testing
    -> canonical HostAction
    -> existing MessageNavigationSession
```

For normal operation today, the active display layout is a direct canonical
adapter. It contains the same English bytes and the same geometry as before.
Classic and Enhanced Faithful therefore remain unchanged.

A future localization path may produce another display layout, but it must pass
a strict compatibility check. The translated layout may change text, wrapping,
horizontal or vertical geometry and even display order. It may not change:

| May change in a localized display | Must remain canonical |
| --- | --- |
| visible words | MSG document and card |
| line breaks | owner ordinal |
| row width and height | owner classification |
| vertical position | hidden/displayed publication state |
| display order | selectable versus display-only state |
| searchable display text | canonical visible-index identity |
| font treatment | gameplay action and outcome |

This makes the boundary explicit. Localization is allowed to reshape the
screen. It is not allowed to reshape the game.

## Rendering and clicking the same layout

Separating canonical identity from displayed geometry is useful only if every
part of the frontend respects the same separation.

The SDL path now uses the active `MessageDisplayLayout` for:

- drawing heading and body text;
- drawing selectable and display-only rows;
- hover highlighting;
- row hit testing;
- post-acknowledgement row treatment;
- anchoring alternate-selection popups.

This closes a subtle class of bugs. The renderer cannot draw one set of
rectangles while the pointer tests another.

When the player clicks a displayed row, the hit test returns the canonical
visible index and owner ordinal carried by that display row. The existing
`HostActionAdapter` then validates those values against the canonical
`MessagePresentation`.

It does not inspect the translated text. It does not inspect the localization
ID. It does not inspect locale metadata or searchable text.

The path is therefore:

```text
displayed rectangle
    -> canonical visible index and owner ordinal
    -> existing host action
    -> existing original-backed controller
```

A French sentence may be taller than its English equivalent. The click area can
grow with it. The selected original owner does not change.

## Proving the seam with a language that does not exist

We have not added a real translation yet, but an architectural boundary is not
complete merely because the interfaces look plausible.

The test suite now contains a bounded pseudo-localization proof.

It builds a synthetic MSG card and replaces its short canonical rows with much
longer printable ASCII text. ASCII is used deliberately because this phase is
testing layout and identity, not Unicode rendering.

The longer text wraps onto additional lines. The test verifies that:

- the translated row becomes taller;
- the following row moves downward;
- the active clickable rectangle moves with the displayed text;
- a point inside the new rectangle but outside the old one selects the row;
- the same canonical visible index is returned;
- the same original owner ordinal is retained;
- the resulting host action has the same gameplay identity.

That is the behavior we need from a future real language: a visually different
layout driving the same game.

The proof is intentionally strict. It currently accepts only complete,
token-free, printable-ASCII text whose glyphs exist in the supplied Darklands
FNT font. It rejects:

- a missing required translated slot;
- non-ASCII characters;
- unavailable font glyphs;
- unsupported controls;
- published token-bearing templates;
- any layout that changes canonical row identity or selectability.

A failure rejects the whole localized projection. The caller keeps the complete
canonical English layout.

We do not produce a card with a French heading, two English choices and one
missing line. Localization fallback is atomic: either the entire supported
scene is valid, or the original scene is shown intact.

## The original remains the fallback

This project treats original Darklands data as authority. Localization follows
the same rule as high-resolution artwork: it is an optional presentation layer
above the faithful path, not a replacement for evidence.

The canonical English resources remain available at all times. Locale is not
written into Darklands save files and cannot influence RNG, time, events,
transactions, picture selection, sound selection or state routing.

This also keeps localization reversible. A player can change language without
changing the saved world underneath it. An incomplete language pack cannot
make a choice disappear. A malformed translation cannot unlock an unsupported
route.

The display layer either proves that it is compatible with the canonical card,
or the canonical card wins.

## What this does not implement yet

The groundwork is complete, but localization itself is not.

There is currently:

- no runtime language selector;
- no command-line or configuration locale;
- no external JSON, PO or XLIFF pack loader;
- no production translation;
- no translated token grammar;
- no pluralization, grammatical gender or inflection system;
- no Unicode, TrueType or OpenType text renderer;
- no locale-specific Darklands bitmap font;
- no localized image replacement.

Those decisions remain deliberately deferred.

A future Classic localization will need a validated single-byte encoding and a
matching FNT resource, together with overflow policies for the original
320×200 cards.

A future Enhanced Modern presenter may use Unicode and high-resolution fonts,
but it will still consume the same canonical document, card, owner and action
identities.

Text painted directly into pictures is a separate problem again.
`STARTSCR.PIC`, for example, cannot be translated by changing a string catalog.
It will require either complete locale-specific artwork or a future semantic
menu presenter.

None of those later tasks requires changing the gameplay controller we have
just protected.

## Why build this before the game is finished?

Localization is easy to postpone because it produces no immediate visible
feature. That is also why it becomes expensive when introduced too late.

We are still decoding large portions of Darklands. Every new MSG card, typed
screen and dynamic text source could otherwise add another hardcoded assumption
that English text and gameplay identity are the same thing.

The shared message composer now creates the text plan automatically for every
production generic MSG presentation. Individual card implementations do not
invent their own keys or bypass the scaffold.

The forward rule is simple:

> Every newly reconstructed user-visible semantic text surface must publish a
> stable localization identity and a canonical fallback, or be explicitly
> classified as legacy-only, diagnostic-only or non-localizable original data.

That lets normal reverse engineering resume without accumulating a localization
debt behind it.

## Five thousand tests, twice

This architectural change touched the resolver, composer, row layout, host
snapshot, SDL renderer, hover path, click path and popup anchoring. It therefore
had to prove both the new seam and the absence of changes to the faithful
default path.

Classic regression tests remain unchanged and passing. Enhanced Faithful
regression tests remain unchanged and passing. Formatting and repository-diff
checks also pass.

The number is less important than what those tests defend. They enforce that a
display layout may change text and geometry but not owner identity,
selectability or action identity. They enforce that rendering and hit testing
consume the same layout. They enforce that missing localized content falls back
atomically. They enforce that the original presentation remains untouched.

## What comes next

The next step is not to build an entire translation system immediately. The
project can return to normal decoding work with the localization boundary now
in place.

Later phases can be added incrementally:

```text
L1  strict external language-pack format and validation
L2  translated templates and dynamic argument formatting
L3  Western-European Classic codec, FNT and overflow validation
L4  Enhanced Modern Unicode presentation
L5  specialized and legacy-only screen migration
```

When that work begins, it will attach to stable text IDs, immutable
`MessageTextPlan` values and compatible `MessageDisplayLayout` results. It will
not need to replace the MSG controller or reinterpret gameplay choices.

Darklands can now eventually speak in more than one language.
