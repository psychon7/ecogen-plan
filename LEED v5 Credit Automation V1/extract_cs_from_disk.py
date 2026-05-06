#!/usr/bin/env python3
"""
Extract CS (Core and Shell) LEED v5 credit content from already-saved HTML
files on disk.  Re-uses the html_to_markdown() routine from extract_credits.py.

Source : leed-forms-html-cs/<category>/<slug>.html
Target : leed-forms-md/cs/<category>/<slug>.md

For numeric-ID files (770xxx) we infer the real credit code (e.g. PRINc3)
and a clean slug from the form text itself.

Usage:  python3 extract_cs_from_disk.py
"""
import re
from pathlib import Path

from extract_credits import html_to_markdown, RATINGS

ROOT       = Path(__file__).parent
SRC_DIR    = RATINGS["cs"]["html_dir"]
OUT_DIR    = RATINGS["cs"]["out_dir"]
BASE_URL   = RATINGS["cs"]["base_url"]
LABEL      = RATINGS["cs"]["label"]

CATEGORY_MAP = {                      # credit-code prefix -> output category
    "EA": "ea", "EQ": "eq", "LT": "lt", "MR": "mr",
    "SS": "ss", "WE": "we", "IP": "ip",
    "PR": "in", "IN": "in",            # priorities & innovation
}

def slugify(text: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return s[:80]


def parse_credit_meta(form_html: str, fallback_slug: str) -> dict:
    """
    Look at the form innerHTML and pull out:
      - credit_id   (e.g. EAp1, PRINc3, PRpc169)
      - title       (e.g. "Lead Risk Reduction")
    """
    text = re.sub(r"<[^>]+>", " ", form_html)
    text = re.sub(r"\s+", " ", text).strip()

    # Title sits between "arrow_back_ios_new" and "Not started" / "person Assign"
    m = re.search(
        r"arrow_back_ios_new\s+(.+?)\s+(?:Not started|In progress|Complete|person Assign|Mark ready)",
        text,
    )
    title = m.group(1).strip() if m else fallback_slug

    # Credit id sits before "| LEED v5 BD+C: Core and Shell"
    m = re.search(
        r"([A-Z]{2}(?:[a-z]{1,4})?\d+|PR[A-Za-z]{1,4}\d+|IN[A-Za-z]{1,4}\d+)\s*\|\s*LEED v5 BD\+C:\s*Core and Shell",
        text,
    )
    cid = m.group(1) if m else ""

    return {"credit_id": cid, "title": title}


def main():
    files = sorted(p for p in SRC_DIR.rglob("*.html") if p.parent.name != "_state")
    saved, skipped, no_form = 0, 0, 0

    for f in files:
        html = f.read_text(errors="ignore")
        m = re.search(r"<usgbc-credit-form[^>]*>.*?</usgbc-credit-form>",
                      html, re.DOTALL)
        if not m:
            no_form += 1
            continue
        form_outer = m.group(0)
        if len(form_outer) < 5000:
            no_form += 1
            continue

        category_in = f.parent.name           # ea, lt, mr, ss, other, ...
        slug_in     = f.stem                  # eap1-..., 770171-770171

        # Resolve credit_id + title + final category
        meta = parse_credit_meta(form_outer, slug_in)
        cid  = meta["credit_id"]
        title = meta["title"]

        if slug_in.split("-")[0].isdigit():
            # Numeric file: derive everything from form contents
            if not cid:
                # Could not parse code; place in 'in/' with title-based slug
                cat = "in"
                slug = slugify(title) or slug_in
            else:
                prefix = re.match(r"[A-Z]+", cid).group(0)[:2]
                cat = CATEGORY_MAP.get(prefix, "in")
                slug = f"{cid.lower()}-{slugify(title)}"
        else:
            cat  = category_in if category_in != "other" else CATEGORY_MAP.get(cid[:2], "in") if cid else "in"
            slug = slug_in

        arc_id_for_header = cid or slug_in.split("-")[0].upper()

        markdown = html_to_markdown(form_outer, arc_id_for_header, BASE_URL, LABEL)
        out_path = OUT_DIR / cat / f"{slug}.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        saved += 1
        print(f"  ✓ {f.relative_to(SRC_DIR)} → {out_path.relative_to(ROOT)} "
              f"({len(markdown):,} chars)  [{arc_id_for_header}: {title[:40]}]")

    print("\n" + "=" * 60)
    print(f"Total HTML files scanned : {len(files)}")
    print(f"  ✓ markdown written     : {saved}")
    print(f"  ⚠ no form / too small  : {no_form}")


if __name__ == "__main__":
    main()
