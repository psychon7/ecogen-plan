#!/usr/bin/env python3
"""
Extract LEED v5 credit form content as Markdown + download all referenced
template files (.xlsx, .docx, etc.) from the live ARC sample-forms portal.

For each credit it produces:
    leed-forms-md/<rating>/<category>/<slug>.md
    leed-forms-md/<rating>/<category>/templates/<filename>

The credit list is derived from the already-downloaded HTML directories:
    leed-forms-html/      (NC – New Construction)
    leed-forms-html-cs/   (CS – Core and Shell)

Usage:
    python3 extract_credits.py            # both NC + CS
    python3 extract_credits.py --only nc
    python3 extract_credits.py --only cs
    python3 extract_credits.py --credits EAc1,WEp1
"""
import argparse
import re
import time
from pathlib import Path

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from playwright.sync_api import sync_playwright, Download

LEED_EMAIL    = "vandana.ravi@red-eng.com"
LEED_PASSWORD = "Artify2032$$"
ARC_LOGIN_URL = "https://arc-app.gbci.org"

ROOT = Path(__file__).parent
OUT_ROOT = ROOT / "leed-forms-md"

RATINGS = {
    "nc": {
        "html_dir":   ROOT / "leed-forms-html",
        "out_dir":    OUT_ROOT / "nc",
        "base_url":   "https://arc-app.gbci.org/projects/sample-forms/leed-v5-new-constructions",
        "label":      "LEED v5 BD+C: New Construction",
    },
    "cs": {
        "html_dir":   ROOT / "leed-forms-html-cs",
        "out_dir":    OUT_ROOT / "cs",
        "base_url":   "https://arc-app.gbci.org/projects/sample-forms/leed-v5-core-shell",
        "label":      "LEED v5 BD+C: Core and Shell",
    },
}

# ----------------------------------------------------------------------------
# Build credit list from existing HTML directory structure
# ----------------------------------------------------------------------------
def derive_arc_id(category: str, slug: str) -> str:
    """
    'ea' + 'eac1-electrification' -> 'EAc1'
    'other' + '770170-770170'     -> '770170'  (numeric – not navigable, skipped)
    """
    first = slug.split("-")[0]
    if first.isdigit():
        return first
    return first[:2].upper() + first[2:]


def discover_credits(html_dir: Path) -> list[dict]:
    creds = []
    for path in sorted(html_dir.rglob("*.html")):
        category = path.parent.name           # ea, eq, lt, mr, ss, we, ip, in, pi, other
        slug     = path.stem                  # eac1-electrification or 770170-770170
        arc_id   = derive_arc_id(category, slug)
        creds.append({"category": category, "slug": slug, "arc_id": arc_id})
    return creds


