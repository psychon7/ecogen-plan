-- LEED AI Platform Database Schema
-- PostgreSQL 15+ with PostGIS extension

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ============================================
-- USERS & AUTHENTICATION
-- ============================================

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    avatar_url TEXT,
    role VARCHAR(50) DEFAULT 'consultant',
    leed_ap_number VARCHAR(50),
    email_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);

-- ============================================
-- ORGANIZATIONS
-- ============================================

CREATE TABLE organizations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    plan VARCHAR(50) DEFAULT 'free',
    settings JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE organization_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(organization_id, user_id)
);

CREATE INDEX idx_org_members_org ON organization_members(organization_id);
CREATE INDEX idx_org_members_user ON organization_members(user_id);

-- ============================================
-- PROJECTS
-- ============================================

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    organization_id UUID REFERENCES organizations(id) ON DELETE SET NULL,
    name VARCHAR(255) NOT NULL,
    code VARCHAR(100),
    description TEXT,
    
    -- Building info
    building_type VARCHAR(100) NOT NULL,
    leed_version VARCHAR(20) NOT NULL DEFAULT 'v5',
    rating_system VARCHAR(20) NOT NULL, -- BD+C, ID+C, O+M
    target_level VARCHAR(20) NOT NULL, -- Certified, Silver, Gold, Platinum
    
    -- Location
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip VARCHAR(20) NOT NULL,
    country VARCHAR(2) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    region VARCHAR(50), -- detected from location
    
    -- Progress tracking
    credits_completed INTEGER DEFAULT 0,
    credits_total INTEGER DEFAULT 0,
    points_achieved INTEGER DEFAULT 0,
    points_target INTEGER DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    
    -- Status
    status VARCHAR(50) DEFAULT 'active',
    target_certification_date DATE,
    
    -- Metadata
    settings JSONB DEFAULT '{}',
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_projects_org ON projects(organization_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_projects_location ON projects USING GIST(location);

-- ============================================
-- PROJECT TEAM MEMBERS
-- ============================================

CREATE TABLE project_members (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    email VARCHAR(255) NOT NULL, -- for invited but not yet registered
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    leed_ap_number VARCHAR(50),
    invitation_status VARCHAR(50) DEFAULT 'pending', -- pending, accepted, declined
    invitation_token VARCHAR(255),
    invitation_expires_at TIMESTAMP WITH TIME ZONE,
    joined_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(project_id, email)
);

CREATE INDEX idx_project_members_project ON project_members(project_id);
CREATE INDEX idx_project_members_user ON project_members(user_id);

-- ============================================
-- CREDIT DEFINITIONS (Reference Data)
-- ============================================

CREATE TABLE credit_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    code VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    leed_version VARCHAR(20) NOT NULL,
    rating_system VARCHAR(20) NOT NULL,
    category VARCHAR(100) NOT NULL,
    points INTEGER NOT NULL DEFAULT 0,
    is_prerequisite BOOLEAN DEFAULT FALSE,
    automation_level INTEGER NOT NULL, -- 0-100
    
    -- Configuration
    required_inputs JSONB NOT NULL DEFAULT '[]',
    expected_outputs JSONB NOT NULL DEFAULT '[]',
    workflow_steps JSONB NOT NULL DEFAULT '[]',
    hitl_checkpoints JSONB NOT NULL DEFAULT '[]',
    hitl_required BOOLEAN NOT NULL DEFAULT TRUE,
    confidence_threshold DECIMAL(4,2) NOT NULL DEFAULT 0.85,
    quality_thresholds JSONB NOT NULL DEFAULT '{}',
    skill_version VARCHAR(50) DEFAULT '1.0.0',
    skill_dependencies JSONB NOT NULL DEFAULT '[]',
    
    -- Regional availability
    regional_availability JSONB NOT NULL DEFAULT '{}',
    required_apis JSONB NOT NULL DEFAULT '[]',
    data_quality_rules JSONB NOT NULL DEFAULT '{}',
    
    -- Templates
    document_templates JSONB DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_credit_defs_version ON credit_definitions(leed_version, rating_system);
CREATE INDEX idx_credit_defs_category ON credit_definitions(category);
CREATE INDEX idx_credit_defs_active ON credit_definitions(is_active);

-- ============================================
-- PROJECT CREDITS (Instances)
-- ============================================

CREATE TABLE project_credits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id),
    
    -- Status
    status VARCHAR(50) DEFAULT 'not_started', -- not_started, in_progress, awaiting_review, approved, changes_requested, manual_required
    progress INTEGER DEFAULT 0, -- 0-100
    
    -- Data
    input_data JSONB DEFAULT '{}',
    extracted_data JSONB DEFAULT '{}',
    calculation_results JSONB DEFAULT '{}',
    confidence_score DECIMAL(4,3),
    quality_gate_results JSONB DEFAULT '[]',
    evidence_summary JSONB DEFAULT '{}',
    regional_status VARCHAR(50) DEFAULT 'available', -- available, limited, unavailable, manual_required
    
    -- Documents
    documents JSONB DEFAULT '{}', -- {pdf_url, excel_url, usgbc_form_url}
    
    -- Review tracking
    submitted_for_review_at TIMESTAMP WITH TIME ZONE,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    reviewed_by UUID REFERENCES users(id),
    review_comments TEXT,
    
    -- Points
    points_achieved INTEGER,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    
    UNIQUE(project_id, credit_definition_id)
);

