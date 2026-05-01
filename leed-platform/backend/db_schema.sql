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
    
    -- Regional availability
    regional_availability JSONB NOT NULL DEFAULT '["global"]',
    required_apis JSONB NOT NULL DEFAULT '[]',
    
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
    status VARCHAR(50) DEFAULT 'not_started', -- not_started, in_progress, in_review, approved, changes_requested
    progress INTEGER DEFAULT 0, -- 0-100
    
    -- Data
    input_data JSONB DEFAULT '{}',
    extracted_data JSONB DEFAULT '{}',
    calculation_results JSONB DEFAULT '{}',
    
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
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, running, paused, completed, failed, cancelled
    current_step INTEGER DEFAULT 0,
    total_steps INTEGER NOT NULL,
    
    -- State
    context JSONB DEFAULT '{}',
    step_results JSONB DEFAULT '{}',
    
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
    
    -- Status
    status VARCHAR(50) DEFAULT 'pending', -- pending, assigned, in_review, approved, rejected, escalated, expired
    
    -- Content
    document_url TEXT,
    excel_url TEXT,
    checklist JSONB NOT NULL DEFAULT '[]',
    instructions TEXT,
    
    -- Response
    reviewer_comments TEXT,
    checklist_results JSONB DEFAULT '{}',
    rejection_reason TEXT,
    return_to_step INTEGER,
    
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
    
    -- Regional availability
    regional_availability JSONB DEFAULT '["global"]',
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    last_health_check_at TIMESTAMP WITH TIME ZONE,
    health_status VARCHAR(50) DEFAULT 'unknown',
    
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
    
    -- Response
    response_status INTEGER,
    response_body JSONB,
    
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
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by UUID REFERENCES users(id)
);

