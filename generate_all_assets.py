#!/usr/bin/env python3
"""
EcoGen Visual DNA — Generate all 26 PNG illustration assets via Nanobanana (Gemini 3 Pro Image).

Usage:
    export GEMINI_API_KEY=<your-key>
    python generate_all_assets.py

Build sequence:
    1. Hero asset (01) generated first for style calibration
    2. Remaining 25 assets generated in parallel (4 workers)
"""

import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from threading import Lock

# Add nanobanana scripts to path
NANOBANANA_DIR = os.path.expanduser("~/.agents/skills/nanobanana/scripts")
sys.path.insert(0, NANOBANANA_DIR)

from generate import generate_image

# ─── Configuration ───────────────────────────────────────────────────────────

OUTPUT_DIR = Path(__file__).parent / "Visual-Referance" / "generated-assets"
PARALLEL_WORKERS = 4
STAGGER_DELAY = 3.0  # seconds between job submissions
MAX_RETRIES = 1

print_lock = Lock()

# ─── Universal Prompt Fragments ──────────────────────────────────────────────

STYLE_HEADER = (
    "Premium isometric axonometric illustration for EcoGen, an AI-assisted LEED v5 "
    "evidence automation platform. Sunlit architectural sustainability studio mood on "
    "a pure white #FFFFFF canvas. Use only the EcoGen palette inside the illustration: "
    "Deep Forest #0F3D23, Primary Green #1E7A3D, Soft Sage #CFE8D6, Mist White #F7FAF7, "
    "Glass White #FFFFFC, Warm Sand #F5EEDC, Border Gray #E6EAE6, Success Mint #E6F7ED. "
    "Low-iron liquid glass panels, soft internal highlights, subtle green-tinted object "
    "shadows, natural material tones, rooftop solar, vegetation accents, human-scale "
    "architectural detail, precise 2px rounded linework, clean vector-like rendering, "
    "premium product-diagram clarity, generous untouched white space, no dark mode, "
    "no blue, no purple, no orange, no neon glow, no stock-photo realism."
)

BG_RULE = (
    "Background must be pure white #FFFFFF across the entire image, edge to edge. "
    "No off-white, cream, gray, Mist White, paper texture, vignette, gradient, shadow wash, "
    "transparent background, alpha channel, border frame, or colored backdrop. The illustration "
    "should appear to float and pop up from an untouched white website canvas."
)

NEGATIVE = (
    "Avoid: non-white backgrounds, off-white backgrounds, cream backgrounds, gray canvas, "
    "Mist White canvas, paper texture, vignette, gradients behind the object, transparent "
    "background, alpha channel, colored border frame, purple or blue AI gradients, neon "
    "cyberpunk lighting, dark navy SaaS dashboard, generic stock photos, random abstract blobs, "
    "heavy black shadows, metallic chrome, cluttered labels, illegible text, rainbow KPI colors, "
    "red/yellow/blue status chips, people posing for camera, photorealistic office interior, "
    "cartoon mascots, childish icons, rough sketch style, fake brand logos, certification "
    "guarantee badges, overpacked dashboard panels, tiny standalone icons, icon sheets."
)


def full_prompt(asset_prompt: str) -> str:
    """Combine style header + background rule + negative prompt + asset-specific prompt."""
    return f"{STYLE_HEADER}\n\n{BG_RULE}\n\n{NEGATIVE}\n\n{asset_prompt}"


# ─── Asset Definitions ───────────────────────────────────────────────────────