CREATE INDEX idx_project_credits_project ON project_credits(project_id);
CREATE INDEX idx_project_credits_status ON project_credits(status);
CREATE INDEX idx_project_credits_definition ON project_credits(credit_definition_id);

-- ============================================
-- WORKFLOWS (Durable Execution)
-- ============================================

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    thread_id VARCHAR(255), -- LangGraph thread id: project_id:credit_code:workflow_id
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, running, paused, awaiting_review, completed, failed, cancelled, manual_required
    current_step INTEGER DEFAULT 0,
    current_step_name VARCHAR(100),
    total_steps INTEGER NOT NULL,
    
    -- State
    context JSONB DEFAULT '{}',
    step_results JSONB DEFAULT '{}',
    checkpoint_state JSONB DEFAULT '{}',
    step_history JSONB DEFAULT '[]',
    degraded_sources JSONB DEFAULT '[]',
    quality_gates JSONB DEFAULT '[]',
    confidence_score DECIMAL(4,3),
    revision_count INTEGER DEFAULT 0,
    
    -- Error tracking
    error_message TEXT,
    failed_step INTEGER,
    retry_count INTEGER DEFAULT 0,
    
    -- HITL
    hitl_task_id UUID,
    
    -- Timing
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_workflows_credit ON workflows(project_credit_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_hitl ON workflows(hitl_task_id);
CREATE INDEX idx_workflows_thread ON workflows(thread_id);

-- ============================================
-- HITL TASKS (Human-in-the-Loop)
-- ============================================

CREATE TABLE hitl_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    project_credit_id UUID NOT NULL REFERENCES project_credits(id),
    
    -- Assignment
    assignee_id UUID REFERENCES users(id),
    assignee_role VARCHAR(50) NOT NULL,
    checkpoint_name VARCHAR(100),
    priority VARCHAR(20) DEFAULT 'normal',
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, assigned, in_review, approved, rejected, changes_requested, escalated, expired
    
    -- Content
    document_url TEXT,
    excel_url TEXT,
    documents JSONB DEFAULT '[]',
    checklist JSONB NOT NULL DEFAULT '[]',
    instructions TEXT,
    confidence_scores JSONB DEFAULT '[]',
    quality_gates JSONB DEFAULT '[]',
    
    -- Response
    response_action VARCHAR(50), -- approve, request_changes, reject, escalate
    reviewer_comments TEXT,
    checklist_results JSONB DEFAULT '{}',
    rejection_reason TEXT,
    return_to_step INTEGER,
    return_to_step_name VARCHAR(100),
    document_hash VARCHAR(64),
    
    -- SLA
    sla_hours INTEGER NOT NULL DEFAULT 24,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    assigned_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    escalated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_hitl_tasks_assignee ON hitl_tasks(assignee_id);
CREATE INDEX idx_hitl_tasks_status ON hitl_tasks(status);
CREATE INDEX idx_hitl_tasks_expires ON hitl_tasks(expires_at);
CREATE INDEX idx_hitl_tasks_workflow ON hitl_tasks(workflow_id);

-- ============================================
-- API INTEGRATIONS
-- ============================================

CREATE TABLE api_integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    endpoint_url TEXT NOT NULL,
    auth_type VARCHAR(50) NOT NULL, -- api_key, oauth, none
    
    -- Configuration (encrypted)
    config JSONB DEFAULT '{}',
    
    -- Rate limiting
    rate_limit INTEGER,
    rate_limit_window INTEGER, -- seconds
    quota_config JSONB DEFAULT '{}',
    cache_ttl_seconds INTEGER,
    data_freshness_hours INTEGER,
    fallback_chain JSONB DEFAULT '[]',
    cost_tier VARCHAR(50) DEFAULT 'free',
    
    -- Regional availability
    regional_availability JSONB DEFAULT '{}',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_health_check_at TIMESTAMP WITH TIME ZONE,
    last_success_at TIMESTAMP WITH TIME ZONE,
    health_status VARCHAR(50) DEFAULT 'unknown',
    circuit_state VARCHAR(50) DEFAULT 'closed',
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_api_integrations_name ON api_integrations(name);
CREATE INDEX idx_api_integrations_active ON api_integrations(is_active);

-- ============================================
-- API CALLS (Logging)
-- ============================================

CREATE TABLE api_calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    api_integration_id UUID REFERENCES api_integrations(id),
    
    -- Request
    endpoint TEXT NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_body JSONB,
    request_hash VARCHAR(64),
    
    -- Response
    response_status INTEGER,
    response_body JSONB,
    response_checksum VARCHAR(64),
    cache_status VARCHAR(50), -- miss, hit, stale, static_fallback
    source_snapshot_id UUID,
    
    -- Timing
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    
    -- Error
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_api_calls_workflow ON api_calls(workflow_id);
CREATE INDEX idx_api_calls_api ON api_calls(api_integration_id);
CREATE INDEX idx_api_calls_created ON api_calls(created_at);

-- ============================================
-- DOCUMENTS
-- ============================================

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id),
    
    -- Document info
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- pdf, excel, csv, json
    format VARCHAR(50) NOT NULL, -- usgbc_form, calculation_workbook, report
    
    -- Storage
    storage_path TEXT NOT NULL,
    storage_provider VARCHAR(50) DEFAULT 's3',
    file_size INTEGER,
    checksum VARCHAR(64),
    
    -- Metadata
    metadata JSONB DEFAULT '{}',
    template_version VARCHAR(50),
    manifest_id UUID,
    evidence_ids JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_documents_credit ON documents(project_credit_id);
