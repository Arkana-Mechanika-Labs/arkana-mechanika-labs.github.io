---
title: "Devlog #020 - The Sound of 1992"
date: 2026-04-15
summary: "The .DGT audio format decoded: headerless unsigned 8-bit PCM, mono, 8000 Hz. One ffmpeg command away from a playable WAV. The opening sequence has audio again."
---

## An Unidentified File

Every Darklands session opens the same way: a `.PAN` image sequence, a slow pan across a medieval battlefield. It has always been clear that something was supposed to go with it. `OPENDARK.DGT` sits next to `OPENDARK.PAN` in the game directory, and the name is not subtle. *DGT.* Digital.

Until now, nobody had formally documented what was in it.

## The Format

`.DGT` turns out to be the simplest possible digital audio format: a raw byte stream, no header, no metadata, no compression. Every byte is one audio sample. Unsigned 8-bit PCM, mono. Silence sits at 128; the signal swings above and below from there.

```
Offset    Size    Description
0x0000    N       Raw PCM samples: one byte each, unsigned, silence ≈ 128
```

That is the entire format specification. There is nothing else in the file.

## Finding the Sample Rate

Because there is no header, the sample rate has to come from somewhere else: either the engine hardcodes it, or it reads it from a config structure not in the file itself. The engine side has not been traced yet, so the rate was determined experimentally: convert the raw bytes to WAV at several candidate rates and compare.

At **8000 Hz**, `OPENDARK.DGT` plays back as recognisable, natural-sounding audio. At 11025 Hz, the same audio is noticeably faster and higher-pitched, plausible for a slightly different hardware configuration, but not the best match. 8000 Hz is consistent with one of the standard Sound Blaster DSP playback rates for the era.

The confirmed working conversion:

```bash
ffmpeg -f u8 -ar 8000 -ac 1 -i OPENDARK.DGT OPENDARK.wav
```

Or in Python:

```python
import numpy as np, wave

data = np.fromfile("OPENDARK.DGT", dtype=np.uint8)
with wave.open("OPENDARK.wav", "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(1)
    f.setframerate(8000)
    f.writeframes(data.tobytes())
```

## Where It Fits in the Engine

The presentation system pairs `.DGT` with `.PAN` files. The engine loads both, then plays them in sync through a presentation loop, with audio streaming alongside image sequence rendering. The likely hardware path is Sound Blaster DAC output via DMA-based buffer feeding, driven by a timer, which was the standard playback mechanism for raw PCM in 1992 DOS games.

For the rewrite, the format itself requires no parsing at all:

```csharp
byte[] raw = File.ReadAllBytes("OPENDARK.DGT");
float[] samples = new float[raw.Length];
for (int i = 0; i < raw.Length; i++)
    samples[i] = (raw[i] - 128) / 128f;
```

The complexity is entirely in the engine layer: sample rate selection, hardware abstraction, buffer timing. The format is trivial. This is actually good news: it means the audio data will survive a rewrite intact, and the only work is reimplementing the playback driver.

## What Remains Open

Three questions about the engine side are still open:

1. **What exact sample rate does the engine use?** 8000 Hz is the best experimental match, but confirming it requires tracing the sound subsystem in `DARKLAND.EXE`.
2. **Is the rate fixed globally or per file?** If fixed, one constant needs to be found. If per-file, there must be a lookup table or config structure somewhere.
3. **How is playback implemented?** Blocking read? DMA streaming? Interrupt-driven? The audio driver layer is a forthcoming RE target.

The format documentation is now live in the [File Formats](/formats/audio/dgt-files/) section of this site.
