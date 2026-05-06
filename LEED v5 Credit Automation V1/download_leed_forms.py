#!/usr/bin/env python3
"""
LEED v5 Credit Form Downloader
================================
Downloads all LEED v5 NC credit form pages as HTML from arc-app.gbci.org.
Uses Browser Use Cloud API (https://api.browser-use.com) to handle login
and any CAPTCHA challenges automatically.

Usage:
    python download_leed_forms.py

Output:
    leed-forms-html/<category>/<credit_id>-<credit-name>.html

Set env vars to override credentials:
    BROWSER_USE_API_KEY, LEED_EMAIL, LEED_PASSWORD
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

# ── Configuration ──────────────────────────────────────────────────────────────
BROWSER_USE_API_KEY = os.getenv(
    "BROWSER_USE_API_KEY",
    "bu_hVoABz8LmTqB0fr_rXUrQZIRiLLSQAI_bGjS9UWed08",
)
LEED_EMAIL    = os.getenv("LEED_EMAIL",    "vandana.ravi@red-eng.com")
LEED_PASSWORD = os.getenv("LEED_PASSWORD", "Artify2032$$")
LEED_BASE_URL = "https://arc-app.gbci.org/projects/list/sample-forms"
BU_API        = "https://api.browser-use.com/api/v3"
OUTPUT_DIR    = Path(__file__).parent / "leed-forms-html"

BU_HEADERS = {
    "X-Browser-Use-API-Key": BROWSER_USE_API_KEY,
    "Content-Type": "application/json",
}

# ── LEED v5 NC Credit Catalog ──────────────────────────────────────────────────
CREDITS = [
    # Project Information
    {"id": "PI",   "category": "pi", "name": "Project Information"},
    # Integrative Process
    {"id": "IPp1", "category": "ip", "name": "Climate Resilience Assessment"},
    {"id": "IPp2", "category": "ip", "name": "Human Impact Assessment"},
    {"id": "IPp3", "category": "ip", "name": "Carbon Assessment"},
    {"id": "IPc1", "category": "ip", "name": "Integrative Design Process"},
    # Location and Transportation
    {"id": "LTc1", "category": "lt", "name": "Sensitive Land Protection"},
    {"id": "LTc2", "category": "lt", "name": "Equitable Development"},
    {"id": "LTc3", "category": "lt", "name": "Compact and Connected Development"},
    {"id": "LTc4", "category": "lt", "name": "Transportation Demand Management"},
    {"id": "LTc5", "category": "lt", "name": "Electric Vehicles"},
    # Sustainable Sites
    {"id": "SSp1", "category": "ss", "name": "Minimized Site Disturbance"},
    {"id": "SSc1", "category": "ss", "name": "Biodiverse Habitat"},
    {"id": "SSc2", "category": "ss", "name": "Accessible Outdoor Space"},
    {"id": "SSc3", "category": "ss", "name": "Rainwater Management"},
    {"id": "SSc4", "category": "ss", "name": "Enhanced Resilient Site Design"},
    {"id": "SSc5", "category": "ss", "name": "Heat Island Reduction"},
    {"id": "SSc6", "category": "ss", "name": "Light Pollution Reduction"},
    # Water Efficiency
    {"id": "WEp1", "category": "we", "name": "Water Metering and Reporting"},
    {"id": "WEp2", "category": "we", "name": "Minimum Water Efficiency"},
    {"id": "WEc1", "category": "we", "name": "Water Metering and Leak Detection"},
    {"id": "WEc2", "category": "we", "name": "Enhanced Water Efficiency"},
    # Energy and Atmosphere
    {"id": "EAp1", "category": "ea", "name": "Operational Carbon Projection and Decarbonization Plan"},
    {"id": "EAp2", "category": "ea", "name": "Minimum Energy Efficiency"},
    {"id": "EAp3", "category": "ea", "name": "Fundamental Commissioning"},
    {"id": "EAp4", "category": "ea", "name": "Energy Metering and Reporting"},
    {"id": "EAp5", "category": "ea", "name": "Fundamental Refrigerant Management"},
    {"id": "EAc1", "category": "ea", "name": "Electrification"},
    {"id": "EAc2", "category": "ea", "name": "Reduce Peak Thermal Loads"},
    {"id": "EAc3", "category": "ea", "name": "Enhanced Energy Efficiency"},
    {"id": "EAc4", "category": "ea", "name": "Renewable Energy"},
    {"id": "EAc5", "category": "ea", "name": "Enhanced Commissioning"},
    {"id": "EAc6", "category": "ea", "name": "Grid Interactive"},
    {"id": "EAc7", "category": "ea", "name": "Enhanced Refrigerant Management"},
    # Material and Resources
    {"id": "MRp1", "category": "mr", "name": "Planning for Zero Waste Operations"},
    {"id": "MRp2", "category": "mr", "name": "Quantify and Assess Embodied Carbon"},
    {"id": "MRc1", "category": "mr", "name": "Building and Materials Reuse"},
    {"id": "MRc2", "category": "mr", "name": "Reduce Embodied Carbon"},
    {"id": "MRc3", "category": "mr", "name": "Low-Emitting Materials"},
    {"id": "MRc4", "category": "mr", "name": "Building Product Selection and Procurement"},
    {"id": "MRc5", "category": "mr", "name": "Construction and Demolition Waste Diversion"},
    # Indoor Environmental Quality
    {"id": "EQp1", "category": "eq", "name": "Construction Management"},
    {"id": "EQp2", "category": "eq", "name": "Fundamental Air Quality"},
    {"id": "EQp3", "category": "eq", "name": "No Smoking or Vehicle Idling"},
    {"id": "EQc1", "category": "eq", "name": "Enhanced Air Quality"},
    {"id": "EQc2", "category": "eq", "name": "Occupant Experience"},
    {"id": "EQc3", "category": "eq", "name": "Accessibility and Inclusion"},
    {"id": "EQc4", "category": "eq", "name": "Resilient Spaces"},
    {"id": "EQc5", "category": "eq", "name": "Air Quality Testing and Monitoring"},
    # Project Priorities
    {"id": "PR",   "category": "pr", "name": "Project Priorities"},
]

# ── Candidate URL patterns to try (before asking the agent) ──────────────────
def guess_urls(credit: dict) -> list[str]:
    """Return a prioritised list of URL guesses to try with a HEAD request."""
    cat = credit["category"]
    cid = credit["id"].lower()
    name_slug = credit["name"].lower().replace(" ", "-").replace("/", "-").replace(",", "")
    base = LEED_BASE_URL.rstrip("/")
    return [
        f"{base}/{cat}/{cid}",
        f"{base}/{cat}/{name_slug}",
        f"{base}/{cid}",
        f"{base}/{name_slug}",
    ]


def resolve_url(credit: dict, session: requests.Session) -> str | None:
    """Try known URL patterns via HTTP HEAD; return the first 200/302."""
    for url in guess_urls(credit):
        try:
            r = session.head(url, allow_redirects=True, timeout=10)
            if r.status_code < 400:
                return r.url
        except requests.RequestException:
            pass
    return None


# ── Browser Use API helpers ────────────────────────────────────────────────────
def bu_post(path: str, payload: dict, retries: int = 6) -> dict:
    for attempt in range(retries):
        try:
            r = requests.post(f"{BU_API}{path}", headers=BU_HEADERS, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            wait = 15 * (attempt + 1)
            print(f"  [network] POST {exc.__class__.__name__} – retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"POST {path} failed after {retries} attempts")


def bu_get(path: str, retries: int = 8) -> dict:
    for attempt in range(retries):
        try:
            r = requests.get(f"{BU_API}{path}", headers=BU_HEADERS, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            wait = 15 * (attempt + 1)
            print(f"  [network] GET {exc.__class__.__name__} – retry in {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"GET {path} failed after {retries} attempts")


def wait_for_session(session_id: str, max_wait: int = 600) -> dict:
    """
    Poll until the Browser Use session reaches a terminal or idle-after-task state.
    Terminal:  stopped | timed_out | error
    Idle-done: status==idle AND isTaskSuccessful is not None (keepAlive session)
    """
    start = time.time()
    last_step = -1
    while time.time() - start < max_wait:
        try:
            data = bu_get(f"/sessions/{session_id}")
        except RuntimeError as exc:
            print(f"    [poll error] {exc} – continuing")
            time.sleep(20)
            continue
        status = data["status"]
        step   = data.get("stepCount", 0)

        if step != last_step:
            summary = (data.get("lastStepSummary") or "")[:100]
            print(f"    step {step:>3} [{status}] {summary}")
            last_step = step

        # Terminal states
        if status in ("stopped", "timed_out", "error"):
            return data
        # keepAlive: task done → session goes back to idle with isTaskSuccessful set
        if status == "idle" and data.get("isTaskSuccessful") is not None:
            return data

        time.sleep(5)

    raise TimeoutError(f"Session {session_id} did not complete within {max_wait}s")


def dispatch(session_id: str, task: str) -> dict:
    """Dispatch a new task to an existing idle keepAlive session."""
    return bu_post("/sessions", {
        "sessionId": session_id,
        "task":      task,
        "keepAlive": True,
    })


# ── Phase 1: Login + URL discovery ────────────────────────────────────────────
DISCOVERY_TASK = f"""
Step 1 – Login:
Go to https://auth.gbci.org (or wherever the login page is).
If you land on a login page at any point:
  - Enter email: {LEED_EMAIL}
  - Enter password: {LEED_PASSWORD}
  - Solve any CAPTCHA that appears
  - Click Login / Sign In
  - Wait for the dashboard to load

