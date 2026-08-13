# Darklands 483.07 Reported-Bug Research Catalogue

Status: **research control only**

Runtime authority: **none**

Executable use: **forbidden**

This catalogue preserves versioned bug reports as investigation leads for the
Darklands 483.07 reconstruction. It is deliberately separate from
[`docs/KNOWN_ORIGINAL_BUGS.md`](../KNOWN_ORIGINAL_BUGS.md), whose entries
require original-byte evidence and an explicit rewrite disposition.

The initial source report was supplied for research on 2026-08-13. A second
revision supplied the same day reports a direct mining pass over searchable
Darklands Yahoo/Groups.io mail from November 2011 through April 2026. Its
message-number references and version qualifications are incorporated below.
The complete 1998--2010 archive was not searchable in that pass, so attribution
among 483.05, 483.051, and 483.06 remains unresolved. Inclusion still does not
independently verify a claim. Mojibake in the supplied text has been normalized
in this catalogue.

The mining pass establishes two useful version rules for research triage:

- posts explicitly identifying the GOG or Steam distribution normally concern
  the 1995 CD-ROM/final 483.07 executable;
- modern posts without an installation identity are only *probably* 483.07,
  while older versionless Yahoo reports remain version-unresolved.

## Rules of use

1. A report can prioritize an owner, boundary test, or runtime observation.
   It cannot authorize C# behavior.
2. Before implementation, establish the exact 483.07 owner and path from
   original bytes, focused Ghidra, independent Reko, and the applicable COAB
   certificate or typed boundary.
3. Never infer that a defect existed in 483.07 because an earlier version had
   it. Conversely, “reported in 483.07” does not prove that 483.07 introduced
   it.
4. Do not silently fix a confirmed defect. Promote it to
   `KNOWN_ORIGINAL_BUGS.md`, record the original units and instructions, and
   choose `replicate`, `correct`, `disable`, or `pending` explicitly.
5. Platform, manual, data, and runtime-logic defects remain separate classes.
6. A community explanation of a cause is only a hypothesis until the
   corresponding 483.07 instructions and data relation are closed.

## Catalogue statuses

| Status | Meaning |
| --- | --- |
| `historical_fixed_by_483_07` | Relevant to version history but not expected in the target executable. |
| `official_483_07_report` | A surviving 483.07 issue described by MicroProse documentation. Still requires byte evidence before implementation policy. |
| `reported_483_07` | A final-version community or mechanical report awaiting original-code confirmation. |
| `reported_version_unresolved` | Independently reported behavior whose executable version was not identified. |
| `forensic_final_era` | A final-era save or data artifact establishes the corruption signature, but not its original trigger. |
| `mechanic_or_presentation` | Evidence favors deliberate mechanics, lifecycle behavior, or inadequate feedback rather than defective runtime logic. |
| `byte_confirmed` | Promoted separately to `KNOWN_ORIGINAL_BUGS.md`; that canonical entry controls policy. |
| `disproved_for_483_07` | Investigation showed that the report does not describe the target build or selected path. |
| `platform_or_documentation` | Not a core 483.07 gameplay-rule defect unless later evidence proves otherwise. |

Confidence labels in this file describe the quality of the supplied report,
not COAB implementation grade: `official`, `strong`, `moderate`, or
`tentative`.

## Historical defects not applicable to faithful 483.07 behavior

These remain useful when comparing old saves, patch notes, or versioned data,
but must not be reconstructed as 483.07 mechanics.

