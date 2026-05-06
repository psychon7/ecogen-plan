#!/usr/bin/env python3
"""
LEED v5 Credit Form Downloader  ·  v3  (workspace-based)
==========================================================
Strategy
--------
1.  Create a Browser Use workspace (persistent file storage).
2.  Run ONE Browser Use session that:
    a. Logs in to arc-app.gbci.org
    b. Iterates through every credit URL
    c. Saves document.documentElement.outerHTML to  /workspace/<CREDIT_ID>.html
3.  List workspace files and download them via presigned URLs.

Progress is saved so the script can be re-run to retry failed credits.

Usage:
    python3 download_leed_forms_v3.py

Output:
    leed-forms-html/<category>/<credit_id>-<credit-name>.html
"""

import json
import os
import time
from pathlib import Path

import requests

# ── Config ────────────────────────────────────────────────────────────────────
BROWSER_USE_API_KEY = os.getenv(
    "BROWSER_USE_API_KEY",
    "bu_hVoABz8LmTqB0fr_rXUrQZIRiLLSQAI_bGjS9UWed08",
)
LEED_EMAIL    = os.getenv("LEED_EMAIL",    "vandana.ravi@red-eng.com")
LEED_PASSWORD = os.getenv("LEED_PASSWORD", "Artify2032$$")
NC_BASE       = "https://arc-app.gbci.org/projects/sample-forms/leed-v5-new-constructions"
BU_API        = "https://api.browser-use.com/api/v3"
OUTPUT_DIR    = Path(__file__).parent / "leed-forms-html"
STATE_FILE    = OUTPUT_DIR / "_state_v3.json"

BU_HEADERS = {
    "X-Browser-Use-API-Key": BROWSER_USE_API_KEY,
    "Content-Type": "application/json",
}

# ── Credit catalogue ──────────────────────────────────────────────────────────
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

# The batch task script the agent will run inside the browser session
BATCH_TASK = f"""
You are a web automation agent. Follow these steps exactly.

## Step 1 – Login
Navigate to: {NC_BASE}/PI

If you are redirected to a login page:
- Enter email: {LEED_EMAIL}
- Enter password: {LEED_PASSWORD}
- Solve any CAPTCHA
- Click Login and wait for the dashboard to load

## Step 2 – Save all credit form pages to workspace files
For EACH of the following credit IDs, do this sequence:
  a) Navigate to: {NC_BASE}/<CREDIT_ID>
  b) Wait 3 seconds for the page to fully render
  c) Execute this Python code to save the page HTML:

     ```python
     from playwright.async_api import Page
     html = await page.content()
     with open(f'/workspace/<CREDIT_ID>.html', 'w', encoding='utf-8') as f:
         f.write(html)
     print(f'Saved <CREDIT_ID>.html  ({{len(html)}} bytes)')
     ```

Do this for ALL of these credit IDs in order:
PI, IPp1, IPp2, IPp3, IPc1,
LTc1, LTc2, LTc3, LTc4, LTc5,
SSp1, SSc1, SSc2, SSc3, SSc4, SSc5, SSc6,
WEp1, WEp2, WEc1, WEc2,
EAp1, EAp2, EAp3, EAp4, EAp5, EAc1, EAc2, EAc3, EAc4, EAc5, EAc6, EAc7,
MRp1, MRp2, MRc1, MRc2, MRc3, MRc4, MRc5,
EQp1, EQp2, EQp3, EQc1, EQc2, EQc3, EQc4, EQc5,
569861

## Step 3 – Report
After saving all files, return:
{{
  "saved": ["PI", "IPp1", ...list of successfully saved IDs...],
  "failed": [...any IDs where saving failed...]
}}
"""

