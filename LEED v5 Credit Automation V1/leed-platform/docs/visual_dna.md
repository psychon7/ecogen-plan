# EcoGen Visual DNA And Design Language

## Liquid Glass Compliance Studio x Isometric Sustainability Systems

**Version:** 1.1  
**Last updated:** 2026-05-03  
**Primary source:** `docs/design.md`  
**Companion copy source:** `leed-platform/docs/landing_page_master_copy.md`

> **Purpose**
>
> This document is the single source of truth for the visual language of the EcoGen landing page and related SEO pages. It defines:
>
> - Foundational visual principles from `docs/design.md`.
> - Color, typography, spacing, glass, layout, motion, and component rules.
> - Section-by-section landing page blueprints tied to the master copy.
> - A complete illustration and asset register with paste-ready image-generation prompts.
> - Production guidance for which content belongs in HTML versus generated artwork.
>
> The brand feeling is: sunlit, architectural, evidence-led, green, calm, and professionally accountable. EcoGen should look like a daylight sustainability studio crossed with a governed compliance workspace: beautiful, but never ornamental for its own sake.

---

## 1. Core Principles

| # | Principle | Application |
| - | --------- | ----------- |
| 1 | White canvas is absolute. | The website background and every generated image background must be pure white `#FFFFFF`, edge to edge. No off-white, cream, texture, gradient, or transparent image canvas. |
| 2 | Evidence first. | Every visual should clarify traceability, review, source quality, or certification readiness. Avoid generic "AI magic" imagery. |
| 3 | Liquid glass, not plastic cards. | Elevated surfaces use transparency, inner highlights, soft green-tinted shadows, and 16px blur. |
| 4 | Isometric systems. | Core imagery uses high-quality isometric or axonometric diagrams: buildings, evidence packs, workflows, and source networks. |
| 5 | Green-only discipline. | All emphasis stays inside the EcoGen green-white-sage palette. No purple, blue-neon, orange, pink, or rainbow status colors. |
| 6 | Human review is visible. | Show reviewers, approval records, confidence tiers, and audit trails as first-class visual objects. |
| 7 | Calm density. | Density is 4/10. The page can contain serious information, but it must breathe. |
| 8 | Architectural grid. | Layouts feel like an architecture presentation board: measured columns, clean modules, generous whitespace. |
| 9 | No false proof. | Do not use fake traction numbers, fake client logos, or fake certification success claims. Use target metrics only when labeled as targets. |
| 10 | Diagrams over stock. | Use isometric diagrams, product UI panels, and line icons. Avoid generic stock photos, blurry architecture, or decorative abstract blobs. |
| 11 | Copy remains short. | Visuals do the explanatory work. Text blocks stay concise and scannable. |

---

## 2. Color System

### 2.1 Core palette

| Role | Hex | Usage |
| ---- | --- | ----- |
| Canvas White | `#FFFFFF` | Required page background and required background for every generated asset. |
| Primary Green | `#1E7A3D` | Primary CTA fill, active state, chart emphasis, focus moments. |
| Deep Forest | `#0F3D23` | Headings, strong text, hover states, icon strokes, footer anchors. |
| Soft Sage | `#CFE8D6` | Tinted glass washes, icon wells, hover fills, light diagram planes. |
| Mist White | `#F7FAF7` | Subtle internal panel tint only; never use as full page or image background. |
| Glass White | `#FFFFFC` | Elevated panels, buttons, cards, input fills. |
| Warm Sand | `#F5EEDC` | Tiny internal warmth for illustration details or glass reflections only; never full-section background. |
| Border Gray | `#E6EAE6` | Lines, dividers, inputs, table borders, card outlines. |
| Success Mint | `#E6F7ED` | Positive metrics, confirmation chips, subtle readiness states. |

### 2.2 Translucency tokens

| Token | Value | Usage |
| ----- | ----- | ----- |
| Glass Fill Strong | `rgba(255,255,252,0.78)` | Major panels, nav, modal surfaces. |
| Glass Fill Soft | `rgba(247,250,247,0.64)` | Secondary panels, background washes. |
| Inner Highlight | `rgba(255,255,255,0.76)` | Top edge highlight on glass surfaces. |
| Outer Edge | `rgba(15,61,35,0.08)` | Hairline border for glass panels. |
| Focus Ring | `rgba(30,122,61,0.28)` | Keyboard and input focus. |

### 2.3 Usage rules

- Primary Green is the single conversion accent.
- Canvas White `#FFFFFF` is the only full-bleed page background and the only image-generation background.
- Deep Forest carries seriousness and brand authority.
- Soft Sage and Success Mint are green-family support tones, not separate accents.
- Warm Sand and Mist White may appear only inside internal surfaces, soft glass fills, or very small low-contrast accents. They must never tint the outer page canvas or exported image background.
- Data visualization uses tonal green only: Deep Forest, Primary Green, Soft Sage, Success Mint, Border Gray.
- Do not introduce yellow warning chips, red error cards, blue info states, or purple AI highlights.

### 2.4 Status semantics

| State | Treatment |
| ----- | --------- |
| Ready | Success Mint fill, Deep Forest label, Primary Green check or seal. |
| In review | Glass White fill, Primary Green outline, reviewer icon. |
| Needs data | Mist White fill, Deep Forest label, dashed Border Gray outline. |
| Manual mode | Soft Sage fill, Deep Forest label, small source icon. |
| Blocked | Deep Forest text with structured inline message. Use calm contrast, not red. |

---

## 3. Typography

### 3.1 Stack

Use Open Sans first to match the EcoGen brand board.

```css
font-family: 'Open Sans', 'Geist', 'Manrope', system-ui, sans-serif;
```

Fallbacks:

- Use Geist if Open Sans is unavailable.
- Use Manrope if Geist is unavailable.
- Do not use Inter.
- Do not use generic serif fonts.

### 3.2 Scale

| Role | Desktop | Mobile | Weight | Notes |
| ---- | ------- | ------ | ------ | ----- |
| Display | 72px / 80px | clamp(44px, 10vw, 60px) | Semibold | Hero only. Tracking `-0.03em`. |
| H1 | 48px / 56px | clamp(34px, 8vw, 48px) | Semibold | Page or major section headline. |
| H2 | 28px / 36px | 24px / 32px | Semibold | Section headings. |
| H3 | 18px / 26px | 17px / 24px | Semibold | Card titles and subheads. |
| Body | 16px / 24px | 16px / 24px | Regular | Max width 65ch. |
| Caption | 12px / 16px | 12px / 16px | Regular | Notes, labels, metadata. |
| Button / Label | 14px / 16px | 14px / 16px | Semibold | Tracking `0.01em`. |