| Report | Status | Confidence | Research note |
| --- | --- | --- | --- |
| Quest-blocking memory leak in early retail builds | `historical_fixed_by_483_07` | official | Designer testimony associates it with original releases; fixed during the stabilization cycle. |
| Save corruption caused by the same early memory defect | `historical_fixed_by_483_07` | official | Do not conflate with the distinct unsafe-location save rollback acknowledged in 483.07. |
| Broad 483.04/05/051 machine-compatibility failures | `historical_fixed_by_483_07` | official but nonspecific | Primarily addressed by 483.06. |
| Earlier save/load unreliability | `historical_fixed_by_483_07` | official but nonspecific | 483.07 substantially improved it; this does not disprove the surviving rollback behavior below. |
| Graz exit/progression-state problem | `historical_fixed_by_483_07` | official | Fixed in 483.07, though old saves could retain the bad state. |
| Roland music plus DMA digital-audio regression | `platform_or_documentation` | official | Present in the 483.07 distribution and fixed by the separate March 1993 DRKSND driver update; not a core MSG/gameplay rule. |
| High-reputation merchant buy/resell arbitrage | `historical_fixed_by_483_07` | strong player comparison | Yahoo #9494 recalls the original as probably 483.04 and reports the exploit absent after upgrading to 483.07. The exact first fixed version is unknown. Test preserved binaries at reputation 99/100/101/120/150; do not reconstruct this as final-version commerce behavior. |

## Officially reported surviving 483.07 issues

| ID | Report | Status | Confidence | Suggested evidence target |
| --- | --- | --- | --- | --- |
| `RPT-SAVE-0001` | Saving while complex transient event state is being committed can restore an earlier state or time. | `official_483_07_report` | official | Save controller, temporary-to-persistent event transfer, and restore boundary. |
| `RPT-PALETTE-0001` | Character battlefield colors can become corrupted, appear in a later battle, and persist in a save. | `official_483_07_report` | official; trigger unknown | Character palette mutation, battle-entry publication, and save serialization. |
| `RPT-FILES-0001` | Character generation depends on `SAVES\DEFAULT`; deleting it disables creation. | `official_483_07_report` | official | Startup/party-creation resource dependency. The rewrite already deliberately loads the default save, but the original failure relation is not yet a known-bug entry. |
| `RPT-LOAD-0001` | The in-game Load dialog cannot be cancelled once opened. | `official_483_07_report` | official | Universal menu/load controller and its input dispatch. |
| `RPT-PLATFORM-0001` | Some disk controllers fail during the opening and two later cinematics; `/Q` bypasses animations. | `platform_or_documentation` | official, hardware-sensitive | Typed platform boundary only if a game-observable dependency requires it. Do not emulate obsolete controller failure. |

## Inventory and numeric boundary reports

| ID | Report | Status | Confidence | Suggested boundary tests |
| --- | --- | --- | --- | --- |
| `RPT-INV-0001` | More than approximately 64 distinct inventory records can cause silent item loss. | `reported_483_07` | strong | 63/64/65 records across loot, transfer, purchase, save, and reload. Distinguish failure to insert from later serialization loss. |
| `RPT-INV-0002` | A stack quantity is structurally bounded by one byte; behavior of an attempted quantity 256 remains unknown. | `reported_483_07` | strong structure, runtime overflow unverified | Test quantities 254/255 plus insertion, merge, split, transfer, consumption, and save/load. Do not state wrap, loss, or corruption without reproduction. |
| `RPT-INV-0003` | Aggregate inventory above 255 was proposed as a palette-corruption trigger. | `reported_483_07` | weak/conflicted | A character has only 64 record slots; the claim may conflate stack quantity, aggregate objects, inn indexing, or an unrelated palette copy defect. It is not an established trigger for `RPT-PALETTE-0001`. |
| `RPT-INN-0001` | More than 255 items stored at an inn may be lost on retrieval. | `reported_483_07` | moderate | Inn-storage quantity/record layouts at 254/255/256 and retrieval compaction. |
| `RPT-INN-0002` | Inn storage and enemy cloth drops stopped working in one long-running world; moving the party to a fresh world restored storage. | `reported_483_07` | moderate; one detailed 2025 case | Investigate world/event-table corruption or exhaustion separately from party records. Copying the old four-byte world RNG seed happened after storage was repaired and is not evidence that the seed caused or fixed the defect. “Storing cloth causes it” remains unsupported. |
| `RPT-NUM-0001` | Attributes or temporarily boosted skills above 99 can behave incorrectly. | `reported_483_07` | moderate | Values 98/99/100 and expiration/reapplication paths; do not assume a common cause across fields. |
| `DL-ORIG-GAME-0001` | A merchant can charge for an item that a full inventory cannot accept. | `byte_confirmed` | original bytes | Canonical policy and exact predicate are in `KNOWN_ORIGINAL_BUGS.md`. This is narrower than a general “64 items disappear” claim. |

