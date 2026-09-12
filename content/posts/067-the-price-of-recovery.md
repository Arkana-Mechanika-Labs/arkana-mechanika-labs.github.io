---
title: "Devlog #067 - The price of recovery"
date: 2026-08-31
draft: false
tags: ["gameplay", "healing", "city-navigation", "reverse-engineering", "darklands"]
description: "Paid care, charity, and the original rules behind both."
summary: "Paid care, charity, and the original rules behind both."
---

Getting a wounded party back on its feet sounds like one of the simpler jobs in an RPG. Find someone willing to help, pay the bill, and wait for the numbers to recover.

The convent has other ideas. It charges a contribution, considers requests for charity, gives each character a separate recovery roll, and decides when the party can resume its business. Even two visits that both end at seven in the morning need not have taken the same amount of time.

The ordinary convent care menu now works in the reconstructed C# engine and its SDL frontend: paid care, a conditional request for free care, refusal, and leaving. This is a small but useful addition to the city. The party can do more than look at another restored room; it can use a service and carry the consequences back outside.

## One florin, four patients

For the supported four-character party, the contribution is one florin: four shares of sixty pfennigs. The displayed amount comes from that particular service, rather than a generic money token filled with a convenient value.

Payment has a definite place in the interaction. Selecting the option first presents a message. The purse remains unchanged until that message is acknowledged. Then the game takes the contribution, checks whether another payment would still be affordable, performs recovery, and advances time.

That second affordability check matters. Spend your last florin and, when the care menu returns, the paid option remains visible but disabled. It does not disappear, and it does not remain usable because the screen was built before the money changed.

This is the difference between drawing the menu and rebuilding it from the party's current circumstances.

## Recovery is not a reset button

The recovery routine does not simply restore everyone to maximum Strength. It makes an independent random draw for each active character and passes a result from zero to two to the original Strength-adjustment routine.

A controlled observation in the original game made this particularly clear. All four characters began the watched recovery pass with current Strength set to one:

| Party member | Strength before | Recovery draw | Strength after |
| --- | ---: | ---: | ---: |
| First | 1 | 1 | 2 |
| Second | 1 | 0 | 1 |
| Third | 1 | 1 | 2 |
| Fourth | 1 | 2 | 3 |

There were four watched Strength writes, with no additional full-heal pass in that invocation. The second character received no increase at all.

Those were deliberately prepared research conditions, not a claim about an ordinary adventuring party. Their purpose was to distinguish two interpretations that could look similar when testing healthier characters: incremental recovery and unconditional restoration. The original instructions and the observed writes supported the former.

The reconstruction preserves those separate rolls. Replacing them with a single party-wide roll would change both who recovers and the random state left for subsequent actions.

## Asking for charity

The request for free care is a different action, not paid care with the price set to zero.

Its normal threshold combines the four active characters' average current Virtue with the selected character's current Charisma. There is also a special affordability rule: when the contribution check finds insufficient money, the threshold is replaced with 90 before the final clamp.

We can establish that rule without inventing an explanation for why its designers chose that number. Nor should the threshold simply be reported as a percentage: the original accepts a random result equal to the threshold, as well as one below it.

Acceptance displays its own response and waits for acknowledgement before recovery and calendar effects occur. Refusal displays another response and returns to the church without performing recovery or advancing the calendar in that action.

That refusal needs to be tested as seriously as acceptance. Otherwise a convincing-looking message could conceal a party that was healed anyway.

## Seven o'clock is not a duration

Both care routes return to seven in the morning, but their calculations differ.

Paid care first finds the forward distance to five o'clock, then adds two hours. Accepted free care uses the direct distance to seven. At six in the morning, that means twenty-five hours for the paid route, but one hour for the accepted free-care route.

The same final clock display can therefore conceal a different date and a different amount of calendar maintenance. We preserve the original calculations rather than replacing both with a generic “rest until morning.” The selected same-month calendar relations have been checked across all twenty-four starting hours.

## Back through the door

The ordinary care choices now join messages, money, character changes, time, and return navigation. Leaving the convent has its own one-hour cost; receiving a refusal does not borrow that cost merely because the party also ends up outside.

Some less common continuations and month-end maintenance remain outside the supported route. They stop explicitly rather than borrowing the ordinary behavior. A developer command can also prepare the care menu for testing, but bypassing the approach is not evidence that the approach has been reconstructed.

Within those boundaries, another piece of the city has become functional. The party can pay, ask, recover a little, receive an unwelcome answer, or discover that the last florin really was the last florin.
