# EcoGen LEED v5 AI Automation Platform
# Complete Product Design Specification
# Version 2.0 â€” May 2026

---

# PART 1: DESIGN SYSTEM

## 1. Visual Theme & Atmosphere

EcoGen should feel like a daylight sustainability studio translated into premium product UI. The atmosphere is calm, architectural, and evidence-led rather than flashy. Use liquid glass, pale botanical whites, and deep green anchors to create trust, clarity, and gentle innovation.

* **Density:** 4/10 â€” airy daily-app balance
* **Variance:** 6/10 â€” offset asymmetric, but still disciplined
* **Motion:** 5/10 â€” fluid, restrained, quietly alive
* **Emotional keywords:** regenerative, precise, human, sunlit, transparent, credible
* **Surface character:** frosted low-iron glass, soft internal reflections, subtle green-tinted depth, rounded edges with physical refraction
* **Critical palette rule:** the UI is monochromatic-green in feeling. All emphasis, states, charts, icons, pills, and dashboard highlights must stay within the EcoGen green family plus the approved warm/white neutrals.

## 2. Color Palette & Roles

* **Primary Green** `#1E7A3D` â€” single accent color for primary CTAs, active states, chart emphasis, and focus moments
* **Deep Forest** `#0F3D23` â€” headings, emphasized text, hover/pressed CTA states, strong icon strokes
* **Soft Sage** `#CFE8D6` â€” tinted glass washes, secondary backgrounds, icon wells, hover fills
* **Mist White** `#F7FAF7` â€” main canvas background
* **Glass White** `#FFFFFC` â€” elevated glass panels, buttons, cards, and input fills
* **Warm Sand** `#F5EEDC` â€” subtle warmth inside background gradients and low-contrast callout moments
* **Border Gray** `#E6EAE6` â€” structural borders, dividers, table lines, and input outlines
* **Success Mint** `#E6F7ED` â€” positive metrics, confirmation surfaces, success chips

### Derived Translucency Rules

* **Glass Fill Strong:** `rgba(255,255,252,0.78)`
* **Glass Fill Soft:** `rgba(247,250,247,0.64)`
* **Inner Highlight:** `rgba(255,255,255,0.76)`
* **Outer Edge:** `rgba(15,61,35,0.08)`
* **Focus Ring:** `rgba(30,122,61,0.28)`

### Palette Enforcement

* No extra accent colors. Do not introduce blue, cyan, purple, pink, orange, or neon emerald.
* Warm Sand is a neutral only â€” never a competing CTA, chart, tag, or primary icon color.
* Success Mint is part of the green system, treated as a lighter green utility tone.
* The entire interface must remain inside the green-white-sage family.

## 3. Typography Rules

Use Open Sans as the primary typeface.

* **Display:** Open Sans Semibold, 72/80, tracking -0.03em
* **H1:** Open Sans Semibold, 48/56, tracking -0.03em
* **H2:** Open Sans Semibold, 28/36
* **Body:** Open Sans Regular, 16/24, max width 65ch
* **Caption:** Open Sans Regular, 12/16
* **Button / Label:** Open Sans Semibold, 14/16, tracking 0.01em
* **Numerical emphasis:** tabular numerals for dashboards

Fallback: Geist or Manrope (not Inter). No generic serifs, no all-caps overuse, no giant screaming H1s.

## 4. Surface Language: Liquid Glass

### Default Glass Recipe

* Fill: `linear-gradient(180deg, rgba(255,255,252,0.82) 0%, rgba(247,250,247,0.70) 100%)`
* Border: `1px solid rgba(15,61,35,0.08)`
* Inner refraction: `inset 0 1px 0 rgba(255,255,255,0.78)`
* Backdrop blur: `16px`
* Soft shadow: `0 4px 20px rgba(16,24,16,0.06)`

### Elevated Glass Recipe

* Elevated shadow: `0 12px 40px rgba(16,24,16,0.12)`
* Add narrow top sheen across the upper 20% of the surface

### Radius System

* Small controls: 12px
* Standard components: 16px
* Major panels and hero cards: 24px

## 5. Component Stylings

### Buttons

* **Primary:** Deep green liquid-glass capsule. `#1E7A3D` fill, `#0F3D23` press state, near-white label, inset highlight, narrow top gloss. Hover: `translateY(-1px)`. Press: `scale(0.985)`.
* **Secondary:** Glass-white capsule with Deep Forest text and faint green stroke. Hover: soft sage wash.
* **Disabled:** Desaturated toward Soft Sage and Border Gray; no gloss.

### Glass Navigation Pill

Floating pill, glass-white fill, 16px blur, 9999px radius, subtle shadow. Active tab: pale sage capsule or understated underline.

### Chips and Tags

Rounded capsule, Success Mint or Soft Sage fill, Deep Forest text, 1px border. Variants come from opacity or green-tone shifts only â€” no rainbow hues.

### Inputs and Search

Label-above-input structure only. Frosted white, 16px radius, Border Gray outline, green focus ring. Errors inline, calm and readable.

### Stat Cards

Glass cards, generous padding, one large green number, one supporting label, abundant whitespace. Green-only numeric emphasis and icon wells.

### Loaders, Empty States, and Errors

* Loaders: skeleton shimmers shaped like the final layout
* Empty states: soft line art or isometric cues plus one clear next action
* Errors: inline, controlled, not loud

## 6. Layout Principles

* 12-column desktop grid, 1200px max-width
* Offset asymmetry, not chaos
* Spacing scale: 4, 8, 12, 16, 24, 32, 48, 64, 80
* Ban: generic row of 3 equal cards. Use 2-column zig-zag, 8/4 split, 7/5 split instead.
* Dashboards: Mist White or Glass White canvas. Sidebar: translucent glass-white or pale sage â€” never indigo or navy.
* Tables: thin border-gray dividers, green status treatments, generous row spacing.

## 7. Motion & Interaction

* Default curve: `cubic-bezier(0.16, 1, 0.3, 1)`
* Spring: stiffness 100, damping 20
* Stagger: 60â€“90ms between siblings
* Animate only `transform` and `opacity`
* Cards hover: 2px lift + slight shadow bloom
* No aggressive parallax or bouncy overshoot

## 8. Responsive Behavior

* Collapse to single column below 768px
* Minimum tap targets: 44px
* Headings scale with `clamp()`
* Preserve generous side padding on mobile; cards never touch viewport edge

## 9. Anti-Patterns (Banned)

* No purple, blue-neon, or multicolor gradient accents
* No navy sidebars, indigo rails, or violet chips
* No pure black `#000000`
* No heavy dark mode as default
* No Inter
* No centered hero composition
* No 3-column equal feature-card rows
* No emoji, badge clutter, or noisy admin-dashboard density
* No vague AI filler copy such as "next-gen", "seamless", "elevate", "unleash"
* No rainbow charts or multicolor KPI cards

---

# PART 2: PRODUCT UX SPECIFICATION

---

## Section 2: Authentication Screens

### 2.1 Login Screen

**URL:** `/auth/login`

Two-panel split. Left: auth form card. Right: decorative brand panel with isometric illustration.

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [Logo]                                  â”‚
â”‚  Welcome back                            â”‚
â”‚  Log in to your EcoGen workspace         â”‚
â”‚                                          â”‚
â”‚  [Email input]                           â”‚
â”‚  [Password input]         [Forgot?]      â”‚
â”‚  [â˜ Remember me for 30 days]             â”‚
â”‚                                          â”‚
â”‚  [Log In â€” full width]                   â”‚
â”‚                                          â”‚
â”‚  â”€â”€â”€â”€â”€ or continue with â”€â”€â”€â”€â”€â”€           â”‚
â”‚  [Google SSO]                            â”‚
â”‚  [Microsoft SSO]                         â”‚
â”‚                                          â”‚
â”‚  No account? Sign up â†’                   â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

| Field | Type | Placeholder | Validation | Error |
|---|---|---|---|---|
| Email | email | `you@company.com` | Required, valid email | "Please enter a valid email address" |
| Password | password (eye toggle) | `Enter your password` | Required | "Password is required" |

**Error states:** Wrong password (attempts 1â€“4): inline error + remaining attempts count. Account locked: full-form banner. Unverified email: amber banner + resend link. Server error: toast.

**API calls:**

| Method | Endpoint | Request | Response |
|---|---|---|---|
| POST | `/api/auth/login` | `{email, password, remember_me}` | `{access_token, refresh_token}` â†’ redirect `/dashboard` |
| POST | `/api/auth/oauth/google/initiate` | `{}` | `{redirect_url}` |
| POST | `/api/auth/oauth/microsoft/initiate` | `{}` | `{redirect_url}` |

### 2.2 Sign Up Screen

**URL:** `/auth/signup`

| Field | Type | Placeholder | Validation | Error |
|---|---|---|---|---|
| Full name | text | `Sarah Chen` | Required, 2â€“80 chars, two words | "Please enter your first and last name" |
| Work email | email | `you@company.com` | Required, valid, not personal domain | "Please enter a valid work email" |
| Company / Organization | text | `Sustainability Partners LLC` | Required, 2â€“100 chars | "Please enter your organization name" |
| Role | select | `Select your primary role` | Required | "Please select your role" |
| Password | password | `Create a strong password` | 8+ chars, complexity | Inline strength meter |

