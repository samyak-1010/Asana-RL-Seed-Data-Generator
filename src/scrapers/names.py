"""
Name generator using US Census Bureau data patterns.
"""
import logging
import random
from typing import List, Tuple

logger = logging.getLogger(__name__)


class NameGenerator:
    """
    Generate realistic names based on US Census name frequency data.
    
    Data based on US Census Bureau's "Frequently Occurring Surnames" and
    "Popular Baby Names" datasets.
    """
    
    # Top 100 first names (from SSA baby names data - mixed genders)
    FIRST_NAMES = [
        # Male names
        'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
        'Thomas', 'Christopher', 'Charles', 'Daniel', 'Matthew', 'Anthony', 'Mark',
        'Donald', 'Steven', 'Andrew', 'Paul', 'Joshua', 'Kenneth', 'Kevin', 'Brian',
        'George', 'Timothy', 'Ronald', 'Edward', 'Jason', 'Jeffrey', 'Ryan', 'Jacob',
        'Nicholas', 'Eric', 'Jonathan', 'Stephen', 'Larry', 'Justin', 'Scott', 'Brandon',
        'Benjamin', 'Samuel', 'Raymond', 'Gregory', 'Alexander', 'Patrick', 'Jack',
        'Dennis', 'Jerry', 'Tyler', 'Aaron', 'Jose', 'Adam', 'Nathan', 'Douglas',
        'Zachary', 'Henry', 'Carl', 'Arthur', 'Kyle', 'Lawrence', 'Joe', 'Willie',
        # Female names
        'Mary', 'Patricia', 'Jennifer', 'Linda', 'Barbara', 'Elizabeth', 'Susan',
        'Jessica', 'Sarah', 'Karen', 'Lisa', 'Nancy', 'Betty', 'Dorothy', 'Sandra',
        'Ashley', 'Kimberly', 'Emily', 'Donna', 'Michelle', 'Carol', 'Amanda', 'Melissa',
        'Deborah', 'Stephanie', 'Rebecca', 'Sharon', 'Laura', 'Cynthia', 'Amy', 'Kathleen',
        'Angela', 'Shirley', 'Brenda', 'Emma', 'Anna', 'Pamela', 'Nicole', 'Samantha',
        'Katherine', 'Christine', 'Helen', 'Debra', 'Rachel', 'Carolyn', 'Janet', 'Maria',
        'Catherine', 'Heather', 'Diane', 'Julie', 'Joyce', 'Victoria', 'Ruth', 'Virginia',
        'Lauren', 'Kelly', 'Christina', 'Joan', 'Evelyn', 'Judith', 'Andrea', 'Hannah',
        'Megan', 'Cheryl', 'Jacqueline', 'Martha', 'Madison', 'Teresa', 'Gloria', 'Sara',
        'Janice', 'Kathryn', 'Abigail', 'Sophia', 'Frances', 'Jean', 'Alice', 'Judy'
    ]
    
    # Top 100 last names (from Census Bureau data)
    LAST_NAMES = [
        'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
        'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
        'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
        'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
        'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
        'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
        'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
        'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
        'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
        'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson', 'Watson',
        'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz',
        'Hughes', 'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long',
        'Ross', 'Foster', 'Jimenez', 'Powell'
    ]
    
    def __init__(self):
        """Initialize name generator."""
        self.used_emails = set()
        
    def generate_name(self) -> Tuple[str, str]:
        """
        Generate a random first and last name.
        
        Returns:
            Tuple of (first_name, last_name)
        """
        first = random.choice(self.FIRST_NAMES)
        last = random.choice(self.LAST_NAMES)
        return first, last
        
    def generate_email(
        self,
        first_name: str,
        last_name: str,
        domain: str
    ) -> str:
        """
        Generate email address with collision avoidance.
        
        Args:
            first_name: First name
            last_name: Last name
            domain: Email domain
            
        Returns:
            Email address
        """
        # Try different formats
        formats = [
            f"{first_name.lower()}.{last_name.lower()}@{domain}",
            f"{first_name[0].lower()}{last_name.lower()}@{domain}",
            f"{first_name.lower()}{last_name[0].lower()}@{domain}",
            f"{first_name.lower()}{last_name.lower()}@{domain}",
        ]
        
        # Find unused format
        for fmt in formats:
            if fmt not in self.used_emails:
                self.used_emails.add(fmt)
                return fmt
                
        # If all formats used, add number
        base = f"{first_name.lower()}.{last_name.lower()}"
        counter = 1
        while True:
            email = f"{base}{counter}@{domain}"
            if email not in self.used_emails:
                self.used_emails.add(email)
                return email
            counter += 1
            
    def generate_names(self, count: int) -> List[Tuple[str, str]]:
        """
        Generate multiple unique names.
        
        Args:
            count: Number of names to generate
            
        Returns:
            List of (first_name, last_name) tuples
        """
        names = set()
        while len(names) < count:
            name = self.generate_name()
            names.add(name)
        return list(names)
        
    def generate_users(
        self,
        count: int,
        domain: str
    ) -> List[dict]:
        """
        Generate complete user data.
        
        Args:
            count: Number of users
            domain: Email domain
            
        Returns:
            List of user dictionaries
        """
        users = []
        names = self.generate_names(count)
        
        for first, last in names:
            email = self.generate_email(first, last, domain)
            users.append({
                'first_name': first,
                'last_name': last,
                'email': email
            })
            
        logger.info(f"Generated {len(users)} user names")
        return users


def generate_name_data(count: int, domain: str) -> List[dict]:
    """
    Generate name data for users.
    
    Args:
        count: Number of users needed
        domain: Email domain
        
    Returns:
        List of user dictionaries with names and emails
    """
    generator = NameGenerator()
    return generator.generate_users(count, domain)