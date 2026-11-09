# Paper to Research Video

A portable Codex/ChatGPT skills-only plugin. Give the skill an academic paper and available figures, data, or footage; it builds a source-linked, approximately 90-second research film with captions and a checked MP4. It does not include any paper, unpublished experiment, institutional logo, personal credential, or AI-RAN video asset.

The skill is designed for research groups and conference demos. It requires Codex with access to the paper and a local rendering environment; the supplied Remotion starter declares its Node dependencies. A paper alone can yield animated diagrams and figures, but real hardware footage or logs must be supplied or captured. The skill labels reconstructions and prevents the untouched synthetic example from passing its release check.

## Local use

Install the skill into a repository with:

```text
python scripts/install_repo_skill.py <repository-directory>
```

Start a new Codex conversation in that repository and ask: `Use $paper-to-research-video to make a 90-second video from paper.pdf.` In a production folder, copy `skills/paper-to-research-video/assets/remotion-starter/`, replace its synthetic `film.json`, and customize the TSX scenes to the paper. With Node/npm available, run `npm install`, `npm run typecheck`, `npm run studio`, then `npm run render`. Validate the source-linked manifest with `--release` before rendering, export SRT captions, and verify the final video with the skill's Python helpers. A render from the untouched sample is visibly marked as a synthetic fixture and is not a publishable research film.

The project was smoke-tested with a 2700-frame, 1920×1080, 30 fps synthetic composition, a rendered still, and a short H.264 MP4. A full production result from an independent paper has not yet been evaluated.

## Distribution

Build a clean portable ZIP:

```text
python scripts/package_release.py --output paper-to-research-video-0.1.0.zip
```

The ZIP contains root `plugin.json` plus `skills/paper-to-research-video/`. It is ready for local/team installation or draft upload to the OpenAI plugin dashboard. Public listing still requires the publisher's account/identity, review, and a final publish step; no publication happens during packaging. See the [official plugin package guide](https://developers.openai.com/plugins/build/plugins) and [upload flow](https://developers.openai.com/plugins/deploy/submission).

This package is source code and workflow instructions. A paper's video is generated locally in a separate working folder. Tool dependencies for that working folder are listed in the starter's `package.json`; they are not bundled into the plugin ZIP.
