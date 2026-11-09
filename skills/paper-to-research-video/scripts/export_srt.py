#!/usr/bin/env python3
"""Export one caption cue per scene from a validated film manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def timestamp(seconds: float) -> str:
    total_ms = round(seconds * 1000)
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, milliseconds = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("film_json", type=Path)
    parser.add_argument("output_srt", type=Path)
    args = parser.parse_args()
    data = json.loads(args.film_json.read_text(encoding="utf-8"))
    cursor = 0.0
    cues: list[str] = []
    for index, scene in enumerate(data["scenes"], 1):
        end = cursor + float(scene["seconds"])
        cues.append(f"{index}\n{timestamp(cursor)} --> {timestamp(end)}\n{scene['caption'].strip()}\n")
        cursor = end
    args.output_srt.parent.mkdir(parents=True, exist_ok=True)
    args.output_srt.write_text("\n".join(cues), encoding="utf-8")
    print(f"Wrote {len(cues)} cues to {args.output_srt}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
