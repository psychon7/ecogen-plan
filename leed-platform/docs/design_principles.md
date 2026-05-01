# Design Principles

## 1. Clarity First

**Principle:** Every element must have a clear purpose. Remove anything that doesn't serve the user.

**Application:**
- Dashboard shows only relevant projects and actions
- Credit cards display status at a glance
- No decorative elements without function

**Example:**
```
❌ Bad: Dashboard with decorative charts that don't help decision-making
✅ Good: Dashboard with clear project cards showing status, progress, and next actions
```

## 2. Progressive Disclosure

**Principle:** Show only what's needed at each step. Reveal complexity gradually.

**Application:**
- Credit overview shows summary first
- Detailed calculations available on expand
- Advanced options hidden by default

**Example:**
```
Step 1: Upload files (simple)
Step 2: Review extracted data (more detail)
Step 3: See full calculations (full detail)
```

## 3. Confidence Through Feedback

**Principle:** Users must always know what's happening and what to expect.

**Application:**
- Progress indicators for long operations
- Success/error states clearly communicated
- Time estimates provided

**Example:**
```
Uploading... 45% (about 10 seconds remaining)
✓ Upload complete
⚠️ Some data had low confidence - please review
```

## 4. Forgiveness

**Principle:** Allow users to recover from mistakes easily.

**Application:**
- Auto-save on all inputs
- Cancel/undo on actions
- Clear error messages with recovery paths

**Example:**
```
❌ Bad: "Error occurred"
✅ Good: "Upload failed. [Retry] or [Upload different file]"
```

## 5. Consistency

**Principle:** Same patterns, same behaviors, same language throughout.

**Application:**
- All buttons follow same interaction model
- Same color means same thing everywhere
- Navigation pattern consistent across screens

**Example:**
```
- Primary action: Green button, right side
- Secondary action: Gray button, left side
- Destructive: Red button
```

## 6. Efficiency for Experts

**Principle:** Power users should be able to work quickly.

**Application:**
- Keyboard shortcuts
- Bulk actions
- Quick filters
- Remember preferences

**Example:**
```
- Cmd+K: Quick command palette
- Bulk select credits for automation
- Remember last used reviewer
```

## 7. Trust Through Transparency

**Principle:** Show how AI works. Don't hide the process.

**Application:**
- Show confidence scores
- Explain data sources
- Display calculation steps
- Allow inspection of AI outputs

**Example:**
```
Carbon calculation:
- Grid factor: 0.0005 kg CO2e/kWh (from EPA eGRID, 95% confidence)
- Annual electricity: 500,000 kWh (from EnergyPlus model)
- Operational CO2: 250 tonnes/year
```

## 8. Mobile-Responsive, Desktop-First

**Principle:** Design for desktop (primary use case), but ensure mobile works.

**Application:**
- Full features on desktop
- Review and approve on mobile
- View-only dashboard on mobile

**Breakpoints:**
- Desktop: 1280px+ (full features)
- Tablet: 768px-1279px (adapted layout)
- Mobile: <768px (essential features only)

## 9. Accessibility

**Principle:** Everyone should be able to use the product.

**Requirements:**
- WCAG 2.1 AA compliance
- Keyboard navigation
- Screen reader support
- Color contrast minimum 4.5:1
- Focus indicators visible

**Implementation:**
- Semantic HTML
- ARIA labels
- Alt text for images
- Skip links

## 10. Performance Perception

**Principle:** Make it feel fast, even when it's not.

**Techniques:**
- Skeleton screens during loading
- Optimistic UI updates
- Progressive loading
- Cache aggressively

**Example:**
```
❌ Bad: Blank screen while loading
✅ Good: Skeleton layout that fills in as data arrives
```

---

*Version: 1.0*
*Last Updated: 2026-03-21*
