# Starter film manifest

The Remotion starter reads `film.json` from its project root. This is a *production scaffold*, not a substitute for a paper-specific script. `scripts/validate_film.py` checks structure, time, references, and local assets before rendering. The sample is synthetic and explicitly marked as such.

Top-level fields:

| Field | Meaning |
| --- | --- |
| `paper` | `title`, `authors`, `institution`, `source` (path/DOI/URL) |
| `settings` | `fps`, `width`, `height`, `target_seconds`, `language` |
| `claims` | `id`, `text`, `status` (`reported`, `interpreted`, `illustrative`), nonempty `evidence` for reported/interpreted claims |
| `assets` | `id`, relative `path`, `kind` (`recorded`, `archive`, `paper-figure`, `simulation`, `illustration`), `credit`, `rights` |
| `scenes` | Ordered `id`, `seconds`, `kind`, `eyebrow`, `headline`, `body`, `caption`, `claim_ids`, `asset_ids`, `visual` |

Each evidence item in `claims[].evidence` has `source` and `location` such as `paper.pdf` and `Fig. 3b, p. 7`. Reported or interpreted claims need at least one. Treat the paper URL/DOI as a pointer, not enough by itself to verify an individual number.

Scene `kind` is `title`, `system`, `problem`, `method`, `comparison`, `result`, `mechanism`, `bridge`, or `closing`. `visual` may contain `left_label`, `right_label`, `left_value`, `right_value`, `left_note`, `right_note`, or `accent` for the starter's generic panels. Extend these for the actual paper rather than force the paper into the starter panel layout.

Use `claim_ids` to associate a scene with its evidence; comparison/result/mechanism scenes require at least one. Claims can be repeated in multiple scenes. `asset_ids` refer to the local file inventory; all files must exist and remain inside the project folder. Record media rights in the manifest. Set scene durations so their sum equals `target_seconds` within one frame. Keep all durations positive and align to the chosen FPS when exact frame timings matter.

The validator cannot prove whether the paper supports a claim or whether a license permits publication. The film maker must compare the final visual and wording with the actual source.
