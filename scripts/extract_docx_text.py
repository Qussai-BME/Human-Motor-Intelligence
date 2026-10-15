#!/usr/bin/env python3
"""Extract paragraph text from a DOCX using only the Python standard library."""
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_docx", type=Path)
    parser.add_argument("output_txt", type=Path)
    args = parser.parse_args()
    with zipfile.ZipFile(args.input_docx) as archive:
        root = ET.fromstring(archive.read("word/document.xml"))
    paragraphs: list[str] = []
    for paragraph in root.iter(f"{W}p"):
        text = "".join(node.text or "" for node in paragraph.iter(f"{W}t")).strip()
        if text:
            paragraphs.append(text)
    args.output_txt.parent.mkdir(parents=True, exist_ok=True)
    args.output_txt.write_text("\n".join(paragraphs) + "\n", encoding="utf-8")
    print(f"paragraphs={len(paragraphs)} output={args.output_txt}")


if __name__ == "__main__":
    main()
