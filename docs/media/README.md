# README media

Everything in the README is generated from the repository itself.

| Asset | Source | Rebuild |
| --- | --- | --- |
| `assets/architecture-{light,dark}.svg` | Counts read from `skills/`, `agents/`, schemas, and the control-plane manifests | `python docs/media/build_architecture_svg.py` |
| `assets/media/audit-report.png` | `tests/fixtures/reports/sanitized-report.html`, the golden output of `super_ads_core` report rendering | Screenshot the HTML at 2x |
| `assets/demo/super-ads-demo.{gif,mp4}` | Real `super-ads-core` CLI output on synthetic fixture data | See below |

## Demo video

1. `python docs/media/capture_demo.py . <work-dir> scenes.json` runs the real CLI
   (`--version`, `ingest-export`, `cockpit demo`, `render`, `next`) in a scratch
   directory and records its output. Absolute scratch paths are rewritten to
   `~/super-ads-demo`; long JSON output is truncated with `...`.
2. Substitute `scenes.json` (with a `caption` per scene) for `__SCENES__` in
   `demo-player.template.html`, and place `audit-report.png` beside it as
   `report.png`.
3. `node docs/media/record_demo.js <dir-containing-player.html>` records a
   1280x720 WebM with Playwright.
4. Encode:

```bash
ffmpeg -i demo.webm -c:v libx264 -crf 22 -pix_fmt yuv420p -movflags +faststart -an assets/demo/super-ads-demo.mp4
ffmpeg -i demo.webm -vf "fps=10,scale=960:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=96:stats_mode=diff[p];[b][p]paletteuse=dither=none:diff_mode=rectangle" assets/demo/super-ads-demo.gif
```

No ad account, credential, or client data is used anywhere in these assets.
