/**
 * 用本地 KaTeX 把报告中的公式渲染成离线可用的 HTML + 内嵌字体 CSS。
 *
 * 输入：  ../00-dsp-bidding-response-strategy.md   （仓库内 Markdown 原文）
 * 输出：  ./math_resolved.md   （公式已替换为 KaTeX HTML）
 *         ./katex_fonts.css    （@font-face，字体以 base64 内嵌）
 * 用法：  node katex_render.js
 */
const fs = require("fs");
const path = require("path");

const KATEX_DIST = "C:\\Users\\Administrator\\.dsh\\profiles\\web\\node_modules\\katex\\dist";
const katex = require(path.join(KATEX_DIST, "katex.min.js"));

const BASE = __dirname;
const SRC = path.join(BASE, "..", "00-dsp-bidding-response-strategy.md");
const OUT_MD = path.join(BASE, "math_resolved.md");
const OUT_CSS = path.join(BASE, "katex_fonts.css");

// ---------------------------------------------------------------------------
// 1. 生成内嵌字体的 CSS
// ---------------------------------------------------------------------------
const cssRaw = fs.readFileSync(path.join(KATEX_DIST, "katex.min.css"), "utf8");
let embedded = 0, missing = [];

const cssEmbedded = cssRaw.replace(
  /url\(fonts\/([A-Za-z0-9_\-.]+?\.(?:woff2|woff|ttf))\)/g,
  (m, file) => {
    const p = path.join(KATEX_DIST, "fonts", file);
    if (!fs.existsSync(p)) { missing.push(file); return m; }
    const b64 = fs.readFileSync(p).toString("base64");
    embedded++;
    const mime = file.endsWith(".woff2") ? "font/woff2"
               : file.endsWith(".woff") ? "font/woff" : "font/ttf";
    return `url(data:${mime};base64,${b64})`;
  }
);

fs.writeFileSync(OUT_CSS, cssEmbedded, "utf8");
console.log(`fonts embedded: ${embedded}, missing: ${missing.length}`);
if (missing.length) console.log("  missing:", [...new Set(missing)].join(", "));

// ---------------------------------------------------------------------------
// 2. 渲染公式
// ---------------------------------------------------------------------------
let md = fs.readFileSync(SRC, "utf8");

// 去掉 UTF-8 BOM：否则 Markdown 解析器会把首行 "# 标题" 当作普通段落
if (md.charCodeAt(0) === 0xFEFF) md = md.slice(1);

function render(tex, displayMode) {
  return katex.renderToString(tex, {
    displayMode,
    throwOnError: false,
    strict: "ignore",
    trust: false,
    output: "html",
  });
}

let nBlock = 0, nInline = 0;

// 块级：$$ ... $$（允许多行）
md = md.replace(/\$\$([\s\S]+?)\$\$/g, (m, tex) => {
  nBlock++;
  return `<div class="math-block">${render(tex.trim(), true)}</div>`;
});

// 行内：$ ... $（不跨行、非空）
md = md.replace(/\$([^$\n]+?)\$/g, (m, tex) => {
  nInline++;
  return render(tex.trim(), false);
});

// 写回时同样不带 BOM
fs.writeFileSync(OUT_MD, md.replace(/^\uFEFF/, ""), "utf8");
console.log(`formulas: block=${nBlock}, inline=${nInline}`);
console.log(`written: ${OUT_MD}`);