CREATE INDEX idx_documents_credit ON documents(project_credit_id);
CREATE INDEX idx_documents_workflow ON documents(workflow_id);

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
('IPp3', 'Carbon Assessment', 'v5', 'BD+C', 'Integrative Process', 0, true, 85, 
 '[{"name": "project_location", "type": "coordinates", "required": true}, {"name": "energy_model_output", "type": "file", "required": true}, {"name": "material_quantities", "type": "file", "required": true}, {"name": "service_life", "type": "number", "required": true}]',
 '["25-year carbon projection report", "calculation workbook", "USGBC submission form"]',
 '["validate_inputs", "fetch_grid_factors", "fetch_embodied_carbon", "calculate_operational", "calculate_refrigerant", "calculate_embodied", "generate_projection", "generate_report", "hitl_review", "finalize"]',
 '["US", "CA", "EU", "UK", "AU"]'
),
('PRc2', 'LEED AP', 'v5', 'BD+C', 'Project Priorities', 1, false, 95,
 '[{"name": "team_members", "type": "array", "required": true}, {"name": "project_rating_system", "type": "string", "required": true}]',
 '["LEED AP verification report"]',
 '["validate_inputs", "verify_credentials", "check_specialty", "generate_report"]',
 '["global"]'
),
('WEp2', 'Minimum Water Efficiency', 'v5', 'BD+C', 'Water Efficiency', 0, true, 90,
 '[{"name": "fixture_schedule", "type": "file", "required": true}, {"name": "occupancy_counts", "type": "object", "required": true}]',
 '["water efficiency calculations", "fixture compliance report"]',
 '["validate_inputs", "parse_fixture_schedule", "calculate_baseline", "calculate_proposed", "calculate_reduction", "generate_report"]',
 '["global"]'
),
('EAp5', 'Fundamental Refrigerant Management', 'v5', 'BD+C', 'Energy & Atmosphere', 0, true, 90,
 '[{"name": "hvac_equipment_schedule", "type": "file", "required": true}]',
 '["refrigerant compliance report"]',
 '["validate_inputs", "parse_equipment_schedule", "check_cfc", "check_gwp", "generate_report"]',
 '["global"]'
),
('MRp2', 'Quantify and Assess Embodied Carbon', 'v5', 'BD+C', 'Materials & Resources', 0, true, 85,
 '[{"name": "structural_drawings", "type": "file", "required": true}, {"name": "material_specifications", "type": "file", "required": true}]',
 '["bill of materials", "embodied carbon report", "top 3 hotspots"]',
 '["validate_inputs", "extract_quantities", "fetch_gwp_data", "calculate_embodied", "identify_hotspots", "generate_report"]',
 '["global"]'
),
('EAc3', 'Enhanced Energy Efficiency', 'v5', 'BD+C', 'Energy & Atmosphere', 10, false, 70,
 '[{"name": "proposed_energy_model", "type": "file", "required": true}, {"name": "baseline_energy_model", "type": "file", "required": true}, {"name": "building_type", "type": "string", "required": true}, {"name": "climate_zone", "type": "string", "required": true}]',
 '["energy comparison report", "calculation workbook", "USGBC submission form"]',
 '["validate_inputs", "parse_energy_models", "fetch_energy_rates", "calculate_costs", "calculate_improvement", "calculate_points", "hitl_review", "generate_report"]',
 '["US", "CA", "EU", "UK", "AU"]'
),
('WEc2', 'Enhanced Water Efficiency', 'v5', 'BD+C', 'Water Efficiency', 8, false, 85,
 '[{"name": "all_water_uses", "type": "file", "required": true}, {"name": "alternative_water_sources", "type": "object", "required": false}]',
 '["whole-project water model", "reduction calculation", "USGBC submission form"]',
 '["validate_inputs", "parse_water_data", "calculate_baseline", "calculate_proposed", "calculate_reduction", "hitl_review", "generate_report"]',
 '["global"]'
),
('MRc2', 'Reduce Embodied Carbon', 'v5', 'BD+C', 'Materials & Resources', 6, false, 80,
 '[{"name": "material_quantities", "type": "file", "required": true}, {"name": "epds", "type": "file", "required": false}, {"name": "baseline_project_data", "type": "object", "required": false}]',
 '["WBLCA results", "reduction percentage", "EPD analysis", "USGBC submission form"]',
 '["validate_inputs", "perform_wblca", "calculate_reduction", "hitl_review", "generate_report"]',
 '["global"]'
),
('LTc3', 'Compact and Connected Development', 'v5', 'BD+C', 'Location & Transportation', 6, false, 75,
 '[{"name": "project_location", "type": "coordinates", "required": true}, {"name": "surrounding_parcel_data", "type": "object", "required": false}]',
 '["location efficiency analysis", "density calculations", "transit score", "USGBC submission form"]',
 '["validate_inputs", "fetch_walk_score", "fetch_transit_data", "calculate_density", "generate_report"]',
 '["US", "CA", "UK", "AU", "NZ"]'
),
('SSc3', 'Rainwater Management', 'v5', 'BD+C', 'Sustainable Sites', 3, false, 80,
 '[{"name": "site_area", "type": "number", "required": true}, {"name": "impervious_coverage", "type": "number", "required": true}, {"name": "location", "type": "coordinates", "required": true}]',
 '["rainwater management report", "retention calculations", "LID sizing"]',
 '["validate_inputs", "fetch_rainfall_data", "fetch_soil_data", "calculate_retention", "size_lid", "generate_report"]',
 '["US", "CA", "EU", "UK", "AU"]'
),
('EAc7', 'Enhanced Refrigerant Management', 'v5', 'BD+C', 'Energy & Atmosphere', 2, false, 90,
 '[{"name": "hvac_equipment_schedule", "type": "file", "required": true}]',
 '["enhanced refrigerant report", "GWP calculations"]',
 '["validate_inputs", "parse_refrigerants", "calculate_gwp", "identify_alternatives", "generate_report"]',
 '["global"]'
),
('SSc5', 'Heat Island Reduction', 'v5', 'BD+C', 'Sustainable Sites', 2, false, 85,
 '[{"name": "site_plan", "type": "file", "required": true}, {"name": "material_specifications", "type": "file", "required": true}]',
 '["heat island reduction report", "SRI calculations"]',
 '["validate_inputs", "extract_areas", "calculate_sri", "generate_report"]',
 '["global"]'
),
('SSc6', 'Light Pollution Reduction', 'v5', 'BD+C', 'Sustainable Sites', 1, false, 95,
 '[{"name": "luminaire_schedule", "type": "file", "required": true}, {"name": "lighting_zone", "type": "string", "required": true}]',
 '["lighting compliance report", "BUG rating verification"]',
 '["validate_inputs", "parse_luminaires", "check_bug_ratings", "generate_report"]',
 '["global"]'
),
('LTc1', 'Sensitive Land Protection', 'v5', 'BD+C', 'Location & Transportation', 1, false, 60,
 '[{"name": "site_boundary", "type": "file", "required": true}, {"name": "project_location", "type": "coordinates", "required": true}]',
 '["site sensitivity analysis", "constraint maps", "buffer calculations"]',
 '["validate_inputs", "query_flood_zones", "query_wetlands", "query_habitat", "analyze_constraints", "hitl_review", "generate_report"]',
 '["US"]'
);