### 3.3 Kicker pattern

Kickers are soft botanical tags, not aggressive all-caps tech labels.

```html
<span class="inline-flex rounded-full border border-[rgba(15,61,35,0.08)] bg-[#E6F7ED] px-3 py-1 text-sm font-semibold text-[#0F3D23]">
  LEED v5 evidence automation
</span>
```

Rules:

- Use sentence case or short title case.
- Do not use long all-caps labels.
- Keep contrast calm and readable.

---

## 4. Grid And Spacing

### 4.1 Container

```html
<div class="mx-auto max-w-[1200px] px-5 md:px-8 lg:px-10">
  ...
</div>
```

Hero and full-page presentation slices may extend to `max-w-[1320px]` when the isometric scene needs more width.

### 4.2 12-column grid

```html
<div class="grid grid-cols-12 gap-4 md:gap-6 lg:gap-8">
  <div class="col-span-12 lg:col-span-5">...</div>
  <div class="col-span-12 lg:col-span-7">...</div>
</div>
```

### 4.3 Vertical rhythm

| Token | Usage |
| ----- | ----- |
| `py-12` | Compact bands and footer sections. |
| `py-16` | Standard dense content section. |
| `py-20` | Major landing page section. |
| `py-24` | Hero, evidence showcase, final CTA. |
| `gap-4` | Small card and button groups. |
| `gap-6` | Feature grids and mobile stacks. |
| `gap-8` | Major section grids. |
| `gap-12` | Hero and product showcase spacing. |

### 4.4 Layout patterns

Preferred:

- Split hero: 5 columns copy, 7 columns isometric scene.
- 7/5 product showcase: evidence pack UI next to approval timeline.
- 8/4 problem split: problem cards plus explanatory side panel.
- Mixed-width suite cards: avoid a generic 3-card row.
- Horizontal strip for outcomes and source chips.
- Dense but calm footer with column groups.

Banned:

- Centered hero stack.
- Three equal feature cards as the dominant pattern.
- Cards inside cards.
- Dark navy SaaS dashboards.
- Floating decorative blobs.

---

## 5. Component Vocabulary

### 5.1 Primary button

Liquid-glass green capsule with nested arrow circle.

```html
<button class="group inline-flex min-h-[44px] items-center gap-3 rounded-full bg-[#1E7A3D] px-5 py-3 text-sm font-semibold text-[#FFFFFC] shadow-[inset_0_1px_0_rgba(255,255,255,0.35),0_8px_24px_rgba(16,24,16,0.12)] transition duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:-translate-y-px active:scale-[0.985]">
  Book a demo
  <span class="grid h-7 w-7 place-items-center rounded-full bg-[rgba(255,255,252,0.18)] transition-transform group-hover:translate-x-0.5">-></span>
</button>
```

Rules:

- Primary button is used for demo booking only.
- Arrow sits in its own circular inner capsule.
- No outer neon glow.

### 5.2 Secondary button

Glass capsule with faint green stroke.

```html
<button class="inline-flex min-h-[44px] items-center rounded-full border border-[rgba(15,61,35,0.08)] bg-[rgba(255,255,252,0.78)] px-5 py-3 text-sm font-semibold text-[#0F3D23] shadow-[inset_0_1px_0_rgba(255,255,255,0.76),0_4px_20px_rgba(16,24,16,0.06)] transition duration-300 ease-[cubic-bezier(0.16,1,0.3,1)] hover:bg-[#CFE8D6]">
  Explore supported credits
</button>
```

### 5.3 Glass card

```html
<article class="rounded-2xl border border-[rgba(15,61,35,0.08)] bg-[linear-gradient(180deg,rgba(255,255,252,0.82),rgba(247,250,247,0.70))] p-6 shadow-[inset_0_1px_0_rgba(255,255,255,0.78),0_4px_20px_rgba(16,24,16,0.06)]">
  ...
</article>
```

Rules:

- Use for repeated items, modals, and framed tools.
- Do not nest cards inside cards.
- Feature cards should be slim, single-message, and calm.

### 5.4 Suite card

Used for supported credit suites.

Structure:

- Circular sage icon well.
- Small isometric suite thumbnail.
- Suite name.
- Credit codes.
- 2-line description.
- Text CTA with arrow.

Visual:

- Radius 16px.
- Glass White fill.
- Border Gray edge.
- Primary Green icon stroke.
- Hover lifts 2px and reveals a subtle top sheen.

### 5.5 Evidence pack panel

Used for product showcase.

Structure:

- Left rail: evidence pack sections.
- Main area: credit summary, confidence, region, version, compliance status.
- Source table: documents with date and owner.
- Right rail: review timeline.
- Bottom: primary CTA.

Visual:

- Major panel radius 24px.
- Green-only status chips.
- Thin dividers.
- No dark admin shell.

### 5.6 Outcome strip item

Structure:

- 40px icon well.
- Short label.
- Optional 1-line microcopy on wide screens only.

Usage:

- Automate documentation.
- Centralize evidence.
- Track credits.
- Optimize performance.
- Achieve readiness.

### 5.7 Metric card

Structure:

- Icon well or small line icon.
- Large number in Primary Green.
- Label and caveat.

Rules:

- Do not use fake traction.
- Target metrics must say "target" or "planned".
- One metric per card.

### 5.8 Accordion FAQ

Structure:

- Full-width row.
- Question left.
- Plus/minus icon right.
- Answer expands below.

Visual:

- Border Gray top/bottom separators.
- No heavy card boxes.
- Keep answer text direct for AEO.

### 5.9 Demo form modal

Structure:

- Title, short intro, label-above-input fields.
- Primary interest select.
- Region select.
- Message textarea.
- Confirmation state.

Visual:

- Major glass panel.
- Inputs are frosted white with 16px radius.
- Focus ring uses `rgba(30,122,61,0.28)`.

---

## 6. Iconography

### 6.1 Icon pack strategy

