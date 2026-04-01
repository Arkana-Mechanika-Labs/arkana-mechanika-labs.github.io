---
title: Character Struct (0x22a bytes)
weight: 1
---

Each character in the save file occupies exactly **554 bytes (0x22a)**. Fields are **not sequential** — there are gap bytes throughout. All offsets are relative to the start of the character record.

*Sources: `dksaveXX.sav.xml` + `structures.xml` (wallace.net), confirmed against DARKLAND.EXE decompilation*

> **Note:** Darklands has no class system. Characters are defined by backgrounds, occupations, and 19 individual skills. Equipment type and quality for each slot are **not adjacent** in the struct — see the table below.

## Field Layout

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | 17 | *(unknown)* | — |
| +0x12 | 2 | `age` | Character age |
| +0x15 | 1 | `heraldic_shield` | Coat-of-arms letter (`'A'`–`'O'`); references `pics\shield?.pic` |
| +0x22 | 1 | `equip_missile_type` | Item type of equipped missile weapon |
| +0x25 | 25 | `full_name` | Full character name |
| +0x3e | 11 | `short_name` | Nickname (10 chars + null) |
| +0x4b | 1 | `equip_vital_type` | Item type of equipped vital (torso) armor |
| +0x4c | 1 | `equip_leg_type` | Item type of equipped leg armor |
| +0x4f | 1 | `equip_vital_q` | Quality of equipped vital armor |
| +0x50 | 1 | `equip_leg_q` | Quality of equipped leg armor |
| +0x51 | 1 | `equip_weapon_type` | Item type of equipped weapon |
| +0x58 | 1 | `equip_weapon_q` | Quality of equipped weapon |
| +0x5a | 1 | `equip_missile_q` | Quality of equipped missile weapon |
| +0x5b | 1 | `equip_shield_q` | Quality of equipped shield |
| +0x5c | 1 | `equip_shield_type` | Item type of equipped shield |
| +0x5d | 7 | `curr_attrs` | Current attribute values (`attribute_set`) |
| +0x64 | 7 | `max_attrs` | Maximum attribute values (`attribute_set`) |
| +0x6b | 19 | `skills` | Skill values (`skill_set`) |
| +0x7e | 2 | `num_items` | Number of items carried |
| +0x80 | 20 | `saints_known` | 160-bit bitmask — one bit per saint |
| +0x94 | 22 | `formulae_known` | Bitmask — 3 bits per byte (quality levels q45/q35/q25) |
| +0xaa | 384 | `items` | Up to 64 `item` structs (6 bytes each) |

## attribute_set (7 bytes)

| Offset | Attribute |
|--------|-----------|
| +0x00 | Endurance |
| +0x01 | Strength |
| +0x02 | Agility |
| +0x03 | Perception |
| +0x04 | Intelligence |
| +0x05 | Charisma |
| +0x06 | Divine Favor |

## skill_set (19 bytes)

| Offset | Skill | Code |
|--------|-------|------|
| +0x00 | Edged Weapon | `wEdg` |
| +0x01 | Impact Weapon | `wImp` |
| +0x02 | Flail Weapon | `wFll` |
| +0x03 | Polearm | `wPol` |
| +0x04 | Thrown Weapon | `wThr` |
| +0x05 | Bow | `wBow` |
| +0x06 | Missile Weapon | `wMsl` |
| +0x07 | Alchemy | `alch` |
| +0x08 | Religion | `relg` |
| +0x09 | Virtue | `virt` |
| +0x0a | Speak Common | `spkC` |
| +0x0b | Speak Latin | `spkL` |
| +0x0c | Read/Write | `r_w` |
| +0x0d | Healing | `heal` |
| +0x0e | Artifice | `artf` |
| +0x0f | Stealth | `stlh` |
| +0x10 | Streetwise | `strw` |
| +0x11 | Riding | `ride` |
| +0x12 | Woodwise | `wdws` |

## item (6 bytes)

| Offset | Field |
|--------|-------|
| +0x00 | Item code (word — index into `darkland.lst` item_definitions) |
| +0x02 | Type |
| +0x03 | Quality |
| +0x04 | Quantity |
| +0x05 | Weight |
