#!/usr/bin/env python3
"""Validate a paper-film manifest before rendering (standard library only)."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
import sys


SCENE_KINDS = {
    "title", "system", "problem", "method", "comparison", "result",
    "mechanism", "bridge", "closing",
}
CLAIM_STATUSES = {"reported", "interpreted", "illustrative"}
ASSET_KINDS = {"recorded", "archive", "paper-figure", "simulation", "illustration"}
EVIDENCE_SCENES = {"comparison", "result", "mechanism"}


def nonblank(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate(path: Path, release: bool = False) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return [f"Cannot read JSON: {exc}"]
    if not isinstance(data, dict):
        return ["Root must be a JSON object"]

    paper = data.get("paper")
    if not isinstance(paper, dict):
        errors.append("paper must be an object")
        paper = {}
    for key in ("title", "authors", "source"):
        if not nonblank(paper.get(key)):
            errors.append(f"paper.{key} must be nonempty")

    settings = data.get("settings")
    if not isinstance(settings, dict):
        errors.append("settings must be an object")
        settings = {}
    for key in ("fps", "width", "height"):
        value = settings.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            errors.append(f"settings.{key} must be a positive integer")
    target = settings.get("target_seconds")
    if not isinstance(target, (int, float)) or isinstance(target, bool) or not math.isfinite(target) or target <= 0:
        errors.append("settings.target_seconds must be a positive number")
    if not nonblank(settings.get("language")):
        errors.append("settings.language must be nonempty")
    if release and settings.get("fixture") is True:
        errors.append("Release check rejects the synthetic fixture")

    claims = data.get("claims")
    if not isinstance(claims, list):
        errors.append("claims must be an array")
        claims = []
    claim_ids: set[str] = set()
    claim_statuses: dict[str, str] = {}
    for index, claim in enumerate(claims):
        label = f"claims[{index}]"
        if not isinstance(claim, dict):
            errors.append(f"{label} must be an object")
            continue
        ident = claim.get("id")
        if not nonblank(ident):
            errors.append(f"{label}.id must be nonempty")
        elif ident in claim_ids:
            errors.append(f"Duplicate claim id: {ident}")
        else:
            claim_ids.add(ident)
        if not nonblank(claim.get("text")):
            errors.append(f"{label}.text must be nonempty")
        if release and nonblank(claim.get("text")) and "example" in claim["text"].lower():
            errors.append(f"{label}.text still contains example wording")
        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            errors.append(f"{label}.status must be one of {sorted(CLAIM_STATUSES)}")
        elif nonblank(ident):
            claim_statuses[ident] = status
        evidence = claim.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{label}.evidence must be an array")
            evidence = []
        if status in {"reported", "interpreted"} and not evidence:
            errors.append(f"{label} needs source evidence")
        for eindex, item in enumerate(evidence):
            if not isinstance(item, dict) or not all(nonblank(item.get(key)) for key in ("source", "location")):
                errors.append(f"{label}.evidence[{eindex}] needs source and location")

    assets = data.get("assets")
    if not isinstance(assets, list):
        errors.append("assets must be an array")
        assets = []
    asset_ids: set[str] = set()
    root = path.parent.resolve()
    for index, asset in enumerate(assets):
        label = f"assets[{index}]"
        if not isinstance(asset, dict):
            errors.append(f"{label} must be an object")
            continue
        ident = asset.get("id")
        if not nonblank(ident):
            errors.append(f"{label}.id must be nonempty")
        elif ident in asset_ids:
            errors.append(f"Duplicate asset id: {ident}")
        else:
            asset_ids.add(ident)
        if asset.get("kind") not in ASSET_KINDS:
            errors.append(f"{label}.kind must be one of {sorted(ASSET_KINDS)}")
        for key in ("credit", "rights", "path"):
            if not nonblank(asset.get(key)):
                errors.append(f"{label}.{key} must be nonempty")
        relative = asset.get("path")
        if nonblank(relative):
            candidate = (root / relative).resolve()
            if not candidate.is_relative_to(root):
                errors.append(f"{label}.path escapes project root")
            elif not candidate.is_file():
                errors.append(f"{label}.path does not exist: {relative}")

    scenes = data.get("scenes")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a nonempty array")
        scenes = []
    scene_ids: set[str] = set()
    total_seconds = 0.0
    for index, scene in enumerate(scenes):
        label = f"scenes[{index}]"
        if not isinstance(scene, dict):
            errors.append(f"{label} must be an object")
            continue
        ident = scene.get("id")
        if not nonblank(ident):
            errors.append(f"{label}.id must be nonempty")
        elif ident in scene_ids:
            errors.append(f"Duplicate scene id: {ident}")
        else:
            scene_ids.add(ident)
        seconds = scene.get("seconds")
        if not isinstance(seconds, (int, float)) or isinstance(seconds, bool) or not math.isfinite(seconds) or seconds <= 0:
            errors.append(f"{label}.seconds must be a positive number")
        else:
            total_seconds += seconds
        kind = scene.get("kind")
        if not isinstance(kind, str) or kind not in SCENE_KINDS:
            errors.append(f"{label}.kind must be one of {sorted(SCENE_KINDS)}")
        for key in ("headline", "caption"):
            if not nonblank(scene.get(key)):
                errors.append(f"{label}.{key} must be nonempty")
        if release and any(token in str(scene.get(key, "")).lower() for key in ("headline", "body", "caption") for token in ("synthetic fixture", "replace with", "example comparison", "paper-backed value")):
            errors.append(f"{label} still contains starter placeholder wording")
        for key, valid_ids in (("claim_ids", claim_ids), ("asset_ids", asset_ids)):
            ids = scene.get(key)
            if not isinstance(ids, list):
                errors.append(f"{label}.{key} must be an array")
                continue
            for item in ids:
                if not isinstance(item, str) or item not in valid_ids:
                    errors.append(f"{label}.{key} references unknown ID: {item}")
        if kind in EVIDENCE_SCENES and not scene.get("claim_ids"):
            errors.append(f"{label} ({kind}) needs at least one claim_id")
        scene_claim_ids = scene.get("claim_ids") if isinstance(scene.get("claim_ids"), list) else []
        if release and kind in {"comparison", "result"} and not any(isinstance(ident, str) and claim_statuses.get(ident) in {"reported", "interpreted"} for ident in scene_claim_ids):
            errors.append(f"{label} ({kind}) needs a paper-backed claim for release")
        if "visual" in scene and not isinstance(scene["visual"], dict):
            errors.append(f"{label}.visual must be an object")

    if isinstance(target, (int, float)) and math.isfinite(target) and isinstance(settings.get("fps"), int) and settings["fps"] > 0:
        if abs(total_seconds - target) > 1 / settings["fps"]:
            errors.append(f"Scene durations sum to {total_seconds:.3f}s; target is {target:.3f}s")
    if release and not any(status in {"reported", "interpreted"} for status in claim_statuses.values()):
        errors.append("Release check needs at least one paper-backed claim")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("film_json", type=Path)
    parser.add_argument("--release", action="store_true", help="Reject synthetic fixture and obvious placeholder wording")
    args = parser.parse_args()
    problems = validate(args.film_json, release=args.release)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}", file=sys.stderr)
        return 1
    print(f"VALID: {args.film_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