**Role options:** LEED Consultant / AP | Sustainability Project Manager | Specialist Reviewer | Building Owner / Developer | Other

**Password strength meter:** 4-segment bar (zxcvbn scoring). Weak / Fair / Good / Strong. Label + matching color.

**Terms checkbox:** Required. Links open in new tabs.

**API call:** `POST /api/auth/signup` â†’ `{user_id, requires_verification: true}` â†’ redirect to `/auth/verify-email`.

### 2.3 Email Verification Screen

**URL:** `/auth/verify-email?email=<encoded_email>`

Envelope SVG animation (flap opens, letter slides out, green checkmark appears). Shows email address. "Resend verification email" button (60s rate limit). "Use a different email address" link. Polling `GET /api/auth/verification-status` every 3 seconds â†’ on verified: success animation â†’ redirect `/onboarding/step-1`.

### 2.4 Forgot Password Screen

**URL:** `/auth/forgot-password`

Email field â†’ "Send Reset Link" button. API always returns 200 (prevents email enumeration). Success: card transitions to confirmation view with "Resend link" (60s rate limit).

### 2.5 Reset Password Screen

**URL:** `/auth/reset-password?token=<reset_token>`

Token validated on mount. Invalid/expired: error state with "Request a new link" CTA. Valid: new password + confirm + strength meter. On success: "Password updated" â†’ user must log in fresh (no tokens issued here).

### 2.6 Two-Factor Authentication Screen

**URL:** `/auth/2fa`

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  [Shield icon]                       â”‚
â”‚  Two-step verification               â”‚
â”‚  Enter the 6-digit code from your    â”‚
â”‚  authenticator app.                  â”‚
â”‚                                      â”‚
â”‚  [ _ ] [ _ ] [ _ ]  [ _ ] [ _ ] [ _ ]â”‚
â”‚                                      â”‚
â”‚  [Verify Code]                       â”‚
â”‚  â”€â”€ or â”€â”€                            â”‚
â”‚  [Use a backup code instead]         â”‚
â”‚  [â˜ Remember this device for 30d]    â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

6 individual digit boxes (32Ã—44px each), 8px gap between boxes 3 and 4. Autofocus on first, auto-advance on input, accepts paste. Auto-submits on 6 digits. Wrong code: boxes shake, border turns Deep Forest, values clear.

### 2.7 SSO / OAuth Callback Screen

**URL:** `/auth/oauth/callback?provider=...&code=...&state=...`

Full-screen loading: pulsing EcoGen leaf logo, "Completing sign-in..." heading. Processes OAuth exchange, then redirects to `/dashboard` (existing user) or `/onboarding/step-1` (new user). Error states: state mismatch (CSRF), email collision, provider error, server error â€” each with specific copy and recovery action.

---

## Section 3: Onboarding Wizard

### Wizard Shell

**URL pattern:** `/onboarding/step-<n>`

Full-screen gradient background. Centered card: max-width 760px, white, 24px radius, generous shadow. Progress indicator at top: 6 step nodes connected by lines (Active: `#1E7A3D` filled, Completed: checkmark, Upcoming: gray). Navigation footer: Back (disabled on step 1) | Continue + "Skip this step" link (steps 3, 4, 5). Auto-save: localStorage + debounced API `POST /api/onboarding/save-progress`.

### Step 1 â€” Welcome & Role Confirmation

"Welcome to EcoGen, [First Name]!" Personalized greeting. 5 role-selection cards (2-col + 1 centered bottom):

| Role | Icon | Description |
|---|---|---|
| LEED Consultant / AP | leaf-check | Prepare evidence packs, run credit automations |
| Sustainability Project Manager | gantt | Track credit status, coordinate reviews |
| Specialist Reviewer | magnifier-doc | Review assigned evidence packs |
| Building Owner / Developer | building | Monitor certification progress |
| Other | person-gear | Customize after setup |

Pre-selected from signup. Single-select. API: `PATCH /api/users/me` on Continue.

### Step 2 â€” Organization Setup

| Field | Type | Validation |
|---|---|---|
| Organization name | text | Required, 2â€“100 chars |
| Logo | file upload | Optional, PNG/JPEG/SVG, max 2MB, circular crop |
| Country | searchable select | Required |
| Timezone | select (auto-detected) | Required |
| Organization type | radio (4 horizontal pills) | Required: Consulting / Developer / Government / Non-profit |
| Team size | select | Required: 1 / 2â€“5 / 6â€“15 / 16â€“50 / 50+ |

API: `POST /api/organizations` or `PATCH /api/organizations/:id`.

### Step 3 â€” First Project Setup (Skippable)

| Field | Type | Placeholder | Validation |
|---|---|---|---|
| Project name | text | `Chicago Office Tower` | Required, 2â€“120 chars |
| Building name | text | `200 N Michigan Building` | Optional |
| Address | autocomplete | `Start typing an address...` | Required, resolves to lat/lng |
| Building type | select | `Select building type` | Required |
| Gross floor area | number + unit toggle | `e.g. 25000` | Required, positive |
| Project phase | select | `Select project phase` | Required |
| Target rating system | select | 4 LEED v5 options | Required |
| Target certification level | select | Certified / Silver / Gold / Platinum | Required |

After address selection: 240Ã—120px map thumbnail with green pin. API: `POST /api/projects`.

### Step 4 â€” Invite Team Members (Skippable)

Up to 5 invitee rows: Email input + Role dropdown + Remove button. "Add another person" ghost link (max 20). Roles: LEED Consultant / PM / Reviewer / Building Owner / MEP Reviewer / Energy Modeler / GIS Analyst / LCA Specialist / Legal Reviewer. API: `POST /api/organizations/:id/invitations`.

### Step 5 â€” Integration Setup (Skippable)

2-column integration card grid. Integrations: Google Drive / Dropbox / EnergyPlus (local file) / Revit/IFC / EPA ENERGY STAR / Arc Platform (**disabled** â€” "Coming in V2" with tooltip explaining V2 timing). "Set up later" ghost link.

### Step 6 â€” Completion Screen

Confetti burst on mount: 40 particles in green family colors, 2.5s once-only, slow-falling 3â€“5px dots/leaf shapes. Summary card with checkmarks per setup item. "What you can do now" section with 3 feature pills. Two CTAs: "Go to Dashboard" (primary) + "Create First Credit Package" (secondary, only if project was created).

---

## Section 4: Workspace Selector

**URL:** `/workspace-select` (full-page) or right-side drawer (in-app org switching)

**Purpose:** Select active organization when user belongs to 2+ organizations.

Max-width 560px card centered. Search input filters org list. "Recent" section (max 2). "All workspaces" section (alphabetical). Each org row: 72px tall, logo circle, org name, role + member count, chevron. Active org: `2px left border #1E7A3D` + "Active" badge. "Create a new organization" at bottom. Loading: 3 skeleton rows. API: `GET /api/organizations/memberships` + `POST /api/auth/set-active-org`.

**Drawer variant (in-app):** Slides from right, 400px wide, full viewport height. Same org list. Overlay scrim behind. Close button + Esc to dismiss.

---

## Section 5: Application Shell (Persistent Layout)

### 5.1 Layout Structure

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  TopBar (64px, full width, fixed)                       â”‚
â”œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¤
â”‚ Sidebar   â”‚  Main Content Area                         â”‚
â”‚ 240px /   â”‚                                             â”‚
â”‚ 64px      â”‚                                             â”‚
â”‚ collapsed â”‚                                             â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Canvas: `#F7FAF7`. Glass surfaces: `backdrop-filter: blur(16px)`, `rgba(255,255,255,0.55)`, border `1px solid rgba(255,255,255,0.4)`.

### 5.2 Left Sidebar Navigation

**Dimensions:** Expanded 240px, Collapsed 64px. Background: `rgba(207,232,214,0.38)` (pale sage glass). Border-right: `1px solid rgba(255,255,255,0.45)`. Width transition: `300ms cubic-bezier(0.16,1,0.3,1)`.

**Logo Area:** 72px height. Expanded: full logo + "EcoGen" wordmark Open Sans Semibold 18px `#0F3D23`. Collapsed: mark only, centered.

**Primary Nav Items** (6 items): Dashboard | Projects | Review Queue | Documents | Reports | Settings

Each item: 48px-tall row. Icon (2px stroke SVG, eco-motif family) + Label Open Sans 14px + optional badge.

| State | Background | Icon Color | Left Accent |
|---|---|---|---|
| Default | transparent | `#1E7A3D` | none |
| Hover | `rgba(207,232,214,0.55)` | `#0F3D23` | none |
| Active | `rgba(207,232,214,0.85)` capsule | `#0F3D23` | 3px `#1E7A3D` |

**Badge:** Pill `#1E7A3D` bg, white text, 11px. Overdue items: `#0F3D23` bg + `#F5EEDC` text (no red).

**Collapsed Tooltip:** 300ms delay, `rgba(15,61,35,0.92)` glass card, white text, 8px radius, right of sidebar edge.

