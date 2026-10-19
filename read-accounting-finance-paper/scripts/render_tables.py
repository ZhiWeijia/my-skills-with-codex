#!/usr/bin/env python3
"""Render visually verified PDF regions; no table detection or reconstruction.

Crop coordinates are normalized [left, top, right, bottom] in the *rendered*
CropBox page, after PDF rotation. Pages are one-based. See references/tools.md.
"""
import argparse
import hashlib
import json
import math
import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image
from pypdf import PdfReader


def validate_manifest(data, page_count):
    if not isinstance(data, dict) or not isinstance(data.get("tables"), list):
        raise ValueError("Manifest must contain a tables list.")
    ids = set()
    for table in data["tables"]:
        table_id = table.get("id", "")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", table_id) or table_id in ids:
            raise ValueError(f"Invalid or duplicate table id: {table_id!r}")
        ids.add(table_id)
        if not isinstance(table.get("label"), str) or not table["label"].strip():
            raise ValueError(f"Missing label for {table_id}.")
        if not isinstance(table.get("parts"), list) or not table["parts"]:
            raise ValueError(f"No image parts for {table_id}.")
        for part in table["parts"]:
            page = part.get("page")
            if type(page) is not int or not 1 <= page <= page_count:
                raise ValueError(f"Invalid one-based PDF page {page!r} for {table_id}.")
            crop = part.get("crop", [0, 0, 1, 1])
            if (not isinstance(crop, list) or len(crop) != 4
                    or any(type(x) not in (int, float) or not math.isfinite(x) for x in crop)):
                raise ValueError(f"Invalid normalized crop for {table_id}.")
            left, top, right, bottom = crop
            if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
                raise ValueError(f"Crop must be inside the rendered page: {table_id}.")
    return data["tables"]


def render(pdf, manifest, out_dir, dpi=200, pdftoppm=None):
    pdf, out_dir = Path(pdf).resolve(), Path(out_dir).resolve()
    if not 72 <= dpi <= 600:
        raise ValueError("DPI must be between 72 and 600.")
    executable = pdftoppm or shutil.which("pdftoppm")
    if not executable:
        raise RuntimeError("pdftoppm is unavailable; use the bundled Poppler path or --pdftoppm.")
    reader = PdfReader(str(pdf))
    if reader.is_encrypted and not reader.decrypt(""):
        raise ValueError("The supplied PDF is encrypted; request a readable copy.")
    tables = validate_manifest(manifest, len(reader.pages))
    expected_files = [out_dir / f"{table['id']}-{i:02d}.png"
                      for table in tables for i, _ in enumerate(table["parts"], 1)]
    expected_files.append(out_dir / "captures.json")
    existing = [str(path) for path in expected_files if path.exists()]
    if existing:
        raise FileExistsError("Use a fresh output directory; existing captures: " + ", ".join(existing))
    result = {
        "source": {"filename": pdf.name, "path": str(pdf), "pages": len(reader.pages),
                   "sha256": hashlib.sha256(pdf.read_bytes()).hexdigest()},
        "dpi": dpi,
        "coordinate_system": "normalized rendered CropBox, top-left origin, PDF rotation applied",
        "tables": [],
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    # Keep temporary renders in the requested writable output directory. Windows
    # sandbox temp paths are not necessarily writable by child executables.
    with tempfile.TemporaryDirectory(prefix=".render-", dir=out_dir) as temporary:
        if not Path(temporary).resolve().is_relative_to(out_dir):
            raise RuntimeError("Temporary render directory escaped the output directory.")
        cache = {}
        for table in tables:
            entry = {"id": table["id"], "label": table["label"], "parts": []}
            for index, part in enumerate(table["parts"], 1):
                page = part["page"]
                if page not in cache:
                    prefix = Path(temporary) / f"page-{page}"
                    command = [str(executable), "-f", str(page), "-l", str(page), "-singlefile",
                               "-cropbox", "-r", str(dpi), "-png", str(pdf), str(prefix)]
                    completed = subprocess.run(command, capture_output=True, text=True,
                                               encoding="utf-8", errors="replace", timeout=120)
                    if completed.returncode:
                        raise RuntimeError(f"PDF rendering failed on page {page}: {completed.stderr.strip()}")
                    cache[page] = prefix.with_suffix(".png")
                crop = part.get("crop", [0, 0, 1, 1])
                filename = f"{table['id']}-{index:02d}.png"
                with Image.open(cache[page]) as source:
                    width, height = source.size
                    # Floor left/top and ceil right/bottom to retain boundary pixels.
                    box = (math.floor(crop[0] * width), math.floor(crop[1] * height),
                           math.ceil(crop[2] * width), math.ceil(crop[3] * height))
                    region = source.crop(box).convert("RGB")
                    region.save(out_dir / filename, "PNG")
                    entry["parts"].append({
                        "page": page, "crop": crop, "image": filename,
                        "width": region.width, "height": region.height,
                        "rendered_page_size": [width, height], "pixel_crop": list(box),
                        "caption": part.get("caption", f"PDF p. {page}"),
                    })
            result["tables"].append(entry)
    (out_dir / "captures.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--dpi", type=int, default=200)
    parser.add_argument("--pdftoppm")
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
    result = render(args.pdf, data, args.out, args.dpi, args.pdftoppm)
    print(json.dumps({"tables": len(result["tables"]),
                      "image_parts": sum(len(t["parts"]) for t in result["tables"]),
                      "captures": str((args.out / "captures.json").resolve())}))


if __name__ == "__main__":
    main()
