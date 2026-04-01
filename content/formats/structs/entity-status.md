---
title: Entity Status Block (0x80 bytes)
weight: 2
---

The entity status system tracks all active entities in a scene — party members, NPCs, and enemies — in a flat array of fixed-size blocks.

*Confirmed by reverse engineering DARKLAND.EXE combat code*

## Block Array

| Property | Value |
|----------|-------|
| Base address | `0x9c65` |
| Block size | 128 bytes (0x80) |
| Capacity | ~81 entities |
| Stride | 0x80 |

`Block(n)` starts at: `0x9c65 + n × 0x80`

## Block Layout

| Offset | Size | Field | Description |
|--------|------|-------|-------------|
| +0x00 | word | `combat_flags` | Combat status flags (see below) |
| +0x04 | byte | `slot_status` | Entity slot status (see below) |

### combat_flags bits

| Bit value | Meaning |
|-----------|---------|
| 0x0001 | Fighting active |
| 0x0006 | Bleeding |
| 0x000a | Visible |
| 0x0012 | Adjacent to enemy |
| 0x0022 | Prone |
| 0x0040 | Resting |
| 0x0080 | Morale broken |
| 0x0100 | Terrified |
| 0x0400 | Unconscious |

### slot_status values

| Value | Meaning |
|-------|---------|
| 0x00 | Alive / active |
| 0x01 | Loaded |
| 0x03 | Pending overlay load — game loop will call `rtlink_load_char` |
| 0x05 | Removed / dead |

## Parallel Byte Arrays

These run alongside the block array with stride 1, indexed by character index:

| Base address | Field | Values |
|-------------|-------|--------|
| `0xa3d8 + n` | `condition_flag` | 0=ok, 1=bleeding, 2=exhausted |
| `0xa6c4 + n` | `combat_stance` | 1–8 |
| `0xa697 + n×2` | `stance_flags` | Word; bit 0x10 = blocking stance |

## Party Sidebar Layout

Party member N appears at Y pixel position `31 + N × 40`:

| Member | Y position |
|--------|-----------|
| 0 | 31 |
| 1 | 71 |
| 2 | 111 |
| 3 | 151 |
| 4 | 191 |
