# Design System: EcoGen Liquid Glass

## 1. Visual Theme & Atmosphere

EcoGen should feel like a daylight sustainability studio translated into premium product UI. The atmosphere is calm, architectural, and evidence-led rather than flashy. Use liquid glass, pale botanical whites, and deep green anchors to create trust, clarity, and gentle innovation.

* **Density:** **4/10** - airy daily-app balance
* **Variance:** **6/10** - offset asymmetric, but still disciplined
* **Motion:** **5/10** - fluid, restrained, quietly alive
* **Emotional keywords:** regenerative, precise, human, sunlit, transparent, credible
* **Surface character:** frosted low-iron glass, soft internal reflections, subtle green-tinted depth, rounded edges with physical refraction
* **Critical palette rule:** the UI is monochromatic-green in feeling. All emphasis, states, charts, icons, pills, and dashboard highlights must stay within the EcoGen green family plus the approved warm/white neutrals from the palette image.

## 2. Color Palette & Roles

* **Primary Green** **#1E7A3D** - single accent color for primary CTAs, active states, chart emphasis, and focus moments
* **Deep Forest** **#0F3D23** - headings, emphasized text, hover or pressed CTA states, strong icon strokes
* **Soft Sage** **#CFE8D6** - tinted glass washes, secondary backgrounds, icon wells, hover fills
* **Mist White** **#F7FAF7** - main canvas background
* **Glass White** **#FFFFFC** - elevated glass panels, buttons, cards, and input fills
* **Warm Sand** **#F5EEDC** - subtle warmth inside background gradients and low-contrast callout moments
* **Border Gray** **#E6EAE6** - structural borders, dividers, table lines, and input outlines
* **Success Mint** **#E6F7ED** - positive metrics, confirmation surfaces, success chips

### Derived translucency rules

* **Glass Fill Strong** **rgba(255,255,252,0.78)**
* **Glass Fill Soft** **rgba(247,250,247,0.64)**
* **Inner Highlight** **rgba(255,255,255,0.76)**
* **Outer Edge** **rgba(15,61,35,0.08)**
* **Focus Ring** **rgba(30,122,61,0.28)**

### Palette enforcement

* No extra accent colors. Do not introduce blue, cyan, purple, pink, orange, or neon emerald.
* **Warm Sand** is a neutral only. It may appear as a whisper in backgrounds or subtle empty states, but never as a competing CTA, chart, tag, or primary icon color.
* **Success Mint** is still part of the green system and should be treated as a lighter green utility tone, not as a separate accent family.
* The entire interface must remain inside this green-white-sage family. If a screen looks multicolored at a glance, it is wrong.

## 3. Typography Rules

Use a quiet humanist sans system that feels clear and trustworthy. Match the reference brand board with Open Sans first. If Open Sans is unavailable, choose Geist or Manrope rather than Inter.

* **Display:** **Open Sans Semibold**, **72/80**, tracking **-0.03em** - large brand statements and hero headlines
* **H1:** **Open Sans Semibold**, **48/56**, tracking **-0.03em**
* **H2:** **Open Sans Semibold**, **28/36**
* **Body:** **Open Sans Regular**, **16/24**, max width **65ch**
* **Caption:** **Open Sans Regular**, **12/16**
* **Button / Label:** **Open Sans Semibold**, **14/16**, tracking **0.01em**
* **Numerical emphasis:** keep numerals clean and upright; use tabular numerals for dashboards if available

### Typography behavior

* Headlines should feel confident and breathable, never oversized for its own sake.
* Body copy should remain concise, high-clarity, and comfortably readable.
* Use weight and spacing to create hierarchy rather than relying on giant type jumps.

### Banned typography patterns

* **Inter**
* Generic serif fonts
* Ultra-condensed display faces
* All-caps overuse
* Giant screaming H1 headlines

## 4. Surface Language: Liquid Glass

All elevated surfaces should feel like layered architectural glass, not plastic UI. Blur is present but restrained. The glass effect is built from transparency, inner highlights, gentle edge contrast, and soft green-tinted shadowing.

### Default glass recipe

* Fill: **linear-gradient(180deg, rgba(255,255,252,0.82) 0%, rgba(247,250,247,0.70) 100%)**
* Border: **1px solid rgba(15,61,35,0.08)**
* Inner refraction line: **inset 0 1px 0 rgba(255,255,255,0.78)**
* Backdrop blur: **16px**
* Soft shadow: **0 4px 20px rgba(16,24,16,0.06)**

### Elevated glass recipe

