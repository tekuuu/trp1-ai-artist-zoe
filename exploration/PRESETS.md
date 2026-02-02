# Preset Catalog

## Music Presets
| Preset | BPM | Mood |
|---|---:|---|
| jazz | 95 | nostalgic |
| blues | 72 | soulful |
| ethiopian-jazz | 85 | mystical |
| cinematic | 100 | epic |
| electronic | 128 | euphoric |
| ambient | 60 | peaceful |
| lofi | 85 | relaxed |
| rnb | 90 | sultry |
| salsa | 180 | fiery |
| bachata | 130 | romantic |
| kizomba | 95 | sensual |

## Video Presets
| Preset | Aspect Ratio |
|---|---|
| nature | 16:9 |
| urban | 21:9 |
| space | 16:9 |
| abstract | 1:1 |
| ocean | 16:9 |
| fantasy | 21:9 |
| portrait | 9:16 |

## Adding a New Preset
1. Add a new `MusicPreset` or `VideoPreset` in the relevant file:
   - [src/ai_content/presets/music.py](src/ai_content/presets/music.py)
   - [src/ai_content/presets/video.py](src/ai_content/presets/video.py)
2. Insert it into the `MUSIC_PRESETS` or `VIDEO_PRESETS` registry dictionary.
3. It will appear automatically in the CLI via `list-presets`.
