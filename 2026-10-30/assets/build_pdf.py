"""
把报告 Markdown 渲染为 PDF（Headless Chrome 路线）。

流程：
  1. katex_render.js 先把公式渲染成 KaTeX HTML（含 base64 内嵌字体）
  2. 本脚本把 math_resolved.md 拼成完整 HTML（图片转相对路径，Chrome 能直接读）
  3. Chrome --headless --print-to-pdf 输出 A4 PDF

依赖：markdown（Python）；Chrome（本机已装）；katex（Node）
用法： node katex_render.js && python build_pdf.py
"""
from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent                       # .../2026-10-30
SRC = BASE / "math_resolved.md"
KATEX_CSS = BASE / "katex_fonts.css"
OUT = ROOT / "dsp-bidding-response-strategy.pdf"

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

PAGE_CSS = """
@page { size: A4; margin: 18mm 16mm 16mm 16mm; }
body { font-family: "Microsoft YaHei", "Segoe UI", sans-serif;
       font-size: 10.5pt; line-height: 1.8; color: #1a1a1a; text-align: justify;
       margin: 0; }
h1 { font-size: 21pt; line-height: 1.4; margin: 0 0 12pt 0; color: #0b3d6b;
     border-bottom: 3px solid #0b3d6b; padding-bottom: 8pt; }
h2 { font-size: 15.5pt; margin: 22pt 0 9pt; color: #0b3d6b;
     border-left: 5px solid #2b7bb9; padding-left: 9pt; page-break-after: avoid; }
h3 { font-size: 13pt; margin: 16pt 0 7pt; color: #14507f; page-break-after: avoid; }
h4 { font-size: 11.5pt; margin: 13pt 0 6pt; color: #333; page-break-after: avoid; }
p  { margin: 7pt 0; orphans: 2; widows: 2; }
strong { color: #0b3d6b; }

blockquote { background: #f4f8fc; border-left: 4px solid #2b7bb9;
             margin: 12pt 0; padding: 9pt 13pt; font-size: 9.5pt; color: #33475b;
             page-break-inside: avoid; }
blockquote p { margin: 3pt 0; }

table { border-collapse: collapse; width: 100%; margin: 11pt 0;
        font-size: 8.8pt; page-break-inside: avoid; }
th { background: #0b3d6b; color: #fff; padding: 4.5pt 5pt; text-align: left;
     font-weight: 600; border: 0.5pt solid #0b3d6b; }
td { padding: 3.5pt 5pt; border: 0.5pt solid #cdd8e3; vertical-align: top; }
tbody tr:nth-child(even) { background: #f6f9fc; }

code { font-family: "Consolas", "Courier New", monospace; font-size: 9pt;
       background: #eef2f6; padding: 1pt 3pt; border-radius: 2pt; color: #b02a37; }
pre { background: #f6f8fa; border: 0.5pt solid #d0d7de; border-radius: 3pt;
      padding: 8pt 10pt; font-size: 8.3pt; line-height: 1.45;
      white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid; }
pre code { background: none; padding: 0; color: #24292f; font-size: 8.3pt; }

img { max-width: 100%; display: block; margin: 9pt auto;
      border: 0.5pt solid #dde4ec; page-break-inside: avoid; }

ul, ol { margin: 7pt 0; padding-left: 20pt; }
li { margin: 3pt 0; }

.math-block { text-align: center; margin: 10pt 0; page-break-inside: avoid;
              overflow-x: auto; }
.katex-display { margin: 0; }
.katex { font-size: 1em; }

a { color: #0b5fa5; text-decoration: none; }
hr { border: none; border-top: 0.75pt solid #cfd8e3; margin: 16pt 0; }
"""


def find_browser() -> str:
    for p in CHROME_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("未找到 Chrome/Edge，无法导出 PDF")


def build_html() -> Path:
    if not SRC.exists() or not KATEX_CSS.exists():
        raise SystemExit("缺少 math_resolved.md / katex_fonts.css，"
                         "请先运行 node katex_render.js")

    import markdown

    md = markdown.Markdown(extensions=["tables", "fenced_code",
                                       "sane_lists", "attr_list"])
    body = md.convert(SRC.read_text(encoding="utf-8"))
    katex_css = KATEX_CSS.read_text(encoding="utf-8")

    # 图片是相对 root 的 assets/ 路径；HTML 放在 root 下，无需改写
    page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>DSP 竞价应对策略调研</title>
<style>{katex_css}</style>
<style>{PAGE_CSS}</style>
</head><body>{body}</body></html>"""

    tmp = ROOT / "_report_print.html"
    tmp.write_text(page, encoding="utf-8")
    return tmp


def main() -> int:
    browser = find_browser()
    page = build_html()

    if OUT.exists():
        OUT.unlink()

    profile = Path(tempfile.mkdtemp(prefix="chrome_pdf_"))
    cmd = [
        browser,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-pdf-header-footer",          # 不要 Chrome 默认的网址/日期页眉
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",     # 等 KaTeX 字体与图片加载完成
        f"--user-data-dir={profile}",
        f"--print-to-pdf={OUT}",
        page.as_uri(),
    ]
    print("browser:", browser)
    res = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if not OUT.exists():
        print(res.stdout[-3000:])
        print(res.stderr[-3000:])
        raise SystemExit("PDF 未生成")

    head = OUT.open("rb").read(5)
    print(f"PDF written: {OUT}")
    print(f"  size: {OUT.stat().st_size / 1024:.0f} KB, signature: {head.decode()}")
    page.unlink(missing_ok=True)
    return 0 if head == b"%PDF-" else 1


if __name__ == "__main__":
    sys.exit(main())
