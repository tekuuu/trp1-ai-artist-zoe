# CLI Commands Reference

## Main Command
`uv run ai-content [COMMAND] [OPTIONS]`

## Available Commands

### 1. `music`
Generates audio content.
**Options:**
- `--prompt`, `-p`: Description of the music (Required).
- `--provider`: `lyria` (default) or `minimax`.
- `--style`, `-s`: Preset name (e.g., `jazz`, `blues`). Can override prompt.
- `--duration`, `-d`: Duration in seconds (default: 30).
- `--bpm`: Beats per minute (default: 120).
- `--lyrics`, `-l`: Path to lyrics file (MiniMax only).
- `--reference-url`, `-r`: Audio URL for style transfer (MiniMax only).
- `--output`, `-o`: Output file path.
- `--force`, `-f`: Force generation if duplicate exists.

### 2. `video`
Generates video content.
**Options:**
- `--prompt`, `-p`: Scene description (Required).
- `--provider`: `veo` (default) or `kling`.
- `--style`, `-s`: Preset name (e.g., `nature`, `urban`).
- `--aspect`, `-a`: Aspect ratio (default: `16:9`).
- `--duration`, `-d`: Video duration in seconds (default: 5).
- `--image`, `-i`: Path to first frame image (for image-to-video).
- `--output`, `-o`: Output file path.

### 3. `list-providers`
Lists all available music, video, and image providers.

### 4. `list-presets`
Lists all available music and video presets.

### 5. `jobs`
Lists tracked generation jobs.
**Options:**
- `--status`, `-s`: Filter by status (`queued`, `processing`, `completed`, `failed`).
- `--provider`, `-p`: Filter by provider.
- `--limit`, `-l`: Max results (default: 20).

### 6. `jobs-status`
Check status of a specific job (useful for async providers like MiniMax).

### 7. `jobs-sync`
Sync status of pending jobs from the API.
**Options:**
- `--download`, `-d`: Automatically download completed files.