**Collapse Toggle:** 24px circular icon button at logo area right edge. Chevron icon rotates 180Â° on toggle.

**Bottom Zone:** User identity block (avatar + name + role pill) + Organization switcher (if multi-org) + Help & Keyboard Shortcuts links. All collapsed to icon-only when sidebar collapsed.

### 5.3 Top Bar

**Dimensions:** 64px height, full width, fixed. Background: `rgba(255,255,255,0.62)`, `backdrop-filter: blur(16px)`. Border-bottom: `1px solid rgba(207,232,214,0.5)`.

**Left:** Breadcrumb â€” Organization > Project > Screen. Open Sans 13px, separators `/` in `#CFE8D6`.

**Center:** Global search pill (320px, height 36px, `rgba(207,232,214,0.35)` bg, border-radius 18px). Right side: `âŒ˜K` shortcut hint. Focused: `2px solid #1E7A3D` border, `0 0 0 3px rgba(30,122,61,0.12)` shadow.

**Right:** Notification bell (40px, count badge) + User avatar (36px circle, dropdown: Profile / Organization Settings / Appearance / Log Out).

### 5.4 Global Search Panel (Cmd+K Overlay)

600px wide panel, top 15% of viewport, `backdrop-filter: blur(24px)`, 20px radius. Full-viewport dimmed overlay behind. Dismiss: Esc or click backdrop.

Search input: 56px height, borderless, 16px Open Sans, autofocused. Results grouped: Projects | Credits | Documents | Reviews | Team Members. Each result: 52px row, icon in rounded square, title + subtitle, type tag. Keyboard navigation: â†‘â†“ + Enter. Empty state: magnifying glass with leaf illustration.

### 5.5 Notification Center Panel

Slide-in from right, 380px wide, `backdrop-filter: blur(20px)`. Bell icon trigger. Panel header: "Notifications" + "Mark all read" link. Tabs: All | Assigned to me | System.

**Notification item:** 80px min-height. Icon container (36px circle, green-family color per type) + Title (13px Semibold) + Description (12px) + Timestamp + Context chip + CTA button + Mark-read dot (8px `#1E7A3D`).

**Notification types:** Review assigned | SLA warning | Package approved | Changes requested | New team member | Source data stale | Workflow completed | New comment â€” all use green-family icon backgrounds only.

---

## Section 6: Main Dashboard (Portfolio Overview)

### 6.1 Layout

```
[ TopBar ]
[ Sidebar ] | [ Header: Greeting + New Project CTA          ]
             | [ Portfolio Stats Row: 4 stat cards           ]
             | [ Left 8/12: Project List ][ Right 4/12:      ]
             |                            [ Review Queue     ]
             |                            [ Exceptions Panel ]
```

Three parallel API calls on mount: `GET /api/dashboard/stats`, `GET /api/projects?limit=10`, `GET /api/reviews/pending`.

### 6.2 Dashboard Header

Greeting: "Good morning/afternoon/evening, [First Name]" â€” time-based, Open Sans 28px Semibold `#0F3D23`. Subtitle: date + credit work summary. Right: "New Project" primary capsule button (height 40px, `#1E7A3D`, + icon).

### 6.3 Portfolio Stats Row (4 Glass Cards)

Each: `rgba(255,255,255,0.55)`, `backdrop-filter: blur(16px)`, 16px radius, height 104px. Hover: elevated shadow + translateY -2px.

| Card | Primary Number | Sub-label | Icon | Extra |
|---|---|---|---|---|
| Active Projects | Count | "+2 this month" | building | 6-point sparkline |
| In Review | Count | "X packs awaiting approval" | clipboard | SLA overdue chip (`#F5EEDC` bg, `#0F3D23` text â€” no red) |
| Submission Ready | Count | "Ready for Arc upload" | upload-arrow | Up-arrow if trending |
| Awarded Points | Count | "from X credits across Y projects" | leaf-award | 6-point sparkline |

Numbers: Open Sans 36px Bold `#1E7A3D`. Loading: skeleton shimmer.

### 6.4 Project List Panel (8/12 Columns)

**Section header:** "Projects" label + segmented filter (All | Active | In Review | Completed) + sort dropdown.

**Project Card** (hoverable glass, 16px radius, 12px margin-bottom):

| Element | Spec |
|---|---|
| Project name | Open Sans 16px Semibold `#0F3D23`, 1 line |
| Location Â· Rating System Â· Target Level | 12px `rgba(15,61,35,0.6)` + 12px SemiBold `#1E7A3D` for level |
| Region badge | Pill: Full / Limited / Manual Input / Unavailable |
| Status strip | 8px dots in 4 states: Draft / In Review / Ready / Submitted |
| Package counts | 4 inline numbers with labels |
| Risk tag | "Tier C" / "Overdue" / "Missing Source" / "Regional Fallback" â€” `rgba(15,61,35,0.1)` bg |
| Next action | Compact capsule: "Continue" / "Review Required" / "Export Ready" |
| Last activity | 11px muted timestamp |

Empty state: isometric eco-building, "No projects yet", "Create your first project" CTA. Loading: 3 skeleton cards.

### 6.5 Review Queue Panel (Right, Top)

Top 5 most urgent. Each compact card: credit code badge (`#1E7A3D` bg, white text) + credit name + project name (muted) + confidence tier A/B/C badge + SLA countdown + blockers chip + "Review Now" CTA. Filter: by role, SLA, confidence.

**SLA countdown:** `#1E7A3D` if >12h; `rgba(15,61,35,0.7)` on `#F5EEDC` chip if 4â€“12h; `#0F3D23` bold if <4h â€” no red at any point.

### 6.6 Exceptions Panel (Right, Bottom)

"Needs Attention" header + count badge + "View All" link. Exception types: Low-confidence pack | Stale API data | Manual input needed | Overdue review | Missing document. Each: 32px icon circle + title + description + CTA + dismiss Ã— button (fades out on dismiss).

---

## Section 7: Project List Page (/projects)

Filter bar: Rating System | Status | Region | Target Level | Team Member â€” all as pill dropdowns. Sort: Last Updated (default) / Name / Status / Target Level. View toggle: Cards / Table.

**Card View:** Responsive grid (4-col â†’ 3-col â†’ 2-col). Same project card spec as dashboard + full-width 6px status strip at card bottom.

**Table View:** Columns â€” Project Name | Location | Rating System | Target | Credits Status | Team | Last Updated | Actions (â‹¯ menu). Headers: 12px uppercase `#7A9E7E`, sortable. Rows: 60px, alternating tint. Hover: `rgba(207,232,214,0.2)`.

**Bulk Actions Bar:** Appears on selection, slides up from bottom. Dark forest background, "N projects selected", Archive + Export + Deselect All buttons.

**Pagination:** Page number buttons (36px square), active: `#1E7A3D` bg, white text. Or infinite scroll (user preference).

---

## Section 8: New Project Creation Wizard

Full-screen slide-in panel (860px wide on desktop, dimmed backdrop `rgba(15, 61, 35, 0.45)`). 6-step progress stepper at top. Footer: Back (disabled step 1) | Next/Create.

### Step 1 â€” Project Basics

| Field | Type | Placeholder | Validation | Error |
|---|---|---|---|---|
| Project Name | Text | `e.g. 550 Green Tower` | Required, max 100 chars | "Project name is required" |
| Project Description | Textarea | `Briefly describe project scope` | Optional, max 500 chars | Character counter turns error-colored at limit |
| Client / Building Owner Name | Text | `e.g. Greenfield Capital LLC` | Optional, max 120 chars | â€” |
| Project Code / Reference | Text | `Internal reference number` | Optional, max 40 chars, alphanumeric + dashes | "Only letters, numbers, and dashes allowed" |

### Step 2 â€” Building Details

| Field | Type | Validation |
|---|---|---|
| Building Name | Text | Required |
| Street Address | Autocomplete (Google Places / OSM) | Required, must geocode |
| City, State, Country, Postal Code | Auto-filled | Read-only (override link available) |
| Map Preview | 160Ã—100px static map thumbnail | Auto-rendered after geocode |
| Building Type | Dropdown with icons | Required |
| Gross Floor Area | Number + sq ft/mÂ² toggle | Required, positive |
| Number of Floors | Number | Optional |
| Number of Occupants (FTE) | Number | Optional |
| Year Built / Renovation Year | Number | Optional |
| Project Phase | Dropdown | Required |

**Geocode failure:** Manual lat/lng inputs revealed. Building types: Office / Residential / Mixed-Use / Retail / Healthcare / Education / Industrial / Data Center / Other.

### Step 3 â€” LEED Configuration

**Rating System:** 4 radio cards â€” LEED v5 BD+C New Construction | BD+C Core & Shell | ID+C Commercial Interiors | O+M Existing Buildings. Selected: `border: 2px solid #1E7A3D`, `background: rgba(30,122,61,0.08)`, green checkmark top-right.

**Certification Level:** 4 horizontal cards with tier icon + point range. Selecting shows helper text: "Platinum requires 80+ points. Based on selected credits, you are targeting N points."

**Additional fields:** Target submit date (future-only date picker) | Previously certified toggle (conditional version + level fields).

