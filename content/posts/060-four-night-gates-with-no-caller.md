---
title: "Devlog #060 - The wall and lost content"
date: 2026-08-15T22:00:00+02:00
summary: "The city-wall route now reaches the original gate controller, while four authentic nighttime gate cards remain stranded in MSGFILES without a version-483.07 caller."
---

After finishing the marketplace work, we followed one of the less obvious
city choices: leaving the ordinary street route, approaching the outer wall,
and inspecting how the gates are guarded. That path now reaches the original
wall screen, its gate submenu, and the two clean city-side outcomes: return to
the streets or continue toward the still-unfinished world-travel boundary.

In the process, we found four cards that the shipped game (at least 483.07) appears 
never to call.

## Walking around the wall

The route begins in `$SELEC00`, the controller used when the party considers
leaving a city. One of its seven choices is not an attempt to leave conventionally:
it allows the party to move along and examine the wall for a discrete exit.

![$SELECT00 - card 0 as shown from inside our SDL reimplementation](/images/devlogs/060/selec00-SDL.png)


The original callback copies the controller's success text, then the local
action publishes raw state `003Bh`. Central dispatch enters `$SELEC01` card 0
with `PICS\\XMS050.PIC`.

![$SELECT01 - card 0 as shown from inside our SDL reimplementation](/images/devlogs/060/selec01-SDL.png)

The reconstructed route is now:

```text
$SELEC00 card 0
  inspect how the walls are guarded
        ↓
$SELEC01 card 0
  city-wall choices
        ↓
$SELEC01 gate submenu
  leave the city / return to the streets
```

Returning to the streets reaches the ordinary city-street state without
advancing the clock; its owner then chooses the proper day or night
presentation. Choosing to leave reaches the certified city/world boundary,
where the clean runtime deliberately stops. Outside-city travel is a
larger subsystem which we will tackle later.

This is a small route, but it closes an important loop, helping he city become a
connected place rather than a collection of isolated menus.

## Seventeen Cards, Four Without a Caller

`$SELEC00.MSG` contains seventeen cards. Card 0 is the selectable departure
screen. Cards 1 through 12 are result cards used by its escape, persuasion,
alchemy, prayer, and combat-related branches.

Cards 13 through 16 describe a separate nighttime gate sequence:

- the party finds the gate closed for the night;
- a sergeant can accept the party's argument and use a sally port;
- the sergeant can refuse;
- the guards can raise an alarm and attack.

![Cards 13-16 are present in $SELECT00 but never displayed in the original game](/images/devlogs/060/night_rows.png)

These are authentic records in the original `MSGFILES` payload. They are not
unused translation strings or reconstruction notes. The text, card layouts,
and card ordinals were shipped with Darklands 483.07.

But even if the card is here, it doesn't mean it's reachable.

The executable contains one `$Selec00` resource loader. Its owner always asks
the generic scanner for literal card 0. Its result-card calls use ordinals 1
through 12. A complete census of that overlay found no call supplying card 13,
14, 15, or 16.

Even the route that advances one hour before returning to `$SELEC00` still
presents card 0 after nightfall. There is no hidden hour check between the
state transition and the card request.

## Present in the Data, Missing from the Program

This gives us a different kind of lost content from a merely hidden menu row.
The four night cards have:

```text
resource data:       present
original text:       present
version 4.83.07 call site: not found
faithful runtime:    intentionally not exposed
```

We do not yet know whether an earlier build had a caller, whether a late code
change orphaned the cards, or whether the sequence was written but never
connected. The surviving data is strong evidence of intent, but it does not
tell us the exact trigger, how the choices were published, or how every result
returned to the surrounding state machine.

That distinction matters. Automatically substituting card 13 whenever the
clock reaches 19:00 would be plausible, but it would not be a reconstruction
of version 4.83.07. The original owner demonstrably does something else.

## A Future Restored-Content Layer

The wall audit suggests a useful long-term separation.

The faithful mode should reproduce the released executable, including its
missing callers and unreachable data. A separately labelled restored-content
mode could eventually reconnect material such as cards 13 through 16. Such a
mode would preserve the original text and known controller conventions while
making every reconstructed trigger or transition explicit.

That would not be ordinary reverse engineering anymore. It would be editorial
restoration based on reverse-engineering evidence.

For now the cards remain catalogued, tested, and deliberately unreachable. We
know where they are, what they say, and exactly what proof is still missing.
That is already enough to prevent them from disappearing a second time and
we will be ready when the time comes for restored content.