## Deterministic data and gameplay reports

| ID | Report | Status | Confidence | Suggested evidence target |
| --- | --- | --- | --- | --- |
| `RPT-ALCH-0001` | Alchemical vendors appear to select only the first 22 of 66 quality-specific formula records. | `reported_483_07` | strong; Groups.io #9863 | Merchant formula table bound/index and random formula-trade path. The report concerns vendor selection, not total formula availability through trading or special sources. Test indices 21/22/23/65 for alchemists, universities, and overland monasteries. |
| `RPT-SAINT-0001` | Paul the Apostle and Paul the Simple have swapped or contradictory effect associations. | `reported_483_07` | strong | `DARKLAND.SNT` records, selector table, descriptions, and invoked effect vectors. |
| `RPT-SAINT-0002` | Overlapping attribute blessings can leave two expiration events and subtract twice. | `reported_483_07` | moderate; exact v7 status disputed | Blessing replacement plus both expiration-event records, tested in both expiration orders. Keep distinct from equipment modifiers that announce expiration but remain active. |
| `RPT-SAINT-0003` | A flail skill blessing can apply twice when a flail is equipped. | `reported_483_07` | moderate/strong | Saint effect loop and equipped weapon category branch. |
| `RPT-EQUIP-0001` | Equipment-affecting potion/saint modifiers may announce expiration while their armor, weapon, or fire-resistance fields remain active. | `reported_483_07` | strong; repeated 2025/2026 reports plus identified save fields | Modifier-event creation, persistent armor/weapon/fire fields, equipment publication, expiration consumer, and save/reload. Reports specifically include Firewall, St. Polycarp, Deadly Blade, Greatpower, and Strongedge. |
| `RPT-EQUIP-0002` | Reapplying an equipment modifier can recalculate unrelated equipment. | `reported_483_07` | moderate | Reapplication dispatcher and all rewritten equipment fields. |
| `RPT-EQUIP-0003` | Greatpower appears to affect the armed weapon regardless of documented category. | `reported_483_07` | moderate | Effect category predicate; may instead be a documentation mismatch. |
| `RPT-EQUIP-0004` | Overlapping temporary stat effects can expire incorrectly and leave a permanent reduction below the original value. | `reported_483_07` | moderate; one expert 2026 report | Test saint then potion and potion then saint, both expiration orders, and save/reload while both are active. Do not merge with `RPT-EQUIP-0001`: the visible failure and possibly the owner chain differ. |
| `RPT-RELIC-0001` | Battlefield-chest relic weapons are forced to quality 35 despite authored qualities. | `reported_483_07` | strong | Chest-generation item construction and relic definition quality. |
| `RPT-RELIC-0002` | Relics may not improve associated saint prayers. | `reported_483_07` | tentative | Prayer threshold inputs for ordinary and greater relics; absence across all paths is not yet proven. |
| `RPT-EVENT-0001` | High Sabbat can default to invalid “Jan 0” and map coordinates 0,0. | `reported_483_07` | strong | Event initialization and failure/default record writes. |
| `RPT-EVENT-0002` | High Sabbat generation fails beyond 31 December 1499. | `reported_483_07` | strong | Calendar comparison and event generator around year 1500. |
| `RPT-CHURCH-0001` | Confession time can become zero near local reputation 130 and negative above it. | `reported_version_unresolved` | moderate; Yahoo #9553 | Church owner arithmetic at reputation 128--132 and higher; observe the signed calendar-helper argument exactly. The report names no executable version. |
| `RPT-CHURCH-0002` | Tithing was reported to omit the final party member when restoring Divine Favor. | `reported_483_07` | disputed | The mined archive instead observed the Virtue increase on every eligible party member. Retain only as a boundary-test lead for parties of one through five pending exact loop inspection. |
| `RPT-BALANCE-0001` | Sufficient cash and Religion make Virtue gains from the church donation predictable and repeatable. | `mechanic_or_presentation` | strong mechanic, defect status unsupported | The church takes 10% of party cash: 6,001 pf on hand produces a 601-pf donation, reported sufficient for an eligible Religion-30 character. Decode the rule; repeatability alone does not make it a bug. |
| `RPT-COMBAT-0001` | Pause while aiming, choose Flee without a destination, then resume to release repeated missiles through the melee animation. | `reported_version_unresolved` | strong; Yahoo #9455 independently reproduced | Combat action state for bows, firearms, and thrown weapons. Separately observe animation, pending projectile, cooldown, original target, and target-death cleanup. Potions reportedly do not share the same autofire state. |
| `RPT-MERCHANT-0001` | Guild/smith specialization can fail for nighttime inventories. | `reported_483_07` | strong | Day/night merchant catalogue predicate and specialization masks. |
| `RPT-ARMOR-0001` | Damage to one equipped armor copy can affect every identical stacked copy. | `reported_483_07` | strong | Inventory aliasing/stack mutation, equipped-record identity, and damage write target. |
| `RPT-QUEST-0001` | A fortress/Feste ruler can issue a raubritter quest but fail to recognize completion or pay the reward, unlike a Rathaus. | `reported_version_unresolved` | moderate/strong; corroborated 2017 observations | Compare identical targets and simultaneous commissions from Rathaus, Feste, guild, Fugger, and Hanse issuers; inspect completion flags, reward owner, and reputation effects. |
| `RPT-QUEST-0002` | A clerk's “come back tomorrow” appointment may establish no usable follow-up state. | `reported_version_unresolved` | moderate/low | Separate the in-game appointment/event state from limitations of the third-party quest viewer mentioned in the same report. |
| `RPT-WILDHUNT-0001` | World generation may choose a Wild Hunt banishing saint that is unobtainable anywhere in that world. | `reported_483_07` | moderate; one expert report | Enumerate generated saint availability against every Hunt requirement. Random selection itself is intended; only an unavailable, ineffective, or uncleared requirement is suspect. |
| `RPT-STONE-0001` | An attempted Philosopher's Stone upgrade can fail repeatedly without explaining that the university's Stone is not better. | `mechanic_or_presentation` | moderate | Separate legitimate world generation with no superior Stone from the missing comparison feedback. Do not classify it as a broken success roll without operand evidence. |