CREATE INDEX idx_documents_workflow ON documents(workflow_id);

-- ============================================
-- SKILL DEPENDENCIES
-- ============================================

CREATE TABLE skill_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    upstream_credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id) ON DELETE CASCADE,
    downstream_credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id) ON DELETE CASCADE,
    dependency_type VARCHAR(50) NOT NULL DEFAULT 'data_reuse', -- prerequisite, data_reuse, consistency_check
    required BOOLEAN DEFAULT TRUE,
    consumed_artifacts JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(upstream_credit_definition_id, downstream_credit_definition_id, dependency_type)
);

CREATE INDEX idx_skill_dependencies_upstream ON skill_dependencies(upstream_credit_definition_id);
CREATE INDEX idx_skill_dependencies_downstream ON skill_dependencies(downstream_credit_definition_id);

-- ============================================
-- SOURCE SNAPSHOTS & EVIDENCE TRACEABILITY
-- ============================================

CREATE TABLE source_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    api_call_id UUID REFERENCES api_calls(id) ON DELETE SET NULL,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL, -- api, static_dataset, uploaded_document, manual_entry, standard
    source_version VARCHAR(100),
    url TEXT,
    query_params JSONB DEFAULT '{}',
    retrieved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_freshness_at TIMESTAMP WITH TIME ZONE,
    response_checksum VARCHAR(64),
    storage_path TEXT,
    fallback_level VARCHAR(50) DEFAULT 'primary', -- primary, cached, static_fallback, manual
    confidence_score DECIMAL(4,3),
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_source_snapshots_workflow ON source_snapshots(workflow_id);
CREATE INDEX idx_source_snapshots_source ON source_snapshots(source_name);
CREATE INDEX idx_source_snapshots_retrieved ON source_snapshots(retrieved_at);

CREATE TABLE evidence_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    source_snapshot_id UUID REFERENCES source_snapshots(id) ON DELETE SET NULL,
    evidence_type VARCHAR(50) NOT NULL, -- extracted_field, citation, calculation_input, reviewer_note
    locator TEXT, -- page/table/cell/field/API path
    extracted_value JSONB,
    normalized_value JSONB,
    confidence_score DECIMAL(4,3),
    requires_human_review BOOLEAN DEFAULT FALSE,
    reviewed_by UUID REFERENCES users(id),
    reviewed_at TIMESTAMP WITH TIME ZONE,
    checksum VARCHAR(64),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_evidence_items_credit ON evidence_items(project_credit_id);
CREATE INDEX idx_evidence_items_workflow ON evidence_items(workflow_id);
CREATE INDEX idx_evidence_items_source ON evidence_items(source_snapshot_id);
CREATE INDEX idx_evidence_items_review ON evidence_items(requires_human_review);

