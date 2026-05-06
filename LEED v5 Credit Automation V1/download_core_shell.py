#!/usr/bin/env python3
"""
LEED v5 BD+C Core and Shell – Credit Form Downloader
======================================================
Uses Browser Use workspace approach (same as NC v3).
Discovers credits via login + sidebar navigation, then batch-saves all HTML files
to a workspace, then downloads them via fresh presigned URLs.

Usage:
    python3 download_core_shell.py

Output:
    leed-forms-html-cs/<category>/<credit_id>-<credit-name>.html
"""
import json
import os
import time
from pathlib import Path
import requests

BROWSER_USE_API_KEY = os.getenv("BROWSER_USE_API_KEY", "bu_hVoABz8LmTqB0fr_rXUrQZIRiLLSQAI_bGjS9UWed08")
LEED_EMAIL    = "vandana.ravi@red-eng.com"
LEED_PASSWORD = "Artify2032$$"
SAMPLE_LIST   = "https://arc-app.gbci.org/projects/list/sample-forms"
BU_API        = "https://api.browser-use.com/api/v3"
OUTPUT_DIR    = Path(__file__).parent / "leed-forms-html-cs"
STATE_FILE    = OUTPUT_DIR / "_state_cs.json"

BU_HEADERS = {"X-Browser-Use-API-Key": BROWSER_USE_API_KEY, "Content-Type": "application/json"}

# Core & Shell shares most credits with NC. Known credits:
# (will be fully discovered by agent, this is used for filename mapping)
CREDITS = [
    {"id": "PI",   "category": "pi", "name": "Project Information"},
    {"id": "IPp1", "category": "ip", "name": "Climate Resilience Assessment"},
    {"id": "IPp2", "category": "ip", "name": "Human Impact Assessment"},
    {"id": "IPp3", "category": "ip", "name": "Carbon Assessment"},
    {"id": "IPc1", "category": "ip", "name": "Integrative Design Process"},
    {"id": "LTc1", "category": "lt", "name": "Sensitive Land Protection"},
    {"id": "LTc2", "category": "lt", "name": "Equitable Development"},
    {"id": "LTc3", "category": "lt", "name": "Compact and Connected Development"},
    {"id": "LTc4", "category": "lt", "name": "Transportation Demand Management"},
    {"id": "LTc5", "category": "lt", "name": "Electric Vehicles"},
    {"id": "SSp1", "category": "ss", "name": "Minimized Site Disturbance"},
    {"id": "SSc1", "category": "ss", "name": "Biodiverse Habitat"},
    {"id": "SSc2", "category": "ss", "name": "Accessible Outdoor Space"},
    {"id": "SSc3", "category": "ss", "name": "Rainwater Management"},
    {"id": "SSc4", "category": "ss", "name": "Enhanced Resilient Site Design"},
    {"id": "SSc5", "category": "ss", "name": "Heat Island Reduction"},
    {"id": "SSc6", "category": "ss", "name": "Light Pollution Reduction"},
    {"id": "WEp1", "category": "we", "name": "Water Metering and Reporting"},
    {"id": "WEp2", "category": "we", "name": "Minimum Water Efficiency"},
    {"id": "WEc1", "category": "we", "name": "Water Metering and Leak Detection"},
    {"id": "WEc2", "category": "we", "name": "Enhanced Water Efficiency"},
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
    {"id": "MRp1", "category": "mr", "name": "Planning for Zero Waste Operations"},
    {"id": "MRp2", "category": "mr", "name": "Quantify and Assess Embodied Carbon"},
    {"id": "MRc1", "category": "mr", "name": "Building and Materials Reuse"},
    {"id": "MRc2", "category": "mr", "name": "Reduce Embodied Carbon"},
    {"id": "MRc3", "category": "mr", "name": "Low-Emitting Materials"},
    {"id": "MRc4", "category": "mr", "name": "Building Product Selection and Procurement"},
    {"id": "MRc5", "category": "mr", "name": "Construction and Demolition Waste Diversion"},
    {"id": "EQp1", "category": "eq", "name": "Construction Management"},
    {"id": "EQp2", "category": "eq", "name": "Fundamental Air Quality"},
    {"id": "EQp3", "category": "eq", "name": "No Smoking or Vehicle Idling"},
    {"id": "EQc1", "category": "eq", "name": "Enhanced Air Quality"},
    {"id": "EQc2", "category": "eq", "name": "Occupant Experience"},
    {"id": "EQc3", "category": "eq", "name": "Accessibility and Inclusion"},
    {"id": "EQc4", "category": "eq", "name": "Resilient Spaces"},
    {"id": "EQc5", "category": "eq", "name": "Air Quality Testing and Monitoring"},
    {"id": "569861", "category": "pr", "name": "Project Priorities"},
]
CREDIT_META = {c["id"]: c for c in CREDITS}

