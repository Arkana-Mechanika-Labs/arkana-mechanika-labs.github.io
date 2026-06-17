---
title: CHARACTR.TMP — Runtime Character Cache
weight: 2
---

Temporary file containing the current party's character data after a saved game is loaded. A bridge between the durable save format and the live runtime party state.

{{< format-meta
  ext="<code>CHARACTR.TMP</code>"
  location="Game root (runtime-generated)"
  endian="Little-endian (16-bit)"
  size="Variable — 2-byte count + 10-byte index table + 20-byte image IDs + (num_chars × 554-byte character records)"
  compression="None"
  magic="None"
  status="partial"
  source="Wendigo — character.tmp.html; byte-level validation against a live file pending"
>}}

*Canonical source: `character.tmp.html` ([Wendigo's Darklands repo](https://github.com/vvendigo/Darklands))*

## File Layout

```
Offset 0x00:  word        num_characters
Offset 0x02:  word[5]     char_index    — party character indices
Offset 0x0C:  string[5]   images        — 4-byte image-group IDs for each party member
Offset 0x20:  character[] characters    — num_characters × character struct
```

The `character` struct is the same used in the save-file format. See [Save File](/formats/save-file/) for the character struct layout.

### Image group identifiers

Each `images` entry is a 4-byte fixed-width string identifying the character's sprite set (e.g. `E00C`, `F01C`). These correspond to the `*.CAT` file prefixes in the battle sprite catalogs.

## Confidence

Medium. Structure from community reference; byte-level validation against a live file is pending.
