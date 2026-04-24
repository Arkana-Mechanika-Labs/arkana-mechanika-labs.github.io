---
title: PAN Presentation Files (*.PAN)
weight: 1
---

Animated scene container format used for all intro and ending sequences. Opened sequentially
at startup (`OPENING2.PAN` through `OPENING9.PAN`) and again for the ending (`CREDITS.PAN`,
`DEATH.PAN`, `FIN0A.PAN`–`FIN5A.PAN`). Audio is paired separately in `.DGT` files.

*Reverse-engineered from `DARKLAND.EXE` runtime tracing and static analysis. No prior public
documentation of this specific format is known. Despite sharing the `.PAN` extension with other
MicroProse titles, the Darklands structure does not match the PANI-tagged format used in
Covert Action or Railroad Tycoon.*

*Format status: fully decoded. Corpus-validated across all 15 assets and 2,068 frame records.
Runtime SHA1 verification confirms byte-for-byte agreement between static replay and live DOSBox
framebuffer output.*

---

## Format Overview

The format is a five-layer stack:

```
PAN file bytes
  → 0DFC:0070 stateful stream decoder
  → logical stream
  → 5A frame-end table
  → 768-byte embedded VGA palette
  → 42/1 frame-delta records
  → 320×200 indexed framebuffer
```

---

## Layer 1: Compressed Stream

The file-level decompressor is the runtime routine at `0DFC:0070`. It is stateful across calls:
each invocation fills a destination buffer and returns the number of bytes emitted. The next
call resumes from the preserved bitstream state. Related routines in the same segment:

| Address | Role |
|---------|------|
| `0DFC:002A` | Open stream and initialize decoder state |
| `0DFC:000C` | Refill 0x1000-byte file input buffer at `A897` |
| `0DFC:0059` | Close stream handle |
| `0DFC:006A` | Return persistent status word `[08BC]` |
| `0DFC:0070` | Decode one output span |

The decoder maintains a 16-bit control word in `BP` and a bit counter in `DX`. Control bits
are consumed via `RCR BP,1`. When the counter is exhausted, a new little-endian control word
is loaded from the input stream.

### Span grammar

```python
def decode_span(out):
    while True:
        if next_bit() == 1:
            out.append(read_u8())                       # literal byte
            continue

        if next_bit() == 1:
            word = read_u16le()
            backref = 0xE000 | ((word >> 11) << 8) | (word & 0x00FF)
            count3  = (word >> 8) & 0x07
            if count3 != 0:
                count = count3 + 2
            else:
                m = read_u8()
                if m <= 1:
                    status = m ^ 1
                    return                              # span terminates here
                count = m + 1
            copy_from_output(out, signed16(backref), count)
            continue

        count   = 2 + (next_bit() << 1) + next_bit()
        backref = 0xFF00 | read_u8()
        copy_from_output(out, signed16(backref), count)
```

**Critical:** when the inner byte `m` is `0` or `1`, the span terminates. These values do not
encode copies. `m = 0` → status becomes 1 (final span); `m = 1` → status becomes 0 (caller
may invoke `0070` again). Misreading `m = 1` as a copy was the root cause of all earlier failed
parse models.

---

## Layer 2: Logical Stream Header

Every decoded logical stream begins with a `5A` table:

```
0x0000  u16le   magic word = 0x0A5A
0x0002  u16le   frame count N
0x0004  u16le[] cumulative frame-end offsets — N entries
```

Frame-end positions are cumulative from logical offset zero:

```python
record_end[0] = delta[0]
record_end[i] = record_end[i - 1] + delta[i]
```

The layout of the remainder of the logical stream:

```python
table_end           = 4 + 2 * N
palette_offset      = table_end
first_record_offset = table_end + 768
```

Example (`OPENING8.PAN`, 231 frames):

```
table end:    0x01D2
palette:      0x01D2..0x04D2
first record: 0x04D2
stream end:   0x83412
```

---

## Layer 3: Embedded VGA Palette

768 bytes immediately following the `5A` table. 256 RGB triplets, each component a 6-bit
VGA DAC value in the range `0..63`.

Convert each component to 8-bit RGB:

```python
rgb8 = (dac6 << 2) | (dac6 >> 4)
```

The first 16 entries are the standard EGA/VGA base colors. Every PAN asset in the corpus
contains a complete, valid 768-byte palette.

---

## Layer 4: Frame Records

Each frame record begins at the previous record's end, with the first record at
`first_record_offset`. Every record opens with a 4-byte header:

```
42 00 01 00
```

The bytecode payload begins immediately after that header and runs to the record end as
defined by the `5A` table. All records in the corpus terminate with the `end16` opcode.

---

## Layer 5: `42/1` Frame-Delta Bytecode

The payload updates a 320×200 indexed framebuffer (64,000 bytes, row-major, one byte per
pixel). The destination cursor starts at offset 0 for each record.

### Byte opcodes

| Range | Opcode | Action |
|-------|--------|--------|
| `0x01..0x7F` | `lit8 N` | Copy next N literal bytes to framebuffer; cursor += N |
| `0x80..0xFF` | `skip8 N` | cursor += (opcode − 0x80) |
| `0x00` | `fill8` | Next byte = count; next byte = value; write value N times; cursor += N |

### Extended opcodes (introduced by `0x80`, followed by a u16le word)

