#!/usr/bin/env python3
"""Build one offline HTML file from authored report JSON and PDF captures.

This packages source-grounded analysis; it does not read papers or infer content.
Equations use native MathML plus a readable LaTeX transcription, with a source
image fallback for uncertain notation. See references/tools.md for the interface.
"""
import argparse
import base64
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import xml.etree.ElementTree as ET


SECTIONS = [
    ("article-information", "Article Information"),
    ("abstract", "Abstract — Original English and Chinese Translation"),
    ("research-questions", "Research Questions and Hypotheses"),
    ("theoretical-foundations", "Theoretical Foundations and Hypothesis Logic"),
    ("data-sources", "Data Sources and Sample Construction"),
    ("variable-construction", "Variable Construction — Replication-Level Definitions"),
    ("institutional-setting", "Institutional Setting"),
    ("empirical-models", "Empirical Models and Identification Strategy"),
    ("additional-evidence", "Main Tests and Additional Evidence"),
    ("table-walkthrough", "Table-by-Table Walkthrough"),
]
MIME_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
PROVENANCE = {
    "Original equation (transcribed)",
    "Restated from the authors' verbal definition",
    "Restated from the authors' model description",
    "Original equation image; transcription uncertain",
}


def escape(value):
    return html.escape(str(value), quote=True)


def asset_uri(filename, root):
    path = (Path(root) / filename).resolve()
    if not path.is_relative_to(Path(root).resolve()):
        raise ValueError(f"Asset must be inside the input directory: {filename}")
    mime = MIME_TYPES.get(path.suffix.lower())
    if mime is None:
        raise ValueError(f"Unsupported image type: {path.suffix}")
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


class OfflineFragment(HTMLParser):
    """Inline local images and disallow active/remote resources in authored HTML."""
    def __init__(self, root):
        super().__init__(convert_charrefs=False)
        self.root = root
        self.output = []

    def handle_starttag(self, tag, attrs):
        self.start(tag, attrs, False)

    def handle_startendtag(self, tag, attrs):
        self.start(tag, attrs, True)

    def start(self, tag, attrs, closed):
        if tag in {"script", "style", "iframe", "object", "embed", "base", "link", "meta", "form", "foreignobject"}:
            raise ValueError(f"Unsupported active/resource tag in report fragment: {tag}")
        transformed = []
        for key, value in attrs:
            if key.startswith("on") or key in {"srcdoc", "srcset"}:
                raise ValueError(f"Unsupported active/resource attribute: {key}")
            if value is not None:
                if key == "src":
                    if tag != "img":
                        raise ValueError("Only static image sources are supported.")
                    if not value.startswith(tuple(f"data:{m};base64," for m in MIME_TYPES.values())):
                        value = asset_uri(value, self.root)
                if key in {"href", "xlink:href"}:
                    if tag == "a":
                        if not (value.startswith(("#", "https://", "http://"))):
                            raise ValueError("Links must be source anchors or verified HTTP(S) references.")
                    elif not value.startswith("#"):
                        raise ValueError("SVG resources must use in-document fragment references.")
                if key == "style" and re.search(r"url\s*\(|@import|expression\s*\(", value, re.I):
                    raise ValueError("External or active CSS is not supported.")
            transformed.append(key if value is None else f'{key}="{escape(value)}"')
        suffix = (" " + " ".join(transformed)) if transformed else ""
        self.output.append(f"<{tag}{suffix}{' /' if closed else ''}>")

    def handle_endtag(self, tag):
        self.output.append(f"</{tag}>")

    def handle_data(self, data):
        self.output.append(data)

    def handle_entityref(self, name):
        self.output.append(f"&{name};")

    def handle_charref(self, name):
        self.output.append(f"&#{name};")


def offline_fragment(fragment, root):
    if not isinstance(fragment, str):
        raise ValueError("Narrative fragments must be HTML strings.")
    parser = OfflineFragment(root)
    parser.feed(fragment)
    parser.close()
    return "".join(parser.output)


def image_figure(uri, label, caption):
    return (f'<figure><button type="button" class="image-zoom" aria-label="Enlarge {escape(label)}">'
            f'<img src="{uri}" alt="{escape(label)}" loading="lazy"></button>'
            f'<figcaption class="image-caption">{escape(caption)}</figcaption></figure>')


def equation_html(equation, root):
    provenance = equation.get("provenance")
    if provenance not in PROVENANCE:
        raise ValueError("An equation must explicitly label its transcription/restatement provenance.")
    if not equation.get("source") or not equation.get("label"):
        raise ValueError("An equation needs its original label and source location.")
    mathml, tex = equation.get("mathml"), equation.get("tex")
    blocks = []
    if mathml:
        parsed = ET.fromstring(mathml)
        if parsed.tag != "{http://www.w3.org/1998/Math/MathML}math":
            raise ValueError("MathML must have a math root with the MathML namespace.")
        if not tex:
            raise ValueError("A rendered transcription requires readable LaTeX source.")
        blocks.append(f'<div class="math-display">{mathml}</div>')
    if equation.get("image"):
        blocks.append(image_figure(asset_uri(equation["image"], root), equation["label"], equation["source"]))
    if not blocks:
        raise ValueError("An equation needs MathML or a verified original PDF image.")
    if provenance == "Original equation image; transcription uncertain" and not equation.get("image"):
        raise ValueError("An uncertain transcription requires the original image.")
    source = f'<span class="source">{escape(equation["source"])}</span>'
    latex = (f'<details><summary>LaTeX transcription — inspect against the source</summary>'
             f'<pre>{escape(tex)}</pre></details>') if tex else ""
    note = f'<p class="gap">{escape(equation["note"])}</p>' if equation.get("note") else ""
    return (f'<div class="equation"><span class="tag">{escape(provenance)}</span>'
            f'<strong>{escape(equation["label"])}</strong>{"".join(blocks)}{source}{note}{latex}</div>')


