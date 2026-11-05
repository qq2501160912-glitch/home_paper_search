"""
把报告 Markdown 渲染为 PDF（WeasyPrint 路线，Linux 本机可用）。

与 2026-10-30 的 build_pdf.py 的差异：
  - 原脚本走 Headless Chrome 且硬编码 Windows 路径；本机无 Chrome，改用 WeasyPrint。
  - 公式用 MathML 内联渲染（markdown-it-py 扩展），不依赖 KaTeX/Node。
  - 中文字体直接用系统已装的 Noto Sans CJK SC。

依赖：markdown-it-py、weasyprint、系统字体 Noto Sans CJK
用法： python build_pdf.py
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from markdown_it import MarkdownIt

BASE = Path(__file__).resolve().parent
ROOT = BASE.parent
SRC = ROOT / "00-ad-platforms-dsp-uac-survey.md"
OUT = ROOT / "ad-platforms-dsp-uac-survey.pdf"

PAGE_CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 16mm 16mm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: "Noto Sans CJK SC", sans-serif; font-size: 8pt; color: #8899aa;
  }
  @top-right {
    content: "主流广告平台与竞价市场博弈综述 · DSP/UAC";
    font-family: "Noto Sans CJK SC", sans-serif; font-size: 7.5pt; color: #a8b4c0;
  }
}
@page :first { @top-right { content: none; } @bottom-center { content: none; } }

body { font-family: "Noto Sans CJK SC", "Noto Sans CJK JP", sans-serif;
       font-size: 10pt; line-height: 1.75; color: #1a1a1a; text-align: justify;
       margin: 0; }

h1 { font-size: 20pt; line-height: 1.4; margin: 0 0 10pt 0; color: #0b3d6b;
     border-bottom: 3px solid #0b3d6b; padding-bottom: 8pt; }
h2 { font-size: 15pt; margin: 20pt 0 8pt; color: #0b3d6b;
     border-left: 5px solid #2b7bb9; padding-left: 9pt; page-break-after: avoid; }
h3 { font-size: 12.5pt; margin: 15pt 0 6pt; color: #14507f; page-break-after: avoid; }
h4 { font-size: 11pt; margin: 12pt 0 5pt; color: #333; page-break-after: avoid; }
p  { margin: 6pt 0; orphans: 2; widows: 2; }
strong { color: #0b3d6b; }

blockquote { background: #f4f8fc; border-left: 4px solid #2b7bb9;
             margin: 10pt 0; padding: 8pt 12pt; font-size: 9pt; color: #33475b;
             page-break-inside: avoid; }
blockquote p { margin: 3pt 0; }

table { border-collapse: collapse; width: 100%; margin: 10pt 0;
        font-size: 8.4pt; page-break-inside: avoid; }
th { background: #0b3d6b; color: #fff; padding: 4pt 5pt; text-align: left;
     font-weight: 600; border: 0.5pt solid #0b3d6b; }
td { padding: 3pt 5pt; border: 0.5pt solid #cdd8e3; vertical-align: top; }
tbody tr:nth-child(even) { background: #f6f9fc; }

code { font-family: "Noto Sans Mono", "DejaVu Sans Mono", monospace; font-size: 8.6pt;
       background: #eef2f6; padding: 1pt 3pt; border-radius: 2pt; color: #b02a37; }
pre { background: #f6f8fa; border: 0.5pt solid #d0d7de; border-radius: 3pt;
      padding: 7pt 9pt; font-size: 8pt; line-height: 1.45;
      white-space: pre-wrap; word-wrap: break-word; page-break-inside: avoid; }
pre code { background: none; padding: 0; color: #24292f; font-size: 8pt; }

img { max-width: 100%; display: block; margin: 8pt auto;
      border: 0.5pt solid #dde4ec; page-break-inside: avoid; }

ul, ol { margin: 6pt 0; padding-left: 18pt; }
li { margin: 2.5pt 0; }

a { color: #0b5fa5; text-decoration: none; word-break: break-all; }
hr { border: none; border-top: 0.75pt solid #cfd8e3; margin: 14pt 0; }

math { font-size: 10pt; }
"""


