"""
Organization/Workspace generator.
"""
import logging
from datetime import timedelta
import config
from models import Organization
from scrapers import get_company_data

logger = logging.getLogger(__name__)


def generate_organization() -> Organization:
    """
    Generate organization data.
    
    Uses scraped company data from Y Combinator directory.
    
    Returns:
        Organization instance
    """
    # Get a company from YC directory
    companies = get_company_data(limit=1)
    company = companies[0]
    
    # Create organization
    org = Organization(
        name=company['name'],
        domain=company['domain'],
        is_organization=True,
        created_at=config.START_DATE - timedelta(days=365)  # Company existed before simulation
    )
    
    logger.info(f"Generated organization: {org.name}")
    return org