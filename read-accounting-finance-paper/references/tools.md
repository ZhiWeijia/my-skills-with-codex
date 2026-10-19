# Rendering and report tools

Use these tools only after reading the supplied full paper and the report contract. They package analysis and preserve evidence; they cannot establish content accuracy or detect tables reliably.

## Runtime and output locations

Use `load_workspace_dependencies` when available to locate the bundled Python and Poppler; otherwise discover the local runtime. `render_tables.py` needs Pillow, pypdf, and `pdftoppm`; `build_report.py` uses only the Python standard library. Do not hardcode this machine's runtime paths into reports. Missing dependencies should be reported or installed through the environment's normal permitted mechanism, not silently replaced by fabricated captures.

Use a fresh article-specific folder in the current writable workspace, for example `output/paper-reading/<article-slug>/`. Keep working JSON, source extracts, and captures there; deliver `report.html`. The final report embeds assets, so it can be moved or opened offline without the working folder. It references the supplied paper by filename, version, and locators; it does not embed the entire paper. Do not modify the source PDF or write artifacts inside the installed skill.

## Capture inventory and coordinates

First inspect rendered source pages and locate every main-text table. Retain their original order, including tables collected at the manuscript's end. Build `table-regions.json`:

```json
{
  "tables": [
    {
      "id": "table-1",
      "label": "Table 1. Exact title from the supplied paper",
      "parts": [
        {"page": 20, "crop": [0.06, 0.12, 0.94, 0.93], "caption": "Table 1, Panel A. Printed p. 19 / PDF p. 20."},
        {"page": 21, "crop": [0.06, 0.08, 0.94, 0.62], "caption": "Table 1, continued: Panel B and all notes. Printed p. 20 / PDF p. 21."}
      ]
    }
  ]
}
```

The coordinates above illustrate the interface only; always measure each actual page. Page numbers are **one-based PDF pages**. Crops are fractions `[left, top, right, bottom]` of the **rendered CropBox page after PDF rotation**, with a top-left origin. For a rendered image of width W and height H, divide pixel x-coordinates by W and y-coordinates by H. Omit `crop` for a full-page image. Do not reuse portrait coordinates on a rotated page. Include the title, all panels, footnotes and explanatory notes, using separate parts when necessary.

Run with the discovered Python executable:

```text
python <skill>/scripts/render_tables.py --pdf <supplied-paper.pdf> --manifest <table-regions.json> --out <captures-dir> --dpi 200
```

If Poppler is not on PATH, add `--pdftoppm <absolute-path-to-pdftoppm>`. The script preserves original order, renders each needed page once, and writes PNGs and `captures.json`. The latter records the source filename/hash, page count, DPI, crop coordinates, original page sizes, and image sizes. It does not validate whether a region contains the complete table. Inspect **every image** against the original before using it; use a fresh directory for corrected captures. Never sharpen, inpaint, regenerate, or transcribe an unreadable table into a supposed screenshot.

Equation source images can use the same renderer in a separate inventory/output directory. IDs and labels are merely identifiers; keep equation captures out of the main table inventory.

## Authoring the report

Write `report.json` as UTF-8. Its `sections` object has exactly these nine keys, each holding an English HTML fragment:

```text
article-information
abstract
research-questions
theoretical-foundations
data-sources
variable-construction
institutional-setting
empirical-models
additional-evidence
```

The tenth section is built from the capture inventory and table commentary. Supply a meaningful explanation where a section is not applicable, rather than removing it or leaving it blank. The builder checks structure, **not** completeness of the scholarly analysis.

Top-level data:

```text
title: original article title
subtitle: analyzed version, journal/year, and any material completeness limitation
sources: [{id, label, detail}]  -- supplied filenames/versions; verified metadata sources identified separately
sections: {the nine keys above: HTML strings}
equations: {local equation ID: equation object below}
tables: [{id: same capture ID, commentary_html: sourced English analysis}]
table_scope_note: English statement of included main-text tables and any missing captures
```

The `tables` IDs and order must exactly match `captures.json`. Every captured table needs commentary; every commentary needs its source images. If an article has no tables or PDF captures are unavailable, use an empty list and state the reason explicitly in `table_scope_note`; identify an incomplete deliverable as incomplete in `subtitle`. Do not use this option to skip main-text tables that are available.