**Incompatibility warning:** Amber callout if rating system conflicts with building type.

### Step 4 â€” Region & Data Availability Preview

Auto-detected region block. Credit availability matrix table with columns: Credit Code | Credit Name | Suite | Automation Level | Data Support (Full / Limited / Manual / Unavailable) | Notes. Warning callouts per limited/manual/unavailable credit. Acknowledgment checkbox required before Next.

### Step 5 â€” Team Setup

Current user locked as Project Owner. Add invitee rows: Email + Role + Remove. "Add another person" ghost link (max 20). Same 10 role options as Section 4. "Skip for now" link. API: `POST /api/projects`.

### Step 6 â€” Review & Create

Summary of all steps in collapsible sections with "Edit âœ" links per section. "Create Project" button (spinner on loading). On success: redirect to project detail + green toast. On partial failure (invitation errors): amber secondary toast.

---

## Section 9: Project Detail Page

### Layout

```
[ TopBar: breadcrumb Projects > [Project Name] ]
[ Sidebar ]
[ Project Header: name, location, rating, target, status, team avatars, Actions â‹¯ ]
[ Tab Bar: Overview | Credits | Documents | Team | Activity | Settings ]
[ Tab Content ]
```

### Project Header

Glass card, 24px radius, `backdrop-filter: blur(12px)`, padding 24px 32px. Project name (H1, 28px Bold `#0F3D23`). Status badge (Active/Archived/Submitted). Location, rating system, target level, phase â€” all as small badges. Team: stacked 32px avatar circles (max 5 + "+N more" chip). Actions â‹¯: Edit Details | Archive | Export Report | Duplicate.

### Tab: Overview

Left 2/3: donut chart (tonal green segments â€” Not Started/In Progress/In Review/Approved/Submitted) + "N of 9 credits complete" center label. Right 1/3: stack of key metric cards (Credits Pursued | Points Possible | Est. Time Saved | Days Until Target). Below both columns: Regional Data Status strip (4 cards: Full / Limited / Manual / Unavailable counts). Recent activity feed (last 10 events). Quick action buttons.

### Tab: Credits (Credit Board)

**Filter bar:** Suite pills (multi-select) + Status dropdown + Automation % dropdown + Regional Support dropdown + Search input + View toggle (Cards / Table).

**Credit Card** (3-col â†’ 2-col â†’ 1-col responsive grid, glass card 24px radius):

```
â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
â”‚  WEp2 [monospace green] [Water Efficiency ðŸ’§]â”‚
â”‚  Indoor Water Use Reduction                  â”‚
â”‚                                              â”‚
â”‚  8 pts  |  82% automated  |  [AI-generated] â”‚
â”‚                                              â”‚
â”‚  â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ [In Progress]  â”‚
â”‚  Step 3 of 6: Evidence Assembly             â”‚
â”‚  â–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–ˆâ–‘â–‘â–‘â–‘â–‘â–‘â–‘  50%                   â”‚
â”‚                                              â”‚
â”‚  Reviewer: [Av] Alice Chen Â· Sr Consultant  â”‚
â”‚  Confidence: Tier A  |  Support: Full       â”‚
â”‚  âš  1 Blocker  |  Updated: 2h ago           â”‚
â”‚                                              â”‚
â”‚  [           Continue           ]           â”‚
â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
```

Status badge colors: Not Started (neutral) / In Progress (info) / In Review (amber-warm) / Approved (success) / Changes Requested (orange-warm) / Rejected (muted-forest). All within green-family tones.

**Action button by status:** Start Evidence Pack | Continue | View Status | Revise | View & Export | Review Feedback.

**Table View:** Code | Name | Suite | Points | Automation % | Status | Confidence | Reviewer | Last Updated | Action. Rows 56px, alternating tint.

### Tab: Documents

Group by credit. File row: type icon + filename + type chip (Generated/Uploaded) + size + uploader + date + Download/Preview/Delete actions. Upload new file button â†’ modal with credit association selector + drag-and-drop zone.

### Tab: Team

Table: Avatar | Name/Email | Role | Status | Last Active | Actions (Edit role / Remove). Pending invitations section: Resend / Cancel per invite. Role permission matrix link.

### Tab: Activity (Audit Trail)

Filter bar: User | Credit | Event Type | Date Range | Export CSV. Chronological feed grouped by day. Each event: timestamp + actor avatar + action description + credit context + "â–¾ Details" toggle. Event types with icons: Upload / AI Generation / Review / Approval / Status Change / Export / System / Invitation.

### Tab: Settings

Sections: General Information (edit) | Building Details (edit) | LEED Configuration (limited edit with warnings) | Notification Preferences | Danger Zone (Archive with confirmation + Delete with typed project name confirmation).

---

## Section 10: Collaborator Invitation Flow

### Invite Modal

560px wide, glass card. Email rows (up to 20) + Role dropdown per row + Remove button. "Add another person" ghost link. Personal message textarea (optional, 300 char limit). "Send Invitations" â†’ `POST /api/projects/{id}/invitations`. Post-send: each row shows result (Sent âœ“ / Already a member â„¹ / Error âœ—). Footer changes to "Done" after all processed.

### Invitation Email

Subject: "You're invited to join [Project Name] on EcoGen". CTA button: "Accept Invitation". Expiry: 7 days. JWT token link with project_id, invitee_email, role, expiry.

### Accept Invitation Screen

**URL:** `/invitations/{token}`

New user path: Full Name + Password (with strength meter) fields â†’ "Accept Invitation and Create Account" â†’ redirect to project with welcome toast.

Existing user path: "Log in to Accept" â†’ auto-accepts after login â†’ redirect.

**Expired token:** "Request a new invitation" link. **Invalid token:** error screen.

### Role Permission Matrix

Full table. 10 roles Ã— 12 permissions. "Limited" entries have tooltips. Specialist roles (MEP/Energy/GIS/LCA) show domain-restricted editing scope.

---

## Section 11: Credit Selector / Credit Picker Drawer

Right-side drawer, 520px wide. Slides in from right. Grouped by suite. Search input + Suite filter + Status filter.

**Credit row:** Code (monospace green) + Name + Points + Automation % + Product mode pill + Regional support + Warning (if Limited/Manual) + Status badge + Action button (Start / Continue / View). Unavailable credits: greyed, opacity 0.5, tooltip with reason, "Learn more" link. Knowledge panel: slides in from right of drawer with credit description, methodology, required docs, regional notes, FAQ accordion.

---

## Section 12: Credit Evidence Pack Screen (Full Layout)

```
[ TopBar: breadcrumb > Projects > [Project] > Credits > [Credit Code: Name] ]
[ Sidebar ]
[ EvidencePackHeader ]
[ StepIndicator ]
[ Main Panel 8/12 ][ Right Panel 4/12: Confidence + Exceptions + Sources ]
[ HelpPanel: collapsible bottom drawer ]
```

### EvidencePackHeader Component

Sticky, glass card `rgba(247,250,247,0.85)`, padding 20px 32px. Left cluster: credit code pill (monospace `#1E7A3D`) + credit name H2 + project subtitle + product mode badge + region support badge + reviewer chips. Right cluster: status badge (with animated pulse dot if In Progress) + "Saved 2 minutes ago" timestamp + Actions menu (Save & Exit / Download Draft / View Audit Trail / Restart Workflow).

### StepIndicator

Horizontal bar: 6 step nodes (36px circles). States: Not Started (hollow `#CFE8D6` border) / In Progress (animated spinner, `#1E7A3D` border) / Complete (filled `#1E7A3D`, white checkmark) / Error (exclamation `#5A7D65`). Completed steps clickable to navigate back.

### Right Panel â€” Confidence Assessment

Glass card, sticky. Tier badge (A/B/C â€” tonal green variants only, no red/amber). 120px SVG donut gauge (animates on load). 5 component score rows with progress bars. Degradation factors list with suggestions. "What's blocking Tier A?" expandable. Export blocked warning if Tier C + critical exception.

### Right Panel â€” Exceptions

Count badge. Exception mini-cards with: severity icon + title + description + "Fix" CTA. Types: API Timeout | Region Unsupported | Low-confidence extraction | Missing source | Calculation error.

### Right Panel â€” Source Coverage

Required sources list: icon + name + date + confidence + "View" link. Status: Provided âœ“ / Auto-fetched â¬‡ / Stale (clock icon) / Missing (dash).

### HelpPanel

Fixed bottom, 48px collapsed / 280px expanded. Credit reference summary, LEED v5 standard link, FAQ accordion.

---

## Section 13: Step 1 â€” Evidence Pack Overview

Credit identity block: code pill + full name H1 + rating system chips + requirement version. Points row: prerequisite or points badge. Credit description (expandable). "What EcoGen automates" glass card (bulleted checkmarks). "What you must provide" table (input type icons). "What a reviewer will verify" list. Regional support detail block. Reviewer roles + SLA table. Expected evidence pack sections accordion. Time estimate card.

**Actions:** "Prepare Evidence Pack" primary button + "View Full Credit Requirements" ghost button (opens right-side reference panel).

---

## Section 14: Step 2 â€” Inputs

### File Upload Zones