| Word range | Opcode | Action |
|------------|--------|--------|
| `0x0000` | `end16` | Terminate record |
| `0x0001..0x7FFF` | `skip16` | cursor += word |
| `0x8000..0xBFFF` | `lit16` | Copy (word − 0x8000) literal bytes; cursor += count |
| `0xC000..0xFFFF` | `fill16` | Fill (word − 0xC000) cells; value = next byte |

Note: `0x80` is a zero-count `skip8`, so it always introduces an extended word. The distinction
between `skip8` (`0x81..0xFF`) and the extended prefix (`0x80`) is unambiguous.

---

## Reference Parser

```python
def parse_pan(path):
    logical = decode_all_0070_spans(path)

    assert read_u16le(logical, 0) == 0x0A5A
    n = read_u16le(logical, 2)

    total = 0
    ends = []
    for i in range(n):
        total += read_u16le(logical, 4 + 2 * i)
        ends.append(total)

    table_end   = 4 + 2 * n
    palette_rgb = decode_vga_palette(logical[table_end : table_end + 768])

    records = []
    start = table_end + 768
    for end in ends:
        assert logical[start : start + 4] == b"\x42\x00\x01\x00"
        records.append((start, end, logical[start + 4 : end]))
        start = end

    return palette_rgb, records


def replay(palette_rgb, records):
    fb = bytearray(320 * 200)
    frames = []
    for _, _, payload in records:
        execute_42_1(payload, fb)
        frames.append(bytes(fb))
    return frames
```

---

## Corpus

| Asset | Frames | Logical stream |
|-------|-------:|---------------:|
| `CREDITS.PAN` | 132 | `0x49410` |
| `DEATH.PAN` | 184 | `0x4AAA5` |
| `FIN0A.PAN` | 125 | `0x796F0` |
| `FIN1A.PAN` | 107 | `0x241D1` |
| `FIN2A.PAN` | 64 | `0x19E71` |
| `FIN3A.PAN` | 75 | `0x1BCE2` |
| `FIN4A.PAN` | 140 | `0x2C74E` |
| `FIN5A.PAN` | 70 | `0x27559` |
| `OPENIN6Z.PAN` | 70 | `0x68782` |
| `OPENING2.PAN` | 358 | `0xAACC2` |
| `OPENING3.PAN` | 100 | `0x5145A` |
| `OPENING4.PAN` | 190 | `0x269A9` |
| `OPENING7.PAN` | 167 | `0x377EC` |
| `OPENING8.PAN` | 231 | `0x83412` |
| `OPENING9.PAN` | 55 | `0x21A0C` |

**Total:** 15 assets, 2,068 frame records, 0 boundary mismatches.

---

## Player Architecture

The PAN player lives in overlay segment `0B2E`:

| Address | Role |
|---------|------|
| `0B2E:0150` | Loader: strips extension, appends `.PAN`, routes to decompressor |
| `0B2E:0465` | Entry-table copy into working buffer |
| `0B2E:05CA` | Main scene interpreter — top-level command dispatch |
| `0B2E:0508` | Fade/tick progression path |
| `0B2E:0648` | Branch into `42/1` render family |
| `0B2E:067B` | Far call into blit helper thunk |
| `0B2E:068E` | Continuation address computation |
| `0B2E:0568` | Flat-address/range update block |

Load chain:

```
0B2E:0150 → 0DFC:002A → 0E3A:0052 → 0EC4:2C9E
```

### Palette and fade helpers

| Thunk | Target | Role |
|-------|--------|------|
| `11E3:18A1` | `2036:0047` | Blank display before blit |
| `11E3:1897` | `2036:0000` | Upload palette and cache it |
| `11E3:1879` | `2036:0061` | Restore display after blit |
| `11E3:18AB` | `2036:0126` | Advance one fade step |
| `11E3:1883` | `2050:000E` | Main `42/1` blit worker |
| `11E3:188D` | `2050:002E` | Non-`42/1` record worker |

---

## Runtime Validation (OPENING8.PAN)

Live DOSBox `A000` captures versus static replay SHA1:

| Record | Logical boundary | Result |
|-------:|-----------------|--------|
| 0 | `0x04E96` | `c43ae8cf75ac763dabe08970603729ac2e9b97db` ✓ |
| 5 | `0x0AE6E` | `0fa0318fe15fb73696a903461fb5983529404497` ✓ |
| 60 | `0x277F6` | `28761466278129ee75c8a38ebaf0303442d8f235` ✓ |

Full static replay final framebuffer: `c8640a0b692a40ca7e94841f074c0e7eb25899cc`

Physical pool rebase (records 69–76): constant delta `0x26013` between physical pool offsets
and logical record ends. Pool slice SHA1 matches static: `07e6da286075f4bce05e2d462bfdc6182e93d0c3`.

---

## Open Questions

1. Exact mechanics of the `0318`/`0465` physical pool-window rebase path — does not affect
   static parsing or rendering.
2. Palette fade and DAC carry timing between PAN assets at runtime.
3. Runtime asset ordering for the finale sequence.

---

## Confidence

**High.** Format fully decoded for static parsing and rendering. Corpus-validated across all 15
assets and 2,068 frame records with zero mismatches. Runtime SHA1-verified at multiple frame
boundaries in `OPENING8.PAN`. Documented in [devlog #028](/posts/028-the-pan-format-decoded/).