## Potion behavior and description mismatches

These require special care: a mismatch may be defective code, defective text,
or intentional abstraction. MSG descriptions are never runtime authority.

| ID | Report | Status | Confidence | Suggested evidence target |
| --- | --- | --- | --- | --- |
| `RPT-POTION-0001` | New-wind grants temporary Endurance rather than restoring lost Endurance as described. | `reported_483_07` | moderate | Potion effect vector, timed event, and description record. |
| `RPT-POTION-0002` | Black Cloud changes no displayed Stealth/Perception and instead serves event concealment. | `reported_483_07` | moderate | Item availability contexts, event consumer, and effect vector. |
| `RPT-POTION-0003` | Sunburst ignores range and physical obstruction while applying facing/arc logic. | `reported_483_07` | moderate | Combat target enumeration, arc predicate, distance, and line-of-sight calls. |
| `RPT-POTION-0004` | Greatpower category, expiration, and reapplication behavior contradicts documentation. | `reported_483_07` | moderate | Cross-reference `RPT-EQUIP-0001..0003`; do not create duplicate runtime policies. |

## Tentative runtime and content reports

| ID | Report | Status | Confidence | Suggested evidence target |
| --- | --- | --- | --- | --- |
| `RPT-WORLDMAP-0001` | Travel map can freeze or scroll continuously. | `reported_483_07` | tentative | World-map input and scroll controller; first exclude DOSBox/host input behavior. |
| `RPT-COMBAT-0002` | A wilderness battle can begin without enemies. | `reported_483_07` | tentative | Encounter participant publication and zero-enemy continuation. |
| `RPT-MINE-0001` | Mine Problem III parley can produce an empty screen. | `reported_483_07` | tentative | Quest event/card selection and active visual source. |
| `RPT-INITI-0001` | The “Initial Card for Testing Only” card can appear during the main plot. | `reported_483_07` | tentative | `$INITI00` caller/owner and event-card index. Existing research must be consulted before reopening this target. |
| `RPT-ROSTER-0001` | Female or alchemist inn recruits can receive an incorrect sprite/color. | `reported_483_07` | tentative | Recruit template, appearance fields, palette selection, and save publication. |
| `RPT-CALENDAR-0001` | A fresh GOG game reportedly rolled from 28 July 1400 back to 1 July, repeatedly invoked copy protection, and published the first High Sabbat as “Jan 0.” | `reported_483_07` | moderate incident, low causal confidence; Yahoo #9692 | Treat as a possible linked initialization/state-loss cluster, not proof that every Jan-0 event shares one cause. Exercise custom-party starts from April through August 1400 while observing calendar, protection state, event initialization, and quest reset. |

