"""
Teams generator.
"""
import logging
import random
from typing import List
from datetime import timedelta
import config
from models import Team

logger = logging.getLogger(__name__)


def generate_teams(organization_id: str, num_employees: int) -> List[Team]:
    """
    Generate teams based on organization size and distribution.
    
    Team sizes follow industry research from Bureau of Labor Statistics
    and tech industry surveys showing typical team sizes of 5-15 people.
    
    Args:
        organization_id: Organization ID
        num_employees: Total number of employees
        
    Returns:
        List of Team instances
    """
    teams = []
    team_id_counter = {}
    
    # Calculate number of employees per department
    dept_allocations = {}
    for dept, percentage in config.TEAM_DISTRIBUTION.items():
        dept_allocations[dept] = int(num_employees * percentage)
        
    # Generate teams for each department
    for dept_type, num_dept_employees in dept_allocations.items():
        if num_dept_employees == 0:
            continue
            
        # Determine number of teams needed
        min_size, max_size = config.TEAM_SIZE_RANGES.get(dept_type, (5, 10))
        avg_team_size = (min_size + max_size) / 2
        num_teams = max(1, int(num_dept_employees / avg_team_size))
        
        # Generate teams
        for i in range(num_teams):
            team_counter = team_id_counter.get(dept_type, 0) + 1
            team_id_counter[dept_type] = team_counter
            
            # Generate team name
            if num_teams == 1:
                team_name = dept_type
            else:
                # Add team identifiers for multiple teams
                if dept_type == 'Engineering':
                    identifiers = ['Platform', 'Backend', 'Frontend', 'Mobile', 'Infrastructure',
                                  'Data', 'ML', 'Security', 'DevOps', 'QA']
                elif dept_type == 'Product':
                    identifiers = ['Core', 'Growth', 'Platform', 'Enterprise', 'Consumer']
                elif dept_type == 'Design':
                    identifiers = ['Product Design', 'Brand', 'UX Research']
                elif dept_type == 'Marketing':
                    identifiers = ['Growth', 'Brand', 'Content', 'Demand Gen', 'Product Marketing']
                elif dept_type == 'Sales':
                    identifiers = ['Enterprise', 'SMB', 'Inside Sales', 'Sales Ops']
                else:
                    identifiers = [f'Team {j+1}' for j in range(num_teams)]
                    
                if i < len(identifiers):
                    team_name = f"{dept_type} - {identifiers[i]}"
                else:
                    team_name = f"{dept_type} - Team {i+1}"
                    
            # Generate description
            descriptions = {
                'Engineering': 'Responsible for building and maintaining our products',
                'Product': 'Defines product strategy and roadmap',
                'Design': 'Creates user experiences and visual design',
                'Marketing': 'Drives customer acquisition and brand awareness',
                'Sales': 'Acquires new customers and grows revenue',
                'Operations': 'Manages internal processes and operations',
                'HR': 'Supports employee experience and culture',
                'Finance': 'Manages financial planning and operations'
            }
            
            team = Team(
                organization_id=organization_id,
                name=team_name,
                description=descriptions.get(dept_type),
                team_type=dept_type,
                created_at=config.START_DATE - timedelta(days=random.randint(30, 365))
            )
            teams.append(team)
            
    logger.info(f"Generated {len(teams)} teams across {len(dept_allocations)} departments")
    return teams