Per required input type: zone title + accepted formats chips + size limit + drag-and-drop target (dashed `#CFE8D6` border, `#F7FAF7` bg â†’ `#E8F4EC` on drag-over). Post-upload file card: type icon + filename + size + progress bar â†’ "Extracting data..." â†’ confidence score + Preview/Remove buttons. Multiple files supported where applicable.

**WEp2 upload zones:** (1) Fixture Schedule (XLSX/PDF, Required) | (2) Occupancy Data (XLSX/PDF or manual toggle, Required) | (3) Irrigation Area Data (Optional, collapsed by default) | (4) Product Cut Sheets (PDF, multiple).

### Manual Data Entry Section

"Manual Data Entry" sub-tab. Field groups with green uppercase headers. Each field: label with inline unit, input, helper text, source/assumption dropdown (Measured / Estimated / Manufacturer / Industry Standard / Previous Project), "Attach evidence" micro-button.

**WEp2 manual fields:** FTE Occupants | Transient Visitors/day | Retail Customers/day | Flush fixture rates (GPF per type) | Flow fixture rates (GPM per type) | Days per year occupancy.

**Validation:** Required gate (cannot advance without required inputs) | Range warnings | Unit mismatch detection.

### Agent Status Banner

After first upload: glass card `border-left: 4px solid #1E7A3D`. States: Running (animated spinner + real-time progress text) | Complete (âœ“ + summary) | Error (muted warning + Retry/Manual override buttons).

---

## Section 15: Step 3 â€” Extracted Data

Source document selector tabs. Cross-credit reuse banner (if applicable). Bulk action toolbar (Select All / Approve high-confidence / Flag low-confidence / Export CSV).

**Extracted Data Table:**

| Column | Width | Content |
|---|---|---|
| Checkbox | 32px | Row selection |
| Field | 180px | Credit schema label |
| Extracted Value | 140px | Editable inline cell |
| Unit | 60px | + conversion option |
| Source Document | 160px | Filename truncated |
| Location | 100px | "Page 3, Row 12" |
| Method | 110px | OCR / Pattern Match / AI Extraction / Manual |
| Confidence | 90px | High/Moderate/Low badge (green tonal) |
| Override | 80px | Toggle + reason textarea on activate |
| Actions | 80px | View Source / Edit / Flag |

**Low-confidence row:** `rgba(207,232,214,0.2)` tint. Expandable strip: "Why is confidence low?" explanation + "Upload clearer document" link + "Manual override" button.

**Override:** Required reason text + source dropdown. Critical field override: "This will be prominently flagged in the evidence pack audit trail."

---

## Section 16: Step 4 â€” Calculations

### Formula Workspace (7/12)

Glass cards per calculation, collapsible via chevron. Collapsed: formula name + result + pass/fail.

**Expanded card:** Formula name H3 + version tag. Formula display block: dark background `#0F3D23`, monospace, `#CFE8D6` text, variable values substituted in-place. Input values table (Variable | Description | Value | Unit | Source). Intermediate values table (if applicable). Result: large `#0F3D23` number + unit. Pass/Fail: shape+icon only (no red fill) â€” Pass: `#1E7A3D` border + checkmark | Marginal: `#5A7D65` border + asterisk | Does not meet: `#8FA896` border + X.

Warning cards: narrow threshold | unit conversion note | stale factor.

"View Calculation Source Code" expandable: Python function with syntax highlighting, copy button.

**WEp2 formulas:** Baseline Annual Water Use | Design Annual Water Use | % Reduction | Prerequisite Threshold Check.

### Calculation Results Summary Panel (5/12)

Sticky glass card. Summary table (Requirement | Result | Status). Total reduction callout (large `#0F3D23` number). Marginal warning banner if within 5% of threshold.

**Energy model credits:** Muted banner stating platform parses completed model outputs only and cannot perform energy modeling.

---

## Section 17: Agent Interface â€” Activity Stream

### Agent Panel

Collapsible right-side drawer (420px) or full-width bottom drawer (320px tall). Toggle "Pin Agent Panel" replaces right panel. Tab bar: Activity Stream | Agent Thoughts | Files Created.

### Agent Status Widget (Persistent Header)

Dark background `#0F3D23`, `#CFE8D6` text. Status dot (animated ring pulse if Running). Status label + agent name. Step progress (text + 3px progress bar). Buttons: Pause / Resume from checkpoint / Provide Input / Cancel.

### Activity Stream

Newest at top. "Jump to latest" sticky button when scrolled. Each entry:

| Element | Spec |
|---|---|
| Agent icon | 32px circle, distinct per agent (Lead/Extractor/Calculator/Reporter/Checker) |
| Agent label + step type icon | Left side of entry |
| Timestamp | Muted |
| Status indicator | Running (animated dots) / Complete (âœ“) / Failed (wrench) / Waiting (clock) |
| Duration badge | "3.2s" â€” `#E8F4EC` bg, `#3D6B4F` text |
| Description | Human-readable step text |
| "â–¾ Expand" | Technical detail: API endpoint/params/response or formula inputs/outputs |

**Example WEp2 stream:** Lead Agent plans â†’ Data Extractor uploads â†’ extracts 24 fixtures â†’ fetches WaterSense per fixture â†’ Calculation Engine runs formulas â†’ Report Generator creates files.

### Agent Thought Panel

Dark background `#0F3D23` cards. First-person natural language reasoning in 13px `#CFE8D6`. Timestamps per thought. Builds trust by showing AI reasoning in real time. "Agent is thinking..." pulsing disclosure at top while active.

### File Generation Events

Special file-card entries in stream: `#E8F4EC` bg card. File icon + "Report Generator created a file" + filename + size + "Open in Preview" + "Download" buttons. File auto-appears in Documents tab.

### API Call Events

Collapsed: "Fetched [data] from [source] (cache hit/miss, Xh old) Â· duration Â· Complete". Expanded: endpoint + parameters + response hash + latency + cache status. Stale cache: "Re-fetch" ghost button.

### Error Events

`border-left: 3px solid #5A7D65`. Message + cached fallback note + confidence impact + [Retry API call] / [Use cached data] / [Manual entry] buttons. Retry leverages durable workflow checkpoint (no full restart needed).

### Workflow Resume State

On return after interruption: full-width banner "Workflow paused. Saved at [step] [timestamp]. Resume from where you left off, or start over." "Resume Workflow" primary + "Start Over" ghost (with confirmation modal).

---

## Section 18: Step 5 â€” Evidence Pack Preview

### Layout

Left 2/12: section navigation list (numbered, scrollable, sticky). Center 7/12: document preview. Right 3/12: annotation panel.

**Section nav:** Each item â€” number badge + section name + completion icon (âœ“ / spinner / dash). Clicking scrolls document to that section. Active: `#E8F4EC` bg.

**Document Preview:** Rendered as clean styled HTML (not PDF embed â€” for interactivity). `#FFFFFF` bg, A4-proportioned, Open Sans 15px 1.7 line-height. Section headers: `#0F3D23` bg bars. Hover reveals "Edit" pencil per content block. Inline edit â†’ save bar below block.

### Narrative Section (7) â€” Rich Text Editor

Toolbar: Bold | Italic | Bullet | Numbered | H1 | H2 | Undo | Redo. Editor: 14px 1.7 line-height, `#1A3A28`, min-height 300px. Actions: "Regenerate narrative" (confirmation modal â†’ 10â€“15s â†’ new content) | "AI suggestions" panel (2â€“3 alternative phrasings, "Use this" per) | Version history dropdown (side-by-side diff before restore). Word count + character count live.

### Compliance Matrix (Section 8)

Table: LEED Requirement | Evidence Provided | Status | Source Reference. "Meets" in Bold `#1E7A3D`. "Gap" in italic `#6B8F76`. Source references: clickable links opening source document at relevant page.

### Annotation Panel

"Add note" ghost button â†’ text input â†’ comment card (avatar + name + timestamp + text + reply + resolve). Resolved comments: small gray dot. Visible to reviewer during HITL review.

### Export Bar (Sticky Bottom)

Download PDF | Download XLSX (Calculation Workbook) | Download Full Package (.zip â€” all 12 sections + source docs + audit trail). File size estimate in tooltip. Disabled if Tier C + critical exception.

### Inline Value Editing in Preview

Click any extracted value or result â†’ overlay with current value + new value input + edit reason (required for audit) â†’ Save updates all referencing sections + triggers recalculation + creates audit record.

---

## Section 19: Step 6 â€” Submit to Review

### Pre-Submission Checklist

Glass card. "N of 5 complete" badge. Checklist items:

| Item | Status | Action |
|---|---|---|
| All required inputs provided | âœ“ / âœ— | Fix link |
| Extracted data reviewed | âœ“ / âœ— | Fix link |
| Calculations complete | âœ“ / âœ— | Fix link |
| Compliance narrative generated | âœ“ / âœ— | Fix link |
| Confidence tier â‰¥ Tier B | âœ“ / âœ— | Fix link |
| All critical exceptions resolved | âœ“ / âœ— | Fix link |

Submit button disabled until all required items complete.

### Reviewer Assignment

Role label + required credential tag + search-and-select (shows availability: Available / At capacity / On leave) + "Suggested:" top 3 ranked by credential + availability + project history.

