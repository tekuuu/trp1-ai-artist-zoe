# Provider Capabilities

## Music Providers
### `lyria` (Google Lyria Realtime)
- **Instrumental only** (no vocals/lyrics)
- **Realtime streaming** generation
- Supports **BPM** and **temperature** controls
- No reference audio

### `minimax` (MiniMax Music 2.0 via AIMLAPI)
- **Vocals/lyrics supported**
- **Reference audio** style transfer supported
- Non‑realtime; async polling
- BPM is ignored by provider

## Video Providers
### `veo` (Google Veo 3.1)
- **Text‑to‑video** and **image‑to‑video** supported (first frame)
- Fast generation (~30s typical)
- Aspect ratios: 16:9, 9:16, 1:1

### `kling` (KlingAI Direct)
- **Text‑to‑video** and **image‑to‑video** supported
- Highest quality, but slow (5–14 min)
- Requires JWT auth with API + secret

## Image Providers
### `imagen` (Google Imagen 4 / Gemini experimental)
- Text‑to‑image generation
- Multiple aspect ratios

## Vocals/Lyrics Support
- **Only MiniMax (`minimax`)** supports vocals/lyrics.
