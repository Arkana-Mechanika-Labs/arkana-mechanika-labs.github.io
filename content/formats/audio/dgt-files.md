---
title: Raw Audio (*.DGT)
weight: 1
---

`.DGT` files are the raw digital audio assets used in Darklands, most visibly in the intro sequence where they accompany `.PAN` visual assets. The format is about as minimal as digital audio gets: no header, no metadata, just a stream of unsigned 8-bit PCM samples.

*Source: experimental validation via waveform and spectrogram analysis of `OPENDARK.DGT`.*

---

## Format Specification

| Property | Value |
|----------|-------|
| Extension | `.DGT` |
| Encoding | Raw unsigned 8-bit PCM |
| Channels | Mono |
| Header | None |
| Compression | None |
| Sample range | 0–255 (silence ≈ 128) |

### Binary Layout

```
Offset    Size    Description
0x0000    N       Raw PCM sample data (one byte per sample)
```

The entire file is sample data. There are no leading or trailing structures.

---

## Playback Parameters

Because the format carries no metadata, all playback parameters are supplied externally by the engine.

| Parameter | Confirmed value |
|-----------|----------------|
| Sample rate | **8000 Hz** (best match for `OPENDARK.DGT`) |
| Channels | 1 (mono) |
| Bit depth | 8-bit unsigned |

**Notes:**
- 11025 Hz is plausible but produces slightly accelerated, higher-pitched audio.
- The exact sample rate is likely hardcoded or stored in the engine's sound system configuration — determining this requires tracing the sound driver in `DARKLAND.EXE`.

---

## Conversion

### ffmpeg

```bash
ffmpeg -f u8 -ar 8000 -ac 1 -i OPENDARK.DGT OPENDARK.wav
```

### Python

```python
import numpy as np
import wave

data = np.fromfile("OPENDARK.DGT", dtype=np.uint8)

with wave.open("OPENDARK.wav", "wb") as f:
    f.setnchannels(1)
    f.setsampwidth(1)   # 8-bit = 1 byte per sample
    f.setframerate(8000)
    f.writeframes(data.tobytes())
```

---

## Engine Integration

`.DGT` files are part of the **presentation system**, paired with `.PAN` image sequences in the intro and likely other cutscene-style sequences:

```
Load .PAN  → visual frame sequence
Load .DGT  → audio stream
Play both in sync via presentation loop
```

The engine almost certainly:
1. Loads the `.DGT` file into a memory buffer
2. Configures the audio device (sample rate, output channel)
3. Streams the raw buffer to the sound hardware

Given the era, the likely hardware path is **Sound Blaster DAC output** via DMA-based streaming or timer-driven buffer feeding (port `0x22C`). This is consistent with the 8000 Hz sample rate, which is a typical Sound Blaster DSP rate.

---

## Reimplementation

Decoding is trivial — no parsing required:

```csharp
byte[] raw = File.ReadAllBytes("OPENDARK.DGT");

// Convert to normalised float samples for a modern audio API
float[] samples = new float[raw.Length];
for (int i = 0; i < raw.Length; i++)
    samples[i] = (raw[i] - 128) / 128f;
```

All complexity is in the engine's playback layer (sample rate selection, hardware abstraction), not in the format itself.

---

## Known Files

| File | Usage |
|------|-------|
| `OPENDARK.DGT` | Audio for the opening / intro sequence |

---

## Open Questions

- What is the exact sample rate used by the engine — 8000 Hz, 11025 Hz, or something else?
- Is the sample rate fixed globally or configurable per-file?
- Is playback blocking, interrupt-driven, or DMA-streamed?

Answering these requires tracing the sound subsystem in `DARKLAND.EXE`. The audio driver layer is a key upcoming RE target.

---

## Status

| Item | State |
|------|-------|
| Format identified | ✅ |
| Playback confirmed (8000 Hz WAV) | ✅ |
| Engine playback routine traced | ⏳ |
