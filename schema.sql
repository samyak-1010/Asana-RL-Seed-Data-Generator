-- Asana Simulation Database Schema
-- SQLite 3 compatible DDL
-- Represents a B2B SaaS company workspace with 5K-10K employees

-- Organizations/Workspaces
CREATE TABLE organizations (
    organization_id TEXT PRIMARY KEY,  -- UUID format (simulating Asana GID)
    name TEXT NOT NULL,
    domain TEXT NOT NULL,  -- Email domain (e.g., 'company.com')
    is_organization BOOLEAN NOT NULL DEFAULT 1,  -- vs workspace
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(domain)
);

-- Teams within the organization
CREATE TABLE teams (
    team_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    team_type TEXT CHECK(team_type IN ('Engineering', 'Marketing', 'Sales', 'Operations', 'Product', 'Design', 'HR', 'Finance')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- Users in the workspace
CREATE TABLE users (
    user_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    role TEXT CHECK(role IN ('admin', 'member', 'guest', 'limited_access')),
    job_title TEXT,
    department TEXT,
    is_active BOOLEAN NOT NULL DEFAULT 1,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_active_at TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- Team membership (many-to-many relationship)
CREATE TABLE team_memberships (
    membership_id TEXT PRIMARY KEY,
    team_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    is_team_lead BOOLEAN NOT NULL DEFAULT 0,
    joined_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(team_id, user_id)
);

-- Projects
CREATE TABLE projects (
    project_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    team_id TEXT,  -- Nullable for cross-team projects
    name TEXT NOT NULL,
    description TEXT,
    project_type TEXT CHECK(project_type IN ('Sprint', 'Kanban', 'Timeline', 'List', 'Calendar')),
    workflow_type TEXT CHECK(workflow_type IN ('Engineering', 'Marketing', 'Operations', 'Product', 'Design', 'General')),
    status TEXT CHECK(status IN ('active', 'on_hold', 'completed', 'archived')),
    owner_id TEXT,  -- Project owner
    is_public BOOLEAN NOT NULL DEFAULT 1,
    color TEXT,  -- Hex color code
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date DATE,
    completed_at TIMESTAMP,
    archived_at TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Project members (many-to-many)
CREATE TABLE project_memberships (
    membership_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    can_edit BOOLEAN NOT NULL DEFAULT 1,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id),
    UNIQUE(project_id, user_id)
);

-- Sections within projects
CREATE TABLE sections (
    section_id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    name TEXT NOT NULL,
    position INTEGER NOT NULL,  -- Order within project
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(project_id)
);

-- Tasks (includes both tasks and subtasks)
CREATE TABLE tasks (
    task_id TEXT PRIMARY KEY,
    project_id TEXT,  -- Nullable for personal tasks
    section_id TEXT,  -- Nullable
    parent_task_id TEXT,  -- NULL for top-level tasks, non-NULL for subtasks
    name TEXT NOT NULL,
    description TEXT,  -- Rich text/HTML
    assignee_id TEXT,  -- Nullable for unassigned
    created_by TEXT NOT NULL,
    status TEXT CHECK(status IN ('incomplete', 'complete')) NOT NULL DEFAULT 'incomplete',
    due_date DATE,
    start_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    completed_by TEXT,
    is_milestone BOOLEAN NOT NULL DEFAULT 0,
    num_likes INTEGER NOT NULL DEFAULT 0,
    num_subtasks INTEGER NOT NULL DEFAULT 0,
    num_comments INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    FOREIGN KEY (section_id) REFERENCES sections(section_id),
    FOREIGN KEY (parent_task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (assignee_id) REFERENCES users(user_id),
    FOREIGN KEY (created_by) REFERENCES users(user_id),
    FOREIGN KEY (completed_by) REFERENCES users(user_id),
    CHECK (parent_task_id IS NULL OR parent_task_id != task_id)  -- Prevent self-reference
);

-- Task dependencies
CREATE TABLE task_dependencies (
    dependency_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,  -- Dependent task
    depends_on_task_id TEXT NOT NULL,  -- Task that must be completed first
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (depends_on_task_id) REFERENCES tasks(task_id),
    UNIQUE(task_id, depends_on_task_id),
    CHECK (task_id != depends_on_task_id)  -- Task can't depend on itself
);

-- Comments/Stories on tasks
CREATE TABLE comments (
    comment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    comment_type TEXT CHECK(comment_type IN ('comment', 'system', 'status_change', 'assignment_change')) NOT NULL DEFAULT 'comment',
    text TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_pinned BOOLEAN NOT NULL DEFAULT 0,
    num_likes INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Custom field definitions
CREATE TABLE custom_field_definitions (
    field_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    field_type TEXT CHECK(field_type IN ('text', 'number', 'enum', 'multi_enum', 'date', 'people')) NOT NULL,
    is_global BOOLEAN NOT NULL DEFAULT 0,  -- Available across all projects or project-specific
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id)
);

-- Custom field enum options (for enum/multi_enum types)
CREATE TABLE custom_field_enum_options (
    option_id TEXT PRIMARY KEY,
    field_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,  -- Hex color
    position INTEGER NOT NULL,
    enabled BOOLEAN NOT NULL DEFAULT 1,
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id)
);

-- Custom field values on tasks (EAV pattern)
CREATE TABLE custom_field_values (
    value_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    field_id TEXT NOT NULL,
    text_value TEXT,
    number_value REAL,
    date_value DATE,
    enum_option_id TEXT,  -- For enum types
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    modified_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (field_id) REFERENCES custom_field_definitions(field_id),
    FOREIGN KEY (enum_option_id) REFERENCES custom_field_enum_options(option_id),
    UNIQUE(task_id, field_id)
);

-- Tags
CREATE TABLE tags (
    tag_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    color TEXT,  -- Hex color
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    UNIQUE(organization_id, name)
);

-- Task-Tag associations (many-to-many)
CREATE TABLE task_tags (
    task_tag_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    tag_id TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (tag_id) REFERENCES tags(tag_id),
    UNIQUE(task_id, tag_id)
);

-- Attachments metadata
CREATE TABLE attachments (
    attachment_id TEXT PRIMARY KEY,
    task_id TEXT NOT NULL,
    uploaded_by TEXT NOT NULL,
    filename TEXT NOT NULL,
    file_type TEXT,  -- MIME type
    file_size INTEGER,  -- bytes
    storage_url TEXT,  -- Simulated cloud storage URL
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id),
    FOREIGN KEY (uploaded_by) REFERENCES users(user_id)
);

-- Portfolios (collections of projects)
CREATE TABLE portfolios (
    portfolio_id TEXT PRIMARY KEY,
    organization_id TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT,
    owner_id TEXT,
    color TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (organization_id) REFERENCES organizations(organization_id),
    FOREIGN KEY (owner_id) REFERENCES users(user_id)
);

-- Portfolio-Project associations
CREATE TABLE portfolio_projects (
    portfolio_project_id TEXT PRIMARY KEY,
    portfolio_id TEXT NOT NULL,
    project_id TEXT NOT NULL,
    added_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id),
    UNIQUE(portfolio_id, project_id)
);

-- Indexes for performance
CREATE INDEX idx_users_org ON users(organization_id);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_teams_org ON teams(organization_id);
CREATE INDEX idx_team_memberships_team ON team_memberships(team_id);
CREATE INDEX idx_team_memberships_user ON team_memberships(user_id);
CREATE INDEX idx_projects_org ON projects(organization_id);
CREATE INDEX idx_projects_team ON projects(team_id);
CREATE INDEX idx_projects_owner ON projects(owner_id);
CREATE INDEX idx_projects_status ON projects(status);
CREATE INDEX idx_sections_project ON sections(project_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_section ON tasks(section_id);
CREATE INDEX idx_tasks_assignee ON tasks(assignee_id);
CREATE INDEX idx_tasks_parent ON tasks(parent_task_id);
CREATE INDEX idx_tasks_created_by ON tasks(created_by);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);
CREATE INDEX idx_comments_task ON comments(task_id);
CREATE INDEX idx_comments_user ON comments(user_id);
CREATE INDEX idx_custom_field_values_task ON custom_field_values(task_id);
CREATE INDEX idx_custom_field_values_field ON custom_field_values(field_id);
CREATE INDEX idx_task_tags_task ON task_tags(task_id);
CREATE INDEX idx_task_tags_tag ON task_tags(tag_id);
CREATE INDEX idx_attachments_task ON attachments(task_id);