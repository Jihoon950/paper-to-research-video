#!/usr/bin/env python3
"""Check duration, video format, and full decode of a delivered MP4."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--target-seconds", type=float, default=90.0)
    parser.add_argument("--tolerance-seconds", type=float, default=1.0)
    args = parser.parse_args()
    if not args.video.is_file():
        print(f"ERROR: missing video: {args.video}", file=sys.stderr)
        return 1
    ffprobe = shutil.which("ffprobe")
    ffmpeg = shutil.which("ffmpeg")
    if not ffprobe or not ffmpeg:
        print("ERROR: ffprobe and ffmpeg must be on PATH for verification", file=sys.stderr)
        return 2
    probe = subprocess.run(
        [ffprobe, "-v", "error", "-show_entries", "format=duration:stream=codec_type,codec_name,width,height,avg_frame_rate",
         "-of", "json", str(args.video)],
        capture_output=True, text=True, check=False,
    )
    if probe.returncode:
        print(f"ERROR: ffprobe failed: {probe.stderr.strip()}", file=sys.stderr)
        return 1
    data = json.loads(probe.stdout)
    duration = float(data.get("format", {}).get("duration", 0))
    streams = data.get("streams", [])
    video = next((stream for stream in streams if stream.get("codec_type") == "video"), None)
    problems: list[str] = []
    if not video:
        problems.append("no video stream")
    else:
        if video.get("codec_name") != "h264":
            problems.append(f"expected H.264, got {video.get('codec_name')}")
        if video.get("width") != 1920 or video.get("height") != 1080:
            problems.append(f"expected 1920x1080, got {video.get('width')}x{video.get('height')}")
    if abs(duration - args.target_seconds) > args.tolerance_seconds:
        problems.append(f"duration {duration:.3f}s outside {args.target_seconds:.3f}±{args.tolerance_seconds:.3f}s")
    decode = subprocess.run([ffmpeg, "-v", "error", "-xerror", "-i", str(args.video), "-f", "null", "-"], capture_output=True, text=True, check=False)
    if decode.returncode:
        problems.append(f"full decode failed: {decode.stderr.strip()[-500:]}")
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print(f"VALID: {args.video} | {duration:.3f}s | {video['width']}x{video['height']} | {video['codec_name']} | full decode OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
