-- LEED v5 Automation Platform — Schema for Restate + OpenAI Agents SDK Architecture
-- PostgreSQL 15+ with PostGIS
-- Migrated from Deer-Flow/LangGraph schema; removes thread_id, adds agent execution tracking.

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
    building_type VARCHAR(100) NOT NULL,
    leed_version VARCHAR(20) NOT NULL DEFAULT 'v5',
    rating_system VARCHAR(20) NOT NULL,
    target_level VARCHAR(20) NOT NULL,
    address TEXT NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    zip VARCHAR(20) NOT NULL,
    country VARCHAR(2) NOT NULL,
    location GEOGRAPHY(POINT, 4326),
    region VARCHAR(50),
    credits_completed INTEGER DEFAULT 0,
    credits_total INTEGER DEFAULT 0,
    points_achieved INTEGER DEFAULT 0,
    points_target INTEGER DEFAULT 0,
    progress_percentage DECIMAL(5,2) DEFAULT 0,
    status VARCHAR(50) DEFAULT 'active',
    target_certification_date DATE,
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
    email VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    leed_ap_number VARCHAR(50),
    invitation_status VARCHAR(50) DEFAULT 'pending',
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
    automation_level INTEGER NOT NULL,
    required_inputs JSONB NOT NULL DEFAULT '[]',
    expected_outputs JSONB NOT NULL DEFAULT '[]',
    workflow_steps JSONB NOT NULL DEFAULT '[]',
    hitl_checkpoints JSONB NOT NULL DEFAULT '[]',
    hitl_required BOOLEAN NOT NULL DEFAULT TRUE,
    confidence_threshold DECIMAL(4,2) NOT NULL DEFAULT 0.85,
    quality_thresholds JSONB NOT NULL DEFAULT '{}',
    skill_version VARCHAR(50) DEFAULT '1.0.0',
    skill_dependencies JSONB NOT NULL DEFAULT '[]',
    regional_availability JSONB NOT NULL DEFAULT '{}',
    required_apis JSONB NOT NULL DEFAULT '[]',
    data_quality_rules JSONB NOT NULL DEFAULT '{}',
    document_templates JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_credit_defs_version ON credit_definitions(leed_version, rating_system);
CREATE INDEX idx_credit_defs_category ON credit_definitions(category);

-- ============================================
-- PROJECT CREDITS (Instances)
-- ============================================

CREATE TABLE project_credits (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
    credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id),
    status VARCHAR(50) DEFAULT 'not_started',
    progress INTEGER DEFAULT 0,
    input_data JSONB DEFAULT '{}',
    extracted_data JSONB DEFAULT '{}',
    calculation_results JSONB DEFAULT '{}',
    confidence_score DECIMAL(4,3),
    confidence_tier VARCHAR(1),
    quality_gate_results JSONB DEFAULT '[]',
    evidence_summary JSONB DEFAULT '{}',
    regional_status VARCHAR(50) DEFAULT 'available',
    documents JSONB DEFAULT '{}',
    submitted_for_review_at TIMESTAMP WITH TIME ZONE,
    reviewed_at TIMESTAMP WITH TIME ZONE,
    reviewed_by UUID REFERENCES users(id),
    review_comments TEXT,
    points_achieved INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(project_id, credit_definition_id)
);

CREATE INDEX idx_project_credits_project ON project_credits(project_id);
CREATE INDEX idx_project_credits_status ON project_credits(status);

-- ============================================
-- WORKFLOWS (Restate-managed, tracked in Postgres for queries)
-- ============================================

