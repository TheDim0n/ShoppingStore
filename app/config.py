from pydantic import BaseSettings


class Settings(BaseSettings):
    # database settings
    database_url: str

    # main app settings
    debug: bool = False
    secret_key: str
    access_token_expires_minutes: int
    refresh_token_expires_days: int
    initial_user_username: str
    initial_user_password: str
    cors_origins: str = ""

    # proxy settings
    root_path: str = ''

    class Config:
        env_file = ".env"