### Review Options

Priority segmented control: Normal / High / Urgent. SLA display updates dynamically: "Review expected within 24h / 8h / 2h". Notes to reviewer textarea (1000 char limit).

### Submit Actions

"Submit to Review" primary (disabled until checklist passes). On click: spinner â†’ success screen. "Save Draft" secondary (ghost).

### Post-Submission Success Screen

80px animated SVG checkmark (draws then pulses once). "Evidence Pack Submitted for Review" heading. Reviewer + SLA + priority details. HITL Task ID card (monospace, copy button). "What happens next" numbered steps. Two CTAs: "View Review Status" + "Return to Credit Board".

---

## Section 20: HITL Review Screen

**URL:** `/review/[task_id]`

### Full Layout

```
[ TopBar: Review Queue > [Credit Code] â€” [Project Name] ]
[ Sidebar ]
[ ReviewHeader: full-width task info ]
[ Left 3/12: Checklist + Actions ][ Center 6/12: Doc Viewer ][ Right 3/12: Sources + Comments + History ]
```

### ReviewHeader

Full-width glass band. Credit code pill + name H2 + project/location. Reviewer role badge "Reviewing as: [Role]". SLA countdown (live, updates per minute â€” no red, uses forest depth for urgency). Priority badge. Task ID (copyable). Submission timestamp + submitted-by avatar. Confidence tier badge with tooltip. Quick stats: X flagged assumptions | X required checklist items | X optional.

### Left Panel â€” Review Checklist

Collapsible groups: Data Verification (Required) | Calculation Verification (Required) | Narrative Review (Optional) | Regional/Source Verification (conditional) | Exception Review (conditional).

**Per item:** 18px custom checkbox (checked: fills `#1E7A3D`) + item text 14px + Required/Optional 11px label + "View in evidence pack â†’" link (scrolls center panel + highlights passage) + "+ Add note" expandable textarea.

**Checked item:** strikethrough in `#7A9E7E`, opacity 0.8.

**Flagged Assumptions:** Below checklist. Each: description + "Why flagged" + Accept / Mark as Corrected (requires note) / Escalate.

**Progress bar:** "8 of 12 required items complete." 6px bar `#1E7A3D` fill.

### Left Panel â€” Review Actions (Sticky Bottom)

1. **Approve** (primary `#1E7A3D`, full-width) â€” disabled until all required items checked. Confirmation dialog with reviewer name/date/role + "I confirm..." checkbox.
2. **Request Changes** (secondary ghost, full-width) â€” always active â†’ Request Changes Modal.
3. **Reject** (secondary, warning text, full-width) â†’ Reject Modal.
4. **Reassign** (ghost text link, centered below).
5. **Save Progress** link (saves without action, "Saved âœ“" inline for 2s).
6. Keyboard shortcuts hint: "A = Approve | R = Request Changes".

### Request Changes Modal

640px glass card. Return-to-step selector (dropdown of completed steps). Comments textarea (required, min 20 chars). Pre-filled unchecked checklist items. "Attach reference" option. "Send Change Request" button â€” triggers workflow rewind to selected step, email notification, status â†’ `changes_requested`.

### Reject Modal

Reason selector (5 options). Explanation textarea (required). "Move to Manual Preparation mode" toggle. Consequence warning. "Reject Evidence Pack" button (`#0F3D23` fill â€” serious but not red).

### Reassign Modal

Team member selector (filtered by required role). Shows availability. Priority maintain/change. Note textarea. "Reassign" button.

### Center Panel â€” Evidence Pack Document Viewer

Section navigation tabs 1â€“12 with completion + flag indicators. Document rendered as clean HTML. Reviewer annotation tools:

**Annotation toolbar (on text selection):** Highlight | Comment | Flag Section.

- Highlight: `background: rgba(207, 232, 214, 0.5)` on selected text.
- Comment: right-margin bubble with reviewer avatar + text + Resolve link.
- Flag Section: adds flag icon to section tab nav.

**Section-specific reviewer interactions:** Section 6 (Calculations): formula cards read-only + commentable. Section 7 (Narrative): suggest text replacements (tracked-change style, not applied until submitter accepts). Section 8 (Compliance Matrix): individual row flagging. Section 9 (Confidence): per-factor commenting.

### Right Panel â€” Source Index

"All sources verified" or "X sources need verification" status banner. Per source: file type icon + filename + credit + upload date + file hash (SHA-256, collapsible) + "View" button.

### Right Panel â€” Comments Thread

Chronological thread. "Add general comment" button. @mention autocomplete. Threaded replies (16px indent).

### Right Panel â€” Review History

Prior reviews (if any): reviewer + date + action + summary + "View full record" link.

---

## Section 21: Reviewer Dashboard

**URL:** `/reviewer-dashboard`

Stats row: Pending | Overdue | Completed This Week | Average Review Time. Overdue card: deeper forest background, no red.

**Filter/Sort:** All | Assigned to Me | Overdue | By Credit | By Project | By Confidence Tier. Sort: SLA Urgent First (default). Batch actions: Reassign Selected | Export Review Report.

**Task Table:** Checkbox | Credit | Project | Submitted By | Confidence | SLA Remaining | Status | Action. Overdue rows: `border-left: 3px solid #0F3D23`, "OVERDUE" in Bold `#0F3D23`. "Start Review" â†’ `/review/[task_id]`. "Continue" shows prior progress "8/12 items".

**Completed Reviews:** Last 30 days. Approved (green) / Changes Requested (sage) / Rejected (forest) pills. "View review record" link.

---

## Section 22: File Management System

**URL:** `/documents`

Split layout: Left file tree (40%) | Right file details panel (60%).

### Left: File Tree

Group by: Project (default) / Credit / File Type / Date. Project groups: collapsible `â–¾`, file count shown. Credit sub-groups indented 16px. File rows: type icon + filename + credit badge + size + date. Selected: `#CFE8D6` tint, `3px solid #1E7A3D` left border. Hover: `#F7FAF7`. Right-click: Download | Preview | Rename | Move | Share link | Delete. Multi-select: checkbox + bulk actions bar.

### Right: File Details Panel

Filename (editable inline on pencil click). Metadata grid: type | size | upload date | uploaded by | associated credits | SHA-256 hash (collapsible). Version history: date + uploader + size + Restore + Download + Compare (text files). Access log: actor | action | timestamp (last 20). Sticky actions bar: Download | Preview | Share Link | Move | Delete.

### In-App File Preview

**PDF:** Toolbar: page navigation + zoom + search + download + annotations (Highlight / Comment). "Return to evidence pack" link if applicable.

**XLSX/CSV:** Read-only spreadsheet. Tab selector for multi-sheet files. Column sort/filter. Pagination (200 rows/page).

**DOCX:** Styled HTML render. "Edit Narrative" button for AI-generated files.

### In-App Document Editor (AI-generated narratives)

Minimal toolbar: Bold | Italic | Bullet | Numbered | H1 | H2 | Link. Autosave every 30 seconds ("Saved at [time]" indicator). "Unsaved changes" native dialog on close. AI Assist panel (collapsible right): "Regenerate this section" â†’ suggestion panel with Accept/Dismiss. "Restore original AI draft" (confirmation + version history preserved). "Mark as reviewed" toggle. Word count + character count.

---

## Section 23: Evidence Pack Export & Download

### Export Modal

Format selector (radio): Full Package (.zip) | PDF Report | Calculation Workbook (.xlsx) | Narrative Only (.docx) | Source Index (.xlsx) | Audit Trail (.csv). Include checkboxes: Source documents | Agent activity log | Reviewer annotations | Confidence scores. Package name: auto-generated (editable). "Generate Export" â†’ progress bar "Compiling sections... (N/12)" â†’ "Download Ready" button (expires 24h). Export recorded in audit trail.

### Manual Upload to Arc Guide

Step-by-step numbered instructions for LEED Online / Arc manual upload. Upload checklist table (Document | Upload Location | Notes). "Mark as Submitted to Arc" button â†’ dialog with submission date â†’ records `arc_submitted_at` + submitter + audit trail record. **No programmatic Arc communication.** V1 is manual-only.

---

## Section 24: Audit Trail Viewer

**Access:** Evidence pack header â†’ "View Audit Trail" | Project Settings â†’ "Audit & Compliance" | `/projects/[id]/credits/[code]/audit`.

### Layout

Full-width timeline. Filter bar: Event Type | Date Range | Actor | Export CSV. Integrity banner: "Tamper-evident. All records cryptographically signed." [Verify Integrity] button.

### Timeline Entry

Two-column: timestamp (120px) | event card (fill). Event card: `1px solid #CFE8D6`, 8px radius, left border color by event type.

| Event Type | Icon | Left Border |
|---|---|---|
| Upload | upload-arrow | `#4A8C5C` |
| Extract | scissors/parse | `#4A8C5C` |
| Calculate | sigma | `#1E7A3D` |
| Generate | document + sparkle | `#1E7A3D` |
| Review | eye | `#0F3D23` |
| Approve | checkmark circle | `#1E7A3D` bold |
| Export | share/download | `#4A6741` |
| API Call | circuit | `#7A9E7E` |
| Manual Override | hand | `#0F3D23` |

