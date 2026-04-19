---
title: CHARACTR.TMP — Runtime Character Cache
weight: 2
---

Temporary file containing the current party's character data after a saved game is loaded. A bridge between the durable save format and the live runtime party state.

*Canonical source: `character.tmp.html` (wallace.net)*

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
