#!/usr/bin/env python3
"""One-shot helper: add Stick Cut to catalog.json and bump README counts. Idempotent by import URL."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / "catalog.json"
data = json.loads(path.read_text())

entry = {
    "slug": "stick-cut",
    "name": "Stick Cut",
    "author": {"name": "Michael", "url": "https://x.com/MichaelHeckert"},
    "summary": "Turns a two-sided concept into a looping stick-figure explainer for X, Reels, or TikTok. You post it.",
    "summary_zh": "把正反两面的概念做成可循环的简笔画解说视频，用于 X、Reels 或 TikTok，由你自己发布。",
    "import": "https://x.ai/bot/rET0A-uXf1XKqb_z5vjwl",
    "category": "content-publishing",
    "tags": ["video", "explainer", "content", "stick-figure"],
    "license": "CC0-1.0",
    "verified": False,
    "updated": "2026-11-13",
    "shelf": "raw",
}

imports = {e.get("import") for e in data["entries"]}
if entry["import"] in imports:
    print("Stick Cut already in catalog, skipping append")
else:
    data["entries"].append(entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    print("appended Stick Cut, entries:", len(data["entries"]))

en_line = "- [Stick Cut](https://x.ai/bot/rET0A-uXf1XKqb_z5vjwl) - Turns a two-sided concept into a looping stick-figure explainer for X, Reels, or TikTok. You post it. [Michael](https://x.com/MichaelHeckert)."
zh_line = "- [Stick Cut](https://x.ai/bot/rET0A-uXf1XKqb_z5vjwl) - 把正反两面的概念做成可循环的简笔画解说视频，用于 X、Reels 或 TikTok，由你自己发布。 [Michael](https://x.com/MichaelHeckert)."

def append_line(p, line):
    text = Path(p).read_text()
    if line in text:
        print(p, "already has line")
        return
    if not text.endswith("\n"):
        text += "\n"
    Path(p).write_text(text + line + "\n")
    print("appended to", p)

append_line(ROOT / "catalog/en/content-publishing.md", en_line)
append_line(ROOT / "catalog/zh-CN/content-publishing.md", zh_line)

def bump_readme(p, zh=False):
    text = Path(p).read_text()
    orig = text
    text = text.replace(
        "| [Content & publishing](#content--publishing) | 1015 |",
        "| [Content & publishing](#content--publishing) | 1016 |",
    )
    if zh:
        text = text.replace("| **合计** | **7805** |", "| **合计** | **7806** |")
        text = text.replace("**0 条已核验 / 7805 条已收录**", "**0 条已核验 / 7806 条已收录**")
        text = text.replace("完整列表（1015 条）：", "完整列表（1016 条）：")
        text = text.replace("> 7805 条", "> 7806 条")
    else:
        text = text.replace("| **Total** | **7805** |", "| **Total** | **7806** |")
        text = text.replace("**0 verified / 7805 listed**", "**0 verified / 7806 listed**")
        text = text.replace("Full list (1015 shares):", "Full list (1016 shares):")
        text = text.replace("> 7805 live", "> 7806 live")
    if text != orig:
        Path(p).write_text(text)
        print("updated", p)
    else:
        print("README already bumped or patterns missing:", p)
        # If llms/README already show 7806 from a partial commit, that's fine
        # as long as catalog is 7806 and lint passes.

bump_readme(ROOT / "README.md", zh=False)
bump_readme(ROOT / "README.zh-CN.md", zh=True)
