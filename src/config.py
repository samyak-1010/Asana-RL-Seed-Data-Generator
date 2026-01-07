"""
Configuration settings for Asana seed data generation.
"""
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')

# Generation Parameters
NUM_EMPLOYEES = int(os.getenv('NUM_EMPLOYEES', '7500'))
SIMULATION_MONTHS = 6  # 6 months of historical data

# Date range
END_DATE = datetime.strptime(
    os.getenv('SIMULATION_END_DATE', '2026-01-07'),
    '%Y-%m-%d'
)
START_DATE = END_DATE - timedelta(days=180)  # 6 months ago

# LLM Settings
LLM_MODEL = os.getenv('LLM_MODEL', 'claude-sonnet-4-20250514')
LLM_TEMPERATURE = float(os.getenv('LLM_TEMPERATURE', '0.7'))
LLM_MAX_TOKENS = int(os.getenv('LLM_MAX_TOKENS', '1000'))

# Database
DB_PATH = os.getenv('DB_PATH', 'output/asana_simulation.sqlite')

# Logging
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Organization Settings
COMPANY_DOMAIN = 'company.com'  # Will be replaced with scraped company name

# Team Distribution (approximate percentages)
TEAM_DISTRIBUTION = {
    'Engineering': 0.40,  # 40% of employees
    'Product': 0.10,
    'Design': 0.08,
    'Marketing': 0.12,
    'Sales': 0.15,
    'Operations': 0.08,
    'HR': 0.04,
    'Finance': 0.03
}

# Team Size Distribution (people per team)
TEAM_SIZE_RANGES = {
    'Engineering': (8, 15),  # Min, Max
    'Product': (5, 10),
    'Design': (5, 8),
    'Marketing': (6, 12),
    'Sales': (8, 15),
    'Operations': (5, 10),
    'HR': (4, 8),
    'Finance': (3, 6)
}

# Project Type Distribution by Team
PROJECT_TYPE_BY_TEAM = {
    'Engineering': {'Sprint': 0.60, 'Kanban': 0.30, 'List': 0.10},
    'Product': {'Timeline': 0.50, 'List': 0.30, 'Kanban': 0.20},
    'Design': {'Kanban': 0.50, 'Timeline': 0.30, 'List': 0.20},
    'Marketing': {'Timeline': 0.40, 'Calendar': 0.30, 'List': 0.30},
    'Sales': {'List': 0.60, 'Kanban': 0.30, 'Timeline': 0.10},
    'Operations': {'List': 0.50, 'Kanban': 0.40, 'Timeline': 0.10},
    'HR': {'List': 0.70, 'Timeline': 0.20, 'Kanban': 0.10},
    'Finance': {'List': 0.80, 'Timeline': 0.20}
}

# Task Completion Rates by Project Type (from Asana research)
COMPLETION_RATES = {
    'Sprint': (0.70, 0.85),  # Min, Max
    'Kanban': (0.60, 0.70),
    'Timeline': (0.50, 0.65),
    'List': (0.40, 0.55),
    'Calendar': (0.65, 0.75)
}

# Due Date Distribution (based on project management research)
DUE_DATE_DISTRIBUTION = {
    'within_1_week': 0.25,
    'within_1_month': 0.40,
    'within_3_months': 0.20,
    'no_due_date': 0.10,
    'overdue': 0.05
}

# Task Assignment Rate
UNASSIGNED_TASK_RATE = 0.15  # 15% of tasks unassigned per Asana benchmarks

# Custom Fields
STANDARD_CUSTOM_FIELDS = [
    {
        'name': 'Priority',
        'type': 'enum',
        'options': ['Critical', 'High', 'Medium', 'Low']
    },
    {
        'name': 'Effort',
        'type': 'enum',
        'options': ['XS', 'S', 'M', 'L', 'XL']
    },
    {
        'name': 'Status',
        'type': 'enum',
        'options': ['Not Started', 'In Progress', 'Blocked', 'In Review', 'Done']
    },
    {
        'name': 'Story Points',
        'type': 'number'
    },
    {
        'name': 'Sprint',
        'type': 'text'
    }
]

# Tags
COMMON_TAGS = [
    'bug', 'feature', 'enhancement', 'urgent', 'blocked',
    'needs-review', 'documentation', 'technical-debt', 'customer-request',
    'security', 'performance', 'ux', 'backend', 'frontend'
]

# Subtask Rate
SUBTASK_RATE = 0.30  # 30% of tasks have subtasks
SUBTASKS_PER_TASK = (1, 5)  # Min, Max

# Comment Rate
COMMENT_RATE = 0.45  # 45% of tasks have comments
COMMENTS_PER_TASK = (1, 8)  # Min, Max

# Attachment Rate
ATTACHMENT_RATE = 0.20  # 20% of tasks have attachments

# Section Names by Workflow Type
SECTION_TEMPLATES = {
    'Engineering': ['Backlog', 'To Do', 'In Progress', 'In Review', 'Done'],
    'Marketing': ['Ideas', 'Planning', 'In Production', 'Review', 'Published'],
    'Product': ['Discovery', 'Prioritized', 'In Development', 'Testing', 'Shipped'],
    'Design': ['Backlog', 'To Do', 'In Progress', 'Review', 'Done'],
    'Operations': ['New Requests', 'In Progress', 'Waiting', 'Done'],
    'General': ['To Do', 'In Progress', 'Done']
}

# File Types for Attachments
ATTACHMENT_FILE_TYPES = [
    ('application/pdf', ['.pdf']),
    ('image/png', ['.png']),
    ('image/jpeg', ['.jpg', '.jpeg']),
    ('application/vnd.openxmlformats-officedocument.wordprocessingml.document', ['.docx']),
    ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', ['.xlsx']),
    ('application/vnd.openxmlformats-officedocument.presentationml.presentation', ['.pptx']),
    ('text/plain', ['.txt']),
    ('application/zip', ['.zip']),
]

# Workload Distribution (Pareto principle)
# Top 20% of users handle 80% of tasks
WORKLOAD_PARETO_RATIO = 0.8

# Weekend Avoidance Rate for Due Dates
WEEKEND_AVOIDANCE_RATE = 0.85

# Sprint Duration (days)
SPRINT_DURATION = 14  # 2 weeks