-- ============================================
-- CALCULATION RECORDS
-- ============================================

CREATE TABLE calculation_records (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    skill_version VARCHAR(50) NOT NULL,
    formula_name VARCHAR(100) NOT NULL,
    formula_hash VARCHAR(64) NOT NULL,
    inputs_hash VARCHAR(64) NOT NULL,
    parameters JSONB NOT NULL DEFAULT '{}',
    source_snapshot_ids JSONB NOT NULL DEFAULT '[]',
    evidence_item_ids JSONB NOT NULL DEFAULT '[]',
    output JSONB NOT NULL DEFAULT '{}',
    unit_checks JSONB DEFAULT '[]',
    confidence_score DECIMAL(4,3),
    sandbox_id VARCHAR(100),
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_calculation_records_workflow ON calculation_records(workflow_id);
CREATE INDEX idx_calculation_records_credit ON calculation_records(project_credit_id);
CREATE INDEX idx_calculation_records_formula ON calculation_records(formula_name);

-- ============================================
-- DOCUMENT MANIFESTS & AUDIT EXPORTS
-- ============================================

CREATE TABLE document_manifests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    package_type VARCHAR(50) NOT NULL, -- credit_package, audit_export, project_package
    manifest JSONB NOT NULL DEFAULT '{}',
    checksum VARCHAR(64) NOT NULL,
    storage_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_document_manifests_credit ON document_manifests(project_credit_id);
CREATE INDEX idx_document_manifests_workflow ON document_manifests(workflow_id);

CREATE TABLE audit_exports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    project_credit_id UUID REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    status VARCHAR(50) DEFAULT 'queued', -- queued, running, completed, failed
    redaction_level VARCHAR(50) DEFAULT 'standard',
    include_raw_api_responses BOOLEAN DEFAULT FALSE,
    storage_path TEXT,
    manifest_checksum VARCHAR(64),
    requested_by UUID REFERENCES users(id),
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT
);

CREATE INDEX idx_audit_exports_project ON audit_exports(project_id);
CREATE INDEX idx_audit_exports_credit ON audit_exports(project_credit_id);
CREATE INDEX idx_audit_exports_status ON audit_exports(status);

-- ============================================
-- ACTIVITY LOG
-- ============================================

CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    project_id UUID REFERENCES projects(id),
    project_credit_id UUID REFERENCES project_credits(id),
    
    -- Event
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    
    -- IP & User Agent for audit
    ip_address INET,
    user_agent TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_activity_log_user ON activity_log(user_id);
CREATE INDEX idx_activity_log_project ON activity_log(project_id);
CREATE INDEX idx_activity_log_type ON activity_log(event_type);
CREATE INDEX idx_activity_log_created ON activity_log(created_at);

-- ============================================
-- NOTIFICATIONS
-- ============================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    -- Content
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    data JSONB DEFAULT '{}',
    
    -- Status
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    
    -- Action
    action_url TEXT,
    action_text VARCHAR(100),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read);
CREATE INDEX idx_notifications_created ON notifications(created_at);

-- ============================================
-- FUNCTIONS & TRIGGERS
-- ============================================

-- Update timestamps automatically
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply to all tables with updated_at
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_organizations_updated_at BEFORE UPDATE ON organizations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_projects_updated_at BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_credit_definitions_updated_at BEFORE UPDATE ON credit_definitions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_project_credits_updated_at BEFORE UPDATE ON project_credits
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_workflows_updated_at BEFORE UPDATE ON workflows
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_api_integrations_updated_at BEFORE UPDATE ON api_integrations
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Update project progress when credits change
CREATE OR REPLACE FUNCTION update_project_progress()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE projects
    SET 
        credits_completed = (
            SELECT COUNT(*) FROM project_credits 
            WHERE project_id = NEW.project_id AND status = 'approved'
        ),
        points_achieved = (
            SELECT COALESCE(SUM(points_achieved), 0) FROM project_credits 
            WHERE project_id = NEW.project_id AND status = 'approved'
        ),
        progress_percentage = (
            SELECT 
                CASE 
                    WHEN COUNT(*) = 0 THEN 0
                    ELSE ROUND(
                        (COUNT(*) FILTER (WHERE status = 'approved')::DECIMAL / COUNT(*)) * 100, 
                        2
                    )
                END
            FROM project_credits 
            WHERE project_id = NEW.project_id
        ),
        updated_at = NOW()
    WHERE id = NEW.project_id;
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_project_on_credit_change
    AFTER INSERT OR UPDATE OF status ON project_credits
    FOR EACH ROW
    EXECUTE FUNCTION update_project_progress();

