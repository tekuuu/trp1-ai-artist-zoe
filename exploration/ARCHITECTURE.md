# Codebase Architecture Overview

## Package Structure (src/ai_content/)
- **core/**: Protocols, registry, result objects, exceptions, job tracking.
- **config/**: Pydantic settings and YAML loader.
- **providers/**: Concrete provider integrations (Google, AIMLAPI, KlingAI) registered via decorators.
- **presets/**: Style presets for music and video.
- **pipelines/**: Orchestrated workflows that chain providers and combine outputs.
- **integrations/**: External services (archive, media merge, YouTube).
- **utils/**: Shared utilities (lyrics parsing, file handling, retries).
- **cli/**: Typer CLI entrypoint.

## Provider Organization
Providers are grouped by vendor:
- **google/**: Lyria (music), Veo (video), Imagen (image)
- **aimlapi/**: MiniMax music provider + HTTP client
- **kling/**: KlingAI direct video provider

Each provider class registers itself using `@ProviderRegistry.register_music|video|image("name")`, enabling dynamic lookup by name.

## Pipelines Purpose
The `pipelines/` directory provides higher‑level orchestration beyond single provider calls:
- **MusicPipeline**: performance‑first, lyrics‑first, reference‑based, and provider comparisons.
- **VideoPipeline**: text‑to‑video and image‑to‑video flows.
- **FullContentPipeline**: end‑to‑end music → image → video → merge with optional upload.

Pipelines aggregate `GenerationResult` objects into `PipelineResult` with unified error handling and output tracking.