Use an icon pack for all small UI icons, feature icons, status icons, FAQ icons, step icons, metric icons, and role icons. Do not generate AI images for these small assets.

Preferred pack:

- Primary: `lucide-react`
- Fallback: `@phosphor-icons/react`

Reasoning:

- Small AI-generated icons are slower to produce, harder to keep consistent, and harder to recolor responsively.
- Icon-pack icons can inherit CSS color, stroke width, hover state, focus state, and accessibility labels.
- PNG generation should be reserved for large isometric illustrations where the brand world needs depth and composition.

Rules:

- 2px stroke.
- Rounded joins.
- Open, friendly geometry.
- Color: Deep Forest or Primary Green.
- Icon well: Soft Sage or Success Mint.
- Do not mix many icon libraries in one page.
- Avoid emoji in UI and alt text.
- No AI-generated PNG icons for simple controls or repeated card icons.

### 6.2 Icon pack mapping

Use these as implementation defaults. If a named icon is unavailable in the chosen pack, use the closest equivalent with the same meaning.

| Use | Suggested icon |
| --- | -------------- |
| Book a demo arrow | `ArrowRight` |
| Navigation dropdown | `ChevronDown` |
| Language selector | `Globe2` |
| Log in | `LogIn` |
| Water Efficiency | `Droplets` |
| Refrigerant Management | `Snowflake` |
| Low-Emitting Materials | `Leaf` |
| Quality Plans | `ClipboardCheck` |
| Integrative Process | `Workflow` |
| Reviewer-ready evidence pack | `FileCheck2` |
| Confidence tier | `Gauge` |
| Source index | `ListChecks` or `Link2` |
| Human approval record | `ShieldCheck` |
| Automate documentation | `FileCog` |
| Centralize evidence | `FolderArchive` |
| Track credits | `ChartNoAxesColumnIncreasing` |
| Optimize performance | `Activity` |
| Achieve readiness | `BadgeCheck` |
| Source-grounded extraction | `ScanSearch` |
| Deterministic calculations | `Calculator` |
| Evidence pack builder | `PackageCheck` |
| Workflow and tasks | `ListTodo` |
| Regional source routing | `Route` |
| Reviewer-ready exports | `Send` |
| Portfolio visibility | `MonitorCog` |
| Set up project | `Building2` |
| Upload/connect evidence | `UploadCloud` |
| Run workflows | `Workflow` |
| Review confidence | `ClipboardCheck` |
| Export package | `PackageCheck` |
| Time saved | `Clock3` |
| Human approval | `UserCheck` |
| Claim-source link | `Link2` |
| Hidden gaps | `SearchCheck` |
| Senior consultant | `UserRoundCheck` |
| Project manager | `CalendarCheck2` |
| Junior consultant | `GraduationCap` |
| Specialist reviewer | `ScanSearch` |
| Building owner | `Landmark` |
| FAQ row | `CircleHelp` |
| Security/trust | `LockKeyhole` |

### 6.3 Large illustration style

AI image generation is reserved for key PNG illustrations only.

Style for generated PNGs:

- Isometric or axonometric.
- Pure white `#FFFFFF` full-bleed background.
- Deep Forest primary line/detail color.
- Primary Green only for active paths, checks, seals, and highlighted data.
- Soft Sage, Success Mint, Mist White, and Glass White can appear inside the object, panels, vegetation, and glass surfaces.
- Subtle object shadows are allowed only under illustration objects to create a 3D pop-up illusion on the white website canvas.
- No icon-pack replacement by generated image unless the icon is part of a larger illustration.

---

## 7. Motion

Motion should feel like glass settling and diagrams quietly coming alive.

| Element | Motion |
| ------- | ------ |
| Buttons | Hover translateY(-1px), press scale(0.985), inner arrow shifts 2px. |
| Cards | Hover lift 2px, shadow bloom, optional top sheen. |
| Hero callouts | 60-90ms staggered fade-up. |
| Isometric scene | Slow 2-4px float on isolated layers only. |
| Source path lines | Optional slow stroke-dash reveal on first load. |
| Evidence pack panel | Step timeline checks fade in sequentially. |
| FAQ | Height transition with opacity fade. |

Technical rules:

- Animate transform and opacity only.
- Use `cubic-bezier(0.16, 1, 0.3, 1)`.
- Respect `prefers-reduced-motion`.
- Do not use aggressive parallax.
- Do not animate large backdrop-blur layers while scrolling.

---

## 8. Landing Page Layout Blueprints

These blueprints map `landing_page_master_copy.md` into implementation sections, components, and required assets.

### 8.1 Header navigation

**Purpose:** Establish brand, structure, and demo conversion.

**Layout:**

- Floating glass nav pill inside a max-width container.
- Left: EcoGen logo.
- Center: nav labels on desktop only.
- Right: Log in text link and Book a demo button.
- Mobile: logo and demo button; optional compact menu only if needed.

**Components:**

- Logo lockup.
- Glass navigation pill.
- Primary CTA.
- Text link.

**Assets:**

- Existing logo asset or coded vector mark.
- No generated artwork needed.

### 8.2 Hero

**Purpose:** Communicate the entire product in one scene: LEED evidence automation, supported credit suites, source traceability, human approval.

**Layout:**

- 5/7 split.
- Left: eyebrow, H1, subheadline, CTA group, trust line.
- Right: large isometric sustainable building and evidence workflow scene.
- Below visual: microcopy about workflow variability.

**Components:**

- Kicker chip.
- Display H1.
- CTA pair.
- Trust line with small source/leaf icon.
- Isometric hero scene with callout chips.

**Required asset:**

- Asset 01: Hero ecosystem and evidence map.

**Responsive:**

- Image moves below copy on mobile.
- Hide nonessential callouts on small screens.
- Keep CTA buttons full-width or stacked at 320px.

### 8.3 Outcome strip

**Purpose:** Translate the promise into five fast outcomes.

**Layout:**

- Full-width glass rail.
- Five equal outcome cells on desktop.
- Two-column wrap on tablet.
- Single column or horizontal snap strip on mobile.

**Components:**

- Outcome strip item.
- Vertical dividers on desktop.
- Compact icons.

**Icon pack:**

- Use icon-pack icons only: `FileCog`, `FolderArchive`, `ChartNoAxesColumnIncreasing`, `Activity`, `BadgeCheck`.
- No AI-generated image assets needed for this strip.