## Forensic save signatures

These entries identify durable corruption patterns in affected saves. They do
not establish which original runtime path produced the corruption.

| ID | Forensic observation | Status | Confidence | Suggested evidence target |
| --- | --- | --- | --- | --- |
| `RPT-PALETTE-0002` | In two damaged final-era saves, the party color block was displaced by exactly one 16-bit word; its trailing bytes overwrote the beginning of character record 0. Repositioning the block repaired both saves. | `forensic_final_era` | very strong signature; trigger unknown; Groups.io #9968 | Byte-diff the party header and first character record across 4-to-5 recruitment, dismissal, temporary absence/imprisonment, death, inventory mutation, and intervening saves. Do not claim that party size or inventory quantity is the trigger until reproduced. |

## Documentation and deliberate limitations

| Report | Status | Note |
| --- | --- | --- |
| Printed map says “Freiberg im Breisgau” instead of Freiburg | `platform_or_documentation` | Artwork/manual error, not a world-data defect if the game records are correct. |
| Manual describes a Hall of Fame that is absent | `platform_or_documentation` | Abandoned or incorrectly documented feature, not an executable bug. |
| Battlefield saving is restricted to particular cleared locations | `platform_or_documentation` | Deliberate rule unless original evidence exposes a separate failure. |
| Modern fullscreen, mouse, audio, or filesystem failures | `platform_or_documentation` | Reproduce under the original environment or trace into original behavior before cataloguing as a game defect. |
| A purchased formula belongs to the purchasing character; a traded formula goes to the current leader | `mechanic_or_presentation` | Character-owned formula knowledge is intentional according to the archive. The collective-looking interface communicates ownership poorly. |
| The main-quest fortress monastery disappears after an attempt | `mechanic_or_presentation` | Reported to reappear after a later Sabbat. Record a defect only if the intended lifecycle fails to respawn it. |
| Tarnhelm interaction causes the party to “crash through the floor” | `mechanic_or_presentation` | This is a scripted trap, not a software crash. Purifying the tomb, including through Transformation, is part of the intended route. |
| Different Wild Hunts require different randomly selected saints | `mechanic_or_presentation` | Random choice is intended. Investigate only unavailable saints, ineffective valid saints, or a Hunt that fails to clear after success. |
| Protection prompts occur at every map event after editing a save | `platform_or_documentation` | Yahoo #9643 explicitly ties this case to Jugglindan's editor. Keep separate from the fresh-GOG calendar/protection incident in `RPT-CALENDAR-0001`. |

## Archive confidence corrections

The Yahoo/Groups.io pass materially changes the confidence or category of the
following earlier claims:

- final-member omission during tithing is disputed, not corroborated;
- the church donation is 10% of cash: 6,001 pf held means 601 pf donated, not
  a 6,001-pf donation;
- predictable Virtue gain is presently a mechanic/balance question, not a
  confirmed defect;
