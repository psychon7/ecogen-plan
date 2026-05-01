# Screen: Project Detail

## Purpose
Central hub for a single LEED project. Shows all credits, progress, and team information.

## Layout Structure

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ TOP BAR                                                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│ SIDEBAR │ MAIN CONTENT                                                      │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ PROJECT HEADER                                              │ │
│         │ │ [Back] Acme HQ - New York                    [Edit] [Share]│ │
│         │ │ 123 Main St, New York, NY 10001                            │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ PROGRESS OVERVIEW                                           │ │
│         │ │ ┌────────────┐ ┌────────────┐ ┌────────────┐               │ │
│         │ │ │ 12/40      │ │ 28%        │ │ Gold       │               │ │
│         │ │ │ Credits    │ │ Complete   │ │ Target     │               │ │
│         │ │ └────────────┘ └────────────┘ └────────────┘               │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ CREDITS GRID                                                │ │
│         │ │                                                             │ │
│         │ │ Filter: [All ▼] [Status ▼] [Category ▼]        [Search...] │ │
│         │ │                                                             │ │
│         │ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │ │
│         │ │ │ IPp3         │ │ WEp2         │ │ EAp5         │         │ │
│         │ │ │ Carbon       │ │ Water        │ │ Refrigerant  │         │ │
│         │ │ │ [Approved ✓] │ │ [In Review]  │ │ [Not Started]│         │ │
│         │ │ └──────────────┘ └──────────────┘ └──────────────┘         │ │
│         │ │                                                             │ │
│         │ │ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐         │ │
│         │ │ │ SSc6         │ │ PRc2         │ │ EAc7         │         │ │
│         │ │ │ Light        │ │ LEED AP      │ │ Enhanced     │         │ │
│         │ │ │ [Approved ✓] │ │ [Approved ✓] │ │ [In Progress]│         │ │
│         │ │ └──────────────┘ └──────────────┘ └──────────────┘         │ │
│         │ │                                                             │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
│         │ ┌─────────────────────────────────────────────────────────────┐ │
│         │ │ TEAM MEMBERS                                                │ │
│         │ │ Sarah (LEED Consultant)                                     │ │
│         │ │ Mike (Energy Modeler)                                       │ │
│         │ │ [+ Invite Member]                                           │ │
│         │ └─────────────────────────────────────────────────────────────┘ │
│         │                                                                   │
└─────────┴───────────────────────────────────────────────────────────────────┘
```

## Component Tree

```
ProjectDetail
├── TopBar
├── Sidebar
└── MainContent
    ├── ProjectHeader
    │   ├── BackButton
    │   ├── ProjectInfo
    │   │   ├── Name
    │   │   └── Address
    │   └── Actions
    │       ├── EditButton
    │       └── ShareButton
    ├── ProgressOverview
    │   └── StatCard (×3)
    ├── CreditsSection
    │   ├── FilterBar
    │   │   ├── FilterDropdown (Category)
    │   │   ├── FilterDropdown (Status)
    │   │   └── SearchInput
    │   └── CreditGrid
    │       └── CreditCard (×N)
    └── TeamSection
        ├── SectionHeader
        ├── TeamMemberList
        │   └── TeamMemberItem (×N)
        └── InviteButton
```

## Spacing & Layout

### Project Header
- Padding: 24px 32px
- Background: `color.base.white`
- Border-bottom: 1px solid `color.neutral.200`

### Progress Overview
- Padding: 24px 32px
- Display: flex, gap 24px
- Background: `color.neutral.50`

### Credits Section
- Padding: 32px
- Filter bar margin-bottom: 24px
- Grid: 3 columns, gap 16px

### Credit Card
- Width: 100%
- Height: 200px
- Padding: 20px
- Border: 1px solid `color.neutral.200`
- Radius: `borderRadius.lg`

## Credit Card States

### Not Started
- Badge: gray "Not Started"
- Button: "Start Automation" (primary)
- Progress: hidden

### In Progress
- Badge: blue "In Progress"
- Button: "Continue" (primary)
- Progress bar: partial fill

### In Review
- Badge: yellow "In Review"
- Button: "View Status" (secondary)
- Progress bar: 100%, yellow

### Approved
- Badge: green "Approved"
- Button: "View Documents" (secondary)
- Progress bar: 100%, green
- Checkmark icon

### Changes Requested
- Badge: red "Changes Requested"
- Button: "Revise" (primary)
- Progress bar: partial, red

## Typography

| Element | Font Size | Weight | Color |
|---------|-----------|--------|-------|
| Project Name | 28px | 700 | `color.neutral.900` |
| Address | 14px | 400 | `color.neutral.500` |
| Stat Value | 36px | 700 | `color.primary.600` |
| Stat Label | 14px | 400 | `color.neutral.500` |
| Credit Code | 12px | 600 | `color.primary.600` |
| Credit Name | 16px | 600 | `color.neutral.900` |
| Points | 14px | 400 | `color.neutral.500` |

## Colors

| Element | Token |
|---------|-------|
| Page background | `color.neutral.50` |
| Header background | `color.base.white` |
| Card background | `color.base.white` |
| Card hover border | `color.primary.300` |
| Approved badge | `color.semantic.success` |
| In review badge | `color.semantic.warning` |
| Changes requested | `color.semantic.error` |

## User Actions

| Action | Trigger | Result |
|--------|---------|--------|
| Start Credit | Click "Start Automation" | Navigate to credit automation |
| Continue Credit | Click "Continue" | Resume credit automation |
| View Documents | Click "View Documents" | Open document viewer |
| Revise Credit | Click "Revise" | Return to credit input |
| Filter Credits | Select filter | Update grid |
| Search Credits | Type in search | Filter grid |
| Edit Project | Click "Edit" | Open project edit modal |
| Invite Member | Click "+ Invite" | Open invite modal |

## Micro-interactions

### Credit Card Hover
- Border: `color.primary.300`
- Shadow: `shadow.md`
- Transform: `translateY(-2px)`
- Duration: `motion.duration.fast`

### Progress Bar Animation
- Width animates on load
- Duration: 600ms
- Easing: `motion.easing.out`

### Filter Change
- Grid fades out/in
- Duration: `motion.duration.normal`

## API Dependencies

```yaml
GET /api/projects/{id}:
  response:
    id: string
    name: string
    address: string
    city: string
    state: string
    zip: string
    country: string
    building_type: string
    leed_version: string
    rating_system: string
    target_level: string
    credits_completed: number
    credits_total: number
    progress_percentage: number

GET /api/projects/{id}/credits:
  response:
    credits: array
      - id: string
        code: string
        name: string
        points: number
        automation_level: number
        status: string
        progress: number

GET /api/projects/{id}/team:
  response:
    members: array
      - id: string
        name: string
        email: string
        role: string
        avatar_url: string
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