### 8.4 Supported credit scope

**Purpose:** Show the suite-based MVP scope and avoid "all credits" overclaiming.

**Layout:**

- Section heading and short intro.
- Mixed-width suite card group, 5 cards.
- Water Efficiency card can be slightly emphasized as first commercial wedge.
- Scope note and CTA beneath.

**Components:**

- Suite cards.
- Isometric thumbnails.
- Text CTA.
- Scope note.

**Required assets:**

- Asset 02a: Water Efficiency suite miniature.
- Asset 02b: Refrigerant Management suite miniature.
- Asset 02c: Quality Plans suite miniature.
- Asset 02d: Integrative Process suite miniature.
- Asset 02e: Low-Emitting Materials suite miniature.

### 8.5 Problem section

**Purpose:** Show the cost of fragmented LEED documentation.

**Layout:**

- 8/4 split.
- Left: narrative copy and a fragmented evidence diagram.
- Right: four problem cards.
- Bottom: transition statement in Deep Forest.

**Components:**

- Problem cards.
- Fragmented sources diagram.
- Calm callout.

**Required asset:**

- Asset 03: Fragmented evidence risk diagram.

### 8.6 Product value section

**Purpose:** Explain "AI-assisted, reviewer-controlled" in product terms.

**Layout:**

- Asymmetric 2-row grid.
- Use 8 feature cards, not three equal columns.
- Larger feature cards for source-grounded extraction and evidence pack builder.

**Components:**

- Feature card.
- Circular sage icon well.
- 2-line copy.

**Icon pack:**

- Use icon-pack icons only: `ScanSearch`, `Calculator`, `PackageCheck`, `ListTodo`, `Gauge`, `Route`, `Send`, `MonitorCog`.
- No AI-generated image assets needed for these feature cards.

### 8.7 Evidence pack showcase

**Purpose:** Make the core product tangible and credible.

**Layout:**

- 7/5 split.
- Left or center: evidence pack UI panel.
- Right: approval timeline card with reviewer record.
- Bottom: CTA.

**Components:**

- Evidence pack panel.
- Review timeline.
- Confidence chip.
- Source table.
- Approval signature block.

**Required asset:**

- Asset 04: Evidence pack product illustration.

### 8.8 How it works

**Purpose:** Turn the workflow into a simple, memorable 5-step system.

**Layout:**

- Horizontal five-step flow on desktop.
- Connected path line.
- CTA centered below.
- Mobile: vertical stepper.

**Components:**

- Numbered step chips.
- Step icons.
- Path connectors.
- CTA.

**Icon pack and optional asset:**

- Use icon-pack icons for each step: `Building2`, `UploadCloud`, `Workflow`, `ClipboardCheck`, `PackageCheck`.
- Optional Asset 05: Master workflow flow diagram, if the page needs a larger explanatory visual.

### 8.9 Building typologies

**Purpose:** Show breadth while keeping applicability conditional.

**Layout:**

- Heading and short intro.
- Six typology cards in a 3x2 desktop grid or horizontal scroll group.
- Each card uses a small isometric building miniature.

**Components:**

- Typology card.
- Building miniature.
- Caption.
- Scope note.

**Required assets:**

- Asset 06a: Data center.
- Asset 06b: Hospital.
- Asset 06c: School.
- Asset 06d: Office.
- Asset 06e: Campus.
- Asset 06f: Sites and masterplans.

### 8.10 Readiness and impact

**Purpose:** Show readiness metrics without fake traction.

**Layout:**

- Left intro panel.
- Four metric cards.
- One caveat card explaining targets and evidence alignment.

**Components:**

- Metric card.
- Inline caveat note.
- Readiness icon.

**Icon pack:**

- Use icon-pack icons only: `Clock3`, `UserCheck`, `Link2`, `SearchCheck`.
- No AI-generated image assets needed for metric icons.

### 8.11 Pilot case study block

**Purpose:** Provide a realistic proof container for Water Efficiency.

**Layout:**

- 5/7 split.
- Left: pilot story and mini building illustration.
- Right: metric table or result grid.
- Until real data exists, placeholders must be visibly marked.

**Components:**

- Pilot card.
- Water Efficiency building miniature.
- Result cells.
- CTA.

**Required asset:**

- Asset 07: Water Efficiency pilot illustration.

### 8.12 Persona section

**Purpose:** Show EcoGen is designed around risk-bearing users.

**Layout:**

- Compact horizontal role cards on desktop.
- Two-column wrap on tablet.
- Single-column on mobile.

**Components:**

- Role card.
- Reviewer/user icon.
- Short role outcome.

**Icon pack:**

- Use icon-pack icons only: `UserRoundCheck`, `CalendarCheck2`, `GraduationCap`, `ScanSearch`, `Landmark`.
- No AI-generated image assets needed for role cards.

### 8.13 Integrations and inputs

**Purpose:** Show source flexibility while respecting regional/API uncertainty.

**Layout:**

- Left: source chip group.
- Right: source routing diagram.
- Bottom: trust note about degradation to assisted/manual mode.

**Components:**

- Source chips.
- Integration family tags.
- Source routing diagram.

**Required asset:**

- Asset 08: Source routing network.

### 8.14 Trust, governance, and security

**Purpose:** Prove this is not black-box automation.

**Layout:**

- 5 trust pillars in mixed-width grid.
- Center or side: audit chain diagram.

**Components:**

- Trust pillar cards.
- Audit chain graphic.
- Human approval badge.

**Required asset:**

- Asset 09: Audit trail and human approval chain.

### 8.15 FAQ

**Purpose:** Answer AI and LEED trust objections directly for conversion and AEO.

**Layout:**

- Left: H2 and short reassurance.
- Right: accordion list.

**Components:**

- FAQ accordion.
- Inline help icon.

**Icon pack:**

- Use `CircleHelp`, `Plus`, and `Minus` from the icon pack.
- No AI-generated image asset needed for FAQ rows.

### 8.16 Final CTA

**Purpose:** End with confident demo conversion.

**Layout:**

- Full-width white glass CTA zone on the same pure white page canvas.
- Left: short CTA copy.
- Center/right: primary and secondary CTAs.
- Subtle botanical or isometric line illustration floating on white, never on a tinted section background.

**Components:**

