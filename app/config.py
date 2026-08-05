# app/config.py
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "InvoiceForge Microservice"
    ENVIRONMENT: str = "development"
    API_KEY: str = Field(default="dev_secret_api_key_12345", env="API_KEY")
    
    # Database
    DATABASE_URL: str = Field(
        default="postgresql+asyncpg://postgres:postgres@localhost:5432/invoicedb", 
        env="DATABASE_URL"
    )
    
    # Email Settings
    SMTP_HOST: str = Field(default="localhost", env="SMTP_HOST")
    SMTP_PORT: int = Field(default=1025, env="SMTP_PORT")
    SMTP_USER: str = Field(default="", env="SMTP_USER")
    SMTP_PASSWORD: str = Field(default="", env="SMTP_PASSWORD")
    EMAILS_FROM_EMAIL: str = Field(default="billing@company.com", env="EMAILS_FROM_EMAIL")
    
    # Storage
    STORAGE_DIR: str = "storage/invoices"

    class Config:
        env_file = ".env"

settings = Settings()