ASSETS = [
    # ── ASSET 01: Hero ──
    {
        "id": "01",
        "filename": "01-hero-ecosystem-evidence-map.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Create a wide isometric hero scene showing a sustainable mid-rise building as "
            "the central object: rooftop solar panels, green roof, planted terraces, visible "
            "interior floors, small human-scale paths, a service lane, and a calm landscaped "
            "site. Around the building, connect six floating glass callout panels with thin "
            "Primary Green #1E7A3D connector lines. The callouts represent Water Efficiency, "
            "Refrigerant Management, Low-Emitting Materials, Quality Plans, Integrative Process, "
            "and Reviewer-ready Evidence Pack. Include a smaller evidence-pack UI tile near the "
            "lower right with abstract document rows, a source index icon, a confidence tier seal, "
            "and a human approval record. The whole image should read as one governed evidence "
            "ecosystem, not a decorative building render. Keep the background pure white #FFFFFF "
            "with abundant untouched whitespace so the building and glass panels appear to pop up "
            "from the page. Short labels may appear as simple plaques, but all readable text "
            "should be minimal and replaceable by HTML overlay."
        ),
    },

    # ── ASSET 02a: Suite — Water Efficiency ──
    {
        "id": "02a",
        "filename": "02a-suite-water-efficiency.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A compact isometric sustainable building water-efficiency diagram for a LEED evidence "
            "workflow card. Show a small building with a green roof, visible restroom/fixture zone "
            "as simplified interior blocks, water droplet icon wells, a subtle pipe route line in "
            "Primary Green #1E7A3D, and a glass evidence panel with abstract calculation rows. The "
            "scene should communicate indoor and outdoor water use reduction evidence, not plumbing "
            "complexity. Minimal label plaque for 'WEp2 + WEc2' only if text renders cleanly."
        ),
    },

    # ── ASSET 02b: Suite — Refrigerant Management ──
    {
        "id": "02b",
        "filename": "02b-suite-refrigerant-management.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A compact isometric rooftop mechanical equipment scene for refrigerant management. "
            "Show a small green-roof building with rooftop HVAC units, a service technician scale "
            "figure as a tiny neutral silhouette, a snowflake/refrigerant icon well, and a glass "
            "evidence panel showing abstract equipment inventory rows and a Primary Green approval "
            "seal. Keep refrigerant lines subtle and green-only. Minimal label plaque for "
            "'EAp5 + EAc7' if needed."
        ),
    },

    # ── ASSET 02c: Suite — Quality Plans ──
    {
        "id": "02c",
        "filename": "02c-suite-quality-plans.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A compact isometric construction quality plan scene. Show a partially finished "
            "sustainable building, clean construction staging area, protective material zones, "
            "checklist board, ventilation/airflow arrows in Soft Sage and Primary Green, and a "
            "glass plan document with abstract checklist rows. The mood should be orderly and "
            "controlled, not messy construction. Minimal label plaque for 'EQp1 + EQp2' if needed."
        ),
    },

    # ── ASSET 02d: Suite — Integrative Process ──
    {
        "id": "02d",
        "filename": "02d-suite-integrative-process.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A compact isometric planning table and site-analysis scene. Show a small architectural "
            "site model with a green building, climate layer, map contour lines, community context "
            "nodes, and two glass research cards connected by Primary Green lines. The image should "
            "suggest early collaboration, climate and human-impact research, and project-specific "
            "synthesis. Minimal label plaque for 'IPp1 + IPp2' if needed."
        ),
    },

    # ── ASSET 02e: Suite — Low-Emitting Materials ──
    {
        "id": "02e",
        "filename": "02e-suite-low-emitting-materials.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A compact isometric material library scene. Show stacked sample boards, flooring tile, "
            "paint can silhouette, adhesive tube, and certificate cards arranged on a glass surface. "
            "Primary Green check seals connect product certificates to a small evidence panel with "
            "abstract rows. The image should communicate product evidence screening and low-emitting "
            "material validation. Minimal label plaque for 'MRc3' if needed."
        ),
    },

    # ── ASSET 03: Fragmented Evidence Risk ──
    {
        "id": "03",
        "filename": "03-fragmented-evidence-risk.png",
        "ratio": "3:2",
        "prompt": full_prompt(
            "A calm isometric diagram showing fragmented LEED documentation before EcoGen. On the "
            "left, separate floating glass fragments: spreadsheet grid, PDF stack, email thread card, "
            "product certificate, calculator sheet, and reviewer comment bubble. These fragments are "
            "disconnected and slightly misaligned, with pale Border Gray connector lines that do not "
            "meet. On the right, a single clean evidence workspace panel begins to organize the "
            "fragments with a Primary Green path line. The tone should show risk and clutter without "
            "looking chaotic or dark. No readable body text, only abstract lines and icons."
        ),
    },

    # ── ASSET 04: Evidence Pack Product Illustration ──
    {
        "id": "04",
        "filename": "04-evidence-pack-product-illustration.png",
        "ratio": "3:2",
        "prompt": full_prompt(
            "A premium isometric product UI panel showing a LEED evidence pack workspace for Water "
            "Efficiency. The main glass panel has a left rail of abstract section rows, a top summary "
            "card, a confidence tier chip, region and version chips, a calculation summary area, and "
            "a source table with abstract document rows. On the right, a vertical human-review "
            "timeline shows intake, data extraction, calculation, internal review, and human approval "
            "as small circular steps with Primary Green completed states. Include a small "
            "signature/approval card at the bottom right using abstract lines, not readable text. "
            "Keep everything light, glassy, green-only, and implementation-friendly."
        ),
    },

    # ── ASSET 05: Master Workflow Flow ──
    {
        "id": "05",
        "filename": "05-master-workflow-flow.png",
        "ratio": "21:9",
        "prompt": full_prompt(
            "A wide horizontal isometric flow diagram with five stations: project setup, evidence "
            "intake, workflow automation, human review, export package. One continuous Primary Green "
            "path line connects all stations left to right. Each station is a glass tile with a small "
            "icon and abstract UI lines. Use generous whitespace and make the sequence easy to "
            "implement as a page section. No paragraphs or dense labels."
        ),
    },

    # ── ASSET 06a: Typology — Data Center ──
    {
        "id": "06a",
        "filename": "06a-typology-data-center.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric data center building with rooftop solar, green roof strips, clean "
            "service yard, and subtle cooling equipment. Include evidence workflow glass tile beside "
            "it with abstract rows. Calm and precise, no dark server-room aesthetic."
        ),
    },

    # ── ASSET 06b: Typology — Hospital ──
    {
        "id": "06b",
        "filename": "06b-typology-hospital.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric hospital building in EcoGen palette, with planted terraces, clear "
            "entry canopy, rooftop mechanical units, and a small reviewer-ready evidence tile. Use "
            "a simple medical cross shape only if it stays green and subtle, no red."
        ),
    },

    # ── ASSET 06c: Typology — School ──
    {
        "id": "06c",
        "filename": "06c-typology-school.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric school campus with classroom blocks, courtyard greenery, sports court, "
            "solar roof panels, and a small evidence workflow tile. Warm, educational, and architectural."
        ),
    },

    # ── ASSET 06d: Typology — Office ──
    {
        "id": "06d",
        "filename": "06d-typology-office.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric office building with glass facade, green roof, planted plaza, bike "
            "parking, and a clean evidence dashboard tile. Precise, calm, premium."
        ),
    },

    # ── ASSET 06e: Typology — Campus ──
    {
        "id": "06e",
        "filename": "06e-typology-campus.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric multi-building campus with connected paths, tree canopy, water feature, "
            "and portfolio evidence tiles floating above several buildings. Show portfolio visibility "
            "with green path lines."
        ),
    },

    # ── ASSET 06f: Typology — Sites & Masterplans ──
    {
        "id": "06f",
        "filename": "06f-typology-sites-masterplans.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "A small isometric masterplan site with contour-like landscape, paths, stormwater garden, "
            "site boundary line, and GIS/source evidence nodes. Use Primary Green to trace the site "
            "boundary and source route."
        ),
    },

    # ── ASSET 07: Water Efficiency Pilot ──
    {
        "id": "07",
        "filename": "07-water-efficiency-pilot.png",
        "ratio": "4:3",
        "prompt": full_prompt(
            "An isometric Water Efficiency pilot scene showing a mid-size office building with green "
            "roof and visible water-efficient fixture zones, a small fixture schedule spreadsheet tile, "
            "a baseline/proposed calculation tile, and a reviewer approval card connected by Primary "
            "Green path lines. The image should clearly communicate 'fixture schedule to evidence pack' "
            "in a calm premium way. No exaggerated claims, no fake certification badge, no dense text."
        ),
    },

    # ── ASSET 08: Source Routing Network ──
    {
        "id": "08",
        "filename": "08-source-routing-network.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "A wide isometric source routing network diagram. Left side contains input source tiles: "
            "Excel/CSV schedule, PDF certificate, product database, public dataset, completed model "
            "output, manual reviewer entry. Center has a glass source router node with a leaf-shaped "
            "circuit mark. Right side has an evidence pack output panel and a manual-mode fallback "
            "lane. Use Primary Green lines for verified source paths and Soft Sage dashed lines for "
            "assisted/manual fallback paths. No brand logos, no readable API names, no blue cloud icons."
        ),
    },

    # ── ASSET 09: Audit Trail & Approval Chain ──
    {
        "id": "09",
        "filename": "09-audit-approval-chain.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "An isometric audit trail diagram showing a chain of glass tiles: source upload, "
            "extraction, formula, confidence tier, reviewer comment, human approval, export. Each "
            "tile has an abstract icon and short placeholder label bar. A continuous Primary Green "
            "trace line links the tiles, with small check nodes at reviewer and approval steps. "
            "Include one final sealed evidence pack at the end. The feeling should be trustworthy "
            "and governed, not automated magic."
        ),
    },

    # ── ASSET 10: Final CTA Botanical Band ──
    {
        "id": "10",
        "filename": "10-final-cta-botanical-band.png",
        "ratio": "21:9",
        "prompt": full_prompt(
            "A wide, low-contrast final CTA illustration band on a pure white #FFFFFF canvas. Show "
            "very pale line-art botanical leaves, a faint isometric building outline, subtle glass "
            "panel edges, and a Primary Green path line that gently curves toward a small evidence "
            "pack seal. Keep the outer image background completely white and mostly empty so HTML "
            "headline and buttons can sit on top. No readable text, no high contrast, no busy detail."
        ),
    },

    # ── ASSET 11: Open Graph Image ──
    {
        "id": "11",
        "filename": "11-og-default.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "A 1200x630 social preview image for EcoGen. Left side: large empty pure white space "
            "reserved for the EcoGen wordmark and headline overlay in HTML or design tool. Right "
            "side: compact isometric sustainable building plus evidence pack tile, connected by "
            "Primary Green source paths. Include subtle glass panels, rooftop solar, vegetation, "
            "and approval seal. Use pure white #FFFFFF background and no colored frame. Do not "
            "include readable body text."
        ),
    },

    # ── SEO-1: Water Efficiency Workflow ──
    {
        "id": "seo-1",
        "filename": "seo-water-efficiency-workflow.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a Water Efficiency evidence workflow "
            "diagram showing fixture schedule upload, baseline calculation, proposed-use calculation, "
            "reduction result, and reviewer approval as five isometric glass stations connected by "
            "Primary Green path lines. No dense text, no fake point guarantee."
        ),
    },

    # ── SEO-2: Refrigerant Workflow ──
    {
        "id": "seo-2",
        "filename": "seo-refrigerant-workflow.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a refrigerant management evidence "
            "workflow diagram showing equipment schedule, refrigerant identity lookup, GWP risk flag, "
            "calculation summary, and MEP reviewer approval. Use rooftop mechanical equipment and "
            "green-only evidence paths. No warning colors, no chemical hazard look."
        ),
    },

    # ── SEO-3: Low-Emitting Materials ──
    {
        "id": "seo-3",
        "filename": "seo-low-emitting-materials.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a low-emitting materials evidence "
            "workflow diagram showing product list intake, certificate matching, VOC evidence card, "
            "exception review, and final evidence pack. Use material samples and certificate cards "
            "in an isometric glass workspace. No brand logos."
        ),
    },

    # ── SEO-4: LEED Checklist ──
    {
        "id": "seo-4",
        "filename": "seo-leed-checklist.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a clean isometric checklist poster "
            "showing the components of a LEED evidence pack: source index, calculations, narrative, "
            "evidence matrix, confidence tier, human approval, export. Use simple glass tiles arranged "
            "in a measured grid with Primary Green check path. Keep labels as blank bars for HTML overlay."
        ),
    },

    # ── SEO-5: Spreadsheets vs Workspace ──
    {
        "id": "seo-5",
        "filename": "seo-spreadsheets-vs-workspace.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a side-by-side isometric comparison: "
            "left side shows disconnected spreadsheets, PDFs, emails, and calculators in pale Border "
            "Gray; right side shows one organized glass evidence workspace with source path, confidence, "
            "and reviewer approval in green. Avoid negative or alarmist colors."
        ),
    },

    # ── SEO-6: AI for LEED Consultants ──
    {
        "id": "seo-6",
        "filename": "seo-ai-for-consultants.png",
        "ratio": "16:9",
        "prompt": full_prompt(
            "Generate as a PNG-only page-specific illustration: a trust-centered AI workflow "
            "illustration for LEED consultants: AI assistant represented as a transparent workflow "
            "node, not a robot; source documents, formula trail, confidence indicator, and human "
            "reviewer approval surround it. The human review path should be visually stronger "
            "than the AI node."
        ),
    },
]