-- ============================================
-- SEED DATA
-- ============================================

-- Insert credit definitions for LEED v5 BD+C
INSERT INTO credit_definitions (code, name, leed_version, rating_system, category, points, is_prerequisite, automation_level, required_inputs, expected_outputs, workflow_steps, regional_availability) VALUES
('WEp2', 'Minimum Water Efficiency', 'v5', 'BD+C', 'Water Efficiency', 0, true, 90,
 '[{"name":"fixture_schedule","type":"file_or_table","required":true},{"name":"occupancy_counts","type":"object","required":true},{"name":"operating_days","type":"number","required":true}]',
 '["water efficiency report","calculation workbook","source index","WEc2 handoff JSON"]',
 '["validate_inputs","parse_fixture_schedule","verify_product_data","calculate_baseline","calculate_design","calculate_reduction","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('WEc2', 'Enhanced Water Efficiency', 'v5', 'BD+C', 'Water Efficiency', 8, false, 85,
 '[{"name":"wep2_results","type":"object","required":true},{"name":"outdoor_water_data","type":"object","required":false},{"name":"process_water_data","type":"object","required":false},{"name":"alternative_water_sources","type":"object","required":false}]',
 '["enhanced water calculations","points optimization report","calculation workbook","source index"]',
 '["validate_wep2_handoff","evaluate_indoor_options","evaluate_outdoor_options","evaluate_process_water","optimize_points","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('EAp5', 'Fundamental Refrigerant Management', 'v5', 'BD+C', 'Energy & Atmosphere', 0, true, 90,
 '[{"name":"hvac_equipment_schedule","type":"file_or_table","required":true}]',
 '["refrigerant inventory","GWP analysis","compliance declaration","source index"]',
 '["validate_inputs","parse_equipment_schedule","lookup_gwp","check_cfc_hcfc","apply_regional_rules","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('EAc7', 'Enhanced Refrigerant Management', 'v5', 'BD+C', 'Energy & Atmosphere', 2, false, 90,
 '[{"name":"eap5_inventory","type":"object","required":true},{"name":"equipment_status","type":"object","required":false}]',
 '["enhanced refrigerant report","GWP benchmark workbook","leakage minimization plan"]',
 '["validate_eap5_inventory","calculate_weighted_gwp","verify_refrigerant_free_options","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('EQp1', 'Construction Management', 'v5', 'BD+C', 'Indoor Environmental Quality', 0, true, 85,
 '[{"name":"project_schedule","type":"file_or_table","required":true},{"name":"contractor_info","type":"object","required":true},{"name":"site_controls","type":"object","required":true}]',
 '["construction management plan","implementation checklist","photo log templates","review record"]',
 '["validate_inputs","generate_plan_sections","generate_checklist","generate_evidence_pack","contractor_review","leed_review","finalize"]',
 '["global"]'
),
('EQp2', 'Fundamental Air Quality', 'v5', 'BD+C', 'Indoor Environmental Quality', 0, true, 80,
 '[{"name":"hvac_zone_schedule","type":"file_or_table","required":true},{"name":"space_schedule","type":"file_or_table","required":true},{"name":"filtration_specs","type":"file_or_table","required":true}]',
 '["IAQ management plan","VRP calculation workbook","filtration compliance table","outdoor air quality narrative"]',
 '["validate_inputs","lookup_ashrae_tables","calculate_vrp","verify_filtration","generate_evidence_pack","engineer_review","leed_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('IPp1', 'Climate Resilience Assessment', 'v5', 'BD+C', 'Integrative Process', 0, true, 80,
 '[{"name":"project_location","type":"coordinates","required":true},{"name":"building_type","type":"string","required":true},{"name":"service_life","type":"number","required":true}]',
 '["climate resilience assessment","hazard source index","priority hazard rationale","review record"]',
 '["validate_inputs","fetch_hazard_sources","rank_hazards","draft_assessment","generate_evidence_pack","hitl_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('IPp2', 'Human Impact Assessment', 'v5', 'BD+C', 'Integrative Process', 0, true, 80,
 '[{"name":"project_location","type":"coordinates","required":true},{"name":"population_context","type":"object","required":false},{"name":"project_scope","type":"object","required":true}]',
 '["human impact assessment","demographic source index","community impact narrative","review record"]',
 '["validate_inputs","fetch_demographic_sources","summarize_community_context","draft_assessment","generate_evidence_pack","hitl_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('MRc3', 'Low-Emitting Materials', 'v5', 'BD+C', 'Materials & Resources', 2, false, 90,
 '[{"name":"product_list","type":"file_or_table","required":true},{"name":"submittal_pdfs","type":"file_array","required":false},{"name":"project_type","type":"string","required":true}]',
 '["material compliance matrix","certification lookup report","exception report","points calculation workbook"]',
 '["validate_inputs","classify_products","query_certification_sources","parse_test_reports","calculate_category_compliance","generate_evidence_pack","exception_review","finalize"]',
 '["US","CA","EU","UK","AU","APAC","manual_other"]'
),
('PRc2', 'LEED AP', 'v5', 'BD+C', 'Project Priorities', 1, false, 95,
 '[{"name":"team_members","type":"array","required":true},{"name":"project_rating_system","type":"string","required":true}]',
 '["LEED AP verification report","review record"]',
 '["validate_inputs","verify_credentials","check_specialty","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('IPp3', 'Carbon Assessment', 'v5', 'BD+C', 'Integrative Process', 0, true, 70,
 '[{"name":"eap1_outputs","type":"object","required":true},{"name":"eap5_outputs","type":"object","required":true},{"name":"mrp2_outputs","type":"object","required":true}]',
 '["cross-credit carbon assessment","calculation workbook","source index","review record"]',
 '["validate_cross_credit_inputs","aggregate_operational_refrigerant_embodied","generate_projection","generate_evidence_pack","hitl_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('MRp2', 'Quantify and Assess Embodied Carbon', 'v5', 'BD+C', 'Materials & Resources', 0, true, 85,
 '[{"name":"material_takeoff","type":"file_or_table","required":true},{"name":"epds","type":"file_array","required":false},{"name":"lca_tool_outputs","type":"file_array","required":false}]',
 '["embodied carbon assessment report","EPD summary","material GWP workbook","HITL log"]',
 '["validate_inputs","parse_epds","match_materials","calculate_gwp","generate_evidence_pack","lca_review","finalize"]',
 '["US","CA","EU","UK","AU","APAC","manual_other"]'
),
('MRc2', 'Reduce Embodied Carbon', 'v5', 'BD+C', 'Materials & Resources', 6, false, 80,
 '[{"name":"mrp2_baseline","type":"object","required":true},{"name":"lca_tool_outputs","type":"file_array","required":true},{"name":"material_changes","type":"array","required":false}]',
 '["reduction report","baseline/design comparison workbook","points calculation","review record"]',
 '["validate_inputs","import_wblca_outputs","check_scope_consistency","calculate_reduction","generate_evidence_pack","lca_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('EAp1', 'Operational Carbon Projection and Decarbonization Plan', 'v5', 'BD+C', 'Energy & Atmosphere', 0, true, 80,
 '[{"name":"energy_model_output","type":"file","required":true},{"name":"project_location","type":"coordinates","required":true},{"name":"grid_factor_source","type":"string","required":false}]',
 '["operational carbon projection","decarbonization plan","grid factor source index","review record"]',
 '["validate_inputs","fetch_or_enter_grid_factors","parse_energy_outputs","calculate_projection","generate_evidence_pack","hitl_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('EAp2', 'Minimum Energy Efficiency', 'v5', 'BD+C', 'Energy & Atmosphere', 0, true, 60,
 '[{"name":"proposed_energy_model_output","type":"file","required":true},{"name":"baseline_energy_model_output","type":"file","required":true},{"name":"modeler_attestation","type":"file","required":true}]',
 '["energy model output summary","compliance narrative","modeler review record"]',
 '["validate_inputs","parse_completed_model_outputs","calculate_summary_metrics","generate_evidence_pack","modeler_review","leed_review","finalize"]',
 '["global"]'
),
('EAc3', 'Enhanced Energy Efficiency', 'v5', 'BD+C', 'Energy & Atmosphere', 10, false, 60,
 '[{"name":"proposed_energy_model_output","type":"file","required":true},{"name":"baseline_energy_model_output","type":"file","required":true},{"name":"modeler_attestation","type":"file","required":true}]',
 '["energy comparison report","points calculation workbook","model summary","review record"]',
 '["validate_inputs","parse_completed_model_outputs","calculate_improvement","calculate_points","generate_evidence_pack","modeler_review","leed_review","finalize"]',
 '["global"]'
),
('LTc3', 'Compact and Connected Development', 'v5', 'BD+C', 'Location & Transportation', 6, false, 75,
 '[{"name":"project_location","type":"coordinates","required":true},{"name":"site_area","type":"number","required":true},{"name":"gross_floor_area","type":"number","required":true}]',
 '["location efficiency analysis","density calculations","transit report","regional caveat report"]',
 '["validate_inputs","fetch_walkability_sources","fetch_transit_data","calculate_density","generate_evidence_pack","planner_review","finalize"]',
 '["US","CA","AU","EU_limited","manual_other"]'
),
('SSc3', 'Rainwater Management', 'v5', 'BD+C', 'Sustainable Sites', 3, false, 80,
 '[{"name":"site_area","type":"number","required":true},{"name":"impervious_coverage","type":"number","required":true},{"name":"location","type":"coordinates","required":true}]',
 '["rainwater management report","retention calculations","LID sizing","source index"]',
 '["validate_inputs","fetch_or_enter_rainfall_data","fetch_or_enter_soil_data","calculate_retention","size_lid","generate_evidence_pack","hitl_review","finalize"]',
 '["US","CA","EU","UK","AU","manual_other"]'
),
('SSc5', 'Heat Island Reduction', 'v5', 'BD+C', 'Sustainable Sites', 2, false, 85,
 '[{"name":"site_plan_data","type":"file_or_table","required":true},{"name":"roof_and_paving_materials","type":"file_or_table","required":true}]',
 '["heat island reduction report","SRI calculation workbook","exception report"]',
 '["validate_inputs","extract_or_enter_areas","lookup_sri","calculate_compliance","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('SSc6', 'Light Pollution Reduction', 'v5', 'BD+C', 'Sustainable Sites', 1, false, 90,
 '[{"name":"luminaire_schedule","type":"file_or_table","required":true},{"name":"lighting_zone","type":"string","required":true}]',
 '["lighting compliance report","BUG rating workbook","cut sheet index","review record"]',
 '["validate_inputs","parse_luminaires","check_bug_ratings","generate_evidence_pack","hitl_review","finalize"]',
 '["global"]'
),
('LTc1', 'Sensitive Land Protection', 'v5', 'BD+C', 'Location & Transportation', 1, false, 60,
 '[{"name":"site_boundary","type":"file","required":true},{"name":"project_location","type":"coordinates","required":true}]',
 '["site sensitivity analysis","constraint maps","buffer calculations","regional caveat report"]',
 '["validate_inputs","query_us_gis_sources","analyze_constraints","generate_evidence_pack","gis_review","finalize"]',
 '["US","manual_other"]'
);

