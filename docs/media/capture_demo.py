"""Run the real Super Ads CLI and capture outputs for the README demo."""
import json, shutil, subprocess, sys
from pathlib import Path
repo = Path(sys.argv[1]); work = Path(sys.argv[2]); out = Path(sys.argv[3])
if work.exists() and any(work.iterdir()):
    sys.exit(f"refusing to use non-empty work directory: {work}")
work.mkdir(parents=True, exist_ok=True)
(work / "exports").mkdir(); shutil.copy(repo / "tests/fixtures/exports/google.csv", work / "exports/google.csv")
env = {"PYTHONPATH": str(repo), "PATH": "/usr/bin:/bin:/usr/local/bin"}
def run(display, argv, shell_filter=None, max_lines=None):
    cmd = [sys.executable, "-m", "super_ads_core", *argv]
    text = subprocess.run(cmd, cwd=work, env=env, capture_output=True, text=True).stdout
    lines = text.rstrip("\n").splitlines()
    if shell_filter: lines = [l for l in lines if shell_filter in l]
    if max_lines and len(lines) > max_lines: lines = lines[:max_lines] + ["  ..."]
    return {"cmd": display, "out": lines}
scenes = [
  run("super-ads-core --version", ["--version"]),
  run("super-ads-core ingest-export --platform google exports/google.csv", ["ingest-export", "--platform", "google", "exports/google.csv"], max_lines=17),
  run("super-ads-core cockpit demo --runs-root runs | grep title", ["cockpit", "demo", "--runs-root", "runs"], shell_filter='"title"'),
  run("super-ads-core render runs/demo-showcase/report.json --format html --root reports --policy-root runs/_policy", ["render", "runs/demo-showcase/report.json", "--format", "html", "--root", "reports", "--policy-root", "runs/_policy"]),
  run("super-ads-core next --as-of 2026-10-16", ["next", "--as-of", "2026-10-16"], max_lines=9),
]
for s in scenes:
    s["out"] = [l.replace(str(work), "~/super-ads-demo") for l in s["out"]]
out.write_text(json.dumps(scenes, indent=1))
print(json.dumps(scenes, indent=1)[:3000])
