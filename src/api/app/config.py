from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    cosmos_endpoint: str
    cosmos_key: str
    cosmos_database: str = "cloudnotes"
    cosmos_container: str = "notes"
    blob_connection_string: str
    blob_container: str = "attachments"

    class Config:
        env_file = ".env"

settings = Settings()