-- Normalize V1 review policy: every skill requires human review before approval.
UPDATE credit_definitions
SET hitl_required = TRUE,
    hitl_checkpoints = '[{"name":"final_review","reviewer_role":"leed_consultant","sla_hours":24,"required":true,"trigger":"before_package_export"}]'::jsonb;

UPDATE credit_definitions
SET hitl_checkpoints = '[
  {"name":"methodology_review","reviewer_role":"energy_modeler_or_discipline_expert","sla_hours":48,"required":true,"trigger":"after_calculate"},
  {"name":"final_review","reviewer_role":"leed_consultant","sla_hours":24,"required":true,"trigger":"before_package_export"}
]'::jsonb
WHERE code IN ('EAp2', 'EAc3', 'MRc2', 'LTc1', 'LTc3', 'IPp3');

-- Structured regional availability for API consumers. Limited means fallbacks/manual inputs are expected.
UPDATE credit_definitions
SET regional_availability = '{
  "US": {"status":"available","notes":"Primary automated data sources available for V1."},
  "CA": {"status":"limited","notes":"Regional substitutions or manual source confirmation may be required."},
  "EU": {"status":"limited","notes":"Regional substitutions or manual source confirmation may be required."},
  "UK": {"status":"limited","notes":"Regional substitutions or manual source confirmation may be required."},
  "AU": {"status":"limited","notes":"Regional substitutions or manual source confirmation may be required."},
  "Other": {"status":"limited","notes":"Manual data entry and conservative assumptions are expected."}
}'::jsonb;