- CTA band.
- Primary button.
- Secondary text link.
- Small print.

**Required asset:**

- Asset 10: Final CTA botanical architecture band.

### 8.17 Footer

**Purpose:** Provide navigation, legal clarity, and trust.

**Layout:**

- Logo and tagline left.
- Columns: Platform, Solutions, Certifications, Resources, About.
- Legal row with privacy, terms, trust center.

**Components:**

- Footer logo.
- Column links.
- Social icons.
- Trademark note.

**Assets:**

- Existing logo.
- Social icons from the same icon pack.

### 8.18 Mobile adaptation summary

- Hero image moves below copy.
- Hide secondary hero callouts below 480px.
- Outcome strip becomes 2-column or horizontal snap.
- Suite cards become single-column, with thumbnails kept above titles.
- Evidence pack panel becomes simplified product card, with review timeline below.
- How-it-works becomes vertical stepper.
- Typology cards become horizontal snap carousel if space is tight.
- Footer columns stack with accordion behavior if needed.

---

## 9. PNG Illustration Asset Register And Image-Generation Prompts

### 9.1 Universal style header

Prepend this style header to every generated PNG illustration prompt unless the asset says otherwise. This header is intentionally strict about the background because the website uses a pure white canvas.

> Premium isometric axonometric illustration for EcoGen, an AI-assisted LEED v5 evidence automation platform. Sunlit architectural sustainability studio mood on a pure white #FFFFFF canvas. Use only the EcoGen palette inside the illustration: Deep Forest #0F3D23, Primary Green #1E7A3D, Soft Sage #CFE8D6, Mist White #F7FAF7, Glass White #FFFFFC, Warm Sand #F5EEDC, Border Gray #E6EAE6, Success Mint #E6F7ED. Low-iron liquid glass panels, soft internal highlights, subtle green-tinted object shadows, natural material tones, rooftop solar, vegetation accents, human-scale architectural detail, precise 2px rounded linework, clean vector-like rendering, premium product-diagram clarity, generous untouched white space, no dark mode, no blue, no purple, no orange, no neon glow, no stock-photo realism.

### 9.1.1 Absolute background rule

Use `[ABSOLUTE BACKGROUND RULE]` as this exact instruction:

Add this line to every image-generation request, even when using the style header:

> Background must be pure white #FFFFFF across the entire image, edge to edge. No off-white, cream, gray, Mist White, paper texture, vignette, gradient, shadow wash, transparent background, alpha channel, border frame, or colored backdrop. The illustration should appear to float and pop up from an untouched white website canvas.

### 9.2 Universal negative prompt

> Avoid: non-white backgrounds, off-white backgrounds, cream backgrounds, gray canvas, Mist White canvas, paper texture, vignette, gradients behind the object, transparent background, alpha channel, colored border frame, purple or blue AI gradients, neon cyberpunk lighting, dark navy SaaS dashboard, generic stock photos, random abstract blobs, heavy black shadows, metallic chrome, cluttered labels, illegible text, rainbow KPI colors, red/yellow/blue status chips, people posing for camera, photorealistic office interior, cartoon mascots, childish icons, rough sketch style, fake brand logos, certification guarantee badges, overpacked dashboard panels, tiny standalone icons, icon sheets.

### 9.3 PNG-only generation policy

All AI-generated image assets in this document must be PNG.

- Do not request SVG, WebP, PDF, vector source files, transparent PNG, or icon sprites from the image model.
- Generate high-resolution PNGs, then convert or optimize separately during implementation if needed.
- Large isometric scenes, product compositions, page hero art, and explanatory diagrams are valid PNG-generation targets.
- Small icons, repeated feature icons, FAQ marks, metric marks, step icons, role icons, and divider marks should come from the icon pack, not the image model.

### 9.4 Text policy

Generated image models often distort text. For production assets:

- Prefer text-free illustrations with HTML labels overlaid in the page.
- If labels are needed, use short placeholder plaques and replace with HTML in implementation.
- UI mockups can contain abstract lines, dots, and blank label bars.
- Do not put body copy inside generated images.

### 9.5 Asset bucket definitions

| Bucket | Meaning | Production rule |
| ------ | ------- | --------------- |
| A: Key PNG illustration | Large isometric or product scene. | Generate with AI as PNG only. |
| B: PNG UI mockup | Product-like panel with abstract UI lines. | Generate with AI as PNG only; keep text abstract. |
| C: Icon pack | Small functional icon or repeated UI mark. | Use `lucide-react` or fallback icon pack, not AI image generation. |
| D: Manual brand asset | Logo, favicon, social icons. | Produce in Figma or code, not AI image generation. |

### 9.6 Key PNG illustration summary

| ID | Asset | Section | Bucket | Format | Priority |
| -- | ----- | ------- | ------ | ------ | -------- |
| 01 | Hero ecosystem and evidence map | Hero | A | PNG, 2400x1500 | Critical |
| 02a-02e | Supported suite miniatures | Suite scope | A | PNG, 1000x750 each | Critical |
| 03 | Fragmented evidence risk diagram | Problem | A | PNG, 1600x1100 | High |
| 04 | Evidence pack product illustration | Evidence pack showcase | B | PNG, 1800x1100 | Critical |
| 05 | Master workflow flow diagram | How it works | A | PNG, 2000x900 | Medium |
| 06a-06f | Building typology miniatures | Typologies | A | PNG, 1000x750 each | Critical |
| 07 | Water Efficiency pilot illustration | Case study | A | PNG, 1400x1000 | High |
| 08 | Source routing network | Integrations | A | PNG, 1600x1000 | High |
| 09 | Audit trail and human approval chain | Trust | A | PNG, 1600x1000 | High |
| 10 | Final CTA botanical architecture band | Final CTA | A | PNG, 2000x500 | Medium |
| 11 | Open Graph image | Social | A | PNG, 1200x630 | High |

### 9.7 Icon-pack-only summary

Do not create image-generation prompts or PNG files for these. Use the icon pack mapping in Section 6.

| Area | Use icon pack for |
| ---- | ----------------- |
| Outcome strip | Automate documentation, centralize evidence, track credits, optimize performance, achieve readiness. |
| Product value cards | All 8 feature-card icon wells. |
| How-it-works steps | The 5 step icons. |
| Readiness metrics | Time saved, human approval, claim-source link, hidden gaps. |
| Persona cards | Senior consultant, project manager, junior consultant, specialist reviewer, building owner. |
| FAQ | Plus/minus controls and inline help icon. |
| Section dividers | Use CSS, tiny inline icon, or no divider mark. |