CREATE TABLE workflows (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    restate_workflow_id VARCHAR(255) UNIQUE NOT NULL,
    skill_name VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    current_step INTEGER DEFAULT 0,
    current_step_name VARCHAR(100),
    total_steps INTEGER NOT NULL,
    context JSONB DEFAULT '{}',
    step_results JSONB DEFAULT '{}',
    confidence_score DECIMAL(4,3),
    error_message TEXT,
    failed_step INTEGER,
    retry_count INTEGER DEFAULT 0,
    hitl_task_id UUID,
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_workflows_credit ON workflows(project_credit_id);
CREATE INDEX idx_workflows_status ON workflows(status);
CREATE INDEX idx_workflows_restate ON workflows(restate_workflow_id);

-- ============================================
-- HITL TASKS
-- ============================================

CREATE TABLE hitl_tasks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID NOT NULL REFERENCES workflows(id) ON DELETE CASCADE,
    project_credit_id UUID NOT NULL REFERENCES project_credits(id),
    assignee_id UUID REFERENCES users(id),
    assignee_role VARCHAR(50) NOT NULL,
    checkpoint_name VARCHAR(100),
    priority VARCHAR(20) DEFAULT 'normal',
    status VARCHAR(50) DEFAULT 'pending',
    document_url TEXT,
    documents JSONB DEFAULT '[]',
    checklist JSONB NOT NULL DEFAULT '[]',
    instructions TEXT,
    confidence_scores JSONB DEFAULT '[]',
    response_action VARCHAR(50),
    reviewer_comments TEXT,
    checklist_results JSONB DEFAULT '{}',
    rejection_reason TEXT,
    return_to_step INTEGER,
    return_to_step_name VARCHAR(100),
    document_hash VARCHAR(64),
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
-- AGENT EXECUTIONS (new — tracks OpenAI SDK calls)
-- ============================================

CREATE TABLE agent_executions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    project_credit_id UUID REFERENCES project_credits(id),
    provider VARCHAR(50) NOT NULL DEFAULT 'openai',
    agent_name VARCHAR(100) NOT NULL,
    model VARCHAR(100),
    idempotency_key VARCHAR(64) UNIQUE,
    request_payload JSONB NOT NULL DEFAULT '{}',
    response_payload JSONB DEFAULT '{}',
    input_checksum VARCHAR(64),
    output_checksum VARCHAR(64),
    token_usage JSONB DEFAULT '{}',
    execution_time_ms INTEGER,
    status VARCHAR(50) DEFAULT 'pending',
    error_message TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_agent_executions_workflow ON agent_executions(workflow_id);
CREATE INDEX idx_agent_executions_idempotency ON agent_executions(idempotency_key);
CREATE INDEX idx_agent_executions_provider ON agent_executions(provider);

-- ============================================
-- API INTEGRATIONS & CALLS
-- ============================================

CREATE TABLE api_integrations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL,
    provider VARCHAR(100) NOT NULL,
    endpoint_url TEXT NOT NULL,
    auth_type VARCHAR(50) NOT NULL,
    config JSONB DEFAULT '{}',
    rate_limit INTEGER,
    rate_limit_window INTEGER,
    cache_ttl_seconds INTEGER,
    fallback_chain JSONB DEFAULT '[]',
    regional_availability JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    health_status VARCHAR(50) DEFAULT 'unknown',
    last_health_check_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE api_calls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    api_integration_id UUID REFERENCES api_integrations(id),
    endpoint TEXT NOT NULL,
    method VARCHAR(10) NOT NULL,
    request_body JSONB,
    request_hash VARCHAR(64),
    response_status INTEGER,
    response_body JSONB,
    response_checksum VARCHAR(64),
    cache_status VARCHAR(50),
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_ms INTEGER,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_api_calls_workflow ON api_calls(workflow_id);

-- ============================================
-- DOCUMENTS & EVIDENCE
-- ============================================

CREATE TABLE documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL,
    format VARCHAR(50) NOT NULL,
    storage_path TEXT NOT NULL,
    storage_provider VARCHAR(50) DEFAULT 's3',
    file_size INTEGER,
    checksum VARCHAR(64),
    metadata JSONB DEFAULT '{}',
    template_version VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_documents_credit ON documents(project_credit_id);

-- ============================================
-- SOURCE SNAPSHOTS & EVIDENCE ITEMS
-- ============================================

CREATE TABLE source_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    api_call_id UUID REFERENCES api_calls(id) ON DELETE SET NULL,
    source_name VARCHAR(255) NOT NULL,
    source_type VARCHAR(50) NOT NULL,
    source_version VARCHAR(100),
    url TEXT,
    query_params JSONB DEFAULT '{}',
    retrieved_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data_freshness_at TIMESTAMP WITH TIME ZONE,
    response_checksum VARCHAR(64),
    storage_path TEXT,
    fallback_level VARCHAR(50) DEFAULT 'primary',
    confidence_score DECIMAL(4,3),
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_source_snapshots_workflow ON source_snapshots(workflow_id);

CREATE TABLE evidence_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID NOT NULL REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    source_snapshot_id UUID REFERENCES source_snapshots(id) ON DELETE SET NULL,
    agent_execution_id UUID REFERENCES agent_executions(id) ON DELETE SET NULL,
    evidence_type VARCHAR(50) NOT NULL,
    locator TEXT,
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
CREATE INDEX idx_evidence_items_agent ON evidence_items(agent_execution_id);

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
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_calculation_records_workflow ON calculation_records(workflow_id);

-- ============================================
-- DOCUMENT MANIFESTS
-- ============================================

CREATE TABLE document_manifests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_credit_id UUID REFERENCES project_credits(id) ON DELETE CASCADE,
    workflow_id UUID REFERENCES workflows(id) ON DELETE SET NULL,
    package_type VARCHAR(50) NOT NULL,
    manifest JSONB NOT NULL DEFAULT '{}',
    checksum VARCHAR(64) NOT NULL,
    storage_path TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

-- ============================================
-- AUDIT LOG (append-only)
-- ============================================

CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    actor_id UUID REFERENCES users(id),
    actor_type VARCHAR(20) NOT NULL DEFAULT 'system',
    project_id UUID REFERENCES projects(id),
    credit_code VARCHAR(20),
    workflow_id UUID REFERENCES workflows(id),
    agent_execution_id UUID REFERENCES agent_executions(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    input_checksum VARCHAR(64),
    output_checksum VARCHAR(64),
    ip_address INET,
    user_agent TEXT
);

CREATE INDEX idx_audit_log_project ON audit_log(project_id);
CREATE INDEX idx_audit_log_type ON audit_log(event_type);
CREATE INDEX idx_audit_log_timestamp ON audit_log(timestamp);
CREATE INDEX idx_audit_log_actor ON audit_log(actor_id);

-- ============================================
-- ACTIVITY LOG (user-facing)
-- ============================================

CREATE TABLE activity_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    organization_id UUID REFERENCES organizations(id),
    project_id UUID REFERENCES projects(id),
    project_credit_id UUID REFERENCES project_credits(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_activity_log_user ON activity_log(user_id);
CREATE INDEX idx_activity_log_project ON activity_log(project_id);
CREATE INDEX idx_activity_log_created ON activity_log(created_at);

-- ============================================
-- NOTIFICATIONS
-- ============================================

CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT,
    data JSONB DEFAULT '{}',
    is_read BOOLEAN DEFAULT FALSE,
    read_at TIMESTAMP WITH TIME ZONE,
    action_url TEXT,
    action_text VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_user ON notifications(user_id);
CREATE INDEX idx_notifications_unread ON notifications(user_id, is_read);

-- ============================================
-- SKILL DEPENDENCIES
-- ============================================

CREATE TABLE skill_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    upstream_credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id) ON DELETE CASCADE,
    downstream_credit_definition_id UUID NOT NULL REFERENCES credit_definitions(id) ON DELETE CASCADE,
    dependency_type VARCHAR(50) NOT NULL DEFAULT 'data_reuse',
    required BOOLEAN DEFAULT TRUE,
    consumed_artifacts JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(upstream_credit_definition_id, downstream_credit_definition_id, dependency_type)
);

-- ============================================
-- TRIGGERS
-- ============================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

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
