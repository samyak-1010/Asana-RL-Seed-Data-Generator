"""
Project template and naming patterns from public sources.
"""
import logging
import random
from typing import List, Dict

logger = logging.getLogger(__name__)


class ProjectTemplateGenerator:
    """
    Generate project names based on patterns from:
    - Asana public templates
    - GitHub project boards
    - ProductHunt launches
    """
    
    # Engineering project patterns (from GitHub)
    ENGINEERING_PATTERNS = [
        "{component} {version} {work_type}",
        "Q{quarter} {component} Improvements",
        "{component} - {feature}",
        "{system} Migration",
        "{feature} Implementation",
        "Technical Debt - {area}",
        "{service} Refactoring",
        "Infrastructure - {focus}",
        "{platform} Upgrade",
        "API {version} Development"
    ]
    
    ENGINEERING_COMPONENTS = [
        'Authentication', 'API', 'Database', 'Frontend', 'Backend', 'Mobile',
        'Infrastructure', 'Analytics', 'Search', 'Payments', 'Notifications',
        'Dashboard', 'Admin Panel', 'User Management', 'Reporting', 'Integration'
    ]
    
    ENGINEERING_FEATURES = [
        'OAuth Integration', 'Real-time Updates', 'Caching Layer', 'Load Balancing',
        'Error Handling', 'Monitoring', 'CI/CD Pipeline', 'Security Audit',
        'Performance Optimization', 'GraphQL API', 'Microservices', 'Containerization'
    ]
    
    # Marketing project patterns
    MARKETING_PATTERNS = [
        "Q{quarter} {campaign_type} Campaign",
        "{channel} Marketing - {period}",
        "{event} Launch Campaign",
        "{product} Go-to-Market",
        "Content Calendar - {period}",
        "{channel} Optimization",
        "Brand {initiative}",
        "{campaign} Execution",
        "{event} Event Planning",
        "Customer {program}"
    ]
    
    MARKETING_CAMPAIGNS = [
        'Brand Awareness', 'Lead Generation', 'Product Launch', 'Seasonal',
        'Holiday', 'Webinar Series', 'Email Marketing', 'Social Media',
        'Content Marketing', 'SEO', 'Paid Ads', 'Influencer'
    ]
    
    MARKETING_CHANNELS = [
        'Email', 'Social Media', 'Blog', 'Video', 'Podcast', 'Webinar',
        'Events', 'PR', 'Partnerships', 'Community'
    ]
    
    # Product project patterns
    PRODUCT_PATTERNS = [
        "{feature} Development",
        "Q{quarter} Roadmap",
        "{product_area} Enhancements",
        "User Research - {focus}",
        "{feature} Beta",
        "Product Discovery - {area}",
        "{initiative} Planning",
        "Customer Feedback - {period}",
        "{feature} Specs",
        "Product Metrics - {area}"
    ]
    
    PRODUCT_FEATURES = [
        'Dashboard', 'Onboarding', 'Mobile App', 'Integrations', 'Analytics',
        'Collaboration', 'Notifications', 'Search', 'Settings', 'Admin Tools',
        'Reporting', 'Export', 'Templates', 'Workflow', 'Automation'
    ]
    
    # Operations project patterns
    OPERATIONS_PATTERNS = [
        "{process} Optimization",
        "Q{quarter} {department} Planning",
        "{system} Implementation",
        "{process} Documentation",
        "{area} Compliance",
        "Vendor Management - {category}",
        "{initiative} Rollout",
        "{department} Onboarding",
        "{process} Audit",
        "Cost Optimization - {area}"
    ]
    
    OPERATIONS_PROCESSES = [
        'Hiring', 'Onboarding', 'Performance Review', 'Budget Planning',
        'Procurement', 'Facilities', 'IT Support', 'Security', 'Compliance',
        'Training', 'Travel', 'Equipment', 'Vendor', 'Contract'
    ]
    
    def __init__(self):
        """Initialize generator."""
        self.quarters = ['1', '2', '3', '4']
        self.years = ['2025', '2026']
        self.periods = ['H1', 'H2', 'Q1', 'Q2', 'Q3', 'Q4', 'January', 'February',
                       'March', 'April', 'May', 'June', 'July', 'August',
                       'September', 'October', 'November', 'December']
        
    def generate_engineering_project(self) -> Dict[str, str]:
        """Generate engineering project name and description."""
        pattern = random.choice(self.ENGINEERING_PATTERNS)
        
        name = pattern.format(
            component=random.choice(self.ENGINEERING_COMPONENTS),
            version=f"v{random.randint(1, 5)}.{random.randint(0, 9)}",
            work_type=random.choice(['Sprint', 'Development', 'Updates']),
            quarter=random.choice(self.quarters),
            feature=random.choice(self.ENGINEERING_FEATURES),
            system=random.choice(self.ENGINEERING_COMPONENTS),
            service=random.choice(self.ENGINEERING_COMPONENTS),
            focus=random.choice(['Scalability', 'Performance', 'Security', 'Reliability']),
            area=random.choice(self.ENGINEERING_COMPONENTS),
            platform=random.choice(['AWS', 'GCP', 'Azure', 'Kubernetes'])
        )
        
        return {
            'name': name,
            'workflow_type': 'Engineering'
        }
        
    def generate_marketing_project(self) -> Dict[str, str]:
        """Generate marketing project name and description."""
        pattern = random.choice(self.MARKETING_PATTERNS)
        
        name = pattern.format(
            quarter=random.choice(self.quarters),
            campaign_type=random.choice(self.MARKETING_CAMPAIGNS),
            channel=random.choice(self.MARKETING_CHANNELS),
            period=random.choice(self.periods),
            event=random.choice(['Product Launch', 'Conference', 'Webinar', 'Summit']),
            product=random.choice(['New Feature', 'Platform', 'Service']),
            initiative=random.choice(['Refresh', 'Redesign', 'Guidelines', 'Awareness']),
            campaign=random.choice(self.MARKETING_CAMPAIGNS),
            program=random.choice(['Success', 'Advocacy', 'Retention', 'Acquisition'])
        )
        
        return {
            'name': name,
            'workflow_type': 'Marketing'
        }
        
    def generate_product_project(self) -> Dict[str, str]:
        """Generate product project name and description."""
        pattern = random.choice(self.PRODUCT_PATTERNS)
        
        name = pattern.format(
            feature=random.choice(self.PRODUCT_FEATURES),
            quarter=random.choice(self.quarters),
            product_area=random.choice(self.PRODUCT_FEATURES),
            focus=random.choice(['Usability', 'Features', 'Performance']),
            initiative=random.choice(['Strategic', 'Feature', 'Enhancement']),
            period=random.choice(self.periods),
            area=random.choice(self.PRODUCT_FEATURES)
        )
        
        return {
            'name': name,
            'workflow_type': 'Product'
        }
        
    def generate_operations_project(self) -> Dict[str, str]:
        """Generate operations project name and description."""
        pattern = random.choice(self.OPERATIONS_PATTERNS)
        
        name = pattern.format(
            process=random.choice(self.OPERATIONS_PROCESSES),
            quarter=random.choice(self.quarters),
            department=random.choice(['HR', 'Finance', 'IT', 'Legal', 'Operations']),
            system=random.choice(['ERP', 'CRM', 'HRIS', 'Expense Management']),
            area=random.choice(['Security', 'Privacy', 'Financial', 'HR']),
            category=random.choice(['Software', 'Hardware', 'Services']),
            initiative=random.choice(['Tool', 'Process', 'Policy'])
        )
        
        return {
            'name': name,
            'workflow_type': 'Operations'
        }
        
    def generate_design_project(self) -> Dict[str, str]:
        """Generate design project name and description."""
        templates = [
            "Design System {version}",
            "UX Research - {focus}",
            "{component} Redesign",
            "Visual Design - {project}",
            "UI Component Library",
            "{feature} Design Sprint",
            "Brand Guidelines {version}",
            "Accessibility Audit",
            "Mobile App Design",
            "Design QA - {period}"
        ]
        
        pattern = random.choice(templates)
        name = pattern.format(
            version=f"v{random.randint(1, 3)}.{random.randint(0, 9)}",
            focus=random.choice(['User Flows', 'Information Architecture', 'Usability']),
            component=random.choice(['Dashboard', 'Onboarding', 'Settings', 'Navigation']),
            project=random.choice(['Q1', 'Q2', 'Q3', 'Q4', 'Website', 'App']),
            feature=random.choice(self.PRODUCT_FEATURES),
            period=random.choice(self.periods)
        )
        
        return {
            'name': name,
            'workflow_type': 'Design'
        }
        
    def generate_project(self, workflow_type: str) -> Dict[str, str]:
        """
        Generate project based on workflow type.
        
        Args:
            workflow_type: Type of workflow
            
        Returns:
            Project data dictionary
        """
        generators = {
            'Engineering': self.generate_engineering_project,
            'Marketing': self.generate_marketing_project,
            'Product': self.generate_product_project,
            'Operations': self.generate_operations_project,
            'Design': self.generate_design_project,
            'General': self.generate_operations_project  # Fallback
        }
        
        generator = generators.get(workflow_type, self.generate_operations_project)
        return generator()


def generate_project_names(workflow_type: str, count: int) -> List[Dict[str, str]]:
    """
    Generate project names for a given workflow type.
    
    Args:
        workflow_type: Workflow type
        count: Number of projects to generate
        
    Returns:
        List of project data dictionaries
    """
    generator = ProjectTemplateGenerator()
    projects = []
    
    for _ in range(count):
        project = generator.generate_project(workflow_type)
        projects.append(project)
        
    logger.info(f"Generated {len(projects)} {workflow_type} project names")
    return projects