* Elevated shadow: **0 12px 40px rgba(16,24,16,0.12)**
* Add a narrow top sheen across the upper **20%** of the surface
* Preserve transparency; never turn glass into a fully opaque white slab

### Radius system

* **Small controls:** **12px**
* **Standard components:** **16px**
* **Major panels and hero cards:** **24px**

Glass should feel low-iron, luminous, and tactile. Avoid hard reflections, metallic gradients, chrome effects, or glossy black glass.

## 5. Component Stylings

### Buttons

* **Primary button:** deep green liquid-glass capsule. Use **Primary Green** fill with a darker **Deep Forest** press state, near-white label text, an inset highlight, a soft internal shadow, and a narrow top gloss band.
* **Secondary button:** glass-white or mist-white capsule with **Deep Forest** text and a faint green stroke. Hover introduces a soft sage wash.
* **Disabled button:** desaturate toward **Soft Sage** and **Border Gray**; remove gloss drama and strong elevation.
* **Active feedback:** **translateY(-1px)** on hover, **scale(0.985)** on press. No outer neon glow.

### Glass navigation pill

* Floating pill container with glass-white fill, **16px** blur, **9999px** radius, subtle shadow, and evenly spaced labels
* Active tab uses a pale sage capsule or understated underline, never a bright saturated chip

### Chips and tags

* Rounded capsule with **Success Mint** or **Soft Sage** fill, **Deep Forest** text, and a 1px border in **rgba(15,61,35,0.08)**
* Tags should feel botanical and lightweight, not badge-heavy or gamified
* Never assign different hues to different tag types. Variants must come from opacity, border treatment, or green-tone shifts only.

### Inputs and search

* Use label-above-input structure only
* Input fields are frosted white with **16px** radius, **Border Gray** outline, and soft green focus ring
* Placeholder text is muted and descriptive
* Search icons and supporting UI strokes use **Primary Green** or softened forest tones
* Errors sit directly below the field and stay calm, precise, and readable

### Stat cards

* Use glass cards with generous padding, one large green number, one supporting label, and abundant whitespace
* Numeric emphasis uses **Primary Green**
* Icon wells, micro-trend lines, and metric accents must also stay green-only
* Keep stat cards calm and singular: one message per card

### Feature cards

* Tall, slim glass cards with a circular sage icon well at the top, short heading, and **2-3** lines of copy
* Use only when elevation helps hierarchy
* Prefer **2-up zig-zag**, **7/5 split**, or mixed-width arrangements over three equal cards

### Loaders, empty states, and errors

* Loaders use skeleton shimmers shaped like the exact final layout
* Empty states use soft line art or isometric cues plus one clear next action
* Errors remain inline and controlled, not loud or alarmist

## 6. Layout Principles

The layout should feel like an architecture presentation board translated into product UI: measured grid, large white margins, and clean sectional framing.

* Use a **12-column** desktop grid with a maximum content width of **1200px**
* Favor split-screen heroes: left-aligned content, right-aligned isometric eco-building or interface preview
* Use offset asymmetry, not chaos; uneven widths are welcome, but every alignment must still feel intentional
* Keep section spacing airy using the scale **4, 8, 12, 16, 24, 32, 48, 64, 80**
* Prefer white space, dividers, and surface changes over excessive card nesting
* The generic row of **3 equal cards** is banned; use **2-column zig-zag**, **8/4 split**, **7/5 split**, or selective horizontal scroll groups instead
* No overlapping UI layers in core layouts; every major element gets its own clear spatial zone
* Full-height sections must use **min-height: 100dvh**, never **h-screen**

### Dashboard-specific layout rules

* Default dashboards should use **Mist White** or **Glass White** as the primary field of view, not navy or charcoal.
* If a sidebar is present, it must be either translucent glass-white, pale sage, or **Deep Forest**. Never use indigo, midnight blue, or purple-black rails.
* Tables should feel light and editorial: thin border-gray dividers, green status treatments, generous row spacing, and no hard dark containers.

## 7. Hero Direction

The hero should immediately communicate trust, sustainability, and product rigor.

* Structure: strong left-aligned headline, one short support paragraph, one primary CTA, and a right-side isometric building or product scene
* Media: use architectural eco imagery, solar rooftops, greenery, compliance workflows, or clean dashboard crops
* Optional signature moment: if the headline needs a visual accent, insert one small rounded eco-architecture or botanical tile inline between headline lines; use only once and never let it overlap text
* No centered hero stacks
* No secondary CTA clutter
* No filler copy such as scroll prompts or bouncing chevrons