---

### ASSET 01 - Hero ecosystem and evidence map

**Where:** Hero  
**Format:** PNG, 2400x1500, pure white #FFFFFF background required  
**File:** `01-hero-ecosystem-evidence-map.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Create a wide isometric hero scene showing a sustainable mid-rise building as the central object: rooftop solar panels, green roof, planted terraces, visible interior floors, small human-scale paths, a service lane, and a calm landscaped site. Around the building, connect six floating glass callout panels with thin Primary Green #1E7A3D connector lines. The callouts represent Water Efficiency, Refrigerant Management, Low-Emitting Materials, Quality Plans, Integrative Process, and Reviewer-ready Evidence Pack. Include a smaller evidence-pack UI tile near the lower right with abstract document rows, a source index icon, a confidence tier seal, and a human approval record. The whole image should read as one governed evidence ecosystem, not a decorative building render. Keep the background pure white #FFFFFF with abundant untouched whitespace so the building and glass panels appear to pop up from the page. Short labels may appear as simple plaques, but all readable text should be minimal and replaceable by HTML overlay.

---

### ASSET 02 - Supported suite miniatures

**Where:** Supported credit scope cards  
**Format:** PNG, 1000x750 each, pure white #FFFFFF background required  
**Bucket:** A

#### ASSET 02a - Water Efficiency suite miniature

**File:** `02a-suite-water-efficiency.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A compact isometric sustainable building water-efficiency diagram for a LEED evidence workflow card. Show a small building with a green roof, visible restroom/fixture zone as simplified interior blocks, water droplet icon wells, a subtle pipe route line in Primary Green #1E7A3D, and a glass evidence panel with abstract calculation rows. The scene should communicate indoor and outdoor water use reduction evidence, not plumbing complexity. Minimal label plaque for "WEp2 + WEc2" only if text renders cleanly.

#### ASSET 02b - Refrigerant Management suite miniature

**File:** `02b-suite-refrigerant-management.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A compact isometric rooftop mechanical equipment scene for refrigerant management. Show a small green-roof building with rooftop HVAC units, a service technician scale figure as a tiny neutral silhouette, a snowflake/refrigerant icon well, and a glass evidence panel showing abstract equipment inventory rows and a Primary Green approval seal. Keep refrigerant lines subtle and green-only. Minimal label plaque for "EAp5 + EAc7" if needed.

#### ASSET 02c - Quality Plans suite miniature

**File:** `02c-suite-quality-plans.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A compact isometric construction quality plan scene. Show a partially finished sustainable building, clean construction staging area, protective material zones, checklist board, ventilation/airflow arrows in Soft Sage and Primary Green, and a glass plan document with abstract checklist rows. The mood should be orderly and controlled, not messy construction. Minimal label plaque for "EQp1 + EQp2" if needed.

#### ASSET 02d - Integrative Process suite miniature

**File:** `02d-suite-integrative-process.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A compact isometric planning table and site-analysis scene. Show a small architectural site model with a green building, climate layer, map contour lines, community context nodes, and two glass research cards connected by Primary Green lines. The image should suggest early collaboration, climate and human-impact research, and project-specific synthesis. Minimal label plaque for "IPp1 + IPp2" if needed.

#### ASSET 02e - Low-Emitting Materials suite miniature

**File:** `02e-suite-low-emitting-materials.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A compact isometric material library scene. Show stacked sample boards, flooring tile, paint can silhouette, adhesive tube, and certificate cards arranged on a glass surface. Primary Green check seals connect product certificates to a small evidence panel with abstract rows. The image should communicate product evidence screening and low-emitting material validation. Minimal label plaque for "MRc3" if needed.

---

### ASSET 03 - Fragmented evidence risk diagram

**Where:** Problem section  
**Format:** PNG, 1600x1100, pure white #FFFFFF background required  
**File:** `03-fragmented-evidence-risk.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A calm isometric diagram showing fragmented LEED documentation before EcoGen. On the left, separate floating glass fragments: spreadsheet grid, PDF stack, email thread card, product certificate, calculator sheet, and reviewer comment bubble. These fragments are disconnected and slightly misaligned, with pale Border Gray connector lines that do not meet. On the right, a single clean evidence workspace panel begins to organize the fragments with a Primary Green path line. The tone should show risk and clutter without looking chaotic or dark. No readable body text, only abstract lines and icons.

---

### ASSET 04 - Evidence pack product illustration

**Where:** Evidence pack showcase  
**Format:** PNG, 1800x1100, pure white #FFFFFF background required  
**File:** `04-evidence-pack-product-illustration.png`  
**Bucket:** B

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A premium isometric product UI panel showing a LEED evidence pack workspace for Water Efficiency. The main glass panel has a left rail of abstract section rows, a top summary card, a confidence tier chip, region and version chips, a calculation summary area, and a source table with abstract document rows. On the right, a vertical human-review timeline shows intake, data extraction, calculation, internal review, and human approval as small circular steps with Primary Green completed states. Include a small signature/approval card at the bottom right using abstract lines, not readable text. Keep everything light, glassy, green-only, and implementation-friendly.

---

### ASSET 05 - Master workflow flow diagram

**Where:** How it works  
**Format:** PNG, 2000x900, pure white #FFFFFF background required  
**File:** `05-master-workflow-flow.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A wide horizontal isometric flow diagram with five stations: project setup, evidence intake, workflow automation, human review, export package. One continuous Primary Green path line connects all stations left to right. Each station is a glass tile with a small icon and abstract UI lines. Use generous whitespace and make the sequence easy to implement as a page section. No paragraphs or dense labels.

---

### ASSET 06 - Building typology miniatures

**Where:** Designed for every building typology  
**Format:** PNG, 1000x750 each, pure white #FFFFFF background required  
**Bucket:** A

#### ASSET 06a - Data center

