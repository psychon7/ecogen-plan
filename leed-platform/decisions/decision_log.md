# Decision Log

## ADR-001: Use Deer-Flow as Foundation

**Status:** Accepted

**Context:**
We need a workflow orchestration system for credit automation. Options:
1. Build from scratch (LangGraph + custom code)
2. Use Deer-Flow (ByteDance's open-source agent framework)
3. Use Temporal (workflow engine)

**Decision:**
Use Deer-Flow as the foundation.

**Rationale:**
- Provides 70-80% of needed infrastructure (skills, HITL, durable workflows)
- Aligns with our skill-based architecture design
- Active community (60.2k stars)
- Built on LangGraph (industry standard)
- Saves 10+ weeks of development

**Tradeoffs:**
- ✅ Faster time to market
- ✅ Proven patterns
- ⚠️ Less control over internals
- ⚠️ Need to learn Deer-Flow conventions

**Consequences:**
- Must follow Deer-Flow's SKILL.md format
- Customization limited to what's exposed
- May need to fork for deep changes

---

## ADR-002: PostgreSQL with PostGIS

**Status:** Accepted

**Context:**
Need a database for structured data with geographic queries for location-based credits.

**Decision:**
Use PostgreSQL 15+ with PostGIS extension.

**Rationale:**
- PostGIS required for location-based queries (LTc3, LTc1)
- JSONB support for flexible credit data
- Full ACID compliance
- Excellent Django/FastAPI support
- Proven at scale

**Tradeoffs:**
- ✅ Full SQL + GIS capabilities
- ✅ JSONB for flexible schemas
- ⚠️ More complex than NoSQL for simple use cases

---

## ADR-003: FastAPI for Backend

**Status:** Accepted

**Context:**
Need a Python web framework for API. Options:
1. Django + DRF
2. FastAPI
3. Flask

**Decision:**
Use FastAPI.

**Rationale:**
- Native async support (critical for API calls)
- Automatic OpenAPI documentation
- Type hints throughout
- Better performance than Django
- Easy integration with Deer-Flow (Python)

**Tradeoffs:**
- ✅ Fast, modern, async
- ✅ Auto-generated docs
- ⚠️ Less mature ecosystem than Django
- ⚠️ Need to build more from scratch

---

## ADR-004: React + TypeScript Frontend

**Status:** Accepted

**Context:**
Need a frontend framework. Options:
1. React
2. Vue
3. Svelte

**Decision:**
Use React with TypeScript.

**Rationale:**
- Largest ecosystem
- Excellent TypeScript support
- Many component libraries
- Easy hiring
- Deer-Flow UI uses React (can reuse patterns)

**Tradeoffs:**
- ✅ Largest talent pool
- ✅ Rich ecosystem
- ⚠️ More boilerplate than Vue/Svelte

---

## ADR-005: HITL Required for Complex Credits

**Status:** Accepted

**Context:**
Some credits (EAc3 Energy, MRc2 Embodied Carbon) require expert judgment.

**Decision:**
Require human review for credits with automation level < 85%.

**Rationale:**
- Energy modeling requires expert verification
- Compliance decisions need human accountability
- Builds trust with users
- Reduces liability

**Tradeoffs:**
- ✅ Higher accuracy
- ✅ Expert accountability
- ⚠️ Slower than full automation
- ⚠️ Requires reviewer availability

---

## ADR-006: Regional Credit Filtering

**Status:** Accepted

**Context:**
Some credits (LTc1 Land Protection) only work in US due to GIS data availability.

**Decision:**
Filter credits by regional data availability.

**Rationale:**
- Don't promise what we can't deliver
- Clear expectations for users
- Can expand regions over time
- Better UX than failing silently

**Implementation:**
- Detect region from project location
- Show only credits with available APIs
- Mark limited credits with warning

---

## ADR-007: JWT for API Authentication

**Status:** Accepted

**Context:**
Need authentication for API. Options:
1. Session cookies
2. JWT tokens
3. API keys

**Decision:**
Use JWT access tokens (24h) + refresh tokens (30d).

**Rationale:**
- Stateless (no server-side session storage)
- Works across domains
- Industry standard
- Easy to implement

**Tradeoffs:**
- ✅ Stateless, scalable
- ✅ Cross-domain support
- ⚠️ Can't revoke instantly (need revocation list)

---

## ADR-008: S3 for Document Storage

**Status:** Accepted

**Context:**
Need to store generated PDFs, Excel files, uploads.

**Decision:**
Use S3 (or GCS/Azure equivalent) with CDN.

**Rationale:**
- Infinite scalability
- CDN integration for fast downloads
- Versioning support
- Lifecycle policies for cost optimization

**Tradeoffs:**
- ✅ Scalable, durable
- ✅ CDN integration
- ⚠️ Ongoing cost
- ⚠️ Need to manage permissions

---

## ADR-009: Celery + RabbitMQ for Workers

**Status:** Accepted

**Context:**
Need background job processing for credit automation.

**Decision:**
Use Celery with RabbitMQ.

**Rationale:**
- Celery: Mature, feature-rich, Python-native
- RabbitMQ: Reliable, supports priority queues
- Works well with FastAPI
- Can scale workers independently

**Tradeoffs:**
- ✅ Proven, reliable
- ✅ Priority queues
- ⚠️ More complex than simple queues

---

## ADR-010: Freemium Pricing Model

**Status:** Proposed

**Context:**
Need a business model for monetization.

**Decision:**
Freemium: 2 credits free/month, then $299/user/month.

**Rationale:**
- Free tier for trial and small users
- Pro tier for serious consultants
- Per-user pricing aligns with value
- Simple to understand

**Tradeoffs:**
- ✅ Easy to understand
- ✅ Trial without commitment
- ⚠️ Need to prevent abuse of free tier
- ⚠️ May need enterprise tier later

---

## ADR-011: 14-Day MVP Timeline

**Status:** Accepted

**Context:**
Need to ship quickly to validate market.

**Decision:**
Build MVP with 8 credits in 14 days using Deer-Flow.

**Rationale:**
- Deer-Flow provides 70-80% of infrastructure
- Focus on high-automation credits first
- Get user feedback early
- Iterate based on real usage

**MVP Credits:**
1. PRc2 - LEED AP (95% automation)
2. SSc6 - Light Pollution (95% automation)
3. EAp5 - Refrigerant (90% automation)
4. WEp2 - Water Min (90% automation)
5. SSc5 - Heat Island (85% automation)
6. EAc7 - Refrigerant Enhanced (90% automation)
7. IPp3 - Carbon (85% automation)
8. MRp2 - Embodied Carbon (85% automation)

---

## ADR-012: No USGBC Integration in V1

**Status:** Accepted

**Context:**
USGBC Arc integration would allow direct submission.

**Decision:**
Defer USGBC integration to V2.

**Rationale:**
- Manual download/upload works for MVP
- USGBC API is complex and rate-limited
- Focus on core automation first
- Can add later without breaking changes

**V1 Output:**
- Download PDF/Excel/USGBC form
- User uploads manually to LEED Online

**V2 Enhancement:**
- Direct USGBC Arc submission

---

*Version: 1.0*
*Last Updated: 2026-03-21*