Step 2 – Navigate to the sample forms list:
Go to: {LEED_BASE_URL}
You should see a list of LEED v5 rating system sample projects/forms.

Step 3 – Find the LEED v5 New Construction (NC) entry:
Look for a project or form labelled "LEED v5" or "LEED v5 New Construction" or similar.
Click on it to open the project scorecard.

Step 4 – Click every credit in the left-hand sidebar:
The scorecard has a sidebar with categories: PI, IP, LT, SS, WE, EA, MR, EQ, PR.
Click EVERY category header AND every prerequisite/credit listed under it.
After each click, record the full browser URL for that credit page.

Step 5 – Return results:
Return a JSON object:
{{
  "login_successful": true,
  "base_url": "<the common URL prefix>",
  "credits": [
    {{"id": "IPp1", "url": "<full URL of that credit form>"}},
    {{"id": "LTc1", "url": "<full URL>"}},
    ...
  ]
}}

Include ALL credits you visited. Use the exact credit IDs: PI, IPp1, IPp2, IPp3, IPc1,
LTc1–LTc5, SSp1, SSc1–SSc6, WEp1, WEp2, WEc1–WEc2, EAp1–EAp5, EAc1–EAc7,
MRp1–MRp2, MRc1–MRc5, EQp1–EQp3, EQc1–EQc5, PR.
If you cannot determine the URL for a credit, omit it rather than guessing.
"""


def phase1_login_and_discover() -> tuple[str, dict[str, str]]:
    """
    Create a keepAlive Browser Use session, login, and collect credit URLs.
    Returns (session_id, {credit_id: url}).
    """
    print("\n=== Phase 1: Login + URL discovery ===")
    session = bu_post("/sessions", {
        "task":      DISCOVERY_TASK,
        "keepAlive": True,
        "model":     "claude-sonnet-4.6",
        "outputSchema": {
            "type": "object",
            "properties": {
                "login_successful": {"type": "boolean"},
                "base_url":         {"type": "string"},
                "credits": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id":  {"type": "string"},
                            "url": {"type": "string"},
                        },
                        "required": ["id", "url"],
                    },
                },
            },
        },
    })

    session_id = session["id"]
    print(f"  Session ID : {session_id}")
    print(f"  Live view  : {session.get('liveUrl') or 'N/A'}")

    result  = wait_for_session(session_id, max_wait=3600)
    output  = result.get("output") or {}

    if isinstance(output, str):
        try:
            output = json.loads(output)
        except json.JSONDecodeError:
            print("  Warning: output was not valid JSON; URL map will be empty")
            output = {}

    url_map: dict[str, str] = {}
    if isinstance(output, dict):
        for item in output.get("credits", []):
            if item.get("id") and item.get("url"):
                url_map[item["id"]] = item["url"]

    print(f"  Discovered {len(url_map)} credit URLs from the agent")
    return session_id, url_map


# ── Phase 2: Download each credit form ────────────────────────────────────────
def build_nav_task(credit: dict, url: str | None) -> str:
    if url:
        nav = f"Navigate to: {url}"
    else:
        nav = (
            f"Navigate to the LEED v5 credit form for '{credit['name']}' "
            f"(credit ID: {credit['id']}) under category "
            f"'{credit['category'].upper()}'. "
            f"Start from: {LEED_BASE_URL} and click the correct entry in the "
            f"left-hand navigation sidebar."
        )

    return f"""
{nav}

