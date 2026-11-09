---
name: paper-to-research-video
description: Produce a polished 80–100 second research video from an academic paper or preprint, with paper-backed claims, custom animated scenes, captions, and a verified MP4. Use for paper-to-video or research-demo-film requests; not for merely summarizing a paper or editing an unrelated video.
---

# Paper to Research Video

Create a film that lets a new viewer understand **the problem, what was built or proposed, what was tested, and what the evidence actually shows** in about 90 seconds. Treat the supplied paper as the evidence source, not as a slide deck to pan across.

## Start with the source

1. Read the complete paper, including figure captions, methods, units, baselines, limitations, and supplement when supplied. For a URL or DOI, fetch the referenced paper. For a local PDF, extract text and inspect the actual figure pages; OCR scanned pages when needed. Do not infer results from the abstract alone.
2. Make a compact claim ledger: each on-screen quantitative or causal claim needs the exact source location (page, figure, table, or supplementary item), metric definition, comparison condition, and any qualification. Separate reported measurements, authors' interpretation, and your own explanatory illustration. If a key result is ambiguous, inspect the source again and narrow the claim.
3. Inventory source figures, tables, video, photos, logos, screen recordings, and rights. Prefer the paper's own figures/data or original generated diagrams. If a requested real-system demonstration has no recording, build an explicitly labeled illustration; do not portray it as observed footage. Do not upload private or unpublished source material to an external service without authorization.

## Direct the film

Write a scene-by-scene shot list with timecode, one message per shot, the visual action, what moves where, transition, caption/narration, source claim IDs, and media provenance. Use the narrative shape that fits the paper; a common route is **stakes → system or idea → controlled comparison → mechanism → outcome and boundary**. Put the paper title, authors, and institution at the opening when known. Show the tested system before showing its failure or benefit when that context is needed.

Target 90 seconds by default (80–100 is acceptable); adjust when the user specifies a different duration. Use screen time for experimental setup and denominators, not only the largest number. If a comparison is conditional, identify the state on each side and the baseline; do not turn separate fixed-condition measurements into evidence of a measured online controller. Give the closing frame a precise takeaway and limitation.

Plan the visual language from the science. Animate diagrams, measured plots, traces, and authorized recorded footage in different ways so the audience can tell them apart. Real video or terminal output must retain provenance; replay, illustrative mechanisms, and simulated dashboards must be visibly marked. No invented metric, token stream, utilization trace, failure log, or unmeasured transition. For detailed narrative and labeling guidance, read [editorial-guidance.md](references/editorial-guidance.md).

## Produce and verify

Create a working production folder next to the paper or in the user's chosen location. Save the claim ledger and shot list there, then implement the film with a suitable code-native timeline tool (Remotion and FFmpeg where available; choose another tool if it fits the environment better). The bundled [Remotion starter](assets/remotion-starter/) is a runnable scaffold, not a visual style to leave untouched: replace its sample text and build paper-specific shots and transitions. Its [film manifest](references/film-manifest.md) and `scripts/validate_film.py` provide a reusable evidence/timecode check. Do not copy the starter's synthetic fixture claims into the user's film.

Render a few representative stills early to inspect hierarchy, labels, image rights, and contrast at the target viewing size. Then render the full video, inspect opening/middle/closing and transitions, and fix clipped text, tiny plots, unreadable legends, or abrupt story jumps. Deliver an MP4, source project, claim-to-source ledger, shot list, and captions/subtitle file (or on-screen captions if requested). Default to 1920×1080, 30 fps, H.264, and no audio when the user has not chosen audio; add narration/music only when requested or context clearly calls for it. Respect the user's language.

Run `<skill-dir>/scripts/validate_film.py path/to/film.json --release` when using the starter manifest, and `<skill-dir>/scripts/export_srt.py path/to/film.json path/to/captions.srt` for scene-level subtitles. Then run `<skill-dir>/scripts/verify_video.py path/to/final.mp4 --target-seconds 90` when `ffprobe` and `ffmpeg` are available. These checks do not replace visual and scientific review. State what was measured, what was reconstructed or illustrated, and what footage was unavailable. Do not call a render finished if its duration, decode, captions, or core scientific claims have not been checked.