UPDATE credit_definitions
SET regional_availability = '{
  "US": {"status":"available","notes":"FEMA, NWI, USFWS, NRCS, and USGS sources support automated screening."},
  "Other": {"status":"unavailable","notes":"Equivalent site constraint datasets must be manually provided and reviewed."}
}'::jsonb
WHERE code = 'LTc1';

-- Key source dependencies used by the regional router and audit package.
UPDATE credit_definitions SET required_apis = '["epa_egrid","ec3_database","ipcc_static","usgbc_manual_upload"]'::jsonb WHERE code = 'IPp3';
UPDATE credit_definitions SET required_apis = '["epa_egrid","nrel_pvwatts","energy_model_upload"]'::jsonb WHERE code = 'EAp1';
UPDATE credit_definitions SET required_apis = '["energyplus_local","ashrae_90_1_static","energy_model_upload"]'::jsonb WHERE code IN ('EAp2', 'EAc3');
UPDATE credit_definitions SET required_apis = '["epa_snap","ahri_directory","ipcc_static"]'::jsonb WHERE code IN ('EAp5', 'EAc7');
UPDATE credit_definitions SET required_apis = '["watersense_static","energy_star_product_api"]'::jsonb WHERE code IN ('WEp2', 'WEc2');
UPDATE credit_definitions SET required_apis = '["ashrae_62_1_static","epa_airnow","manual_hvac_schedule"]'::jsonb WHERE code = 'EQp2';
UPDATE credit_definitions SET required_apis = '["template_library","manual_contractor_inputs"]'::jsonb WHERE code = 'EQp1';
UPDATE credit_definitions SET required_apis = '["fema","noaa","usgs","ipcc_sources","manual_local_sources"]'::jsonb WHERE code = 'IPp1';
UPDATE credit_definitions SET required_apis = '["census_or_regional_demographics","epa_ejscreen_or_regional_equivalent","cdc_svi_or_regional_equivalent","manual_local_sources"]'::jsonb WHERE code = 'IPp2';
UPDATE credit_definitions SET required_apis = '["ul_spot","scs_global","cri_green_label","bifma_level","manufacturer_submittals"]'::jsonb WHERE code = 'MRc3';
UPDATE credit_definitions SET required_apis = '["ec3_database","epd_registry","lca_tool_upload"]'::jsonb WHERE code IN ('MRp2', 'MRc2');
UPDATE credit_definitions SET required_apis = '["fema_nfhl","nwi","usfws_critical_habitat","nrcs_soils","usgs_3dep"]'::jsonb WHERE code = 'LTc1';
UPDATE credit_definitions SET required_apis = '["gtfs","walk_score","census_api","manual_parcel_data"]'::jsonb WHERE code = 'LTc3';
UPDATE credit_definitions SET required_apis = '["noaa_atlas_14","nrcs_soils","manual_site_data"]'::jsonb WHERE code = 'SSc3';
UPDATE credit_definitions SET required_apis = '["crrc_database","manual_material_specs"]'::jsonb WHERE code = 'SSc5';
UPDATE credit_definitions SET required_apis = '["ies_tm_15_static","manual_luminaire_schedule"]'::jsonb WHERE code = 'SSc6';
UPDATE credit_definitions SET required_apis = '["gbci_credential_directory","manual_roster"]'::jsonb WHERE code = 'PRc2';

