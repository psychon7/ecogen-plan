#!/usr/bin/env python3
"""
Recover / continue from an existing Browser Use session.
Polls until it finishes, saves the URL map and progress file,
then hands off to the main download loop.

Usage:
    python3 recover_session.py <session_id>
"""
import json
import sys
import time
from pathlib import Path

import requests

BROWSER_USE_API_KEY = "bu_hVoABz8LmTqB0fr_rXUrQZIRiLLSQAI_bGjS9UWed08"
BU_API = "https://api.browser-use.com/api/v3"
BU_HEADERS = {
    "X-Browser-Use-API-Key": BROWSER_USE_API_KEY,
    "Content-Type": "application/json",
}

OUTPUT_DIR = Path(__file__).parent / "leed-forms-html"
PROGRESS_FILE = OUTPUT_DIR / "_progress.json"


def bu_get(path: str, retries: int = 8) -> dict:
    for attempt in range(retries):
        try:
            r = requests.get(f"{BU_API}{path}", headers=BU_HEADERS, timeout=60)
            r.raise_for_status()
            return r.json()
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as exc:
            wait = 15 * (attempt + 1)
            print(f"  [network] {exc.__class__.__name__} – retrying in {wait}s "
                  f"({attempt+1}/{retries})")
            time.sleep(wait)
    raise RuntimeError(f"Failed to GET {path} after {retries} attempts")


def poll_until_done(session_id: str, max_wait: int = 7200) -> dict:
    start = time.time()
    last_step = -1
    while time.time() - start < max_wait:
        try:
            data = bu_get(f"/sessions/{session_id}")
        except RuntimeError as exc:
            print(f"  [poll error] {exc} – will retry outer loop")
            time.sleep(30)
            continue
        status = data["status"]
        step = data.get("stepCount", 0)
        if step != last_step:
            summary = (data.get("lastStepSummary") or "")[:100]
            print(f"  step {step:>4} [{status}] {summary}")
            last_step = step
        if status in ("stopped", "timed_out", "error"):
            return data
        if status == "idle" and data.get("isTaskSuccessful") is not None:
            return data
        time.sleep(6)
    print("WARNING: max_wait exceeded, returning whatever we have")
    return bu_get(f"/sessions/{session_id}")


def main():
    session_id = sys.argv[1] if len(sys.argv) > 1 else "53cd1cbd-6482-4ecd-863c-f05c4ea8d9d6"
    print(f"Recovering session: {session_id}")

    result = poll_until_done(session_id)
    print(f"\nSession finished. status={result['status']}  success={result.get('isTaskSuccessful')}")

    output = result.get("output") or {}
    if isinstance(output, str):
        try:
            output = json.loads(output)
        except json.JSONDecodeError:
            print("Output was not valid JSON — no URL map extracted")
            output = {}

    url_map: dict[str, str] = {}
    if isinstance(output, dict):
        for item in output.get("credits", []):
            if item.get("id") and item.get("url"):
                url_map[item["id"]] = item["url"]

    print(f"\nDiscovered {len(url_map)} credit URLs:")
    for k, v in url_map.items():
        print(f"  {k}: {v}")

    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / "_url_map.json").write_text(json.dumps(url_map, indent=2))

    # Write/merge progress file so main script resumes with this session
    progress = {
        "session_id": session_id,
        "url_map": url_map,
        "downloaded": [],
        "failed": [],
    }
    if PROGRESS_FILE.exists():
        existing = json.loads(PROGRESS_FILE.read_text())
        progress["downloaded"] = existing.get("downloaded", [])
        progress["failed"] = existing.get("failed", [])
        progress["url_map"] = {**url_map, **existing.get("url_map", {})}

    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))
    print(f"\nProgress saved to {PROGRESS_FILE}")
    print("Now run:  python3 download_leed_forms.py")


if __name__ == "__main__":
    main()
