"""
Main orchestration script for Asana seed data generation.

This generates a complete Asana workspace simulation with realistic data.
"""
import logging
import sys
import random
from pathlib import Path
from datetime import timedelta, datetime
from typing import List, Dict
import numpy as np

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

import config
from models import *
from utils import *
from scrapers import *

# Setup logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AsanaDataGenerator:
    """Main data generator for Asana simulation."""
    
    def __init__(self):
        """Initialize generator."""
        self.db = None
        self.llm = None
        self.organization = None
        self.teams = []
        self.users = []
        self.team_memberships = []
        self.projects = []
        self.sections = []
        self.tasks = []
        self.custom_fields = []
        self.custom_field_options = []
        self.tags = []
        
    def setup(self):
        """Setup database and LLM."""
        logger.info("Setting up database...")
        self.db = create_database(config.DB_PATH, 'schema.sql')
        
        logger.info("Setting up LLM generator...")
        self.llm = LLMGenerator()
        
    def generate_all(self):
        """Generate all data."""
        logger.info("="*60)
        logger.info("Starting Asana seed data generation")
        logger.info(f"Target employees: {config.NUM_EMPLOYEES}")
        logger.info(f"Date range: {config.START_DATE.date()} to {config.END_DATE.date()}")
        logger.info("="*60)
        
        self.generate_organization()
        self.generate_teams()
        self.generate_users()
        self.generate_team_memberships()
        self.generate_custom_fields()
        self.generate_tags()
        self.generate_projects()
        self.generate_sections()
        self.generate_tasks()
        self.generate_subtasks()
        self.generate_comments()
        self.generate_custom_field_values()
        self.generate_task_tags()
        self.generate_attachments()
        
        logger.info("="*60)
        logger.info("Data generation complete!")
        self.print_stats()
        logger.info("="*60)
        
    def generate_organization(self):
        """Generate organization."""
        logger.info("\n[1/15] Generating organization...")
        
        # Get company data
        companies = get_company_data(limit=1)
        company = companies[0]
        
        self.organization = Organization(
            name=company['name'],
            domain=company['domain'],
            is_organization=True,
            created_at=config.START_DATE - timedelta(days=365)
        )
        
        # Update config domain
        config.COMPANY_DOMAIN = company['domain']
        
        # Insert into database
        self.db.insert_one('organizations', self.organization.model_dump())
        logger.info(f"Created organization: {self.organization.name}")
        
    def generate_teams(self):
        """Generate teams."""
        logger.info("\n[2/15] Generating teams...")
        
        # Calculate employees per department
        dept_allocations = {}
        for dept, percentage in config.TEAM_DISTRIBUTION.items():
            dept_allocations[dept] = int(config.NUM_EMPLOYEES * percentage)
            
        # Generate teams
        for dept_type, num_dept_employees in dept_allocations.items():
            if num_dept_employees == 0:
                continue
                
            min_size, max_size = config.TEAM_SIZE_RANGES.get(dept_type, (5, 10))
            avg_team_size = (min_size + max_size) / 2
            num_teams = max(1, int(num_dept_employees / avg_team_size))
            
            for i in range(num_teams):
                # Generate team name
                if num_teams == 1:
                    team_name = dept_type
                else:
                    team_name = f"{dept_type} - Team {i+1}"
                    
                team = Team(
                    organization_id=self.organization.organization_id,
                    name=team_name,
                    description=f"{dept_type} team",
                    team_type=dept_type,
                    created_at=config.START_DATE - timedelta(days=random.randint(30, 365))
                )
                self.teams.append(team)
                
        # Insert into database
        self.db.insert_many('teams', [t.model_dump() for t in self.teams])
        logger.info(f"Created {len(self.teams)} teams")
        
    def generate_users(self):
        """Generate users."""
        logger.info("\n[3/15] Generating users...")
        
        # Generate names
        name_data = generate_name_data(config.NUM_EMPLOYEES, self.organization.domain)
        
        for data in name_data:
            role = random.choices(
                ['admin', 'member', 'limited_access'],
                weights=[0.05, 0.90, 0.05]
            )[0]
            
            department = random.choices(
                list(config.TEAM_DISTRIBUTION.keys()),
                weights=list(config.TEAM_DISTRIBUTION.values())
            )[0]
            
            user = User(
                organization_id=self.organization.organization_id,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=role,
                job_title=f"{department} Team Member",
                department=department,
                is_active=True,
                created_at=config.START_DATE - timedelta(days=random.randint(1, 365)),
                last_active_at=config.END_DATE - timedelta(hours=random.randint(0, 168))
            )
            self.users.append(user)
            
        self.db.insert_many('users', [u.model_dump() for u in self.users])
        logger.info(f"Created {len(self.users)} users")
        
    def generate_team_memberships(self):
        """Generate team memberships."""
        logger.info("\n[4/15] Generating team memberships...")
        
        # Group users by department
        users_by_dept = {}
        for user in self.users:
            if user.department not in users_by_dept:
                users_by_dept[user.department] = []
            users_by_dept[user.department].append(user)
            
        # Assign to teams
        for team in self.teams:
            dept_users = users_by_dept.get(team.team_type, [])
            if not dept_users:
                continue
                
            min_size, max_size = config.TEAM_SIZE_RANGES.get(team.team_type, (5, 10))
            target_size = min(random.randint(min_size, max_size), len(dept_users))
            
            team_members = random.sample(dept_users, target_size)
            lead = random.choice(team_members)
            
            for member in team_members:
                dept_users.remove(member)
                membership = TeamMembership(
                    team_id=team.team_id,
                    user_id=member.user_id,
                    is_team_lead=(member.user_id == lead.user_id),
                    joined_at=member.created_at
                )
                self.team_memberships.append(membership)
                
        self.db.insert_many('team_memberships', [m.model_dump() for m in self.team_memberships])
        logger.info(f"Created {len(self.team_memberships)} team memberships")
        
    def generate_custom_fields(self):
        """Generate custom field definitions."""
        logger.info("\n[5/15] Generating custom fields...")
        
        for field_def in config.STANDARD_CUSTOM_FIELDS:
            field = CustomFieldDefinition(
                organization_id=self.organization.organization_id,
                name=field_def['name'],
                field_type=field_def['type'],
                is_global=True
            )
            self.custom_fields.append(field)
            
            # Add enum options if applicable
            if field_def['type'] in ['enum', 'multi_enum'] and 'options' in field_def:
                colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
                for i, option_name in enumerate(field_def['options']):
                    option = CustomFieldEnumOption(
                        field_id=field.field_id,
                        name=option_name,
                        color=colors[i % len(colors)],
                        position=i
                    )
                    self.custom_field_options.append(option)
                    
        self.db.insert_many('custom_field_definitions', [f.model_dump() for f in self.custom_fields])
        self.db.insert_many('custom_field_enum_options', [o.model_dump() for o in self.custom_field_options])
        logger.info(f"Created {len(self.custom_fields)} custom fields")
        
    def generate_tags(self):
        """Generate tags."""
        logger.info("\n[6/15] Generating tags...")
        
        colors = ['#ff5733', '#33ff57', '#3357ff', '#ff33a1', '#a133ff', '#33fff5']
        for i, tag_name in enumerate(config.COMMON_TAGS):
            tag = Tag(
                organization_id=self.organization.organization_id,
                name=tag_name,
                color=colors[i % len(colors)]
            )
            self.tags.append(tag)
            
        self.db.insert_many('tags', [t.model_dump() for t in self.tags])
        logger.info(f"Created {len(self.tags)} tags")
        
    def generate_projects(self):
        """Generate projects."""
        logger.info("\n[7/15] Generating projects...")
        
        # Generate 3-5 projects per team
        for team in self.teams:
            num_projects = random.randint(3, 5)
            
            # Get project types distribution for team
            project_types_dist = config.PROJECT_TYPE_BY_TEAM.get(
                team.team_type,
                {'List': 0.5, 'Kanban': 0.5}
            )
            
            # Get team members for this team
            team_member_ids = [
                m.user_id for m in self.team_memberships 
                if m.team_id == team.team_id
            ]
            
            if not team_member_ids:
                continue
                
            for _ in range(num_projects):
                # Pick project type
                project_type = pick_from_distribution(project_types_dist)
                
                # Generate project name
                project_names = generate_project_names(team.team_type, 1)
                project_data = project_names[0]
                
                # Project status
                status = random.choices(
                    ['active', 'on_hold', 'completed', 'archived'],
                    weights=[0.70, 0.10, 0.15, 0.05]
                )[0]
                
                # Owner
                owner_id = random.choice(team_member_ids)
                
                project = Project(
                    organization_id=self.organization.organization_id,
                    team_id=team.team_id,
                    name=project_data['name'],
                    project_type=project_type,
                    workflow_type=project_data['workflow_type'],
                    status=status,
                    owner_id=owner_id,
                    color='#' + ''.join([random.choice('0123456789ABCDEF') for _ in range(6)]),
                    created_at=generate_created_at(config.START_DATE, config.END_DATE - timedelta(days=30))
                )
                self.projects.append(project)
                
                # Add project members
                num_members = min(len(team_member_ids), random.randint(3, 8))
                project_member_ids = random.sample(team_member_ids, num_members)
                
        self.db.insert_many('projects', [p.model_dump() for p in self.projects])
        logger.info(f"Created {len(self.projects)} projects")
        
    def generate_sections(self):
        """Generate sections for projects."""
        logger.info("\n[8/15] Generating sections...")
        
        for project in self.projects:
            # Get section template
            section_names = config.SECTION_TEMPLATES.get(
                project.workflow_type,
                config.SECTION_TEMPLATES['General']
            )
            
            for i, section_name in enumerate(section_names):
                section = Section(
                    project_id=project.project_id,
                    name=section_name,
                    position=i,
                    created_at=project.created_at
                )
                self.sections.append(section)
                
        self.db.insert_many('sections', [s.model_dump() for s in self.sections])
        logger.info(f"Created {len(self.sections)} sections")
        
    def generate_tasks(self):
        """Generate tasks."""
        logger.info("\n[9/15] Generating tasks...")
        
        # Generate 15-40 tasks per project
        for project in self.projects:
            num_tasks = random.randint(15, 40)
            
            # Get sections for this project
            project_sections = [s for s in self.sections if s.project_id == project.project_id]
            if not project_sections:
                continue
                
            # Get team members (potential assignees)
            team_member_ids = [
                m.user_id for m in self.team_memberships
                if m.team_id == project.team_id
            ]
            
            for i in range(num_tasks):
                # Select section (bias toward early sections)
                section_weights = [1.0 / (i + 1) for i in range(len(project_sections))]
                section = weighted_choice(project_sections, section_weights)
                
                # Generate task name based on project type
                task_name = self._generate_task_name(project.workflow_type, i)
                
                # Assignee (15% unassigned)
                if random.random() < config.UNASSIGNED_TASK_RATE:
                    assignee_id = None
                else:
                    assignee_id = random.choice(team_member_ids) if team_member_ids else None
                    
                # Created by
                created_by = random.choice(team_member_ids) if team_member_ids else assignee_id
                
                # Creation time
                created_at = generate_created_at(
                    project.created_at,
                    config.END_DATE
                )
                
                # Due date
                due_date = generate_due_date(
                    created_at,
                    config.DUE_DATE_DISTRIBUTION
                )
                
                # Completion status
                completion_rate_range = config.COMPLETION_RATES.get(project.project_type, (0.5, 0.6))
                is_completed = random.random() < random.uniform(*completion_rate_range)
                
                if is_completed:
                    status = 'complete'
                    completed_at = generate_completion_time(created_at, due_date)
                    completed_by = assignee_id or created_by
                else:
                    status = 'incomplete'
                    completed_at = None
                    completed_by = None
                    
                task = Task(
                    project_id=project.project_id,
                    section_id=section.section_id,
                    name=task_name,
                    description=self._generate_task_description(task_name, project.workflow_type),
                    assignee_id=assignee_id,
                    created_by=created_by,
                    status=status,
                    due_date=due_date,
                    created_at=created_at,
                    modified_at=generate_modified_at(created_at, completed_at),
                    completed_at=completed_at,
                    completed_by=completed_by,
                    num_likes=random.randint(0, 5) if random.random() < 0.3 else 0
                )
                self.tasks.append(task)
                
        self.db.insert_many('tasks', [t.model_dump() for t in self.tasks])
        logger.info(f"Created {len(self.tasks)} tasks")
        
    def _generate_task_name(self, workflow_type: str, index: int) -> str:
        """Generate realistic task name."""
        patterns = {
            'Engineering': [
                'Fix {bug} in {component}',
                'Implement {feature}',
                'Refactor {component}',
                'Add tests for {feature}',
                'Optimize {component} performance',
                'Update {component} documentation',
                'Migrate {component} to {tech}',
            ],
            'Marketing': [
                'Create {asset} for {campaign}',
                'Schedule {content} posts',
                'Review {campaign} performance',
                'Design {asset}',
                'Write {content} copy',
                'Plan {event}',
            ],
            'Product': [
                'Define requirements for {feature}',
                'Create spec for {feature}',
                'User research on {topic}',
                'Analyze {metric} data',
                'Prioritize {area} backlog',
            ],
            'Design': [
                'Design {component} mockups',
                'Create {asset} assets',
                'Conduct usability testing for {feature}',
                'Update design system {component}',
            ],
        }
        
        templates = patterns.get(workflow_type, patterns['Engineering'])
        template = random.choice(templates)
        
        # Fill in placeholders
        replacements = {
            'bug': random.choice(['authentication error', 'API timeout', 'UI glitch', 'memory leak']),
            'component': random.choice(['dashboard', 'API', 'database', 'frontend', 'auth service']),
            'feature': random.choice(['user profiles', 'notifications', 'search', 'analytics', 'export']),
            'tech': random.choice(['TypeScript', 'React', 'GraphQL', 'PostgreSQL']),
            'asset': random.choice(['email template', 'landing page', 'social post', 'infographic']),
            'campaign': random.choice(['Q1 launch', 'product release', 'brand awareness', 'webinar']),
            'content': random.choice(['blog', 'social media', 'email', 'video']),
            'event': random.choice(['webinar', 'conference', 'product launch', 'workshop']),
            'metric': random.choice(['engagement', 'conversion', 'retention', 'churn']),
            'topic': random.choice(['onboarding', 'navigation', 'checkout', 'settings']),
            'area': random.choice(['features', 'bugs', 'technical debt', 'improvements'])
        }
        
        for key, value in replacements.items():
            template = template.replace('{' + key + '}', value)
            
        return template
        
    def _generate_task_description(self, task_name: str, workflow_type: str) -> str:
        """Generate task description."""
        # 20% empty, 50% short, 30% detailed
        rand = random.random()
        if rand < 0.2:
            return None
        elif rand < 0.7:
            return f"Work on: {task_name.lower()}"
        else:
            return f"Task details:\n- {task_name}\n- Please review and implement\n- Coordinate with team"
            
    def generate_subtasks(self):
        """Generate subtasks."""
        logger.info("\n[10/15] Generating subtasks...")
        
        subtask_count = 0
        for task in self.tasks:
            # 30% of tasks have subtasks
            if random.random() > config.SUBTASK_RATE:
                continue
                
            num_subtasks = random.randint(*config.SUBTASKS_PER_TASK)
            
            for i in range(num_subtasks):
                subtask = Task(
                    project_id=task.project_id,
                    section_id=task.section_id,
                    parent_task_id=task.task_id,
                    name=f"Subtask {i+1}: {task.name[:30]}...",
                    assignee_id=task.assignee_id,
                    created_by=task.created_by,
                    status='complete' if task.status == 'complete' and random.random() < 0.8 else 'incomplete',
                    created_at=task.created_at + timedelta(hours=random.randint(1, 48)),
                    modified_at=task.modified_at
                )
                self.tasks.append(subtask)
                subtask_count += 1
                
        # Update parent tasks with subtask count
        parent_task_counts = {}
        for task in self.tasks:
            if task.parent_task_id:
                parent_task_counts[task.parent_task_id] = parent_task_counts.get(task.parent_task_id, 0) + 1
                
        for task in self.tasks:
            if task.task_id in parent_task_counts:
                task.num_subtasks = parent_task_counts[task.task_id]
                
        self.db.insert_many('tasks', [t.model_dump() for t in self.tasks if t.parent_task_id])
        logger.info(f"Created {subtask_count} subtasks")
        
    def generate_comments(self):
        """Generate comments."""
        logger.info("\n[11/15] Generating comments...")
        
        comments = []
        for task in self.tasks:
            # 45% of tasks have comments
            if random.random() > config.COMMENT_RATE:
                continue
                
            num_comments = random.randint(*config.COMMENTS_PER_TASK)
            
            # Get potential commenters
            if task.assignee_id and task.created_by:
                commenters = [task.assignee_id, task.created_by]
            elif task.assignee_id:
                commenters = [task.assignee_id]
            elif task.created_by:
                commenters = [task.created_by]
            else:
                continue
                
            for i in range(num_comments):
                comment = Comment(
                    task_id=task.task_id,
                    user_id=random.choice(commenters),
                    text=random.choice([
                        'Working on this now',
                        'Updated the implementation',
                        'Ready for review',
                        'Looks good to me',
                        'Need more info on this',
                        'Blocked by another task',
                        'Can we prioritize this?',
                    ]),
                    created_at=task.created_at + timedelta(hours=random.randint(1, 168)),
                    num_likes=random.randint(0, 3) if random.random() < 0.3 else 0
                )
                comments.append(comment)
                
        # Update task comment counts
        for task in self.tasks:
            task.num_comments = len([c for c in comments if c.task_id == task.task_id])
            
        self.db.insert_many('comments', [c.model_dump() for c in comments])
        logger.info(f"Created {len(comments)} comments")
        
    def generate_custom_field_values(self):
        """Generate custom field values."""
        logger.info("\n[12/15] Generating custom field values...")
        
        values = []
        
        # Get priority and effort fields
        priority_field = next((f for f in self.custom_fields if f.name == 'Priority'), None)
        effort_field = next((f for f in self.custom_fields if f.name == 'Effort'), None)
        
        if not priority_field or not effort_field:
            return
            
        # Get options
        priority_options = [o for o in self.custom_field_options if o.field_id == priority_field.field_id]
        effort_options = [o for o in self.custom_field_options if o.field_id == effort_field.field_id]
        
        # 70% of tasks have priority, 50% have effort
        for task in self.tasks:
            if random.random() < 0.7 and priority_options:
                value = CustomFieldValue(
                    task_id=task.task_id,
                    field_id=priority_field.field_id,
                    enum_option_id=random.choice(priority_options).option_id
                )
                values.append(value)
                
            if random.random() < 0.5 and effort_options:
                value = CustomFieldValue(
                    task_id=task.task_id,
                    field_id=effort_field.field_id,
                    enum_option_id=random.choice(effort_options).option_id
                )
                values.append(value)
                
        self.db.insert_many('custom_field_values', [v.model_dump() for v in values])
        logger.info(f"Created {len(values)} custom field values")
        
    def generate_task_tags(self):
        """Generate task-tag associations."""
        logger.info("\n[13/15] Generating task tags...")
        
        task_tags = []
        
        # 30% of tasks have 1-2 tags
        for task in self.tasks:
            if random.random() < 0.3:
                num_tags = random.randint(1, 2)
                selected_tags = random.sample(self.tags, min(num_tags, len(self.tags)))
                
                for tag in selected_tags:
                    task_tag = TaskTag(
                        task_id=task.task_id,
                        tag_id=tag.tag_id
                    )
                    task_tags.append(task_tag)
                    
        self.db.insert_many('task_tags', [tt.model_dump() for tt in task_tags])
        logger.info(f"Created {len(task_tags)} task-tag associations")
        
    def generate_attachments(self):
        """Generate attachment metadata."""
        logger.info("\n[14/15] Generating attachments...")
        
        attachments = []
        
        # 20% of tasks have attachments
        for task in self.tasks:
            if random.random() > config.ATTACHMENT_RATE:
                continue
                
            # Select file type
            mime_type, extensions = random.choice(config.ATTACHMENT_FILE_TYPES)
            extension = random.choice(extensions)
            filename = f"attachment_{random.randint(1000, 9999)}{extension}"
            
            attachment = Attachment(
                task_id=task.task_id,
                uploaded_by=task.created_by,
                filename=filename,
                file_type=mime_type,
                file_size=random.randint(1024, 10485760),  # 1KB to 10MB
                storage_url=f"https://storage.example.com/{filename}",
                created_at=task.created_at + timedelta(hours=random.randint(1, 168))
            )
            attachments.append(attachment)
            
        self.db.insert_many('attachments', [a.model_dump() for a in attachments])
        logger.info(f"Created {len(attachments)} attachments")
        
    def print_stats(self):
        """Print generation statistics."""
        print("\nGeneration Statistics:")
        print("-" * 40)
        print(f"Organizations:       {self.db.count('organizations')}")
        print(f"Teams:               {self.db.count('teams')}")
        print(f"Users:               {self.db.count('users')}")
        print(f"Team Memberships:    {self.db.count('team_memberships')}")
        print(f"Projects:            {self.db.count('projects')}")
        print(f"Sections:            {self.db.count('sections')}")
        print(f"Tasks:               {self.db.count('tasks')}")
        print(f"Comments:            {self.db.count('comments')}")
        print(f"Custom Fields:       {self.db.count('custom_field_definitions')}")
        print(f"Custom Field Values: {self.db.count('custom_field_values')}")
        print(f"Tags:                {self.db.count('tags')}")
        print(f"Task Tags:           {self.db.count('task_tags')}")
        print(f"Attachments:         {self.db.count('attachments')}")
        print("-" * 40)
        
        if self.llm:
            stats = self.llm.get_stats()
            print(f"\nLLM Statistics:")
            print(f"API Calls:  {stats['call_count']}")
            print(f"Total Tokens: {stats['total_tokens']}")


def main():
    """Main entry point."""
    try:
        generator = AsanaDataGenerator()
        generator.setup()
        generator.generate_all()
        
        logger.info(f"\nDatabase saved to: {config.DB_PATH}")
        logger.info("Generation complete!")
        
    except Exception as e:
        logger.error(f"Generation failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    main()