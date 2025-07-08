from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

master_engine = create_engine(settings.master_db_url)
MasterSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=master_engine
)

Base = declarative_base()


def get_master_db():
    db = MasterSessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_org_database(org_name: str):
    from sqlalchemy import text
    
    db_name = f"{settings.org_db_prefix}{org_name.lower().replace(' ', '_')}"
    
    with master_engine.connect() as conn:
        conn.execute(text("COMMIT"))  # End any existing transaction
        conn.execute(text(f"CREATE DATABASE {db_name}"))
    
    return db_name


def get_org_database_url(org_name: str):
    db_name = f"{settings.org_db_prefix}{org_name.lower().replace(' ', '_')}"
    return (
        f"postgresql://{settings.database_user}:{settings.database_password}"
        f"@{settings.database_host}:{settings.database_port}/{db_name}"
    )


def get_org_engine(org_name: str):
    db_url = get_org_database_url(org_name)
    return create_engine(db_url)