- formula ownership, fortress-monastery disappearance, the Tarnhelm floor
  trap, and random Wild Hunt saints are mechanics or lifecycle behavior;
- protection spam after third-party save editing is not evidence of a vanilla
  defect;
- the archive did not independently strengthen the Paul-saint swap, relic
  quality 35, double flail blessing, above-99 attributes, Mine Problem III,
  or `$INITI00` claims. Their existing confidence and sources remain in force.

The archive also supplies two reconstruction leads rather than bug verdicts:

- event-card investigations should observe current card index, option-filter
  flags, and the selected far-handler pointer at the owner boundary;
- timed-modifier investigations must observe both event records and persistent
  weapon, armor, and fire-resistance fields. The latter are not safely assumed
  to be purely derived values.

## Existing byte-confirmed merchant defect not originating in the report

`DL-ORIG-UI-0001`, the merchant Ctrl+F leader/UI corruption, is already
byte-confirmed and documented in `KNOWN_ORIGINAL_BUGS.md`. It is listed here
only because future merchant investigation must distinguish it from the
reported nighttime-specialization defect. The canonical register—not this
catalogue—defines its SDL `disable` disposition.

## Suggested regression boundaries

These are investigation fixtures, not expected corrected outcomes:

- inventory records: 63, 64, and 65;
- stack quantities and inn storage: 254, 255, and attempted 256;
- attributes/skills: 98, 99, 100, with and without temporary modifiers;
- formula indices: 21, 22, 23, and 65;
- parties of one through five, including every eligible member rather than
  presupposing a final-slot omission;
- 31 December 1499 and 1 January 1500;
- local reputation 128, 129, 130, 131, and 132 on church time calculations;
- overlapping blessing/modifier expirations in both orders;
- two identical armor copies with only one equipped;
- combat Pause/Fire/Flee-without-destination sequences for each ranged class;
- party-size 4/5 transitions plus save/reload around the party color block;
- identical quest targets issued by Rathaus, Feste, guild, Fugger, and Hanse;
- Wild Hunt required saints against the complete obtainable set for each world;
- custom-party calendar initialization from April through August 1400;
- save immediately before, during, and after transient event-state commit.

Passing a fixture establishes only the observed C# behavior. A compatibility
claim still requires an independent original oracle or certified owner/path.

## Source index from the supplied report

The catalogue retains these sources as research leads. Their presence does
not elevate their claims above the project’s authority order.

- MicroProse 483.07 README mirror: <https://gamefaqs.gamespot.com/pc/564659-darklands/faqs/1897>
- MicroProse BBS file descriptions: <https://groups.google.com/g/bit.listserv.games-l/c/XTS7J4uQOOI>
- Arnold Hendrick retrospective: <https://rpgcodex.net/article.php?id=8246>
- GOG version/bug discussion: <https://www.gog.com/forum/darklands/i_must_know_are_any_historical_bugs_fixed>
- GOG alchemical-formula discussion: <https://www.gog.com/forum/darklands/alchemical_formulae/post13>
- Darklands Wiki item, alchemy, saint, relic, church, armor, and potion pages cited by the supplied report.
- MobyGames player report concerning the testing-only initial card.
- Searchable Yahoo/Groups.io mail corpus, November 2011--April 2026, mined in
  the second supplied revision. High-value message anchors include Yahoo
  #9455 (missile state exploit), #9494 (merchant arbitrage version comparison),
  #9553 (confession time), #9643 (editor-induced protection spam), #9692
  (fresh-GOG calendar/protection/Sabbat incident), and Groups.io #9863
  (formula bound), #9963/#10020 (modifier expiry), #9968 (palette save
  displacement), and #9994 (inn/world-state corruption).

The Yahoo/Groups.io corpus is incomplete before November 2011. Do not use its
silence to reject a claim or assign behavior among 483.05, 483.051, and 483.06.

When a target becomes active, archive the exact cited page or authoritative
file needed for that target, record its retrieval identity, and then proceed
to original-code verification. Do not repeatedly browse this broad source
list as a substitute for focused evidence.
