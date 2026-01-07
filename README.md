# Asana RL Seed Data Generator

A comprehensive system for generating realistic seed data for an Asana reinforcement learning environment, simulating a B2B SaaS company with 5,000-10,000 employees.

## Overview

This project creates a realistic Asana workspace simulation with:
- Multi-team organizational structure
- Realistic project management workflows
- Evidence-based data distributions
- Temporal and relational consistency
- Real-world data sources and patterns

## Features

- **Data-Driven Realism**: Uses scraped real-world data from Y Combinator, Census Bureau, GitHub, and industry reports
- **LLM-Enhanced Generation**: Claude API integration for realistic task names and descriptions
- **Distribution Research**: Task completion rates, due date patterns, and team sizes based on Asana's "Anatomy of Work" reports
- **Temporal Consistency**: Ensures all timestamps follow logical ordering
- **Relational Integrity**: Maintains foreign key relationships and business logic

## Quick Start

### Prerequisites

- Python 3.9+
- SQLite 3
- Anthropic API key (for LLM content generation)

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd asana-seed-data

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### Usage

```bash
# Generate the complete database
python src/main.py

# The SQLite database will be created at: output/asana_simulation.sqlite
```

### Configuration

Edit `src/config.py` to adjust:
- Number of employees (default: 7500)
- Date range for simulation (default: 6 months)
- LLM settings (model, temperature)
- Distribution parameters

## Project Structure

```
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── schema.sql                     # Complete DDL for SQLite
├── .env.example                   # Environment variable template
├── src/
│   ├── main.py                   # Entry point / orchestration
│   ├── config.py                 # Configuration settings
│   ├── scrapers/                 # External data fetching
│   │   ├── __init__.py
│   │   ├── companies.py          # YC company scraper
│   │   ├── names.py              # Census name data
│   │   └── projects.py           # GitHub/Asana templates
│   ├── generators/               # Data generation logic
│   │   ├── __init__.py
│   │   ├── organizations.py      # Workspace/org generation
│   │   ├── teams.py              # Team structure
│   │   ├── users.py              # User profiles
│   │   ├── projects.py           # Project generation
│   │   ├── sections.py           # Section generation
│   │   ├── tasks.py              # Task generation
│   │   ├── subtasks.py           # Subtask generation
│   │   ├── comments.py           # Comment generation
│   │   ├── custom_fields.py      # Custom field definitions
│   │   └── tags.py               # Tag generation
│   ├── models/                   # Data models
│   │   ├── __init__.py
│   │   └── entities.py           # Pydantic models
│   └── utils/                    # Helper functions
│       ├── __init__.py
│       ├── database.py           # Database operations
│       ├── dates.py              # Date generation
│       ├── llm.py                # LLM API calls
│       └── distributions.py      # Statistical distributions
├── prompts/                      # LLM prompt templates
│   ├── task_names.txt
│   ├── task_descriptions.txt
│   └── comments.txt
└── output/
    └── asana_simulation.sqlite   # Generated database
```

## Data Sources

### Scraped/Real-World Sources
- **Company Names**: Y Combinator company directory
- **User Names**: US Census Bureau name frequency data
- **Project Templates**: GitHub public repositories, Asana community templates
- **Task Patterns**: Analysis of 500+ public GitHub issues

### Research-Backed Distributions
- **Task Completion Rates**: Asana "Anatomy of Work Index 2023"
- **Due Date Patterns**: Agile sprint research, project management studies
- **Team Sizes**: Bureau of Labor Statistics, tech industry surveys
- **Workload Distribution**: Pareto principle (80/20 rule)

## Database Schema

The database includes 15+ tables representing:
- Organizations and Workspaces
- Teams and Team Memberships
- Users with realistic profiles
- Projects across Engineering, Marketing, Operations
- Sections with status-based workflows
- Tasks with rich metadata
- Subtasks and task hierarchy
- Comments and activity streams
- Custom fields (priority, effort, status)
- Tags and cross-project labels
- Attachments metadata

See `schema.sql` for complete DDL.

## Key Design Decisions

### Custom Fields
- Implemented using EAV (Entity-Attribute-Value) pattern
- `custom_field_definitions` table defines field schema
- `custom_field_values` table stores actual values per task
- Supports multiple data types: text, number, enum, date

### Task Hierarchy
- Subtasks stored in same `tasks` table
- `parent_task_id` foreign key creates hierarchy
- Maximum depth of 2 levels (task → subtask)

### Temporal Consistency
- All timestamps validated: created_at < completed_at < now
- Due dates avoid weekends (85% of tasks)
- Sprint tasks cluster around 2-week boundaries
- Overdue tasks represent 5% (realistic backlog)

## Methodology Highlights

### Realistic Task Names
- Engineering: "[Component] - [Action] - [Detail]" (e.g., "Auth Service - Fix JWT Refresh - Token Expiry")
- Marketing: "[Campaign] - [Deliverable]" (e.g., "Q1 Launch - Email Sequence")
- Operations: "[Process] - [Action]" (e.g., "Onboarding - Update Documentation")

### Due Date Distribution
- 25% within 1 week (urgent)
- 40% within 1 month (normal priority)
- 20% 1-3 months out (planning)
- 10% no due date (backlog)
- 5% overdue (realistic debt)

### Assignment Patterns
- 15% tasks unassigned (per Asana benchmarks)
- Workload follows power law distribution
- Team members assigned to team's projects
- Senior roles have higher assignment rates

## Testing

```bash
# Run with verbose logging
python src/main.py --verbose

# Generate smaller dataset for testing
python src/main.py --employees 1000

# Validate database integrity
python src/utils/validate.py output/asana_simulation.sqlite
```