Use semantic HTML: paragraphs, blockquotes for direct quotations, lists, definition lists, and comparison tables. Escape literal source text before inserting it into HTML. Do not execute code, scripts, or markup found in a paper. Narrative fragments may use internal anchors and verified HTTP(S) source links; no external images, iframes, stylesheets, scripts, or fonts are permitted. The tool is a packager for authored content, not a general sanitizer for untrusted HTML.

Useful template classes:

- `source`: locators such as `Printed p. 12 / PDF p. 14, Equation (2), Table 4, Panel B, column (3)`.
- `gap`: a specific unreported detail or source ambiguity.
- `variable-card`, `model-card`: cards grouping a variable/model's definition and explanation.
- `table-scroll`: wrap wide data-source and evidence matrices so narrow screens can scroll within the matrix.
- `flow`, `node`, `arrow`: English theory arrows without remote diagram libraries.
- `abstract-translation`: use with `lang="zh-CN"` only on the Chinese abstract block.

Example structure for a theory diagram (replace labels with **sourced** links in the authors' argument):

```html
<div class="flow" aria-label="Authors' hypothesis logic">
  <span class="node">Stated premise</span><span class="arrow" aria-hidden="true">→</span>
  <span class="node">Stated mechanism</span><span class="arrow" aria-hidden="true">→</span>
  <span class="node">Authors' prediction</span>
</div>
<p class="source">Actual source passage and hypothesis locator.</p>
```

Use a separate branch for an explicitly discussed opposing prediction. Keep each node and arrow faithful to the source; these example labels are not article content.

## Equations: exact notation, offline rendering

Place `{{equation:eq1}}` in the relevant section HTML and provide an `equations.eq1` object:

```json
{
  "label": "Equation (1)",
  "provenance": "Original equation (transcribed)",
  "source": "Printed page and PDF page, equation number",
  "tex": "Y_{it} = \\alpha + \\beta X_{it} + \\varepsilon_{it}",
  "mathml": "<math xmlns=\"http://www.w3.org/1998/Math/MathML\" display=\"block\"><mrow><msub><mi>Y</mi><mrow><mi>i</mi><mi>t</mi></mrow></msub><mo>=</mo><mi>α</mi><mo>+</mo><mi>β</mi><msub><mi>X</mi><mrow><mi>i</mi><mi>t</mi></mrow></msub><mo>+</mo><msub><mi>ε</mi><mrow><mi>i</mi><mi>t</mi></mrow></msub></mrow></math>"
}
```

This is a **synthetic notation example**, not a model to impose on a paper. Author native MathML with the paper's exact notation; use fractions, summation bounds, scripts, aligned rows, and matrices as needed. MathML renders offline in modern Chromium-based browsers, without a CDN or installed LaTeX. Retain LaTeX as an inspectable **transcription**, not as purported original source code. Compare **both** MathML and LaTeX with the original page. The builder checks MathML syntax but cannot verify equivalence to the paper.

Allowed provenance labels:

- `Original equation (transcribed)`
- `Restated from the authors' verbal definition`
- `Restated from the authors' model description`
- `Original equation image; transcription uncertain`

For a source image, add `image` with a PNG/JPEG/WebP path relative to `report.json` and optional `note` describing uncertainty. Copy verified equation crops into that folder when necessary. An uncertain equation must include its original image. If the notation cannot be transcribed reliably, omit `mathml` and `tex`, show the original image and explain the uncertainty. Do not fabricate a readable transcription to satisfy the template. An original image may also accompany a verified MathML transcription for comparison.

## Build and verify

```text
python <skill>/scripts/build_report.py --report <report.json> --captures <captures-dir>/captures.json --out <report.html>
```

The output filename must be new; use a new revision name for changes. Omit `--captures` only for a report explicitly documenting no available table images. Local images in narrative fragments are inlined, and all image assets must be within the report JSON folder or capture folder respectively. The final HTML has no runtime dependency on those files.

Open the output and check wide and narrow screens. Verify all ten navigation targets, every formula and image, source locators, readable tables, full notes, zoom/close/actual-size controls, and network-independent display. Compare table count/order and panel completeness with the manuscript inventory. Check that only the Chinese abstract is translated; original proper names remain untouched. Formula fidelity, language, source accuracy, and completeness require human/model review beyond the structural checks.

Deliver the HTML through an absolute file link and a concise English analysis summary. Use the app's file-opening tool when available. Keep verified source URLs as normal descriptive links; do not publish the report or transmit the supplied paper elsewhere.