**Expandable details by event type:**
- Calculations: formula version + inputs + output + threshold check + Evidence ID
- API calls: endpoint + parameters + response hash + latency + cache status
- Human actions: reviewer + role + action + checklist items checked + comments + session duration
- File events: filename + action + size + full SHA-256 + version

**Integrity Verification:** On pass: "All N records passed checksum validation." On fail: deep forest alert, stays visible, contact admin.

---

## Section 25: Contractor Portal

**Subdomain:** `portal.ecogen.app`

Same liquid glass design tokens at reduced complexity. Mobile-first priority â€” contractors often on-site.

### 25.1 Contractor Login / Registration

**Login Screen:** Magic link tab (default) + Password tab. Magic link: email â†’ "Send Login Link" â†’ confirmation card with resend after 60s. Password: email + password + "Forgot password?" link.

**Registration Screen:** Pre-populated from invitation (email + company locked). Fields: First Name | Last Name | Company | Email | Phone (optional) | Password | Confirm Password | Terms checkbox. On success: redirect to Contractor Dashboard with welcome banner.

### 25.2 Contractor Dashboard

**TopBar:** 56px, EcoGen mark + "Contractor Portal" label, Name menu, Logout. No sidebar â€” all navigation within page.

**Active Data Requests section** (above fold, prominent):

**Request Card:**

| Element | Content |
|---|---|
| Credit type badge | Color-coded per credit type |
| Status badge | Not Started / In Progress / Submitted / Accepted / Revision Requested |
| Project name | From consultant's project |
| Credit name | e.g., "Low-Emitting Materials (MRc3)" |
| Consultant name | "Requested by [Name], [Firm]" |
| Data needed | Plain-language description |
| Due date | Amber if within 7 days, Deep Forest if within 3 |
| Progress bar | Shown only if In Progress: "3 of 7 products documented" |
| Submit Data button | Primary â€” opens data submission form |

**Completed Requests:** Below active, collapsed on mobile (tap to expand).

**Mobile:** Single-column, active requests above fold, floating "Get Help" button.

### 25.3 Low-Emitting Materials Form (MRc3)

**Section 1 â€” Product Inventory Table:**

| Field | Type | Validation |
|---|---|---|
| Product Name | Text | Required, max 120 chars |
| Manufacturer | Text | Required |
| Product Category | Dropdown | Required: Flooring / Paint / Adhesives / Insulation / Ceiling Tiles / Composite Wood / Furniture / Wall Panels / Other |
| SKU / Model Number | Text | Optional |
| Application Area | Text | Required |
| Area Covered | Number + unit toggle | Required, positive |

"Add Product" button. "Import from CSV" (template download + upload + column mapping). Max 40 rows visible before pagination.

**Autosave:** Every field change â†’ debounced 500ms â†’ localStorage + `PATCH /api/contractor/requests/[id]/draft`. Offline sync via IndexedDB.

**Section 2 â€” Per-Product Documentation:**

Collapsible panel per product. Status: No docs / Partial / Complete badge. Per product: cut sheet upload (PDF) + certification type dropdown + certification upload. Certification types: GREENGUARD Gold | FloorScore | Green Seal GS-11 | CRI Green Label Plus | Declare Label | BIFMA | CARB ATCM Phase 2 | VOC content test report | Inherently non-emitting | Other.

VOC manual entry (if no certification): value + unit (g/L) + test standard.

**Section 3 â€” Installation Confirmation:**

Three required checkboxes (all installed as specified, docs match reality, no phantom products). Notes textarea. Typed signature: Full name + Title + auto-dated. "By entering my name above I confirm this information is accurate."

**Submission Review Screen:** Read-only summary â†’ "Submit Data" â†’ loading â†’ confirmation screen with Submission ID + what happens next. API: `POST /api/contractor/requests/[id]/submit`.

### 25.4 Refrigerant Equipment Form (EAp5/EAc7)

**Section 1:** Equipment Schedule table â€” Equipment ID | Type | Manufacturer | Model | Refrigerant Type | Charge (lbs/kg) | Building Location. R-22 selection triggers inline warning. Import from CSV.

**Section 2:** Service Logs â€” PDF uploads + metadata per log (Service Date | Technician | Work Performed | Refrigerant Added/Removed lbs).

**Section 3:** Leak Detection System â€” Yes/No toggle. If yes: Detector Type | Locations | Monitoring Frequency + documentation upload.

### 25.5 Construction IAQ Plan Form (EQp1)

IAQ Management Plan PDF upload (required). SMACNA compliance toggle + alternative description if No. Filter media (MERV rating + locations + change frequency). Source control products table. HVAC protection measures textarea. Multi-image photo documentation (up to 40 images, caption per image, camera capture on mobile).

### 25.6 Fixture Documentation Form (Water Efficiency)

Section 1: Fixture Schedule table â€” Room | Fixture Type | Manufacturer | Model | Flow Rate (GPM/GPF/LPM/LPF) | Quantity | WaterSense (Yes/No). Section 2: Cut sheet uploads per model. Section 3: Installation record PDF upload (required) + plumber confirmation checkbox + typed signature.

### 25.7 Revision Request Flow

Email notification + in-portal "Revision Requested" status. Dashboard card shows consultant revision notes. Re-submission form: all prior data pre-filled, amber persistent revision notes banner, flagged fields with amber border + label, "Updated" pill on changed fields. Resubmit â†’ "Resubmission ID" confirmation.

### 25.8 Mobile Experience

Single-column layouts. Table â†’ card-per-row view on mobile. Sticky "Submit Data" button above keyboard. Camera capture alongside browse for all uploads. Offline: `localStorage` autosave on blur + debounced typing. Service Worker caches form shell. IndexedDB sync queue flushes in order on reconnect. Offline banner (amber) â†’ reconnect banner (green "Syncing..."). Minimum 44Ã—44px touch targets. ARIA error associations.

---

## Section 26: Organization Settings

**Layout:** Settings sidebar (General | Team & Roles | Integrations | Notifications | Billing | Security | API Keys) + content area. Active item: `color.primary.50` bg, 2px primary left border. Unsaved changes: sticky "Save changes / Discard" footer bar.

### 26.1 General Settings

Fields: Organization name | Logo (PNG/SVG, max 2MB, 1:1 crop modal) | Country | Timezone | Organization type | Default LEED rating system | Default units (Imperial/Metric) | Date format.

### 26.2 Team & Roles

**Team members table:** Avatar + Name/Email | Role (inline dropdown) | Joined | Last active | Actions (Remove with confirmation).

**Invite New Member Modal:** Email + Org role + personal message (optional). Sends email with 7-day expiry link.

**Org-level roles:** Owner (all permissions + billing + delete org) | Admin (all except delete/transfer) | Consultant (projects + automation) | Reviewer (assigned tasks only) | Viewer (read-only assigned projects).

**Permission matrix:** 5 roles Ã— 12 permissions. Detailed table.

**Pending invitations:** Email | Role | Sent | Expires | Resend / Revoke.

**SSO (Enterprise only):** Identity provider (Okta / Azure AD / Google Workspace / SAML 2.0) | domain lock | SAML metadata URL | attribute mapping | "Test SSO Configuration" button.

### 26.3 Integrations Settings

Integration cards grid (2-col desktop). Each card: logo + name + description + status badge + last sync + Connect/Disconnect/Settings.

| Integration | V1 Status | Action |
|---|---|---|
| LEED Online / ArcSkip | Coming in V2 | "Notify me when available" (informational only) |
| EC3 (Embodied Carbon) | Connectable | OAuth |
| WaterSense (EPA) | Auto-connected | Settings only |
| Walk Score | Auto-connected | Settings only |
| OSM / ArcGIS | Auto-connected | Settings only |
| Custom CSV/XLSX | Always available | Configure |
| Slack | Connectable | OAuth |

**Arc card explicitly disabled in V1** with tooltip: "Direct Arc submission planned for V2 after API access, schema, and permission verification are complete."

**Webhook settings (advanced):** Endpoint URL (HTTPS only) | Signing secret (generated, copy) | Event type multi-select. "Test webhook" sends payload + shows response status inline.

### 26.4 Notifications Settings

Channel toggles: In-App (always on, locked) | Email (default on) | Slack (requires integration).

Per-event matrix (rows = events, cols = channels, cells = on/off toggles):

| Event | In-App | Email | Slack |
|---|---|---|---|
| Review assigned | Locked on | Default on | Default off |
| Review SLA warning < 4h | Locked on | Default on | Default on |
| Package approved | Locked on | Optional | Optional |
| Changes requested | Locked on | Default on | Optional |
| Workflow completed | Locked on | Optional | Optional |
| API source stale | Locked on | Optional | Optional |
| Contractor submitted | Locked on | Default on | Optional |
| Weekly digest | N/A | Optional | Optional |

SLA warning events always immediate regardless of frequency setting. Email format: HTML (preview link) or plain text toggle. Slack channel assignment per row.

### 26.5 Billing & Subscription

