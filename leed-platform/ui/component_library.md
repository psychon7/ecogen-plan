# Component Library

## Button

### Purpose
Primary action trigger. Used for form submission, navigation, and action initiation.

### Variants

#### Primary
- Background: `color.primary.600`
- Text: `color.base.white`
- Border: none
- Use: Main CTAs, form submission

#### Secondary
- Background: `color.base.white`
- Text: `color.neutral.700`
- Border: 1px solid `color.neutral.300`
- Use: Cancel, back, secondary actions

#### Ghost
- Background: transparent
- Text: `color.primary.600`
- Border: none
- Use: Tertiary actions, links

#### Destructive
- Background: `color.semantic.error.DEFAULT`
- Text: `color.base.white`
- Use: Delete, remove, dangerous actions

### Sizes

| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| sm | 32px | 12px 16px | 14px |
| md | 40px | 16px 20px | 14px |
| lg | 48px | 16px 24px | 16px |

### States

#### Default
As defined in variant.

#### Hover
- Primary: Background `color.primary.700`
- Secondary: Background `color.neutral.50`
- Ghost: Background `color.primary.50`
- Duration: `motion.duration.fast`
- Easing: `motion.easing.DEFAULT`

#### Active
- Transform: `scale(0.98)`
- Duration: `motion.duration.fast`

#### Focus
- Ring: 2px `color.primary.500`
- Offset: 2px

#### Disabled
- Opacity: 0.5
- Cursor: not-allowed
- No hover effects

#### Loading
- Show spinner icon
- Text hidden but preserved for layout
- Disabled interactions

### Props
```typescript
interface ButtonProps {
  variant: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: React.ReactNode;
  iconPosition?: 'left' | 'right';
  onClick?: () => void;
  children: React.ReactNode;
}
```

### Accessibility
- Keyboard focusable
- Enter/Space triggers click
- aria-label if icon-only
- aria-disabled when disabled

---

## Input

### Purpose
Text entry field for forms.

### Variants

#### Text
- Single line text entry

#### Textarea
- Multi-line text entry
- Min-height: 80px
- Resize: vertical only

#### Number
- Numeric entry with step controls

#### File
- File upload with drag-and-drop

### States

#### Default
- Border: 1px solid `color.neutral.300`
- Background: `color.base.white`
- Text: `color.neutral.900`

#### Hover
- Border: `color.neutral.400`

#### Focus
- Border: `color.primary.500`
- Ring: 2px `color.primary.200`

#### Error
- Border: `color.semantic.error.DEFAULT`
- Background: `color.semantic.error.light`
- Icon: Error indicator

#### Disabled
- Background: `color.neutral.100`
- Text: `color.neutral.500`
- Border: `color.neutral.200`

### Props
```typescript
interface InputProps {
  type: 'text' | 'textarea' | 'number' | 'file';
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  error?: string;
  disabled?: boolean;
  required?: boolean;
  helperText?: string;
}
```

---

## Card

### Purpose
Container for related content. Used for credits, projects, and data display.

### Variants

#### Default
- Background: `color.base.white`
- Border: 1px solid `color.neutral.200`
- Radius: `borderRadius.lg`
- Shadow: `shadow.DEFAULT`

#### Hoverable
- Same as default
- Hover: `shadow.md`, border `color.primary.300`
- Cursor: pointer

#### Selected
- Border: 2px solid `color.primary.500`
- Background: `color.primary.50`

### Structure
```
┌─────────────────────────────┐
│ Header (optional)           │
│ Title                    ⋮  │
├─────────────────────────────┤
│ Content                     │
│                             │
├─────────────────────────────┤
│ Footer (optional)           │
│                    [Action] │
└─────────────────────────────┘
```

### Props
```typescript
interface CardProps {
  variant?: 'default' | 'hoverable' | 'selected';
  header?: React.ReactNode;
  footer?: React.ReactNode;
  children: React.ReactNode;
  onClick?: () => void;
}
```

---

## Badge

### Purpose
Status indicator for items. Small, non-interactive label.

### Variants

| Variant | Background | Text | Use Case |
|---------|------------|------|----------|
| default | `color.neutral.100` | `color.neutral.700` | Neutral status |
| success | `color.semantic.success.light` | `color.semantic.success.dark` | Completed, approved |
| warning | `color.semantic.warning.light` | `color.semantic.warning.dark` | Pending, in review |
| error | `color.semantic.error.light` | `color.semantic.error.dark` | Failed, rejected |
| info | `color.semantic.info.light` | `color.semantic.info.dark` | Info, processing |
| primary | `color.primary.100` | `color.primary.700` | Active, featured |