## 8. Illustration, Iconography, and Data

* **Illustration style:** isometric axonometric scenes, soft daylight, natural material tones, vegetation accents, human-scale architectural detail
* **Icons:** **2px** stroke, rounded joins, open and friendly geometry, consistent eco and utility motifs
* **Charts:** use a tonal green scale only. Start with **Deep Forest**, **Primary Green**, **Soft Sage**, **Success Mint**, and low-contrast **Border Gray**. Do not use rainbow category palettes.
* **Chart hierarchy:** the key data series uses **Primary Green**; secondary series use lighter green values or opacity reductions of the same family.
* **Dashboard surfaces:** keep chart panels bright and airy; avoid dark generic SaaS shells. Any anchoring rail must still read as EcoGen green, not cool-toned enterprise navy.
* **Status colors:** do not reach for separate yellow, red, blue, or purple systems by default. Express most states through green depth, border treatment, icons, labels, and transparency unless a true alert state is explicitly required.

### Green-only data visualization examples

* Donut and pie charts: tonal green segments only
* Line and area charts: one dominant green line plus lighter sage fills
* Progress bars: **Primary Green** fill on **Soft Sage** or **Border Gray** track
* Category badges: green text with sage or mint fills, never rainbow badges

## 9. Motion & Interaction

Motion should feel quiet and premium, like glass catching light and panels settling into place.

* Default interaction curve: **cubic-bezier(0.16, 1, 0.3, 1)**
* Spring physics for advanced interactions: **stiffness: 100**, **damping: 20**
* Use reveal cascades with **60-90ms** stagger between sibling items
* Glass buttons can carry a slow internal highlight or shimmer, but it must stay subtle and low-contrast
* Cards hover with a **2px** lift and a slight shadow bloom
* Animate only **transform** and **opacity**
* Continuous motion, if present, should stay soft: slow stat pulses, gentle diagram floats, restrained shimmer on glass surfaces
* Avoid attention-stealing loops, aggressive parallax, or bouncy overshoot everywhere

## 10. Responsive Behavior

* Collapse to a single column below **768px**
* Keep the hero media below the copy on mobile
* Minimum tap targets: **44px**
* Glass buttons must remain legible on smaller screens; reduce gloss and blur before reducing contrast
* Preserve generous side padding on mobile; cards should not touch the viewport edge
* Avoid horizontal scroll unless it is a deliberate carousel or chip group
* Headings should scale with **clamp()** and remain elegant rather than huge

## 11. Voice & Content Tone

The product voice is clear, competent, and measurable.

* Use direct claims anchored in outcomes, compliance, reporting, or performance
* Favor phrases like **first-time pass rate**, **certification readiness**, **measurable impact**, and **evidence across projects**
* Avoid startup hype, vague futurism, and empty AI slogans
* Short copy beats dense marketing paragraphs

## 12. Anti-Patterns (Banned)

* No purple, blue-neon, or multicolor gradient accents
* No navy sidebars, indigo navigation rails, or violet chips
* No pure black **#000000**
* No heavy dark mode as the default direction
* No outer-glow buttons or generic glass blobs
* No **Inter**
* No generic serif fonts
* No centered hero composition
* No **3-column** equal feature-card rows
* No overlapping text and imagery
* No giant gradient headlines
* No emoji, badge clutter, or noisy admin-dashboard density
* No fake round metrics like **99.99%**
* No vague AI filler copy such as **next-gen**, **seamless**, **elevate**, or **unleash**
* No stock-photo energy; imagery must feel architectural, ecological, and precise
* No multicolor KPI cards where each card gets a different hue
* No rainbow donuts, pastel category markers, or blue notification accents
* No visual output that reads like a generic document SaaS dashboard instead of an EcoGen sustainability platform

## 13. Agent Prompt Guide

When generating screens from this file, keep asking: does this feel like a sunlit green compliance product wrapped in real glass?

* **Landing pages:** left text, right isometric eco asset, one strong CTA, calm whitespace
* **Dashboard pages:** mist-white or glass-white canvas, optional deep-forest rail only if still clearly green, glass stat blocks, green-only charts, green-only tags, restrained data density
* **Workflow screens:** step-based cards, evidence uploads, status chips, clean progress markers, subtle success-mint confirmations
* **Component previews:** showcase primary and secondary glass buttons, the nav pill, stat card, feature card, and frosted input states
* **Color sanity check:** if any generated screen contains purple, royal blue, hot pink, amber status chips, or a dark navy sidebar, regenerate because it is off-system
