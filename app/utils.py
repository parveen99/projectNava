import re
from sqlalchemy.exc import IntegrityError, OperationalError

def validate_organization_name(name: str) -> bool:
    if not name or len(name.strip()) < 2:
        return False
    if not re.match(r'^[a-zA-Z0-9\s\-_]+$', name):
        return False
    return True


def handle_database_error(error: Exception) -> str:
    if isinstance(error, IntegrityError):
        if "organizations_name_key" in str(error):
            return "Organization with this name already exists"
        elif "admin_users_email_key" in str(error):
            return "Admin with this email already exists"
        else:
            return "Database constraint violation"
    elif isinstance(error, OperationalError):
        return "Database connection error"
    else:
        return f"Database error: {str(error)}"


def create_organization_tables(engine):
    from sqlalchemy import text
    
    tables_sql = [
        """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email VARCHAR(255) UNIQUE NOT NULL,
            hashed_password VARCHAR(255) NOT NULL,
            full_name VARCHAR(255),
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS organization_settings (
            id SERIAL PRIMARY KEY,
            setting_key VARCHAR(255) UNIQUE NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    
    with engine.connect() as conn:
        for sql in tables_sql:
            conn.execute(text(sql))
        conn.commit() 