"""Render the README's header and project cards to assets/*.png, dark and light.

Run: python3 render/render.py   (needs Google Chrome; set CHROME to override its path)
"""

import html
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
SCALE = 2

# Colours from the nandex design tokens (NandishNaik01/nandex packages/ui/styles/tokens.css).
THEMES = {
    "dark": {
        "bg": "hsl(30 7% 5%)", "fg": "hsl(34 11% 88%)", "subtle": "hsl(38 5% 71%)",
        "muted": "hsl(40 4% 60%)", "border": "hsl(43 7% 19%)", "rule": "hsl(40 6% 14%)",
        "tag": "hsl(43 7% 19%)",
    },
    "light": {
        "bg": "hsl(0 0% 100%)", "fg": "hsl(40 6% 10%)", "subtle": "hsl(36 5% 40%)",
        "muted": "hsl(38 4% 50%)", "border": "hsl(34 11% 88%)", "rule": "hsl(36 15% 94%)",
        "tag": "hsl(36 15% 94%)",
    },
}

HEADER = {
    "eyebrow": "Nandisha D · SDE-II, Harvey AI via Think41 · India",
    "title": "Full stack by day.<br><em>Fiction</em> by night.",
    "lede": "Web, mobile, and the AI plumbing in between. Java, TypeScript, Python. Ships small, ships often.",
    "stats": [
        ("20+", "integrations shipped at Atomicwork"),
        ("22k", "readers on Pratilipi · 333 followers"),
    ],
}

CARDS = [
    {"file": "card-autointerviewer", "kind": "Web app", "tag": "AI", "name": "AutoInterviewer",
     "blurb": "Mock interviews that ask the follow-up a real interviewer would.",
     "link": "autointerviewer.nandish.online"},
    {"file": "card-nantex", "kind": "CLI", "tag": "Open source", "name": "nantex",
     "blurb": "LaTeX to PDF, live, with no local LaTeX install.",
     "link": "github.com/NandishNaik01/nantex"},
    {"file": "card-portfolio", "kind": "Site", "tag": "Personal", "name": "Portfolio",
     "blurb": "Work, writing, and where to find me.",
     "link": "porto.nandish.online"},
]

FONTS = (
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500'
    '&family=Newsreader:ital,opsz,wght@0,6..72,400;1,6..72,400&display=block">'
)


def page(t: dict, width: int, height: int, body: str) -> str:
    return f"""<!doctype html><html><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box;margin:0}}
html,body{{width:{width}px;height:{height}px;background:transparent;overflow:hidden}}
.frame{{width:{width}px;height:{height}px;background:{t['bg']};color:{t['fg']};border:1px solid {t['border']};
  border-radius:12px;font-family:Inter,sans-serif;-webkit-font-smoothing:antialiased;overflow:hidden}}
.serif{{font-family:Newsreader,serif;letter-spacing:-0.02em}}
.eyebrow{{font-size:11px;letter-spacing:.1em;text-transform:uppercase;font-weight:500;color:{t['muted']}}}
.subtle{{color:{t['subtle']}}} .muted{{color:{t['muted']}}}
</style></head><body>{body}</body></html>"""


def header_html(t: dict) -> str:
    stats = f'<div style="height:1px;background:{t["rule"]}"></div>'.join(
        f'<div><div class="serif" style="font-size:40px;line-height:1">{n}</div>'
        f'<div class="subtle" style="font-size:13px;margin-top:4px">{html.escape(label)}</div></div>'
        for n, label in HEADER["stats"]
    )
    body = f"""<div class="frame" style="padding:44px 48px;display:grid;grid-template-columns:1.5fr 1fr;gap:32px">
  <div style="display:flex;flex-direction:column;justify-content:space-between;min-width:0">
    <div class="eyebrow">{html.escape(HEADER['eyebrow'])}</div>
    <div>
      <div class="serif" style="font-size:52px;line-height:1.02">{HEADER['title']}</div>
      <div class="subtle" style="margin-top:18px;font-size:15px;max-width:46ch">{html.escape(HEADER['lede'])}</div>
    </div>
  </div>
  <div style="display:flex;flex-direction:column;justify-content:flex-end;gap:14px;border-left:1px solid {t['rule']};padding-left:32px">{stats}</div>
</div>"""
    return page(t, 1200, 360, body)


def card_html(t: dict, c: dict) -> str:
    body = f"""<div class="frame" style="padding:22px 24px;display:flex;flex-direction:column;justify-content:space-between">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <span class="eyebrow" style="letter-spacing:.08em">{html.escape(c['kind'])}</span>
    <span class="subtle" style="font-size:11px;padding:2px 8px;border-radius:999px;background:{t['tag']}">{html.escape(c['tag'])}</span>
  </div>
  <div>
    <div class="serif" style="font-size:28px;line-height:1.05;letter-spacing:-0.015em">{html.escape(c['name'])}</div>
    <div class="subtle" style="margin-top:8px;font-size:13px;line-height:1.45">{html.escape(c['blurb'])}</div>
  </div>
  <div class="muted" style="font-size:12px;display:flex;justify-content:space-between"><span>{html.escape(c['link'])}</span><span>→</span></div>
</div>"""
    return page(t, 384, 240, body)


def shoot(markup: str, width: int, height: int, out: Path) -> None:
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(markup)
    try:
        subprocess.run(
            [CHROME, "--headless=new", "--hide-scrollbars", "--default-background-color=00000000",
             f"--force-device-scale-factor={SCALE}", f"--window-size={width},{height}",
             "--virtual-time-budget=8000", f"--screenshot={out}", f"file://{f.name}"],
            check=True, capture_output=True,
        )
    finally:
        os.unlink(f.name)
    print(f"{out.relative_to(ROOT)}  {out.stat().st_size // 1024} KB")


def main() -> None:
    ASSETS.mkdir(exist_ok=True)
    for name, t in THEMES.items():
        shoot(header_html(t), 1200, 360, ASSETS / f"header-{name}.png")
        for c in CARDS:
            shoot(card_html(t, c), 384, 240, ASSETS / f"{c['file']}-{name}.png")


if __name__ == "__main__":
    main()