**File:** `06a-typology-data-center.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric data center building with rooftop solar, green roof strips, clean service yard, and subtle cooling equipment. Include evidence workflow glass tile beside it with abstract rows. Calm and precise, no dark server-room aesthetic.

#### ASSET 06b - Hospital

**File:** `06b-typology-hospital.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric hospital building in EcoGen palette, with planted terraces, clear entry canopy, rooftop mechanical units, and a small reviewer-ready evidence tile. Use a simple medical cross shape only if it stays green and subtle, no red.

#### ASSET 06c - School

**File:** `06c-typology-school.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric school campus with classroom blocks, courtyard greenery, sports court, solar roof panels, and a small evidence workflow tile. Warm, educational, and architectural.

#### ASSET 06d - Office

**File:** `06d-typology-office.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric office building with glass facade, green roof, planted plaza, bike parking, and a clean evidence dashboard tile. Precise, calm, premium.

#### ASSET 06e - Campus

**File:** `06e-typology-campus.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric multi-building campus with connected paths, tree canopy, water feature, and portfolio evidence tiles floating above several buildings. Show portfolio visibility with green path lines.

#### ASSET 06f - Sites and masterplans

**File:** `06f-typology-sites-masterplans.png`

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A small isometric masterplan site with contour-like landscape, paths, stormwater garden, site boundary line, and GIS/source evidence nodes. Use Primary Green to trace the site boundary and source route.

---

### ASSET 07 - Water Efficiency pilot illustration

**Where:** Pilot workflow case study block  
**Format:** PNG, 1400x1000, pure white #FFFFFF background required  
**File:** `07-water-efficiency-pilot.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] An isometric Water Efficiency pilot scene showing a mid-size office building with green roof and visible water-efficient fixture zones, a small fixture schedule spreadsheet tile, a baseline/proposed calculation tile, and a reviewer approval card connected by Primary Green path lines. The image should clearly communicate "fixture schedule to evidence pack" in a calm premium way. No exaggerated claims, no fake certification badge, no dense text.

---

### ASSET 08 - Source routing network

**Where:** Integrations and inputs  
**Format:** PNG, 1600x1000, pure white #FFFFFF background required  
**File:** `08-source-routing-network.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A wide isometric source routing network diagram. Left side contains input source tiles: Excel/CSV schedule, PDF certificate, product database, public dataset, completed model output, manual reviewer entry. Center has a glass source router node with a leaf-shaped circuit mark. Right side has an evidence pack output panel and a manual-mode fallback lane. Use Primary Green lines for verified source paths and Soft Sage dashed lines for assisted/manual fallback paths. No brand logos, no readable API names, no blue cloud icons.

---

### ASSET 09 - Audit trail and human approval chain

**Where:** Trust, governance, and security  
**Format:** PNG, 1600x1000, pure white #FFFFFF background required  
**File:** `09-audit-approval-chain.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] An isometric audit trail diagram showing a chain of glass tiles: source upload, extraction, formula, confidence tier, reviewer comment, human approval, export. Each tile has an abstract icon and short placeholder label bar. A continuous Primary Green trace line links the tiles, with small check nodes at reviewer and approval steps. Include one final sealed evidence pack at the end. The feeling should be trustworthy and governed, not automated magic.

---

### ASSET 10 - Final CTA botanical architecture band

**Where:** Final CTA  
**Format:** PNG, 2000x500, pure white #FFFFFF background required  
**File:** `10-final-cta-botanical-band.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A wide, low-contrast final CTA illustration band on a pure white #FFFFFF canvas. Show very pale line-art botanical leaves, a faint isometric building outline, subtle glass panel edges, and a Primary Green path line that gently curves toward a small evidence pack seal. Keep the outer image background completely white and mostly empty so HTML headline and buttons can sit on top. No readable text, no high contrast, no busy detail.

---

### ASSET 11 - Open Graph image

**Where:** Social previews  
**Format:** PNG, 1200x630, pure white #FFFFFF background required  
**File:** `11-og-default.png`  
**Bucket:** A

> **Prompt:**  
> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] A 1200x630 social preview image for EcoGen. Left side: large empty pure white space reserved for the EcoGen wordmark and headline overlay in HTML or design tool. Right side: compact isometric sustainable building plus evidence pack tile, connected by Primary Green source paths. Include subtle glass panels, rooftop solar, vegetation, and approval seal. Use pure white #FFFFFF background and no colored frame. Do not include readable body text.

Recommended overlay copy in design tool:

- EcoGen
- LEED v5 evidence automation
- Every LEED project. Every proof point.

---

## 10. SEO Page Visual Rules

Optional SEO support pages should reuse the same visual DNA, but with fewer bespoke assets.

### 10.1 Water Efficiency page

Use:

- Asset 02a as hero image.
- Asset 07 as process illustration.
- Icon-pack step icons for compact workflow rows.
- Optional Asset 05 if the page needs a larger workflow flow diagram.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a Water Efficiency evidence workflow diagram showing fixture schedule upload, baseline calculation, proposed-use calculation, reduction result, and reviewer approval as five isometric glass stations connected by Primary Green path lines. No dense text, no fake point guarantee.

### 10.2 Refrigerant Management page

Use:

- Asset 02b as hero image.
- Asset 09 for review and audit trail.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a refrigerant management evidence workflow diagram showing equipment schedule, refrigerant identity lookup, GWP risk flag, calculation summary, and MEP reviewer approval. Use rooftop mechanical equipment and green-only evidence paths. No warning colors, no chemical hazard look.

### 10.3 Low-Emitting Materials page

Use:

- Asset 02e as hero image.
- Asset 08 for source routing.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a low-emitting materials evidence workflow diagram showing product list intake, certificate matching, VOC evidence card, exception review, and final evidence pack. Use material samples and certificate cards in an isometric glass workspace. No brand logos.

### 10.4 LEED evidence pack checklist page

Use:

- Asset 04 as core product visual.
- Asset 09 as audit trail visual.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a clean isometric checklist poster showing the components of a LEED evidence pack: source index, calculations, narrative, evidence matrix, confidence tier, human approval, export. Use simple glass tiles arranged in a measured grid with Primary Green check path. Keep labels as blank bars for HTML overlay.

### 10.5 Spreadsheets vs evidence workspace page

Use:

- Asset 03 for fragmented spreadsheet side.
- Asset 04 for evidence workspace side.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a side-by-side isometric comparison: left side shows disconnected spreadsheets, PDFs, emails, and calculators in pale Border Gray; right side shows one organized glass evidence workspace with source path, confidence, and reviewer approval in green. Avoid negative or alarmist colors.

### 10.6 AI for LEED consultants page

Use:

- Asset 09 as trust visual.
- Icon-pack role support icons from Section 6.

Additional PNG prompt if needed:

> [STYLE HEADER] [ABSOLUTE BACKGROUND RULE] Generate as a PNG-only page-specific illustration: a trust-centered AI workflow illustration for LEED consultants: AI assistant represented as a transparent workflow node, not a robot; source documents, formula trail, confidence indicator, and human reviewer approval surround it. The human review path should be visually stronger than the AI node.

---

## 11. Accessibility

- Minimum tap target is 44px.
- Do not use color alone to communicate status.
- Pair all green status marks with icon shape or text.
- Body copy minimum is 16px.
- Use one H1 per page.
- All generated images need descriptive alt text.
- Product UI mockups should not contain critical text that is unavailable to screen readers.
- Respect `prefers-reduced-motion`.
- Ensure glass surfaces maintain contrast; reduce blur before reducing text contrast.

Suggested alt text examples:

- Hero: "Isometric sustainable building connected to LEED evidence workflow callouts and reviewer-ready evidence pack."
- Evidence pack: "EcoGen evidence pack interface showing source index, confidence tier, calculation summary, and human approval timeline."
- Source routing: "Diagram of project documents, public data, and manual reviewer entries routed into a traceable LEED evidence pack."

---

## 12. Tailwind Token Snippet

Use this as the starting point if the implementation uses Tailwind.

```ts
import type { Config } from 'tailwindcss';