UPDATE credit_definitions SET skill_dependencies = '["EAp1","EAp5","MRp2"]'::jsonb WHERE code = 'IPp3';
UPDATE credit_definitions SET skill_dependencies = '["EAp2"]'::jsonb WHERE code = 'EAc3';
UPDATE credit_definitions SET skill_dependencies = '["EAp5"]'::jsonb WHERE code = 'EAc7';
UPDATE credit_definitions SET skill_dependencies = '["WEp2"]'::jsonb WHERE code = 'WEc2';
UPDATE credit_definitions SET skill_dependencies = '["MRp2"]'::jsonb WHERE code = 'MRc2';

INSERT INTO skill_dependencies (upstream_credit_definition_id, downstream_credit_definition_id, dependency_type, consumed_artifacts)
SELECT up.id, down.id, dep.dependency_type, dep.consumed_artifacts
FROM (
    VALUES
      ('EAp1', 'IPp3', 'data_reuse', '["operational_carbon_projection"]'::jsonb),
      ('EAp5', 'IPp3', 'data_reuse', '["refrigerant_inventory"]'::jsonb),
      ('MRp2', 'IPp3', 'data_reuse', '["embodied_carbon_quantification"]'::jsonb),
      ('EAp2', 'EAc3', 'data_reuse', '["energy_model_parse_results"]'::jsonb),
      ('EAp5', 'EAc7', 'data_reuse', '["refrigerant_inventory"]'::jsonb),
      ('WEp2', 'WEc2', 'data_reuse', '["fixture_baseline_and_design_case"]'::jsonb),
      ('MRp2', 'MRc2', 'data_reuse', '["material_takeoff_and_gwp_factors"]'::jsonb)
) AS dep(upstream_code, downstream_code, dependency_type, consumed_artifacts)
JOIN credit_definitions up ON up.code = dep.upstream_code
JOIN credit_definitions down ON down.code = dep.downstream_code
ON CONFLICT (upstream_credit_definition_id, downstream_credit_definition_id, dependency_type) DO NOTHING;
