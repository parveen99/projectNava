from pydantic_settings import BaseSettings


# Import env variables from .env file
class Settings(BaseSettings):
    master_db_url: str
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    secret_key: str 
    jwt_algorithm: str
    access_token_expire_minutes: int
    org_db_prefix: str
    
    class Config:
        env_file = ".env"


settings = Settings()