# ----------------------------------------------------------------------------
# Playwright helpers
# ----------------------------------------------------------------------------
def login(page):
    print("  Logging in to ARC...")
    page.goto(ARC_LOGIN_URL, wait_until="networkidle", timeout=60000)
    page.fill('input[name="username"]', LEED_EMAIL, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    page.wait_for_load_state("networkidle", timeout=20000)
    page.fill('input[name="password"]', LEED_PASSWORD, timeout=20000)
    page.click('button[type="submit"]', timeout=10000)
    page.wait_for_url("**/arc-app.gbci.org/**", timeout=30000)
    page.wait_for_load_state("networkidle", timeout=20000)
    time.sleep(3)
    print(f"  Logged in: {page.url}")


def expand_all_sections(page):
    """Click every collapsible accordion / chevron so its content is in DOM."""
    js = """
        () => {
            let n = 0;
            const sel = [
                'mat-expansion-panel-header[aria-expanded="false"]',
                'button[aria-expanded="false"]',
                '[class*="chevron_right"]',
            ];
            sel.forEach(s => document.querySelectorAll(s).forEach(el => {
                try { el.click(); n++; } catch(e) {}
            }));
            return n;
        }
    """
    # do a few passes – clicking some panels may reveal nested ones
    total = 0
    for _ in range(4):
        try:
            count = page.evaluate(js)
        except Exception:
            count = 0
        total += count
        if count == 0:
            break
        time.sleep(2)
    return total


def wait_for_credit_form(page, timeout_s: int = 30):
    """Wait until the usgbc-credit-form element exists and has substantive content."""
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        try:
            html = page.eval_on_selector(
                "usgbc-credit-form",
                "el => el ? el.innerHTML.length : 0",
            )
            if html and html > 5000:
                return True
        except Exception:
            pass
        time.sleep(0.5)
    return False


# ----------------------------------------------------------------------------
# HTML → Markdown conversion
# ----------------------------------------------------------------------------
def credit_form_html(page) -> str:
    try:
        return page.eval_on_selector("usgbc-credit-form", "el => el.outerHTML")
    except Exception:
        return ""


def html_to_markdown(html: str, arc_id: str, base_url: str, rating_label: str) -> str:
    """Clean Angular junk out of the HTML and convert to Markdown."""
    soup = BeautifulSoup(html, "html.parser")

    # Drop irrelevant elements
    for tag in soup.find_all(["script", "style", "noscript"]):
        tag.decompose()
    # Drop accessibility / icon-only nodes
    for tag in soup.find_all(class_=re.compile(r"(material-icons|aioa|accessibility|mat-mdc-tooltip|cdk-)")):
        tag.decompose()
    # Drop mat-icon elements (purely decorative)
    for tag in soup.find_all("mat-icon"):
        tag.decompose()
    # Strip mat-* attributes / Angular attributes
    for tag in soup.find_all(True):
        for attr in list(tag.attrs.keys()):
            if (attr.startswith("_ng") or attr.startswith("ng-") or
                attr.startswith("data-mat") or attr.startswith("mat") or
                attr.startswith("aria-") or attr in ("cdk-describedby-host",)):
                del tag.attrs[attr]
            elif attr == "class":
                # Drop classes; keep no styling
                del tag.attrs[attr]

    # Promote usgbc-* tags into divs/sections so markdownify handles them
    for tag in soup.find_all(re.compile(r"^usgbc-")):
        tag.name = "div"

    body = soup.decode_contents()
    text_md = md(body, heading_style="ATX", bullets="-", strip=["button"])

    # Collapse 3+ newlines to 2
    text_md = re.sub(r"\n{3,}", "\n\n", text_md)
    text_md = re.sub(r"[ \t]+\n", "\n", text_md)
    text_md = text_md.strip()

    front = (
        f"# {arc_id}\n\n"
        f"*Source:* `{base_url}/{arc_id}`  \n"
        f"*Rating system:* {rating_label}\n\n"
        f"---\n\n"
    )
    return front + text_md + "\n"


# ----------------------------------------------------------------------------
# Template downloads
# ----------------------------------------------------------------------------
def download_templates(page, dest_dir: Path) -> list[str]:
    """
    Click every template-download button on the page and save the resulting
    downloads into dest_dir.
    Returns the list of saved filenames.
    """
    saved = []
    try:
        buttons = page.query_selector_all("usgbc-dynamic-forms-template button")
    except Exception:
        return saved

    if not buttons:
        return saved

    dest_dir.mkdir(parents=True, exist_ok=True)

    for idx, btn in enumerate(buttons):
        try:
            label = (btn.get_attribute("aria-label") or
                     btn.inner_text() or
                     f"template_{idx}").strip()
        except Exception:
            label = f"template_{idx}"

        # Dismiss any overlay backdrops (mat-tooltip, snackbar, etc.) that might
        # be intercepting pointer events
        try:
            page.evaluate("""
                () => document.querySelectorAll('.cdk-overlay-backdrop, .cdk-overlay-container > div').forEach(el => el.remove())
            """)
            page.keyboard.press("Escape")
        except Exception:
            pass

        try:
            with page.expect_download(timeout=20000) as dl_info:
                # force=True bypasses overlay/visibility checks; dispatch via JS as fallback
                try:
                    btn.click(force=True, timeout=5000)
                except Exception:
                    btn.evaluate("el => el.click()")
            dl: Download = dl_info.value
            suggested = dl.suggested_filename or f"template_{idx}"
            target = dest_dir / suggested
            if target.exists():
                stem, suf = target.stem, target.suffix
                target = dest_dir / f"{stem}_{idx}{suf}"
            dl.save_as(str(target))
            saved.append(target.name)
            print(f"      ↓ template: {target.name}")
        except Exception as exc:
            print(f"      template '{label[:40]}' failed: {str(exc)[:100]}")

    return saved


# ----------------------------------------------------------------------------
# Main per-credit processing
# ----------------------------------------------------------------------------
def process_credit(page, credit: dict, rating_cfg: dict) -> dict:
    arc_id   = credit["arc_id"]
    category = credit["category"]
    slug     = credit["slug"]
    out_dir  = rating_cfg["out_dir"] / category
    md_path  = out_dir / f"{slug}.md"
    tpl_dir  = out_dir / "templates" / slug

    url = f"{rating_cfg['base_url']}/{arc_id}"
    page.goto(url, wait_until="networkidle", timeout=90000)

    if not wait_for_credit_form(page, timeout_s=40):
        return {"status": "no-form", "credit": arc_id}

    # Expand collapsible sections
    expanded = expand_all_sections(page)

    # Extra pause for late-rendering content
    time.sleep(2)

    # Extract the form HTML and convert
    html = credit_form_html(page)
    if not html or len(html) < 5000:
        return {"status": "empty", "credit": arc_id}

    markdown = html_to_markdown(html, arc_id, rating_cfg["base_url"], rating_cfg["label"])
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path.write_text(markdown, encoding="utf-8")

    # Download templates (if any)
    templates = download_templates(page, tpl_dir)

    return {
        "status":    "ok",
        "credit":    arc_id,
        "md":        str(md_path),
        "md_size":   md_path.stat().st_size,
        "templates": templates,
        "expanded":  expanded,
    }


# ----------------------------------------------------------------------------
# Entry point
# ----------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", choices=["nc", "cs"], help="Process only one rating system")
    ap.add_argument("--credits", help="Comma-separated credit IDs (e.g. EAc1,WEp1) – overrides discovery")
    ap.add_argument("--headless", action="store_true", help="Run headless (Auth0 may block this)")
    ap.add_argument("--force",    action="store_true", help="Re-process credits even if .md already exists")
    args = ap.parse_args()

    ratings = [args.only] if args.only else ["nc", "cs"]

    # Build work list
    work: list[tuple[str, dict]] = []
    filter_ids = set(c.strip() for c in args.credits.split(",")) if args.credits else None
    for r in ratings:
        cfg = RATINGS[r]
        creds = discover_credits(cfg["html_dir"])
        if filter_ids:
            creds = [c for c in creds if c["arc_id"] in filter_ids]
        for c in creds:
            md_path = cfg["out_dir"] / c["category"] / f"{c['slug']}.md"
            if md_path.exists() and not args.force:
                continue   # already done – resume mode
            work.append((r, c))

    print(f"Processing {len(work)} credits "
          f"({sum(1 for r,_ in work if r=='nc')} NC + {sum(1 for r,_ in work if r=='cs')} CS)",
          flush=True)

    OUT_ROOT.mkdir(exist_ok=True)
    results = {"ok": 0, "no-form": 0, "empty": 0, "error": 0}
    template_count = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless, slow_mo=150)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            accept_downloads=True,
        )
        page = context.new_page()

        login(page)

        for i, (r, c) in enumerate(work, 1):
            cfg = RATINGS[r]
            label = f"[{i}/{len(work)}] {r.upper()} {c['arc_id']:<8} ({c['category']}/{c['slug']})"
            print(f"\n  → {label}")
            try:
                res = process_credit(page, c, cfg)
                status = res["status"]
                results[status] = results.get(status, 0) + 1
                if status == "ok":
                    print(f"      ✓ md={res['md_size']:,} bytes  templates={len(res['templates'])}")
                    template_count += len(res["templates"])
                else:
                    print(f"      ⚠ {status}")
            except Exception as exc:
                results["error"] += 1
                print(f"      ✗ ERROR: {exc}")

        browser.close()

    print("\n" + "=" * 60)
    print(f"  ✅ ok       : {results.get('ok', 0)}")
    print(f"  ⚠  no-form  : {results.get('no-form', 0)}")
    print(f"  ⚠  empty    : {results.get('empty', 0)}")
    print(f"  ✗  error    : {results.get('error', 0)}")
    print(f"  ↓  templates: {template_count}")
    print(f"\nOutput: {OUT_ROOT}")


if __name__ == "__main__":
    main()
