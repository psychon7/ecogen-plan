#!/usr/bin/env python3
"""
Convert downloaded LEED credit HTML files to PDF using Playwright.
Reads from:  leed-forms-html/<category>/*.html
Writes to:   leed-forms-pdf/<category>/<same_name>.pdf

Usage:
    python3 html_to_pdf.py [--dir leed-forms-html-cs] [--out leed-forms-pdf-cs]

If --dir is not given, defaults to leed-forms-html (NC).
"""
import argparse
import sys
from pathlib import Path

def convert(html_dir: Path, pdf_dir: Path):
    html_files = sorted(html_dir.rglob("*.html"))
    if not html_files:
        print(f"No HTML files found in {html_dir}")
        return

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed. Run: pip install playwright && playwright install chromium")
        sys.exit(1)

    print(f"Converting {len(html_files)} HTML → PDF")
    print(f"  Input : {html_dir}")
    print(f"  Output: {pdf_dir}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        done, failed = 0, 0

        for html in html_files:
            rel = html.relative_to(html_dir)
            dest = pdf_dir / rel.parent / (html.stem + ".pdf")
            dest.parent.mkdir(parents=True, exist_ok=True)

            if dest.exists() and dest.stat().st_size > 5000:
                print(f"  skip: {rel}")
                continue

            print(f"  → {rel} ... ", end="", flush=True)
            try:
                page.goto(html.as_uri(), wait_until="networkidle", timeout=60000)
                page.pdf(
                    path=str(dest),
                    format="A4",
                    print_background=True,
                    margin={"top": "15mm", "bottom": "15mm",
                            "left": "15mm", "right": "15mm"},
                )
                size = dest.stat().st_size
                print(f"{size:,} bytes ✓")
                done += 1
            except Exception as exc:
                print(f"FAIL: {exc}")
                failed += 1

        browser.close()

    print(f"\n✅ {done} PDFs created  ❌ {failed} failed")
    print(f"Output: {pdf_dir.absolute()}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default="leed-forms-html",
                    help="HTML source directory (default: leed-forms-html)")
    ap.add_argument("--out", default="leed-forms-pdf",
                    help="PDF output directory (default: leed-forms-pdf)")
    args = ap.parse_args()

    base = Path(__file__).parent
    convert(base / args.dir, base / args.out)
