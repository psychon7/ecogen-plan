# Screen: Dashboard

## Purpose
Main entry point after login. Provides overview of all projects and quick access to key actions.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR (64px height)                                                       │
│ [Logo] [Search]                              [Notif] [Help] [User ▼]       │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│ SIDEBAR (240px)    │  MAIN CONTENT                                          │
│                    │                                                        │
│ [Dashboard]        │  ┌─────────────────────────────────────────────────┐   │
│ [Projects ▼]       │  │ HEADER                                          │   │
│ [Reviews]          │  │ Welcome back, Sarah              [+ New Project]│   │
│ [Team]             │  └─────────────────────────────────────────────────┘   │
│ [Settings]         │                                                        │
│                    │  ┌─────────────────────────────────────────────────┐   │
│                    │  │ STATS ROW                                       │   │
│                    │  │ [Active] [Credits] [Pending] [Points]          │   │
│                    │  └─────────────────────────────────────────────────┘   │
│                    │                                                        │
│                    │  ┌─────────────────────────────────────────────────┐   │
│                    │  │ PROJECTS SECTION                                │   │
│                    │  │ Recent Projects                    [View All →]│   │
│                    │  │                                                 │   │
│                    │  │ ┌──────────┐ ┌──────────┐ ┌──────────┐        │   │
│                    │  │ │ Project 1│ │ Project 2│ │ Project 3│        │   │
│                    │  │ │ Card     │ │ Card     │ │ Card     │        │   │
│                    │  │ └──────────┘ └──────────┘ └──────────┘        │   │
│                    │  └─────────────────────────────────────────────────┘   │
│                    │                                                        │
│                    │  ┌─────────────────────────────────────────────────┐   │
│                    │  │ PENDING REVIEWS                                 │   │
│                    │  │ Reviews requiring your attention    [View All →]│   │
│                    │  │                                                 │   │
│                    │  │ • IPp3 - Acme HQ (Due: 4h)                      │   │
│                    │  │ • WEp2 - Tech Tower (Due: 12h)                  │   │
│                    │  └─────────────────────────────────────────────────┘   │
│                    │                                                        │
└────────────────────┴────────────────────────────────────────────────────────┘
```

## Component Tree

```
Dashboard
├── TopBar
│   ├── Logo
│   ├── SearchInput
│   ├── NotificationBell
│   ├── HelpButton
│   └── UserMenu
├── Sidebar
│   ├── NavItem (Dashboard) - active
│   ├── NavItem (Projects)
│   ├── NavItem (Reviews)
│   ├── NavItem (Team)
│   └── NavItem (Settings)
└── MainContent
    ├── HeaderSection
    │   ├── GreetingText
    │   └── NewProjectButton
    ├── StatsRow
    │   └── StatCard (×4)
    ├── ProjectsSection
    │   ├── SectionHeader
    │   └── ProjectCardGrid
    │       └── ProjectCard (×3)
    └── ReviewsSection
        ├── SectionHeader
        └── ReviewList
            └── ReviewItem (×2)
```

## Spacing & Layout

### Top Bar
- Height: 64px
- Padding: 0 24px
- Background: `color.base.white`
- Border-bottom: 1px solid `color.neutral.200`

### Sidebar
- Width: 240px
- Padding: 16px 0
- Background: `color.base.white`
- Border-right: 1px solid `color.neutral.200`

### Main Content
- Padding: 32px
- Max-width: 1200px
- Gap between sections: 32px

### Stats Row
- Display: grid
- Grid: 4 columns, gap 16px
- Card padding: 20px
- Card radius: `borderRadius.lg`

### Project Cards
- Display: grid
- Grid: 3 columns, gap 16px
- Card height: 180px

## Typography

| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Greeting | 24px | 600 | `color.neutral.900` |
| Section Title | 18px | 600 | `color.neutral.900` |
| Stat Value | 32px | 700 | `color.primary.600` |
| Stat Label | 14px | 400 | `color.neutral.500` |
| Project Name | 16px | 600 | `color.neutral.900` |
| Review Item | 14px | 400 | `color.neutral.700` |

## Colors

| Element | Token |
|---------|-------|
| Page background | `color.neutral.50` |
| Card background | `color.base.white` |
| Card border | `color.neutral.200` |
| Active nav item bg | `color.primary.50` |
| Active nav item text | `color.primary.700` |
| Stat value | `color.primary.600` |

## States

### Loading
- Show skeleton placeholders for stats and cards
- Pulse animation on skeleton

### Empty (No Projects)
- Show illustration
- "No projects yet" message
- Prominent "Create First Project" button

### Error
- Toast notification
- Retry button on failed sections

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Create Project | Click "+ New Project" | Open project creation modal |
| View Project | Click project card | Navigate to project detail |
| View All Projects | Click "View All →" | Navigate to projects list |
| Review Credit | Click review item | Navigate to review interface |
| Search | Type in search | Filter projects/credits |
| Open User Menu | Click avatar | Dropdown with profile, settings, logout |

## Micro-interactions

### Project Card Hover
- Shadow: `shadow.md`
- Border: `color.primary.300`
- Transform: `translateY(-2px)`
- Duration: `motion.duration.fast`

### Stat Card Number
- Count up animation on load
- Duration: 800ms
- Easing: `motion.easing.out`

### New Project Button
- Hover: Background `color.primary.700`
- Active: `scale(0.98)`

## API Dependencies

```yaml
GET /api/dashboard/stats:
  response:
    active_projects: number
    credits_this_month: number
    pending_reviews: number
    points_achieved: number

GET /api/projects?limit=3:
  response:
    projects: array
      - id: string
        name: string
        location: string
        progress: number
        target_level: string

GET /api/reviews/pending:
  response:
    reviews: array
      - id: string
        credit_name: string
        project_name: string
        due_hours: number
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