export default {
  content: ['./src/**/*.{ts,tsx,mdx}'],
  theme: {
    extend: {
      colors: {
        ecogen: {
          canvas: '#FFFFFF',
          primary: '#1E7A3D',
          forest: '#0F3D23',
          sage: '#CFE8D6',
          mist: '#F7FAF7',
          glass: '#FFFFFC',
          sand: '#F5EEDC',
          border: '#E6EAE6',
          mint: '#E6F7ED',
        },
      },
      fontFamily: {
        sans: ['Open Sans', 'Geist', 'Manrope', 'system-ui', 'sans-serif'],
      },
      boxShadow: {
        glass: 'inset 0 1px 0 rgba(255,255,255,0.78), 0 4px 20px rgba(16,24,16,0.06)',
        'glass-elevated': 'inset 0 1px 0 rgba(255,255,255,0.78), 0 12px 40px rgba(16,24,16,0.12)',
      },
      transitionTimingFunction: {
        ecogen: 'cubic-bezier(0.16, 1, 0.3, 1)',
      },
      maxWidth: {
        ecogen: '1200px',
      },
    },
  },
  plugins: [],
} satisfies Config;
```

CSS tokens:

```css
:root {
  --ecogen-canvas: #FFFFFF;
  --ecogen-primary: #1E7A3D;
  --ecogen-forest: #0F3D23;
  --ecogen-sage: #CFE8D6;
  --ecogen-mist: #F7FAF7;
  --ecogen-glass: #FFFFFC;
  --ecogen-sand: #F5EEDC;
  --ecogen-border: #E6EAE6;
  --ecogen-mint: #E6F7ED;
  --ecogen-glass-fill: rgba(255,255,252,0.78);
  --ecogen-focus-ring: rgba(30,122,61,0.28);
}
```

---

## 13. Checklist Before Ship

Visual:

- [ ] The website body and every exported illustration background are pure white `#FFFFFF`.
- [ ] Page reads as EcoGen green-white-sage at a glance.
- [ ] No purple, blue-neon, orange, pink, rainbow charts, or dark navy dashboard shells.
- [ ] Open Sans is loaded or Geist/Manrope fallback is intentional.
- [ ] No Inter.
- [ ] Hero is left-aligned with right-side isometric architecture/product visual.
- [ ] Glass surfaces have inner highlight, subtle edge, and restrained shadow.
- [ ] No cards inside cards.
- [ ] No centered generic SaaS hero.
- [ ] No fake proof metrics or fake customer logos.

Layout:

- [ ] 12-column desktop grid works at 1200px max width.
- [ ] Mobile collapses cleanly below 768px.
- [ ] Tap targets are at least 44px.
- [ ] No text overlaps images or components.
- [ ] Long labels wrap without breaking cards.
- [ ] Evidence pack panel remains legible on tablet and simplifies on mobile.

Assets:

- [ ] Every image-generation prompt includes `[ABSOLUTE BACKGROUND RULE]`.
- [ ] Every AI-generated image asset is requested and exported as PNG only.
- [ ] Every generated asset has a full-bleed pure white `#FFFFFF` canvas with no off-white, gradient, frame, or transparency.
- [ ] Asset 01 hero scene generated and QA'd first.
- [ ] Suite miniatures share the same camera angle and palette.
- [ ] Typology miniatures share the same scale and shadow.
- [ ] Small UI icons, feature icons, step icons, role icons, FAQ icons, and metric icons come from the icon pack, not the image model.
- [ ] All generated images avoid dense embedded text.
- [ ] All assets have alt text.
- [ ] OG image exports at 1200x630.

Product trust:

- [ ] No asset implies guaranteed points or automatic certification.
- [ ] Human approval appears in evidence, workflow, and trust visuals.
- [ ] Regional/manual fallback appears in integrations or trust visuals.
- [ ] Direct Arc/LEED Online upload is not visually implied as V1 automation.

SEO/AEO:

- [ ] Main page headings match `landing_page_master_copy.md`.
- [ ] FAQ answers are HTML text, not image text.
- [ ] Optional SEO pages link back to main platform and relevant solution pages.
- [ ] Resource diagrams support direct answers, not decorative filler.

---

## 14. Recommended Build Sequence

1. Generate Asset 01 first and use it to calibrate the entire illustration style.
2. Generate suite miniatures 02a-02e as a consistent set.
3. Generate product UI Asset 04 after the component structure is defined.
4. Generate typology miniatures 06a-06f as a single batch with identical camera angle.
5. Configure the icon pack and map all small icons to the Section 6 registry.
6. Generate final support diagrams 03, 05, 07, 08, 09, 10, and 11.
7. Run a palette and pure-white canvas sanity check on every PNG asset.
8. Implement page sections using HTML text overlays for all critical labels.
