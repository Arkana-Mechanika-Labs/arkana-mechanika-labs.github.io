---
title: "Devlog #041 - Reconstructing Quickstart"
date: 2026-07-28T20:05:00
summary: "Pressing Q now follows the original Quickstart route: loading the default party, choosing a starting city and time, presenting the PARTY02 sequence, and reaching the first real decision."
---

Quickstart is one of the friendliest features in Darklands.

Press Q on the main menu and the game gives you a ready-made party. A short
series of screens introduces the characters and the starting situation, then
you arrive in a German city and begin playing.

From the player's side, it feels almost effortless.

Inside the game, Quickstart has quite a lot to arrange. It has to load four
characters, prepare the temporary party data, choose a starting city, set the
calendar and time, build several illustrated cards, fill the permanent party
panel, and finally turn the last card into an interactive choice.

The reconstructed engine can now follow that complete route.

## Pressing Q Means Pressing Q

The previous devlog ended on the real Darklands start screen. The new work
continues from its original Q and q keyboard branch.

That point matters because Quickstart is not a command invented by the modern
host. The host reports a key. The reconstructed start-screen controller handles
it, just as the DOS game did, and transfers control into the original
Quickstart setup path.

This path was considerably larger than the label on the menu suggested. What
looked like a simple shortcut turned out to be a chain of file handling,
character setup, random selection, resource loading, text presentation, and
state publication.

We rebuilt it in that order rather than starting from the city and working
backward.

## Loading the Default Party

Quickstart begins with `SAVES\DEFAULT`, the original party supplied with the
game.

The reconstructed path reads the four active character records and performs
the same setup needed to make them the current party. It also reproduces the
temporary `CHARACTR.TMP` exchange used by the DOS code.

There is one modern safety improvement at the boundary. The temporary exchange
happens in memory, so running the development host does not alter the user's
original Darklands installation. The bytes and decisions seen by the
reconstructed game remain the same, but the host does not need to leave a
temporary DOS file behind.

This is a good example of where fidelity belongs. The game should receive the
same data and follow the same logic. The operating system does not have to
pretend it is 1992 when that would only add risk.

## Letting Darklands Choose the City

Once the party exists, the game chooses where and when the adventure begins.

The new route uses the original random-number behavior and the original city
records. It does not always send the party to one convenient test location.
Any of the 90 cities available to Quickstart can be selected, along with the
corresponding starting time values.

For tests and visual comparisons, we can provide a fixed seed and obtain the
same city every time. During an ordinary run, the choice belongs to
Darklands.

Keeping that distinction helped expose assumptions that a single fixed
location had hidden. City names vary in length. Local records carry different
flags. Later screens may publish different rows depending on the selected
place. A route that works only for the city used in one screenshot is not yet
a Quickstart route.

## Four Introductions and One Decision

The visible part of Quickstart comes from `$PARTY02.MSG` and a series of
matching pictures.

Cards 2 through 5 are informational. Each one presents part of the setup and
waits for an acknowledgement. The player can press Enter or Space, or click
anywhere, to continue.

These cards do not contain selectable rows. Treating their text as a modern
dialog with a hidden "Continue" button would produce a similar interaction,
but it would not reproduce the original controller. Darklands has a specific
acknowledgement phase, and the reconstructed route preserves it.

Card 6 is different. It publishes the first genuine choices.

The resource contains five encoded rows, but the original owner exposes only
four of them in this situation. Those four rows use the original positions and
heights. The fifth remains hidden. Pointer movement now changes the highlighted
row, and clicking or pressing the appropriate key selects it.

This is where Quickstart stops being a sequence of illustrated pages and
becomes gameplay.

## Rebuilding the Whole Screen

Displaying the correct paragraph was only part of the visual work.

Each Quickstart card combines an indexed picture with decorative borders,
illuminated initials, the original bitmap font, and the permanent party panel.
That panel includes four shields, four names, statistics, values, and the
small graphic layers shared by many Darklands screens.

The new compositor builds those pieces from the original resources. It does
not use a screenshot as the background and place live text over it.

We compared the result against a captured frame from the DOS game at the
original 320 by 200 resolution. After correcting the old VGA color conversion
and the position of the party statistics, the images matched everywhere except
two pixels at the far right edge. Those pixels belonged to the DOSBox mouse
cursor, not the game screen.

That comparison did more than certify one attractive frame. It corrected
reusable color and layout rules that later MSG screens now share.

## The First Choice Produces a Real State

Selecting the first visible row on card 6 now follows its original handler.
The handler copies the required text, returns its raw result, passes through the
owner's local dispatch, and publishes the next game state.

That state is `001Dh`, the original route into the first urban presentation.

The clean Quickstart session does not know that because someone attached a
friendly destination called "go to the city" to the row. It knows because the
reconstructed owner returned the same state value that the original game
returned.

The difference is important. Text can suggest what a choice probably does, but
only the executable tells us what it actually does. The other card-6 choices
remain closed until their handlers are reconstructed with the same level of
evidence.

## Quickstart Is Now a Route

The complete clean path now looks like this:

```text
main menu
-> Q or q
-> load the default party
-> choose the original starting city and time
-> present PARTY02 cards 2, 3, 4, and 5
-> present the interactive card 6
-> select the certified first row
-> return state 001Dh
```

This route is available in both the deterministic console host and the SDL
frontend. The console version makes exact behavior easy to test. The graphical
version lets us experience the same sequence through pictures, sound, pointer
movement, and keyboard input.

Most importantly, it begins at the real start screen and ends at a real game
state. There is no fixture pretending the party already exists and no host
button teleporting directly into a city.

Quickstart now earns its name. It is the shortest honest path from launching
Darklands to making a decision in its world.

The next devlog follows that decision into the city.
