#!/usr/bin/env python3
"""Download stock videos/photos from Pexels.

This is useful as a fallback source asset when AI video providers are blocked
(e.g., quota/billing). It does NOT generate AI video; it fetches licensed
stock media via the Pexels API.

Auth:
  - Set `PIXEL_API_KEY` (kept for compatibility with this repo's .env)
  - Or set `PEXELS_API_KEY`

Examples:
  uv run python scripts/pexels_download.py video --query "nature" --output output/video/pexels_nature.mp4
  uv run python scripts/pexels_download.py photo --query "sunset mountains" --output output/images/pexels_sunset.jpg
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx


PEXELS_BASE = "https://api.pexels.com"


@dataclass(frozen=True)
class DownloadResult:
    media_path: Path
    metadata_path: Path
    attribution: str


def _get_api_key() -> str:
    api_key = os.getenv("PIXEL_API_KEY") or os.getenv("PEXELS_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing API key. Set PIXEL_API_KEY (or PEXELS_API_KEY) in your environment/.env."
        )
    return api_key


def _headers() -> dict[str, str]:
    return {"Authorization": _get_api_key()}


def _pick_best_video_file(video_files: list[dict[str, Any]]) -> dict[str, Any] | None:
    mp4s = [vf for vf in video_files if (vf.get("file_type") or "").lower() == "video/mp4"]
    if not mp4s:
        mp4s = video_files
    if not mp4s:
        return None

    def score(vf: dict[str, Any]) -> tuple[int, int]:
        return (int(vf.get("width") or 0), int(vf.get("height") or 0))

    return sorted(mp4s, key=score, reverse=True)[0]


def _safe_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True), encoding="utf-8")


def _download_to(url: str, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=120.0, follow_redirects=True) as client:
        with client.stream("GET", url) as resp:
            resp.raise_for_status()
            with output_path.open("wb") as f:
                for chunk in resp.iter_bytes():
                    f.write(chunk)


def download_video(
    *,
    query: str,
    output: Path,
    per_page: int,
    page: int,
    index: int,
    min_duration: int | None,
    max_duration: int | None,
) -> DownloadResult:
    url = f"{PEXELS_BASE}/videos/search"
    params = {"query": query, "per_page": per_page, "page": page}

    with httpx.Client(timeout=30.0, headers=_headers(), follow_redirects=True) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()

    videos: list[dict[str, Any]] = payload.get("videos") or []
    if not videos:
        raise SystemExit(f"No videos found for query: {query!r}")

    filtered = []
    for v in videos:
        duration = v.get("duration")
        if isinstance(duration, int):
            if min_duration is not None and duration < min_duration:
                continue
            if max_duration is not None and duration > max_duration:
                continue
        filtered.append(v)

    candidates = filtered if (min_duration is not None or max_duration is not None) else videos
    if not candidates:
        raise SystemExit(
            "No videos matched duration filters. "
            f"Try widening range; got min_duration={min_duration}, max_duration={max_duration}."
        )

    if index < 0 or index >= len(candidates):
        raise SystemExit(
            f"Index out of range. Got {index}, available 0..{len(candidates)-1} after filtering."
        )

    video = candidates[index]
    best = _pick_best_video_file(video.get("video_files") or [])
    if not best or not best.get("link"):
        raise SystemExit("No downloadable video file found in Pexels response.")

    download_url = best["link"]

    # If user passed a directory, create a default name.
    if output.is_dir() or str(output).endswith("/"):
        output = output / f"pexels_video_{video.get('id','unknown')}.mp4"

    if output.suffix.lower() not in {".mp4", ".mov", ".m4v"}:
        # Default to mp4 for the chosen link
        output = output.with_suffix(".mp4")

    _download_to(download_url, output)

    attribution = (
        f"Pexels video id={video.get('id')} | url={video.get('url')} | "
        f"user={((video.get('user') or {}).get('name'))}"
    )

    metadata = {
        "source": "pexels",
        "type": "video",
        "query": query,
        "page": page,
        "index": index,
        "selected_file": {
            "link": best.get("link"),
            "file_type": best.get("file_type"),
            "width": best.get("width"),
            "height": best.get("height"),
            "fps": best.get("fps"),
            "quality": best.get("quality"),
        },
        "video": {
            "id": video.get("id"),
            "url": video.get("url"),
            "duration": video.get("duration"),
            "width": video.get("width"),
            "height": video.get("height"),
            "user": video.get("user"),
        },
    }

    metadata_path = output.with_suffix(output.suffix + ".json")
    _safe_write_json(metadata_path, metadata)

    return DownloadResult(media_path=output, metadata_path=metadata_path, attribution=attribution)


def download_photo(*, query: str, output: Path, per_page: int, page: int, index: int, size: str) -> DownloadResult:
    url = f"{PEXELS_BASE}/v1/search"
    params = {"query": query, "per_page": per_page, "page": page}

    with httpx.Client(timeout=30.0, headers=_headers(), follow_redirects=True) as client:
        resp = client.get(url, params=params)
        resp.raise_for_status()
        payload = resp.json()

    photos: list[dict[str, Any]] = payload.get("photos") or []
    if not photos:
        raise SystemExit(f"No photos found for query: {query!r}")

    if index < 0 or index >= len(photos):
        raise SystemExit(f"Index out of range. Got {index}, available 0..{len(photos)-1}.")

    photo = photos[index]
    src = photo.get("src") or {}

    # Pexels sizes include: original, large2x, large, medium, small, portrait, landscape, tiny
    download_url = src.get(size) or src.get("large") or src.get("original")
    if not download_url:
        raise SystemExit("No downloadable photo URL found in Pexels response.")

    if output.is_dir() or str(output).endswith("/"):
        output = output / f"pexels_photo_{photo.get('id','unknown')}.jpg"

    if output.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
        output = output.with_suffix(".jpg")

    _download_to(download_url, output)

    attribution = f"Pexels photo id={photo.get('id')} | url={photo.get('url')} | photographer={photo.get('photographer')}"

    metadata = {
        "source": "pexels",
        "type": "photo",
        "query": query,
        "page": page,
        "index": index,
        "size": size,
        "photo": {
            "id": photo.get("id"),
            "url": photo.get("url"),
            "width": photo.get("width"),
            "height": photo.get("height"),
            "photographer": photo.get("photographer"),
            "photographer_url": photo.get("photographer_url"),
            "src": src,
        },
    }

    metadata_path = output.with_suffix(output.suffix + ".json")
    _safe_write_json(metadata_path, metadata)

    return DownloadResult(media_path=output, metadata_path=metadata_path, attribution=attribution)


def main() -> int:
    parser = argparse.ArgumentParser(description="Download stock media from Pexels.")
    sub = parser.add_subparsers(dest="kind", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--query", required=True, help="Search query, e.g. 'nature forest'")
    common.add_argument(
        "--output",
        required=True,
        type=Path,
        help="Output file path (or directory).",
    )
    common.add_argument("--per-page", type=int, default=10, help="Results per page (max varies)")
    common.add_argument("--page", type=int, default=1, help="Page number")
    common.add_argument(
        "--index",
        type=int,
        default=0,
        help="Which item in the returned page to download (0-based)",
    )

    p_video = sub.add_parser("video", parents=[common], help="Download a Pexels video")
    p_video.add_argument(
        "--min-duration",
        type=int,
        default=None,
        help="Minimum video duration (seconds) to filter results",
    )
    p_video.add_argument(
        "--max-duration",
        type=int,
        default=None,
        help="Maximum video duration (seconds) to filter results",
    )

    p_photo = sub.add_parser("photo", parents=[common], help="Download a Pexels photo")
    p_photo.add_argument(
        "--size",
        default="large2x",
        help="Photo size key: original|large2x|large|medium|small|portrait|landscape|tiny",
    )

    args = parser.parse_args()

    try:
        if args.kind == "video":
            result = download_video(
                query=args.query,
                output=args.output,
                per_page=args.per_page,
                page=args.page,
                index=args.index,
                min_duration=args.min_duration,
                max_duration=args.max_duration,
            )
        else:
            result = download_photo(
                query=args.query,
                output=args.output,
                per_page=args.per_page,
                page=args.page,
                index=args.index,
                size=args.size,
            )

        print("✅ Downloaded")
        print(f"   Media: {result.media_path}")
        print(f"   Meta:  {result.metadata_path}")
        print(f"   Info:  {result.attribution}")
        return 0

    except httpx.HTTPStatusError as e:
        body = ""
        try:
            body = e.response.text
        except Exception:
            body = ""
        raise SystemExit(f"Pexels API error: HTTP {e.response.status_code}\n{body}")


if __name__ == "__main__":
    raise SystemExit(main())