# ─── Generation Logic ────────────────────────────────────────────────────────

def generate_asset(asset: dict, index: int, total: int) -> dict:
    """Generate a single asset. Returns result dict."""
    asset_id = asset["id"]
    filepath = OUTPUT_DIR / asset["filename"]

    for attempt in range(1, MAX_RETRIES + 2):
        try:
            result = generate_image(
                prompt=asset["prompt"],
                output_path=str(filepath),
                aspect_ratio=asset["ratio"],
                image_size="4K",
                verbose=False,
            )

            if result.get("success"):
                with print_lock:
                    print(f"  [{index}/{total}] ✅ {asset['filename']}")
                return {"id": asset_id, "filename": asset["filename"], "success": True}
            else:
                error = result.get("error", "Unknown error")
                if attempt <= MAX_RETRIES:
                    with print_lock:
                        print(f"  [{index}/{total}] ⚠️  {asset['filename']} — retry {attempt}/{MAX_RETRIES} ({error})")
                    time.sleep(5)
                else:
                    with print_lock:
                        print(f"  [{index}/{total}] ❌ {asset['filename']} — {error}")
                    return {"id": asset_id, "filename": asset["filename"], "success": False, "error": error}

        except Exception as e:
            if attempt <= MAX_RETRIES:
                with print_lock:
                    print(f"  [{index}/{total}] ⚠️  {asset['filename']} — retry {attempt}/{MAX_RETRIES} ({e})")
                time.sleep(5)
            else:
                with print_lock:
                    print(f"  [{index}/{total}] ❌ {asset['filename']} — {e}")
                return {"id": asset_id, "filename": asset["filename"], "success": False, "error": str(e)}

    return {"id": asset_id, "filename": asset["filename"], "success": False, "error": "Exhausted retries"}


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    total = len(ASSETS)
    print(f"╔══════════════════════════════════════════════════════════╗")
    print(f"║  EcoGen Visual DNA — Asset Generation ({total} assets)       ║")
    print(f"║  Output: {OUTPUT_DIR.relative_to(Path(__file__).parent)}  ║")
    print(f"║  Resolution: 4K  |  Workers: {PARALLEL_WORKERS}  |  Retries: {MAX_RETRIES}       ║")
    print(f"╚══════════════════════════════════════════════════════════╝")
    print()

    # ── Phase 1: Hero asset (style calibration) ──
    hero = ASSETS[0]
    print("━━━ Phase 1: Hero Asset (Style Calibration) ━━━")
    print(f"  Generating {hero['filename']}...")
    hero_result = generate_asset(hero, 1, total)
    print()

    if not hero_result["success"]:
        print("⚠️  Hero failed — continuing with remaining assets anyway.")
    else:
        print(f"  Hero saved to: {OUTPUT_DIR / hero['filename']}")
    print()

    # ── Phase 2: Remaining assets in parallel ──
    remaining = ASSETS[1:]
    print(f"━━━ Phase 2: Remaining {len(remaining)} Assets (4 parallel workers) ━━━")

    results = [hero_result]

    with ThreadPoolExecutor(max_workers=PARALLEL_WORKERS) as executor:
        futures = {}
        for i, asset in enumerate(remaining, start=2):
            future = executor.submit(generate_asset, asset, i, total)
            futures[future] = asset
            # Stagger submissions to reduce rate-limit risk
            if i < total:
                time.sleep(STAGGER_DELAY)

        for future in as_completed(futures):
            results.append(future.result())

    # ── Summary ──
    print()
    print("━━━ Generation Summary ━━━")
    results.sort(key=lambda r: r["id"])
    successes = [r for r in results if r["success"]]
    failures = [r for r in results if not r["success"]]

    print(f"  ✅ Success: {len(successes)}/{total}")
    if failures:
        print(f"  ❌ Failed:  {len(failures)}/{total}")
        for f in failures:
            print(f"     — {f['filename']}: {f.get('error', 'Unknown')}")

    print()
    print(f"  Output directory: {OUTPUT_DIR}")
    print()

    if failures:
        print("  To retry failed assets, run again — existing files will be overwritten.")
        sys.exit(1)
    else:
        print("  All assets generated successfully! 🎉")


if __name__ == "__main__":
    main()
