#!/usr/bin/env python3
"""
Fetch fresh presigned URLs one-by-one for missing NC files from workspace.
Workspace: 23b56bde-ddba-4e40-bd42-178cc1ebb7cf
"""
import json
import time
from pathlib import Path
import requests

BROWSER_USE_API_KEY = "bu_hVoABz8LmTqB0fr_rXUrQZIRiLLSQAI_bGjS9UWed08"
BU_API   = "https://api.browser-use.com/api/v3"
WS_ID    = "23b56bde-ddba-4e40-bd42-178cc1ebb7cf"
OUT_DIR  = Path(__file__).parent / "leed-forms-html"
HDRS     = {"X-Browser-Use-API-Key": BROWSER_USE_API_KEY}

CREDIT_META = {
    "PI":   ("pi",  "project-information"),
    "SSp1": ("ss",  "minimized-site-disturbance"),
    "SSc1": ("ss",  "biodiverse-habitat"),
    "SSc2": ("ss",  "accessible-outdoor-space"),
    "SSc3": ("ss",  "rainwater-management"),
    "SSc4": ("ss",  "enhanced-resilient-site-design"),
    "SSc5": ("ss",  "heat-island-reduction"),
    "SSc6": ("ss",  "light-pollution-reduction"),
    "WEp1": ("we",  "water-metering-and-reporting"),
    "WEp2": ("we",  "minimum-water-efficiency"),
    "WEc1": ("we",  "water-metering-and-leak-detection"),
    "WEc2": ("we",  "enhanced-water-efficiency"),
    "MRp1": ("mr",  "planning-for-zero-waste-operations"),
    "MRp2": ("mr",  "quantify-and-assess-embodied-carbon"),
    "MRc1": ("mr",  "building-and-materials-reuse"),
    "MRc2": ("mr",  "reduce-embodied-carbon"),
    "MRc3": ("mr",  "low-emitting-materials"),
    "MRc4": ("mr",  "building-product-selection-and-procurement"),
    "MRc5": ("mr",  "construction-and-demolition-waste-diversion"),
}

def fresh_url(credit_id: str) -> str | None:
    """Re-list the workspace file right now to get a fresh presigned URL."""
    r = requests.get(
        f"{BU_API}/workspaces/{WS_ID}/files",
        headers=HDRS,
        params={"prefix": f"{credit_id}.html", "includeUrls": "true", "limit": 5},
        timeout=60,
    )
    r.raise_for_status()
    files = r.json().get("files", [])
    for f in files:
        if Path(f["path"]).name == f"{credit_id}.html":
            return f.get("url")
    return None

def download(url: str, dest: Path) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    r = requests.get(url, timeout=120, stream=True)
    r.raise_for_status()
    with open(dest, "wb") as fh:
        for chunk in r.iter_content(65536):
            fh.write(chunk)
    return dest.stat().st_size

done, failed = [], []
for cid, (cat, slug) in CREDIT_META.items():
    dest = OUT_DIR / cat / f"{cid.lower()}-{slug}.html"
    if dest.exists() and dest.stat().st_size > 5000:
        print(f"  skip (exists {dest.stat().st_size:,}b): {dest.name}")
        done.append(cid)
        continue

    print(f"  ↓ {cid} ...", end=" ", flush=True)
    try:
        url = fresh_url(cid)
        if not url:
            print("no URL in workspace")
            failed.append(cid)
            continue
        size = download(url, dest)
        print(f"{size:,} bytes ✓")
        done.append(cid)
    except Exception as exc:
        print(f"FAIL: {exc}")
        failed.append(cid)
    time.sleep(1)

print(f"\n✅ {len(done)} downloaded/skipped  ❌ {len(failed)} failed")
if failed:
    print("Failed:", failed)