### Sizes
- sm: Height 20px, padding 4px 8px, font 12px
- md: Height 24px, padding 4px 12px, font 12px

### Props
```typescript
interface BadgeProps {
  variant: 'default' | 'success' | 'warning' | 'error' | 'info' | 'primary';
  size?: 'sm' | 'md';
  children: React.ReactNode;
}
```

---

## Progress Bar

### Purpose
Visual indicator of completion progress.

### Structure
- Track: Background `color.neutral.200`, height 8px, radius full
- Fill: Background `color.primary.500`, animated width
- Label: Percentage text (optional)

### States
- Determinate: Known progress (0-100%)
- Indeterminate: Unknown progress (animated pulse)

### Props
```typescript
interface ProgressBarProps {
  value: number; // 0-100
  max?: number;
  size?: 'sm' | 'md' | 'lg';
  showLabel?: boolean;
  variant?: 'default' | 'success';
}
```

---

## Modal

### Purpose
Overlay dialog for focused tasks. Blocks interaction with main content.

### Sizes
- sm: 400px max-width
- md: 560px max-width (default)
- lg: 720px max-width
- xl: 960px max-width
- full: 100vw/100vh

### Structure
```
┌─────────────────────────────────────┐
│ ┌───────────────────────────────┐ │
│ │ Header                        │ │
│ │ Title                    [X]  │ │
│ ├───────────────────────────────┤ │
│ │                               │ │
│ │ Content                       │ │
│ │                               │ │
│ ├───────────────────────────────┤ │
│ │ Footer                        │ │
│ │ [Cancel]          [Confirm]   │ │
│ └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Animation
- Enter: Fade in + scale up (0.95 → 1)
- Exit: Fade out + scale down
- Duration: `motion.duration.normal`
- Easing: `motion.easing.out`

### Props
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  size?: 'sm' | 'md' | 'lg' | 'xl' | 'full';
  children: React.ReactNode;
  footer?: React.ReactNode;
  closeOnOverlayClick?: boolean;
}
```

---

## File Upload

### Purpose
Drag-and-drop file upload with progress indication.

### States

#### Default
- Border: 2px dashed `color.neutral.300`
- Background: `color.neutral.50`
- Icon: Upload icon
- Text: "Drag and drop or click to browse"

#### Drag Over
- Border: 2px dashed `color.primary.500`
- Background: `color.primary.50`

#### Uploading
- Progress bar
- File name
- Cancel button

#### Success
- Checkmark icon
- File name
- File size
- Remove button

#### Error
- Error icon
- Error message
- Retry button

### Props
```typescript
interface FileUploadProps {
  accept?: string; // MIME types
  maxSize?: number; // bytes
  multiple?: boolean;
  onUpload: (files: File[]) => void;
  onError?: (error: string) => void;
}
```

---

## Credit Card

### Purpose
Project-specific component showing a LEED credit with status and actions.

### Structure
```
┌─────────────────────────────────────┐
│ [Icon] IPp3              [Status]   │
│ Carbon Assessment                   │
│                                     │
│ 0 pts | 85% automated               │
│                                     │
│ ┌───────────────────────────────┐   │
│ │ Progress: Not Started         │   │
│ └───────────────────────────────┘   │
│                                     │
│ [Start Automation]                  │
└─────────────────────────────────────┘
```

### States
- Not Started: Secondary button "Start"
- In Progress: Progress bar, "Continue"
- In Review: Warning badge, "View Status"
- Approved: Success badge, "View Documents"
- Changes Requested: Error badge, "Revise"

### Props
```typescript
interface CreditCardProps {
  code: string;
  name: string;
  points: number;
  automationLevel: number;
  status: 'not_started' | 'in_progress' | 'in_review' | 'approved' | 'changes_requested';
  progress?: number;
  onAction: () => void;
}
```

---

## Navigation

### Sidebar
- Width: 240px
- Background: `color.base.white`
- Border-right: 1px solid `color.neutral.200`
- Items: Icon + Label
- Active: Background `color.primary.50`, text `color.primary.700`

### Top Bar
- Height: 64px
- Background: `color.base.white`
- Border-bottom: 1px solid `color.neutral.200`
- Left: Logo, Search
- Right: Notifications, User menu

---

*Version: 1.0*
*Last Updated: 2026-03-21*
