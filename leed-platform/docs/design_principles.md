# Design Principles

## 1. Clarity First

**Principle:** Every element must have a clear purpose and make the next responsible action obvious.

**Application:**
- Dashboards show projects, blockers, review tasks, confidence tiers, and package readiness.
- Credit cards distinguish pursued, internally approved, submitted, and awarded status.
- Avoid labels that imply USGBC has accepted a credit before it has been submitted and awarded.

## 2. AI Assists, Humans Decide

**Principle:** Ecogen prepares evidence and drafts; qualified humans approve compliance-critical outputs.

**Application:**
- Every evidence pack has a named human approval gate before it becomes submission-ready.
- Automation percentage changes review depth, not whether review exists.
- UI copy uses "Prepare Evidence Pack," "Run Assistant," or "Generate Draft Package" instead of implying unattended completion.
- Energy modeling workflows say "upload completed model outputs"; they do not imply Ecogen creates or validates the model.

## 3. Progressive Disclosure

**Principle:** Show the summary first, then reveal source evidence, calculations, assumptions, and audit history as needed.

**Application:**
- Credit overview shows scope, inputs, region support, required reviewers, and confidence tier.
- Evidence pack detail expands into input registry, source index, extracted data, calculations, narratives, compliance matrix, review notes, and exception report.
- Advanced formulas and source records are available without overwhelming first-time users.

## 4. Confidence Must Explain Itself

**Principle:** Confidence is useful only when users can see why it changed and what to do next.

**Application:**
- Display evidence pack tiers A/B/C with component scores.
- Show degradation factors such as stale API data, OCR uncertainty, manual entry, unit conversion, missing source coverage, or cross-credit inconsistency.
- Provide specific fixes: upload a cut sheet, verify an occupancy count, refresh an API source, assign specialist review, or move to manual preparation.

## 5. Evidence First

**Principle:** No factual claim, calculation, or generated narrative should stand without evidence.

**Application:**
- Every extracted value links to source document, page/row/location, confidence, and extraction method.
- Every calculation shows formulas, units, intermediate values, and source references.
- Every generated narrative carries requirement version, template version, source citations, and reviewer edits.

## 6. Manual Fallback Is First-Class

**Principle:** Manual entry, regional substitution, and manual preparation are expected workflow paths, not product failures.

**Application:**
- Region support appears before users start a credit.
- Limited data regions show required manual inputs and likely review effort.
- API failures route to fallback data, cached/static sources, manual entry, or manual-prep handoff with audit trail entries.

## 7. Trust Through Transparency

**Principle:** Show what the system did, what it did not do, and who approved the result.

**Application:**
- Show source provenance, workflow steps, retries, fallbacks, and changed data.
- Preserve reviewer identity, credential/scope, comments, approval decision, and timestamp.
- Block export of unresolved critical exceptions unless a reviewer explicitly overrides with justification.

## 8. Forgiveness

**Principle:** Users must recover from mistakes, bad uploads, and review feedback without losing work.

**Application:**
- Auto-save all inputs and reviewer comments.
- Allow correction of extracted fields with source notes.
- Support request-changes workflows that rewind to the right step while preserving previous versions.
- Provide retry and manual fallback paths for upload, parsing, API, and calculation errors.

## 9. Consistency

**Principle:** Same terms, statuses, and controls must mean the same thing everywhere.

**Canonical Status Language:**

| Use | Preferred Copy |
|-----|----------------|
| Start work | Prepare Evidence Pack |
| AI draft ready | Draft Package Ready |
| Awaiting human | In Review |
| Human approved internally | Internally Approved |
| Ready for manual upload | Submission-Ready |
| Sent to USGBC | Submitted |
| Accepted by reviewer | Awarded |
| AI cannot continue safely | Manual Preparation Required |

## 10. Efficiency For Experts

**Principle:** Power users should move quickly while staying inside review and evidence controls.

**Application:**
- Bulk assign reviewers and due dates.
- Filter by confidence tier, blocker count, region support, reviewer role, and SLA risk.
- Remember reviewer preferences and common project defaults.
- Support keyboard navigation through evidence, comments, and checklist items.

## 11. Mobile-Responsive, Desktop-First

**Principle:** Full preparation and evidence review are desktop workflows; mobile supports triage and lightweight approval only when evidence is readable.

**Application:**
- Desktop: full upload, extraction, calculations, evidence pack review, and comments.
- Tablet: review queue, document preview, comments, and status.
- Mobile: task triage, reassignment, SLA checks, and simple approvals with access to evidence.

## 12. Accessibility

**Principle:** Everyone on the project team should be able to use the product.

**Requirements:**
- WCAG 2.1 AA compliance.
- Keyboard navigation.
- Screen reader support.
- Color contrast minimum 4.5:1.
- Visible focus indicators.
- Confidence and status never communicated by color alone.

## 13. Performance Perception

**Principle:** Long-running uploads, parsing, calculations, and review-state changes should feel understandable and controlled.

**Application:**
- Show progress by workflow step.
- Preserve navigation while background tasks run where safe.
- Use skeletons for dashboards and evidence pack sections.
- Show durable resume state after cancellation, retry, or worker failure.

---

*Version: 1.1*
*Last Updated: 2026-05-02*
