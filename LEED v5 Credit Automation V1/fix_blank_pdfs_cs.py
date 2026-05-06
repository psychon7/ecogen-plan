#!/usr/bin/env python3
"""
Re-generate blank/tiny CS PDFs via authenticated Playwright session navigating
live ARC Core and Shell credit form pages.

Blank PDFs occur because the HTML files are Angular SPA skeletons – external JS
can't load from file://.  This script logs in with headless=False (required to
bypass Auth0 bot detection), then prints each credit to PDF.

Usage:
    python3 fix_blank_pdfs_cs.py
"""
import re
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LEED_EMAIL    = "vandana.ravi@red-eng.com"
LEED_PASSWORD = "Artify2032$$"
ARC_LOGIN_URL = "https://arc-app.gbci.org"
CS_BASE_URL   = "https://arc-app.gbci.org/projects/sample-forms/leed-v5-core-and-shell"
PDF_DIR       = Path(__file__).parent / "leed-forms-pdf-cs"

# Threshold: PDFs below this size are blank / SPA skeleton or header-only
# html_to_pdf.py good PDFs are 74-82KB; live fix-script good PDFs should be >50KB
# 32-36KB = only the ARC header loaded (not the form) → needs longer wait
BLANK_THRESHOLD = 70_000   # bytes

# Category-dir → uppercase prefix for ARC credit IDs
DIR_PREFIX = {
    "ea": "EA", "eq": "EQ", "in": "IN", "ip": "IP",
    "lt": "LT", "mr": "MR", "pi": "PI", "ss": "SS", "we": "WE",
}


def derive_arc_id(pdf_path: Path) -> str:
    """
    Derive the ARC credit ID from a PDF path inside leed-forms-pdf-cs/.
    Examples:
        ea/eac1-electrification.pdf    -> EAc1
        other/770170-770170.pdf        -> 770170
        other/ipc2-ipc2.pdf            -> IPc2
    """
    cat = pdf_path.parent.name          # e.g. "ea", "eq", "other"
    stem = pdf_path.stem                # e.g. "eac1-electrification"
    credit_part = stem.split("-")[0]    # e.g. "eac1"

    if credit_part.isdigit():
        return credit_part              # numeric ID used as-is

    # Convert first 2 letters to uppercase: "eac1" -> "EA" + "c1" = "EAc1"
    return credit_part[:2].upper() + credit_part[2:]


def collect_blank_pdfs() -> list[Path]:
    blanks = []
    for pdf in sorted(PDF_DIR.rglob("*.pdf")):
        if pdf.stat().st_size < BLANK_THRESHOLD:
            stem_credit = pdf.stem.split("-")[0]
            # Skip numeric IDs — they don't resolve via leed-v5-core-and-shell/<id>
            if stem_credit.isdigit():
                continue
            blanks.append(pdf)
    return blanks


def login(page):
    print("  Logging in to ARC (login.usgbc.org)...")
    page.goto(ARC_LOGIN_URL, wait_until="networkidle", timeout=60000)
    page.fill('input[name="username"]', LEED_EMAIL, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    page.wait_for_load_state("networkidle", timeout=20000)
    page.fill('input[name="password"]', LEED_PASSWORD, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    page.wait_for_url("**/arc-app.gbci.org/**", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(3)
    print(f"  Logged in. URL: {page.url[:80]}")


def print_credit_pdf(page, arc_id: str, dest: Path) -> int:
    url = f"{CS_BASE_URL}/{arc_id}"
    print(f"  Navigating to {url} ...", end=" ", flush=True)
    page.goto(url, wait_until="networkidle", timeout=90000)

    # Wait for the Angular form to fully render — up to 30 seconds
    # The form is ready when the page body has more than 500 chars of text
    for attempt in range(6):
        time.sleep(5)
        try:
            body_text = page.inner_text("body")
            if len(body_text) > 500:
                break
        except Exception:
            pass

    # Try waiting for a form-specific element as extra signal
    try:
        page.wait_for_selector(
            "main, .credit-form, .form-container, [class*='credit'], [class*='form']",
            timeout=10000,
        )
    except Exception:
        pass

    dest.parent.mkdir(parents=True, exist_ok=True)
    page.pdf(
        path=str(dest),
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
    )
    return dest.stat().st_size


def main():
    blanks = collect_blank_pdfs()
    if not blanks:
        print("No blank CS PDFs found — nothing to fix.")
        return

    print(f"Fixing {len(blanks)} blank CS PDFs via live ARC session\n")

    with sync_playwright() as p:
        # headless=False required: Auth0 blocks fully-headless browsers
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        login(page)

        done, failed = 0, 0
        for pdf_path in blanks:
            arc_id = derive_arc_id(pdf_path)
            label  = f"{arc_id} ({pdf_path.parent.name}/{pdf_path.name})"
            print(f"  → {label} ...", end=" ", flush=True)
            try:
                size = print_credit_pdf(page, arc_id, pdf_path)
                print(f"{size:,} bytes ✓")
                done += 1
            except Exception as exc:
                print(f"FAIL: {exc}")
                failed += 1

        browser.close()

    print(f"\n✅ {done} PDFs fixed  ❌ {failed} failed")


if __name__ == "__main__":
    main()