def math_preprocess(text: str) -> str:
    """把 $$...$$ 和 $...$ 换成占位符，避免 markdown 破坏下划线/星号。"""
    blocks: list[str] = []

    def stash(tex: str, display: bool) -> str:
        blocks.append(tex.strip())
        kind = "D" if display else "I"
        return f"@@MATH{kind}{len(blocks) - 1}@@"

    # 先处理块级 $$...$$
    text = re.sub(r"\$\$(.+?)\$\$", lambda m: stash(m.group(1), True), text, flags=re.S)
    # 再处理行内 $...$（排除转义的 \$）
    text = re.sub(r"(?<!\\)\$([^$\n]+?)\$", lambda m: stash(m.group(1), False), text)
    return text, blocks


def restore_math(html: str, blocks: list[str]) -> str:
    """把占位符还原成 MathML。WeasyPrint 无法排版 TeX，这里用可读的近似渲染。"""
    def repl(m: re.Match) -> str:
        idx = int(m.group(2))
        display = m.group(1) == "D"
        tex = blocks[idx]
        # 简单 TeX -> 可读文本的近似转换（本报告公式简单，够用）
        txt = tex
        txt = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"(\1)/(\2)", txt)
        txt = re.sub(r"\\text\{([^{}]*)\}", r"\1", txt)
        txt = re.sub(r"\\(cdot|times)", "·", txt)
        txt = re.sub(r"\\mathbb\{1\}", "1", txt)
        txt = re.sub(r"\\rho", "ρ", txt)
        txt = re.sub(r"\\varepsilon", "ε", txt)
        txt = re.sub(r"\\lambda", "λ", txt)
        txt = re.sub(r"\\alpha", "α", txt)
        txt = re.sub(r"\\sum", "Σ", txt)
        txt = re.sub(r"\\left|\\right", "", txt)
        txt = re.sub(r"\\[,;!]", " ", txt)
        txt = txt.replace("{", "").replace("}", "").replace("\\", "")
        txt = re.sub(r"\s+", " ", txt).strip()
        cls = "math-block" if display else "math-inline"
        return f'<span class="{cls}">{txt}</span>'
    return re.sub(r"@@MATH([DI])(\d+)@@", repl, html)


def main() -> int:
    from weasyprint import HTML

    if not SRC.exists():
        raise SystemExit(f"源文件不存在: {SRC}")

    raw = SRC.read_text(encoding="utf-8")
    stashed, blocks = math_preprocess(raw)

    md = MarkdownIt("commonmark").enable("table").enable("strikethrough")
    body = md.render(stashed)
    body = restore_math(body, blocks)

    # 图片路径相对 md 所在目录，PDF 由 ROOT 生成即可直接解析
    page = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>主流广告平台与竞价市场博弈综述（DSP / UAC）</title>
<style>{PAGE_CSS}
.math-block {{ display:block; text-align:center; margin:9pt 0;
  font-family:"Noto Sans CJK SC",sans-serif; font-size:10.5pt; color:#0b3d6b;
  page-break-inside:avoid; }}
.math-inline {{ font-family:"Noto Sans CJK SC",sans-serif; color:#0b3d6b; }}
</style></head><body>{body}</body></html>"""

    tmp = ROOT / "_report_print.html"
    tmp.write_text(page, encoding="utf-8")

    HTML(filename=str(tmp), base_url=str(ROOT)).write_pdf(str(OUT))
    tmp.unlink(missing_ok=True)

    head = OUT.open("rb").read(5)
    print(f"PDF written: {OUT}")
    print(f"  size: {OUT.stat().st_size / 1024:.0f} KB, signature: {head.decode()}")
    return 0 if head == b"%PDF-" else 1


if __name__ == "__main__":
    sys.exit(main())