def build(data, report_root, captures, capture_root, template):
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        raise ValueError("A report title is required.")
    section_data = data.get("sections", {})
    expected = {key for key, _ in SECTIONS[:-1]}
    if set(section_data) != expected or any(not section_data[key].strip() for key in expected):
        raise ValueError("Provide a nonempty HTML fragment for each of the nine narrative sections.")
    capture_tables = captures.get("tables", [])
    commentaries = data.get("tables", [])
    capture_ids = [table["id"] for table in capture_tables]
    commentary_ids = [table["id"] for table in commentaries]
    if len(set(capture_ids)) != len(capture_ids) or capture_ids != commentary_ids:
        raise ValueError("Captured tables and commentaries must match exactly in original order.")
    equations = data.get("equations", {})

    def narrative(value):
        def replacement(match):
            key = match.group(1)
            if key not in equations:
                raise ValueError(f"Equation token has no definition: {key}")
            return equation_html(equations[key], report_root)
        value = re.sub(r"\{\{equation:([a-zA-Z0-9_-]+)\}\}", replacement, value)
        if "{{equation:" in value:
            raise ValueError("Malformed equation token.")
        return offline_fragment(value, report_root)

    source_items = []
    for source in data.get("sources", []):
        source_id = source["id"]
        if not re.fullmatch(r"[a-z][a-z0-9-]*", source_id):
            raise ValueError("Source IDs must use lowercase letters, digits, and hyphens.")
        source_items.append(f'<li id="source-{source_id}"><strong>{escape(source["label"])}</strong>: '
                            f'{escape(source["detail"])}</li>')
    if not source_items:
        raise ValueError("Provide an explicit inventory of supplied sources.")
    body = []
    for index, (key, title) in enumerate(SECTIONS[:-1], 1):
        content = narrative(section_data[key])
        if key == "article-information":
            content += '<h3>Source inventory</h3><ol class="sources">' + "".join(source_items) + "</ol>"
        body.append(f'<section id="{key}"><h2>{index:02d} · {escape(title)}</h2>{content}</section>')
    walkthrough = [f'<p>{escape(data.get("table_scope_note", "All main-text tables, in the paper’s original order."))}</p>']
    for table, commentary in zip(capture_tables, commentaries):
        if not commentary.get("commentary_html", "").strip():
            raise ValueError(f"Table {table['id']} needs English commentary.")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", table["id"]) or not table.get("parts"):
            raise ValueError("Invalid capture id or empty captured table.")
        images = []
        for index, part in enumerate(table["parts"], 1):
            label = f"{table['label']} · Part {index} · PDF p. {part['page']}"
            caption = part.get("caption") or label
            images.append(image_figure(asset_uri(part["image"], capture_root), label, caption))
        walkthrough.append(f'<article class="walkthrough" id="capture-{table["id"]}">'
                           f'<h3>{escape(table["label"])}</h3><div class="table-layout">'
                           f'<div class="table-images">{"".join(images)}</div>'
                           f'<div class="table-notes">{narrative(commentary["commentary_html"])}</div>'
                           '</div></article>')
    if not capture_tables and not data.get("table_scope_note"):
        raise ValueError("Explain why no table captures are included.")
    body.append('<section id="table-walkthrough"><h2>10 · Table-by-Table Walkthrough</h2>'
                + "".join(walkthrough) + '</section>')
    values = {
        "TITLE": escape(data["title"]), "SUBTITLE": escape(data.get("subtitle", "")),
        "NAV": "".join(f'<li><a href="#{key}">{escape(title)}</a></li>' for key, title in SECTIONS),
        "BODY": "".join(body),
    }
    for key in values:
        if f"@@{key}@@" not in template:
            raise ValueError(f"Missing template insertion point: {key}")
    return re.sub(r"@@(TITLE|SUBTITLE|NAV|BODY)@@", lambda match: values[match.group(1)], template)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", required=True, type=Path)
    parser.add_argument("--captures", type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    output = args.out.resolve()
    if output.exists():
        raise FileExistsError("Use a fresh output filename rather than overwriting a prior report.")
    report = json.loads(args.report.read_text(encoding="utf-8-sig"))
    captures = json.loads(args.captures.read_text(encoding="utf-8-sig")) if args.captures else {"tables": []}
    capture_root = args.captures.resolve().parent if args.captures else args.report.resolve().parent
    template = (Path(__file__).resolve().parents[1] / "assets" / "report-template.html").read_text(encoding="utf-8")
    result = build(report, args.report.resolve().parent, captures, capture_root, template)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(result, encoding="utf-8")
    print(json.dumps({"report": str(output), "tables": len(captures["tables"]), "bytes": output.stat().st_size}))


if __name__ == "__main__":
    main()