Current plan summary card. Usage stats (projects / evidence packs / team members / storage). Plan comparison table (Free / Starter / Professional / Enterprise). Payment method + billing history. Cancel subscription retention flow (reason dropdown + optional feedback + "Keep" vs "Cancel at period end" options).

### 26.6 Security Settings

Change password (current + new + confirm + strength meter). Two-Factor Authentication toggle + enable flow (QR code â†’ TOTP verification â†’ 10 recovery codes shown once). Trusted devices list (revoke per device). Active sessions table (Device | IP + country flag | Last active | Revoke). "Revoke all other sessions" button. Login history (last 20). Data export (GDPR, ZIP download link within 24h). Account deletion (typed "DELETE" confirmation).

### 26.7 API Keys

Available to Owner and Admin only. Keys table: Name | Prefix (first 8 chars) | Scopes | Created | Last used | Expires | Revoke. "Create New API Key" modal: name + scope checkboxes (Read / Read-Write / Admin) + expiry dropdown. Key shown once on creation with copy button â€” disabled close until "I've copied this key" checkbox checked.

---

## Section 27: User Profile Page

**URL:** `/profile`

Profile photo: 80px circle, change â†’ crop modal (1:1), remove â†’ initials. Display name (required for review signatures) | Title / Role | Email (change triggers verification flow) | Phone (optional). Change email: parallel verification, old email notified, "Pending change" shown with cancel.

**LEED Credentials:** Per-credential: type dropdown (LEED AP BD+C / O+M / ID+C / Homes / ND / Green Associate / PE / SE / RA / MEP / LCA Expert / GIS Analyst / Other) + credential number + expiry date ("Expiring soon" warning if within 90 days). Add/remove credentials.

**Preferences:** Timezone | Language (English only, placeholder) | Date format. All override org defaults for this user.

**Notification preferences:** Same event matrix as 26.4, user-scoped. "Custom" badge on overridden events. "Reset to org defaults" link.

---

## Section 28: Reports & Analytics

**Layout:** Reports sidebar (categories) + content area.

### 28.1 Project Status Report

Filters: Date range | Project (multi-select) | Rating system | Consultant. Table: Project | Credits Pursued | Credits Approved | In Review | Points Possible | Target Level | Est. Points | Status. Sortable. CSV + PDF export (with org letterhead).

### 28.2 Credit Progress Report

Filters: Project (required) + Date range. Donut chart (tonal green segments by status). Horizontal stacked bar by credit category. Detail table per credit: Code | Name | Category | Points | Status | Confidence | Reviewer | Due Date.

### 28.3 Time Savings Report

Configuration: Billable hourly rate | Date range | Project filter. Summary stats: Total hours saved | Dollar value | Credits automated | Avg hours per credit. Horizontal bar chart (credit code on Y, hours saved on X). "How we calculate" expandable. Project-level table.

### 28.4 Review Performance Report

Reviewer table: Name | Assigned | Completed | Avg completion time | On-time rate | Approval rate | Revision rate. SLA compliance summary (% + overdue count + 12-week trend line). Review distribution donut.

### 28.5 Confidence & Quality Report

Confidence tier distribution by credit category (stacked horizontal bar). Quality metrics table (first-pass rate / revision rate / rejection rate / avg confidence at approval / avg exceptions per pack). Rejection reasons breakdown (horizontal bar chart). Detail table with credit + project + tier + outcome + resolution time.

### 28.6 Data Exports

Full project data export: Project multi-select + date range + include checkboxes (evidence packs / audit trails / source indexes / contractor submissions / review records / calculation workbooks). "Request Export" â†’ async â†’ email with ZIP link (7-day validity). Quick exports per credit: evidence pack ZIP | audit trail JSON/PDF | source index CSV.

---

## Section 29: Help & Documentation

### 29.1 In-App Help Panel

Trigger: "?" icon in sidebar or bottom-right floating button. Slides in from right as 400px panel (not a new tab). Has own scroll. Close with Ã— or Esc.

Search bar (full-text across articles). Tabs: Getting Started | Credits | Videos | Support.

**Getting Started:** Onboarding checklist (auto-detected from user actions, checkmarks per task, progress bar). Featured articles below.

**Credit Guide:** Credits listed by category. Click â†’ push navigation inside panel. Per-credit article: what required | what EcoGen automates | what you provide | what reviewer checks | region notes | "Can EcoGen automate this for my region?" decision tree | external USGBC reference link.

**Videos:** 2-col thumbnail grid with duration badges. Click â†’ overlay modal with native video player. Filter by category.

**Support:** Email support form (subject + message + optional screenshot upload, 1 business day SLA). Live chat (business hours Monâ€“Fri 9â€“6 PM ET; "Chat offline" outside hours). Knowledge base external link.

### 29.2 Keyboard Shortcuts Reference

Trigger: `Shift + ?` or Help panel footer link. Read-only modal.

| Shortcut | Action | Context |
|---|---|---|
| `Cmd/Ctrl + K` | Global search | Global |
| `Cmd/Ctrl + S` | Save form state | Forms |
| `Cmd/Ctrl + Enter` | Submit form | Forms |
| `Esc` | Close modal/panel/dropdown | Global |
| `A` | Approve evidence pack | HITL Review |
| `R` | Request changes | HITL Review |
| `J` | Next review task | HITL Review |
| `K` | Previous review task | HITL Review |
| `Shift + ?` | Open shortcuts reference | Global |
| `/` | Focus search bar | Dashboard, project views |
| `N` | New project | Dashboard |
| `T` | Jump to review queue | Dashboard |

Note: Shortcuts disabled when focus is inside a text input.

---

# APPENDIX A: API Response Shapes (Reference)

## Dashboard Stats
```json
{
  "active_projects": number,
  "evidence_packs_in_review": number,
  "submission_ready_packages": number,
  "awarded_points": number,
  "overdue_reviews": number
}
```

## Project Summary (list item)
```json
{
  "id": "string",
  "name": "string",
  "location": "string",
  "rating_system": "string",
  "target_level": "string",
  "region_support": "full | limited | manual | unavailable",
  "status_counts": {
    "draft": number,
    "in_review": number,
    "ready": number,
    "submitted": number
  },
  "highest_risk": "tier_c | overdue | missing_source | regional_fallback | null",
  "last_updated_at": "ISO8601"
}
```

## Evidence Pack Status
```json
{
  "workflow_id": "string",
  "status": "pending | running | paused_for_review | changes_requested | completed | failed | manual_mode",
  "current_step": "string",
  "completed_nodes": ["string"],
  "confidence": {
    "tier": "A | B | C",
    "score": number,
    "component_scores": {
      "calculation_accuracy": number,
      "evidence_provenance": number,
      "narrative_quality": number,
      "source_coverage": number,
      "cross_credit_consistency": number
    },
    "degradation_factors": [{"description": "string", "suggestion": "string", "impact": number}]
  },
  "exceptions": [{"type": "string", "title": "string", "description": "string", "severity": "high | medium | low"}]
}
```

## HITL Task
```json
{
  "task_id": "string",
  "workflow_id": "string",
  "project_id": "string",
  "credit_code": "string",
  "step_name": "string",
  "reviewer_role": "string",
  "assigned_reviewer": {"id": "string", "name": "string", "role": "string"},
  "sla_hours": number,
  "due_at": "ISO8601",
  "created_at": "ISO8601",
  "confidence_tier": "A | B | C",
  "confidence_score": number,
  "blocker_count": number,
  "checklist": [{"id": "string", "text": "string", "required": boolean}],
  "flagged_assumptions": [{"id": "string", "description": "string", "reason": "string"}]
}
```

---

# APPENDIX B: Workflow State Machine

```
pending
  â†’ running
      â†’ paused_for_review
          â†’ running (on approve)
          â†’ changes_requested â†’ running (on resume with return_to_step)
          â†’ failed (on reject with no rewind)
          â†’ manual_mode (on reject with manual flag)
      â†’ completed
  â†’ failed (on unrecoverable error)
```

Canonical status names (do not use informal variants):
- Waiting for review: `paused_for_review`
- Reviewer asks for edits: `changes_requested`
- Irrecoverable rejection: `failed` with rejection metadata
- Manual handling: `manual_mode`

HITL actions: `approve` | `request_changes` (carries `return_to_step`) | `reject` | `reassign`.

SLA expiry **never** auto-approves. Expiry triggers escalation, reassignment, or `manual_mode` only.

---

# APPENDIX C: Confidence Score Reference

| Tier | Score | Meaning | Review Requirement |
|---|---|---|---|
| A | â‰¥ 0.90 | Source-backed, deterministic, complete | Standard review |
| B | 0.75â€“0.89 | Minor gaps, moderate extraction uncertainty | Section review required |
| C | < 0.75 | Critical uncertainty, missing sources | Comprehensive review and correction |

**Floor rule:** If any critical input, formula, or source coverage score is below 0.70, the pack is Tier C regardless of weighted average.

**Weighted blend:** Calculation Accuracy 30% | Evidence Provenance 25% | Narrative Quality 20% | Source Coverage 15% | Cross-Credit Consistency 10%.

---

*EcoGen Product Design Specification v2.0*
*Generated: May 2, 2026*
*Next review: Before V1 development kickoff*
