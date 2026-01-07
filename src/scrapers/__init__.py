"""Scrapers package for external data sources."""
from .companies import get_company_data
from .names import generate_name_data, NameGenerator
from .projects import generate_project_names, ProjectTemplateGenerator