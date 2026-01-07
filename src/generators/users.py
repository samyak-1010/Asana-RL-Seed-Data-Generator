"""
Users generator.
"""
import logging
import random
from typing import List
from datetime import timedelta
import config
from models import User, TeamMembership
from scrapers import generate_name_data

logger = logging.getLogger(__name__)


# Job titles by department
JOB_TITLES = {
    'Engineering': [
        'Senior Software Engineer', 'Software Engineer', 'Staff Engineer',
        'Principal Engineer', 'Engineering Manager', 'Tech Lead',
        'Senior Backend Engineer', 'Senior Frontend Engineer', 'DevOps Engineer',
        'Data Engineer', 'ML Engineer', 'QA Engineer', 'Security Engineer'
    ],
    'Product': [
        'Product Manager', 'Senior Product Manager', 'Director of Product',
        'VP of Product', 'Product Lead', 'Associate Product Manager',
        'Technical Product Manager', 'Group Product Manager'
    ],
    'Design': [
        'Product Designer', 'Senior Product Designer', 'UX Researcher',
        'Design Lead', 'Head of Design', 'Brand Designer', 'Visual Designer',
        'UX Writer', 'Design Systems Designer'
    ],
    'Marketing': [
        'Marketing Manager', 'Content Marketing Manager', 'Growth Marketing Manager',
        'Product Marketing Manager', 'Brand Manager', 'Demand Generation Manager',
        'Marketing Director', 'VP of Marketing', 'Marketing Coordinator'
    ],
    'Sales': [
        'Account Executive', 'Senior Account Executive', 'Sales Development Rep',
        'Sales Manager', 'VP of Sales', 'Sales Engineer', 'Account Manager',
        'Business Development Manager', 'Sales Operations Manager'
    ],
    'Operations': [
        'Operations Manager', 'Operations Coordinator', 'Chief of Staff',
        'Business Operations Manager', 'VP of Operations', 'Program Manager',
        'Project Manager', 'Operations Analyst'
    ],
    'HR': [
        'HR Manager', 'Recruiter', 'Senior Recruiter', 'People Operations Manager',
        'HR Business Partner', 'Talent Acquisition Manager', 'VP of People',
        'People Operations Coordinator'
    ],
    'Finance': [
        'Financial Analyst', 'Senior Financial Analyst', 'Controller',
        'CFO', 'Finance Manager', 'Accounting Manager', 'Finance Director'
    ]
}


def generate_users(
    organization_id: str,
    domain: str,
    num_employees: int
) -> List[User]:
    """
    Generate users with realistic demographics.
    
    Uses US Census Bureau name frequency data for realistic name distribution.
    
    Args:
        organization_id: Organization ID
        domain: Email domain
        num_employees: Number of users to generate
        
    Returns:
        List of User instances
    """
    # Generate name data from Census patterns
    name_data = generate_name_data(num_employees, domain)
    
    users = []
    for data in name_data:
        # Most users are 'member' role
        role = random.choices(
            ['admin', 'member', 'limited_access', 'guest'],
            weights=[0.05, 0.85, 0.08, 0.02]
        )[0]
        
        # Determine department (will be refined with team membership)
        department = random.choices(
            list(config.TEAM_DISTRIBUTION.keys()),
            weights=list(config.TEAM_DISTRIBUTION.values())
        )[0]
        
        # Assign job title based on department
        titles = JOB_TITLES.get(department, ['Team Member'])
        job_title = random.choice(titles)
        
        # Last active time (most active recently, some inactive)
        if random.random() < 0.95:
            last_active = config.END_DATE - timedelta(
                days=random.randint(0, 7),
                hours=random.randint(0, 23)
            )
        else:
            # 5% inactive for 30+ days
            last_active = config.END_DATE - timedelta(days=random.randint(30, 180))
            
        user = User(
            organization_id=organization_id,
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=role,
            job_title=job_title,
            department=department,
            is_active=True,
            created_at=config.START_DATE - timedelta(days=random.randint(1, 365)),
            last_active_at=last_active
        )
        users.append(user)
        
    logger.info(f"Generated {len(users)} users")
    return users


def generate_team_memberships(
    users: List[User],
    teams: List
) -> List[TeamMembership]:
    """
    Assign users to teams.
    
    Users are assigned to teams based on department match.
    Team sizes follow industry research showing optimal sizes of 5-15 people.
    
    Args:
        users: List of users
        teams: List of teams
        
    Returns:
        List of TeamMembership instances
    """
    memberships = []
    
    # Group users by department
    users_by_dept = {}
    for user in users:
        dept = user.department
        if dept not in users_by_dept:
            users_by_dept[dept] = []
        users_by_dept[dept].append(user)
        
    # Assign users to teams
    for team in teams:
        dept_users = users_by_dept.get(team.team_type, [])
        if not dept_users:
            continue
            
        # Calculate team size
        min_size, max_size = config.TEAM_SIZE_RANGES.get(team.team_type, (5, 10))
        target_size = random.randint(min_size, max_size)
        target_size = min(target_size, len(dept_users))
        
        # Select team members
        team_members = random.sample(dept_users, target_size)
        
        # Remove assigned users from pool
        for member in team_members:
            dept_users.remove(member)
            
        # Assign one team lead
        lead = random.choice(team_members)
        
        for member in team_members:
            membership = TeamMembership(
                team_id=team.team_id,
                user_id=member.user_id,
                is_team_lead=(member.user_id == lead.user_id),
                joined_at=member.created_at + timedelta(days=random.randint(0, 30))
            )
            memberships.append(membership)
            
    logger.info(f"Generated {len(memberships)} team memberships")
    return memberships