Wait for the page to fully load (all form fields, tables, and panels visible).
Then scroll to the bottom of the page to trigger any lazy-loaded content.

Execute the following JavaScript in the browser and return its result as your
final output (raw HTML only, no markdown fences or explanation):

    document.documentElement.outerHTML
"""


def download_credit_html(session_id: str, credit: dict, url: str | None, max_wait: int = 600) -> str | None:
    """Dispatch a page-capture task and return the HTML string, or None on failure."""
    try:
        dispatch(session_id, build_nav_task(credit, url))
        result = wait_for_session(session_id, max_wait=max_wait)
        html   = result.get("output") or ""
        if isinstance(html, (dict, list)):
            html = json.dumps(html)
        return str(html) if html else None
    except Exception as exc:
        print(f"    ERROR: {exc}")
        return None


# ── Resume support ─────────────────────────────────────────────────────────────
def load_progress(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"downloaded": [], "failed": [], "session_id": None, "url_map": {}}


def save_progress(path: Path, progress: dict) -> None:
    path.write_text(json.dumps(progress, indent=2))


# ── Main ───────────────────────────────────────────────────────────────────────
def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    progress_file = OUTPUT_DIR / "_progress.json"
    progress      = load_progress(progress_file)

    print(f"Output directory: {OUTPUT_DIR.absolute()}")

    # Phase 1 – only if we don't have a running session from a previous run
    session_id: str = progress.get("session_id") or ""
    url_map: dict[str, str] = progress.get("url_map") or {}

    if not session_id:
        session_id, url_map = phase1_login_and_discover()
        progress["session_id"] = session_id
        progress["url_map"]    = url_map
        save_progress(progress_file, progress)

        # Persist URL map separately for quick reference
        (OUTPUT_DIR / "_url_map.json").write_text(json.dumps(url_map, indent=2))
    else:
        print(f"\n=== Resuming session {session_id} ===")
        print(f"  {len(url_map)} URLs already known, "
              f"{len(progress['downloaded'])} credits already downloaded")

    already_done: set[str] = set(progress.get("downloaded", []))

    # Phase 2 – download each credit form
    print(f"\n=== Phase 2: Downloading {len(CREDITS)} credit forms ===")
    for idx, credit in enumerate(CREDITS, 1):
        credit_id = credit["id"]

        if credit_id in already_done:
            print(f"  [{idx:>2}/{len(CREDITS)}] skip (already done): {credit_id}")
            continue

        credit_url  = url_map.get(credit_id)
        safe_name   = (
            credit["name"]
            .lower()
            .replace(" ", "-")
            .replace("/", "-")
            .replace(",", "")
        )
        filename    = f"{credit_id.lower()}-{safe_name}.html"
        output_path = OUTPUT_DIR / credit["category"] / filename

        print(f"\n  [{idx:>2}/{len(CREDITS)}] {credit_id}: {credit['name']}")
        if credit_url:
            print(f"    URL: {credit_url}")
        else:
            print("    URL: unknown — agent will navigate via sidebar")

        html = download_credit_html(session_id, credit, credit_url, max_wait=600)

        if html and len(html) > 1000:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(html, encoding="utf-8")
            print(f"    ✓ saved {len(html):,} chars → {output_path.name}")
            progress["downloaded"].append(credit_id)
        else:
            size = len(html) if html else 0
            print(f"    ✗ failed or too short ({size} chars)")
            progress["failed"].append(credit_id)

        save_progress(progress_file, progress)
        time.sleep(2)   # brief pause between dispatches

    # ── Summary ────────────────────────────────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"✅  Downloaded : {len(progress['downloaded'])} credits")
    print(f"❌  Failed     : {len(progress['failed'])} credits")
    if progress["failed"]:
        print(f"    IDs        : {', '.join(progress['failed'])}")
    print(f"\nAll files in: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
