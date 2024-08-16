from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    discord_token: str

    class Config:
        env_prefix = 'M_'


settings = Settings()