EXISTING_WORKSPACE_ID = "23b56bde-ddba-4e40-bd42-178cc1ebb7cf"  # reuse NC workspace

BATCH_TASK = f"""
You are a web automation agent.

## Step 1 – Login
Navigate to: {SAMPLE_LIST}
Select or click the "LEED v5 BD+C Core and Shell" project/form from the list.
If you hit a login page first:
  - Email: {LEED_EMAIL}
  - Password: {LEED_PASSWORD}
  - Solve any CAPTCHA, click Login

## Step 2 – Discover and save all credit form pages
Once inside the Core and Shell project scorecard:
1. First, use JavaScript to get the current URL pattern for credits — click a few sidebar items (PI, then IPp1, then LTc1) and note the URL pattern.
2. For EACH credit in the sidebar (all of: PI, IP prerequisites/credits, LT, SS, WE, EA, MR, EQ, PR):
   a) Navigate to the credit's URL
   b) Wait 3 seconds
   c) Use page.content() to get HTML and save it to /workspace/CS_<CREDIT_ID>.html
      Prefix every file with CS_ (e.g. CS_IPp1.html, CS_LTc1.html, CS_EAc3.html)
      For Project Priorities, use CS_569861.html

Process ALL credits visible in the left sidebar. Do not skip any.

## Step 3 – Return summary
Return JSON:
{{
  "rating_system": "LEED v5 BD+C Core and Shell",
  "base_url": "<discovered base URL pattern>",
  "saved": ["CS_PI", "CS_IPp1", ...],
  "failed": []
}}
"""