# ── API helpers ───────────────────────────────────────────────────────────────
def _get(path: str, params: dict | None = None, retries: int = 8) -> dict:
    url = f"{BU_API}{path}"
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=BU_HEADERS, params=params, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            wait = 15 * (attempt + 1)
            print(f"  [GET retry {attempt+1}/{retries}] {exc.__class__.__name__} – wait {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"GET {path} failed after {retries} retries")


def _post(path: str, payload: dict, retries: int = 6) -> dict:
    url = f"{BU_API}{path}"
    for attempt in range(retries):
        try:
            r = requests.post(url, headers=BU_HEADERS, json=payload, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            wait = 15 * (attempt + 1)
            print(f"  [POST retry {attempt+1}/{retries}] {exc.__class__.__name__} – wait {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"POST {path} failed after {retries} retries")


def wait_done(session_id: str, max_wait: int = 7200) -> dict:
    start     = time.time()
    last_step = -1
    while time.time() - start < max_wait:
        try:
            d = _get(f"/sessions/{session_id}")
        except RuntimeError as exc:
            print(f"  [poll error] {exc}")
            time.sleep(30)
            continue
        step   = d.get("stepCount", 0)
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


# ── Workspace helpers ─────────────────────────────────────────────────────────
def create_workspace(name: str) -> str:
    resp = _post("/workspaces", {"name": name})
    wid  = resp["id"]
    print(f"  Workspace created: {wid}")
    return wid


def list_workspace_files(workspace_id: str) -> list[dict]:
    """Return all files (with presigned download URLs)."""
    files = []
    cursor = None
    while True:
        params: dict = {"includeUrls": "true", "limit": 100}
        if cursor:
            params["cursor"] = cursor
        resp   = _get(f"/workspaces/{workspace_id}/files", params=params)
        files += resp.get("files", [])
        if not resp.get("hasMore"):
            break
        cursor = resp.get("nextCursor")
    return files


def download_file(url: str, dest: Path) -> int:
    """Download a presigned URL to dest. Returns file size in bytes."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    for attempt in range(6):
        try:
            r = requests.get(url, timeout=120, stream=True)
            r.raise_for_status()
            with open(dest, "wb") as fh:
                for chunk in r.iter_content(chunk_size=65536):
                    fh.write(chunk)
            return dest.stat().st_size
        except (requests.exceptions.RequestException, OSError) as exc:
            wait = 10 * (attempt + 1)
            print(f"    [dl retry {attempt+1}] {exc} – wait {wait}s")
            time.sleep(wait)
    raise RuntimeError(f"Failed to download {url}")


# ── State persistence ─────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.exists():
        return json.loads(STATE_FILE.read_text())
    return {"workspace_id": None, "session_id": None, "saved": [], "failed": []}


def save_state(s: dict) -> None:
    STATE_FILE.write_text(json.dumps(s, indent=2))


# ── ID → credit meta lookup ───────────────────────────────────────────────────
CREDIT_META = {c["id"]: c for c in CREDITS}


# ── Main ──────────────────────────────────────────────────────────────────────
def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    state = load_state()

    # ── Phase 1: create workspace & run batch session ─────────────────────────
    if not state.get("session_id"):
        print("\n=== Phase 1: Create workspace ===")
        workspace_id = create_workspace("leed-v5-nc-forms")
        state["workspace_id"] = workspace_id
        save_state(state)

        print("\n=== Phase 2: Batch-download all credit pages ===")
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
        print(f"  Session : {session_id}")
        print(f"  Live    : {session.get('liveUrl') or 'N/A'}")

        result = wait_done(session_id)
        print(f"\n  Status  : {result['status']}")
        print(f"  Success : {result.get('isTaskSuccessful')}")
        output = result.get("output") or {}
        if isinstance(output, str):
            try:
                output = json.loads(output)
            except json.JSONDecodeError:
                output = {}
        if isinstance(output, dict):
            state["saved"]  = output.get("saved", [])
            state["failed"] = output.get("failed", [])
            save_state(state)
            print(f"  Agent saved  : {len(state['saved'])} credits")
            print(f"  Agent failed : {len(state['failed'])} credits")
    else:
        print(f"\n=== Resuming (session {state['session_id']}) ===")

    workspace_id = state["workspace_id"]
    if not workspace_id:
        print("ERROR: no workspace_id in state. Delete _state_v3.json and re-run.")
        return

    # ── Phase 3: list workspace files and download ────────────────────────────
    print(f"\n=== Phase 3: Downloading from workspace {workspace_id} ===")
    files = list_workspace_files(workspace_id)
    print(f"  Found {len(files)} file(s) in workspace")

    already_local = {c["id"] for c in CREDITS
                     if any(OUTPUT_DIR.rglob(f"{c['id'].lower()}-*.html"))}

    downloaded, skipped, failed = [], [], []
    for finfo in files:
        fpath = finfo["path"]          # e.g. "EAp1.html" or "workspace/EAp1.html"
        fname = Path(fpath).name       # "EAp1.html"
        credit_id = fname.replace(".html", "")

        meta = CREDIT_META.get(credit_id)
        if not meta:
            print(f"  skip unknown: {fname}")
            skipped.append(fname)
            continue

        safe_name  = (meta["name"].lower()
                      .replace(" ", "-")
                      .replace("/", "-")
                      .replace(",", ""))
        dest = OUTPUT_DIR / meta["category"] / f"{credit_id.lower()}-{safe_name}.html"

        if dest.exists() and dest.stat().st_size > 1000:
            print(f"  skip (exists): {dest.name}")
            skipped.append(credit_id)
            continue

        url = finfo.get("url")
        if not url:
            print(f"  no URL for {fname} — skipping")
            failed.append(credit_id)
            continue

        print(f"  ↓ {credit_id}: {dest.name} ...", end=" ", flush=True)
        try:
            size = download_file(url, dest)
            print(f"{size:,} bytes")
            downloaded.append(credit_id)
        except RuntimeError as exc:
            print(f"FAILED: {exc}")
            failed.append(credit_id)

    # ── Summary ───────────────────────────────────────────────────────────────
    total = len(CREDITS)
    print("\n" + "=" * 60)
    print(f"✅  Downloaded : {len(downloaded)}")
    print(f"⏭   Skipped    : {len(skipped)}")
    print(f"❌  Failed     : {len(failed)}")
    missing = [c["id"] for c in CREDITS
               if c["id"] not in downloaded and c["id"] not in skipped]
    if missing:
        print(f"\nMissing credits (not in workspace): {', '.join(missing)}")
        print("Re-run the script to retry, or check the agent's output.")
    print(f"\nFiles in: {OUTPUT_DIR.absolute()}")


if __name__ == "__main__":
    main()
