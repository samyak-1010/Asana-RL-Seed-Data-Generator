"""
Database operations and utilities.
"""
import sqlite3
import logging
from pathlib import Path
from typing import List, Dict, Any
from contextlib import contextmanager

logger = logging.getLogger(__name__)


class Database:
    """SQLite database manager for Asana simulation."""
    
    def __init__(self, db_path: str):
        """Initialize database connection."""
        self.db_path = db_path
        self.conn = None
        
    def connect(self):
        """Establish database connection."""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        logger.info(f"Connected to database: {self.db_path}")
        
    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
            
    @contextmanager
    def transaction(self):
        """Context manager for database transactions."""
        try:
            yield self.conn
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Transaction failed: {e}")
            raise
            
    def execute_script(self, script_path: str):
        """Execute SQL script from file."""
        with open(script_path, 'r') as f:
            script = f.read()
        self.conn.executescript(script)
        self.conn.commit()
        logger.info(f"Executed script: {script_path}")
        
    def insert_many(self, table: str, records: List[Dict[str, Any]]):
        """
        Bulk insert records into a table.
        
        Args:
            table: Table name
            records: List of dictionaries with column names as keys
        """
        if not records:
            return
            
        # Get column names from first record
        columns = list(records[0].keys())
        placeholders = ','.join(['?' for _ in columns])
        column_names = ','.join(columns)
        
        query = f"INSERT INTO {table} ({column_names}) VALUES ({placeholders})"
        
        # Convert records to tuples
        values = [tuple(r[col] for col in columns) for r in records]
        
        cursor = self.conn.cursor()
        cursor.executemany(query, values)
        self.conn.commit()
        
        logger.info(f"Inserted {len(records)} records into {table}")
        
    def insert_one(self, table: str, record: Dict[str, Any]):
        """Insert a single record."""
        self.insert_many(table, [record])
        
    def query(self, sql: str, params: tuple = None) -> List[sqlite3.Row]:
        """Execute a SELECT query and return results."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchall()
        
    def query_one(self, sql: str, params: tuple = None) -> sqlite3.Row:
        """Execute a SELECT query and return one result."""
        cursor = self.conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        return cursor.fetchone()
        
    def count(self, table: str) -> int:
        """Count rows in a table."""
        result = self.query_one(f"SELECT COUNT(*) as count FROM {table}")
        return result['count'] if result else 0
        
    def get_all(self, table: str) -> List[sqlite3.Row]:
        """Get all rows from a table."""
        return self.query(f"SELECT * FROM {table}")
        
    def table_exists(self, table: str) -> bool:
        """Check if a table exists."""
        result = self.query_one(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
            (table,)
        )
        return result is not None
        
    def get_schema_info(self) -> Dict[str, List[str]]:
        """Get database schema information."""
        tables = self.query(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        
        schema = {}
        for table in tables:
            table_name = table['name']
            columns = self.query(f"PRAGMA table_info({table_name})")
            schema[table_name] = [col['name'] for col in columns]
            
        return schema
        
    def vacuum(self):
        """Optimize database."""
        self.conn.execute("VACUUM")
        logger.info("Database optimized")


def create_database(db_path: str, schema_path: str) -> Database:
    """
    Create a new database with schema.
    
    Args:
        db_path: Path to SQLite database file
        schema_path: Path to SQL schema file
        
    Returns:
        Database instance
    """
    # Remove existing database if it exists
    db_file = Path(db_path)
    if db_file.exists():
        db_file.unlink()
        logger.info(f"Removed existing database: {db_path}")
        
    # Create new database
    db = Database(db_path)
    db.connect()
    db.execute_script(schema_path)
    logger.info(f"Created database with schema: {schema_path}")
    
    return db