def _get(path, params=None, retries=8):
    for i in range(retries):
        try:
            r = requests.get(f"{BU_API}{path}", headers=BU_HEADERS, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            wait = 15*(i+1)
            print(f"  [GET retry {i+1}] {e.__class__.__name__} – wait {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"GET {path} failed")

def _post(path, payload, retries=6):
    for i in range(retries):
        try:
            r = requests.post(f"{BU_API}{path}", headers=BU_HEADERS, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
            wait = 15*(i+1)
            print(f"  [POST retry {i+1}] {e.__class__.__name__} – wait {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"POST {path} failed")

def wait_done(session_id, max_wait=7200):
    start = time.time()
    last_step = -1
    while time.time() - start < max_wait:
        try:
            d = _get(f"/sessions/{session_id}")
        except RuntimeError as e:
            print(f"  [poll error] {e}")
            time.sleep(30)
            continue
        step = d.get("stepCount", 0)
        status = d["status"]
        if step != last_step:
            print(f"  step {step:>4} [{status}] {(d.get('lastStepSummary') or '')[:90]}")
            last_step = step
        if status in ("stopped", "timed_out", "error"):
            return d
        if status == "idle" and d.get("isTaskSuccessful") is not None:
            return d
        time.sleep(6)
    raise TimeoutError(f"Session {session_id} not done after {max_wait}s")

def fresh_url_for(workspace_id, cs_filename):
    """cs_filename = 'CS_MRc1.html' etc."""
    data = _get(f"/workspaces/{workspace_id}/files",
                params={"prefix": cs_filename, "includeUrls": "true", "limit": 5})
    for f in data.get("files", []):
        if Path(f["path"]).name == cs_filename:
            return f.get("url")
    return None

def download_file(url, dest):
    dest.parent.mkdir(parents=True, exist_ok=True)
    for i in range(6):
        try:
            r = requests.get(url, timeout=120, stream=True)
            r.raise_for_status()
            with open(dest, "wb") as fh:
                for chunk in r.iter_content(65536):
                    fh.write(chunk)
            return dest.stat().st_size
        except Exception as e:
            print(f"    [dl retry {i+1}] {e}")
            time.sleep(10*(i+1))
    raise RuntimeError(f"download failed: {url[:80]}")

def load_state():
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"workspace_id": None, "session_id": None}

def save_state(s):
    STATE_FILE.write_text(json.dumps(s, indent=2))

def main():
    OUTPUT_DIR.mkdir(exist_ok=True)
    state = load_state()

    if not state.get("session_id"):
        # Reuse existing NC workspace (402 if we try to create new on free plan)
        workspace_id = EXISTING_WORKSPACE_ID
        state["workspace_id"] = workspace_id
        save_state(state)
        print(f"\n=== Reusing existing workspace: {workspace_id} ===")
        print("    (CS_ prefix used for all Core & Shell files)")

        print("\n=== Running batch download session ===")
        session = _post("/sessions", {
            "task":        BATCH_TASK,
            "workspaceId": workspace_id,
            "model":       "claude-sonnet-4.6",
            "keepAlive":   False,
            "maxCostUsd":  15,
        })
        session_id = session["id"]
        state["session_id"] = session_id
        save_state(state)
        print(f"  Session: {session_id}")
        print(f"  Live:    {session.get('liveUrl') or 'N/A'}")

        result = wait_done(session_id)
        print(f"\n  Status: {result['status']}  Success: {result.get('isTaskSuccessful')}")
        out = result.get("output") or {}
        if isinstance(out, str):
            try: out = json.loads(out)
            except: out = {}
        if isinstance(out, dict):
            print(f"  Base URL: {out.get('base_url','?')}")
            print(f"  Saved {len(out.get('saved',[]))} credits")
    else:
        print(f"\n=== Resuming (workspace {state['workspace_id']}) ===")

    workspace_id = state["workspace_id"]

    # List ALL files in workspace
    print(f"\n=== Downloading files from workspace {workspace_id} ===")
    files_resp = _get(f"/workspaces/{workspace_id}/files", params={"limit": 100})
    all_files = files_resp.get("files", [])
    print(f"  {len(all_files)} file(s) found")

    downloaded, skipped, failed = [], [], []
    # Only process CS_ prefixed files (Core & Shell)
    cs_files = [f for f in all_files if Path(f["path"]).name.startswith("CS_")]
    print(f"  {len(cs_files)} Core & Shell file(s) found")

    for finfo in cs_files:
        fname = Path(finfo["path"]).name          # e.g. CS_MRc1.html
        credit_id = fname.replace("CS_", "").replace(".html", "")  # e.g. MRc1
        meta = CREDIT_META.get(credit_id) or {"category": "other", "name": credit_id.lower()}
        safe_name = (meta["name"].lower()
                     .replace(" ", "-").replace("/", "-").replace(",", ""))
        dest = OUTPUT_DIR / meta["category"] / f"{credit_id.lower()}-{safe_name}.html"

        if dest.exists() and dest.stat().st_size > 5000:
            print(f"  skip: {dest.name}")
            skipped.append(credit_id)
            continue

        print(f"  ↓ {credit_id} ({fname}) ...", end=" ", flush=True)
        # Re-fetch fresh URL right now (avoids 60s S3 presigned URL expiry)
        url = fresh_url_for(workspace_id, fname)
        if not url:
            print("no URL")
            failed.append(credit_id)
            continue
        try:
            size = download_file(url, dest)
            print(f"{size:,} bytes ✓")
            downloaded.append(credit_id)
        except RuntimeError as e:
            print(f"FAIL: {e}")
            failed.append(credit_id)
        time.sleep(0.5)

    print(f"\n{'='*60}")
    print(f"✅  Downloaded : {len(downloaded)}")
    print(f"⏭   Skipped    : {len(skipped)}")
    print(f"❌  Failed     : {len(failed)}")
    print(f"\nFiles in: {OUTPUT_DIR.absolute()}")

if __name__ == "__main__":
    main()
