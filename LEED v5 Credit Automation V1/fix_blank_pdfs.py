#!/usr/bin/env python3
"""
Re-generate PDFs for the 6 credits that rendered as blank pages.
Uses a live authenticated Playwright session navigating directly to ARC URLs.

The blank PDFs occur because those HTML files are SPA skeletons – external JS
can't load from file://.  This script logs in via the browser, navigates to each
credit URL, waits for React hydration, then prints to PDF.

Usage:
    python3 fix_blank_pdfs.py
"""
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

LEED_EMAIL    = "vandana.ravi@red-eng.com"
LEED_PASSWORD = "Artify2032$$"
ARC_LOGIN_URL = "https://arc-app.gbci.org"
NC_BASE_URL   = "https://arc-app.gbci.org/projects/sample-forms/leed-v5-new-constructions"
PDF_DIR       = Path(__file__).parent / "leed-forms-pdf"

# Credits that rendered as blank PDFs – need live authenticated rendering
BLANK_CREDITS = [
    {"id": "EAc4",  "category": "ea", "slug": "eac4-renewable-energy",           "arc_id": "EAc4"},
    {"id": "EAc5",  "category": "ea", "slug": "eac5-enhanced-commissioning",     "arc_id": "EAc5"},
    {"id": "MRc1",  "category": "mr", "slug": "mrc1-building-and-materials-reuse","arc_id": "MRc1"},
    {"id": "MRc4",  "category": "mr", "slug": "mrc4-building-product-selection-and-procurement","arc_id": "MRc4"},
    {"id": "EQp1",  "category": "eq", "slug": "eqp1-construction-management",    "arc_id": "EQp1"},
    {"id": "569861","category": "pr", "slug": "569861-project-priorities",        "arc_id": "569861"},
]

def login(page):
    print("  Logging in to ARC (login.usgbc.org)...")
    page.goto(ARC_LOGIN_URL, wait_until="networkidle", timeout=60000)
    # Step 1: email
    page.fill('input[name="username"]', LEED_EMAIL, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    page.wait_for_load_state("networkidle", timeout=20000)
    # Step 2: password
    page.fill('input[name="password"]', LEED_PASSWORD, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    # Wait until we're back on arc-app.gbci.org
    page.wait_for_url("**/arc-app.gbci.org/**", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)
    import time; time.sleep(3)
    print(f"  Logged in. URL: {page.url[:80]}")

def print_credit_pdf(page, credit_id, dest: Path):
    url = f"{NC_BASE_URL}/{credit_id}"
    print(f"  Navigating to {url} ...")
    page.goto(url, wait_until="networkidle", timeout=90000)
    # Extra wait for React to fully hydrate the form
    time.sleep(5)
    # Try waiting for main content element
    try:
        page.wait_for_selector("main, .credit-form, .form-container, [class*='credit'], [class*='form']",
                               timeout=15000)
    except Exception:
        pass
    dest.parent.mkdir(parents=True, exist_ok=True)
    page.pdf(
        path=str(dest),
        format="A4",
        print_background=True,
        margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
    )
    size = dest.stat().st_size
    return size

def main():
    print(f"Fixing {len(BLANK_CREDITS)} blank PDFs via live ARC session\n")
    with sync_playwright() as p:
        # headless=False required: Auth0 blocks fully-headless browsers
        browser = p.chromium.launch(headless=False, slow_mo=200)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        login(page)

        done, failed = 0, 0
        for c in BLANK_CREDITS:
            dest = PDF_DIR / c["category"] / f"{c['slug']}.pdf"
            print(f"  → {c['id']} ({c['slug']}.pdf) ...", end=" ", flush=True)
            try:
                size = print_credit_pdf(page, c["arc_id"], dest)
                print(f"{size:,} bytes ✓")
                done += 1
            except Exception as exc:
                print(f"FAIL: {exc}")
                failed += 1

        browser.close()

    print(f"\n✅ {done} PDFs fixed  ❌ {failed} failed")

if __name__ == "__main__":
    main()
