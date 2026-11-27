"""Generate assets/architecture-{light,dark}.svg for the README.

Counts are read from the repository so the diagram never drifts:
    python docs/media/build_architecture_svg.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

THEMES = {
    "light": dict(bg="#ffffff", panel="#f8fafc", stroke="#e2e8f0", text="#0f172a", sub="#475569",
                  muted="#94a3b8", line="#94a3b8", chip="#ffffff"),
    "dark": dict(bg="#0b1020", panel="#111827", stroke="#1f2937", text="#f1f5f9", sub="#cbd5e1",
                 muted="#64748b", line="#475569", chip="#0f172a"),
}
ACCENTS = {"host": "#0ea5e9", "conductor": "#8b5cf6", "skills": "#ec4899", "agents": "#f59e0b",
           "core": "#10b981", "control": "#6366f1", "out": "#14b8a6", "gate": "#ef4444"}


def counts() -> dict[str, int]:
    registry = json.loads((ROOT / "control-plane/manifests/control-registry.json").read_text())
    sources = json.loads((ROOT / "control-plane/manifests/source-ledger.json").read_text())
    agents = sorted(p.stem for p in (ROOT / "agents").glob("*.md"))
    return {
        "skills": sum(1 for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").is_file()),
        "agents": len(agents),
        "audit_agents": sum(1 for a in agents if a.startswith("audit-")),
        "references": len(list((ROOT / "ads/references").glob("*.md"))),
        "schemas": len(list((ROOT / "super_ads_core/schemas/v1").glob("*.json"))),
        "controls": len(registry["controls"]),
        "sources": len(sources["sources"]),
    }


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def box(x, y, w, h, t, accent, title, lines, chips=()):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{t["panel"]}" stroke="{t["stroke"]}"/>',
           f'<rect x="{x}" y="{y}" width="6" height="{h}" rx="3" fill="{accent}"/>',
           f'<text x="{x + 22}" y="{y + 30}" font-size="17" font-weight="700" fill="{t["text"]}">{esc(title)}</text>']
    for i, line in enumerate(lines):
        out.append(f'<text x="{x + 22}" y="{y + 54 + i * 20}" font-size="13" fill="{t["sub"]}">{esc(line)}</text>')
    cx, cy = x + 22, y + h - 34
    for chip in chips:
        cw = 14 + len(chip) * 7.1
        if cx + cw > x + w - 12:
            break
        out.append(f'<rect x="{cx}" y="{cy}" width="{cw:.0f}" height="22" rx="11" fill="{t["chip"]}" stroke="{accent}" stroke-opacity=".55"/>')
        out.append(f'<text x="{cx + 7}" y="{cy + 15}" font-size="11.5" fill="{t["sub"]}" font-family="ui-monospace,SFMono-Regular,Menlo,monospace">{esc(chip)}</text>')
        cx += cw + 6
    return "\n".join(out)


def arrow(x1, y1, x2, y2, t, label=None):
    s = [f'<path d="M{x1},{y1} L{x2},{y2}" stroke="{t["line"]}" stroke-width="2" fill="none" marker-end="url(#a)"/>']
    if label:
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        s.append(f'<text x="{mx + 8}" y="{my + 4}" font-size="11.5" fill="{t["muted"]}">{esc(label)}</text>')
    return "\n".join(s)


def render(theme: str, c: dict[str, int]) -> str:
    t = THEMES[theme]
    W, H = 1200, 816
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'font-family="Inter,ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif" role="img" '
        f'aria-labelledby="t d">',
        '<title id="t">Super Ads architecture</title>',
        f'<desc id="d">An operator talks to the /ads conductor inside an agent host. The conductor routes to '
        f'{c["skills"]} skills and {c["agents"]} bounded worker agents, which return schema-valid results to the '
        f'deterministic super_ads_core engine. The control plane supplies sources, controls, capabilities and safety '
        f'policy. Output is one validated JSON bundle rendered to Markdown, HTML or PDF. Account changes pass a '
        f'mutation gate.</desc>',
        f'<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{t["line"]}"/></marker></defs>',
        f'<rect width="{W}" height="{H}" rx="20" fill="{t["bg"]}"/>',
        f'<text x="40" y="52" font-size="26" font-weight="800" fill="{t["text"]}">How Super Ads works</text>',
        f'<text x="40" y="78" font-size="14" fill="{t["muted"]}">One conductor, bounded workers, a deterministic core, and evidence for every claim.</text>',
    ]
    parts.append(box(40, 104, 1120, 74, t, ACCENTS["host"], "You + your agent host",
                     ["Claude Code (verified). Codex, Gemini, Cursor, Windsurf, Goose (experimental)."],
                     ()))
    parts.append(arrow(600, 178, 600, 206, t, "/ads audit · plan · create · monitor · optimize · report"))
    parts.append(box(40, 206, 1120, 108, t, ACCENTS["conductor"], "/ads conductor  ·  ads/SKILL.md",
                     ["Owns scope, policy, aggregation, and final artifacts. Treats exports, URLs, and web content as data, never instructions."],
                     ("setup", "audit", "plan", "create", "launch --draft", "monitor", "optimize --draft", "experiment", "report", "validate", "status", "next")))
    parts.append(arrow(320, 314, 320, 346, t))
    parts.append(arrow(880, 314, 880, 346, t))
    parts.append(box(40, 346, 550, 150, t, ACCENTS["skills"], f'{c["skills"]} focused skills',
                     ["12 platform audits plus lifecycle workflows.",
                      f'{c["references"]} dated reference files, loaded on demand.'],
                     ("google", "meta", "youtube", "linkedin", "tiktok", "microsoft", "amazon")))
    parts.append(box(610, 346, 550, 150, t, ACCENTS["agents"], f'{c["agents"]} bounded worker agents',
                     [f'{c["audit_agents"]} read-only audit workers, research and creative helpers,',
                      "and verifiers. Each returns a schema-valid result."],
                     ("audit-*", "research-worker", "source-verifier", "copy-writer")))
    parts.append(arrow(320, 496, 320, 528, t, "findings"))
    parts.append(arrow(700, 496, 700, 528, t, "worker results"))
    parts.append(box(40, 528, 740, 132, t, ACCENTS["core"], "super_ads_core  ·  deterministic engine",
                     [f'{c["schemas"]} versioned JSON schemas, export adapters, scoring, reporting, and Cockpit IO.',
                      "Unknown is a real answer; no health score without approved evidence."],
                     ("contracts", "adapters", "scoring", "reporting", "cockpit")))
    parts.append(box(800, 528, 360, 132, t, ACCENTS["control"], "control-plane",
                     [f'{c["controls"]} registered controls, {c["sources"]} dated sources,',
                      "capabilities, safety, and release gates."],
                     ("sources", "claims", "capabilities")))
    parts.append(arrow(800, 594, 784, 594, t))
    parts.append(arrow(410, 660, 410, 692, t, "one validated ReportBundle"))
    parts.append(box(40, 692, 740, 92, t, ACCENTS["out"], "Deliverables",
                     ["Markdown, HTML, or PDF rendered from the same JSON. Optional local Cockpit workbench."],
                     ()))
    parts.append(box(800, 692, 360, 92, t, ACCENTS["gate"], "Mutation gate",
                     ["Draft by default. Diff, owner approval, ceilings,", "idempotency, rollback, and verification."],
                     ()))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    c = counts()
    for theme in THEMES:
        (ROOT / f"assets/architecture-{theme}.svg").write_text(render(theme, c), encoding="utf-8")
    print(json.dumps(c))


if __name__ == "__main__":
    main()
