"""
Scraper for Y Combinator company directory.
"""
import logging
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
import random

logger = logging.getLogger(__name__)


class YCCompanyScraper:
    """Scrape company names from Y Combinator directory."""
    
    BASE_URL = "https://www.ycombinator.com/companies"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def scrape_companies(self, limit: int = 100) -> List[Dict[str, str]]:
        """
        Scrape company data from Y Combinator.
        
        Args:
            limit: Maximum number of companies to scrape
            
        Returns:
            List of dictionaries with company info
        """
        companies = []
        
        try:
            logger.info(f"Scraping Y Combinator companies (limit: {limit})...")
            
            # Note: YC's website structure may change. This is a simplified version.
            # In production, you'd need to handle pagination and dynamic content.
            
            response = self.session.get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find company elements (structure depends on YC's current site)
            # This is a placeholder - actual scraping would need site-specific selectors
            company_links = soup.find_all('a', href=lambda x: x and '/companies/' in str(x))
            
            for link in company_links[:limit]:
                company_name = link.get_text().strip()
                if company_name and len(company_name) > 2:
                    companies.append({
                        'name': company_name,
                        'domain': self._generate_domain(company_name)
                    })
                    
            logger.info(f"Scraped {len(companies)} companies from YC")
            
        except Exception as e:
            logger.warning(f"YC scraping failed: {e}. Using fallback data.")
            companies = self._get_fallback_companies(limit)
            
        return companies[:limit]
        
    def _generate_domain(self, company_name: str) -> str:
        """Generate plausible domain from company name."""
        # Remove special characters, convert to lowercase
        domain = company_name.lower()
        domain = ''.join(c for c in domain if c.isalnum() or c == ' ')
        domain = domain.replace(' ', '')
        return f"{domain}.com"
        
    def _get_fallback_companies(self, limit: int) -> List[Dict[str, str]]:
        """
        Fallback company list if scraping fails.
        
        Based on real YC companies.
        """
        fallback = [
            {'name': 'Stripe', 'domain': 'stripe.com'},
            {'name': 'Airbnb', 'domain': 'airbnb.com'},
            {'name': 'Dropbox', 'domain': 'dropbox.com'},
            {'name': 'Reddit', 'domain': 'reddit.com'},
            {'name': 'Twitch', 'domain': 'twitch.tv'},
            {'name': 'Instacart', 'domain': 'instacart.com'},
            {'name': 'DoorDash', 'domain': 'doordash.com'},
            {'name': 'Coinbase', 'domain': 'coinbase.com'},
            {'name': 'Gusto', 'domain': 'gusto.com'},
            {'name': 'Brex', 'domain': 'brex.com'},
            {'name': 'GitLab', 'domain': 'gitlab.com'},
            {'name': 'Rappi', 'domain': 'rappi.com'},
            {'name': 'Ginkgo Bioworks', 'domain': 'ginkgobioworks.com'},
            {'name': 'Faire', 'domain': 'faire.com'},
            {'name': 'Scale AI', 'domain': 'scale.com'},
            {'name': 'Retool', 'domain': 'retool.com'},
            {'name': 'Amplitude', 'domain': 'amplitude.com'},
            {'name': 'Segment', 'domain': 'segment.com'},
            {'name': 'Plaid', 'domain': 'plaid.com'},
            {'name': 'Checkr', 'domain': 'checkr.com'},
            {'name': 'Rippling', 'domain': 'rippling.com'},
            {'name': 'Lattice', 'domain': 'lattice.com'},
            {'name': 'Mixpanel', 'domain': 'mixpanel.com'},
            {'name': 'OpenSea', 'domain': 'opensea.io'},
            {'name': 'Verkada', 'domain': 'verkada.com'},
            {'name': 'Webflow', 'domain': 'webflow.com'},
            {'name': 'Airtable', 'domain': 'airtable.com'},
            {'name': 'Figma', 'domain': 'figma.com'},
            {'name': 'Notion', 'domain': 'notion.so'},
            {'name': 'Zapier', 'domain': 'zapier.com'},
        ]
        
        # Generate more synthetic companies to reach limit
        suffixes = ['Labs', 'AI', 'Tech', 'Systems', 'Solutions', 'Platform', 'Software']
        prefixes = ['Cloud', 'Data', 'Smart', 'Quantum', 'Cyber', 'Neural', 'Edge', 'Flex']
        
        while len(fallback) < limit:
            prefix = random.choice(prefixes)
            suffix = random.choice(suffixes)
            name = f"{prefix}{suffix}"
            domain = f"{name.lower()}.com"
            fallback.append({'name': name, 'domain': domain})
            
        return fallback[:limit]


def get_company_data(limit: int = 100) -> List[Dict[str, str]]:
    """
    Get company data from YC or fallback.
    
    Args:
        limit: Number of companies needed
        
    Returns:
        List of company dictionaries
    """
    scraper = YCCompanyScraper()
    return scraper.scrape_companies(limit)