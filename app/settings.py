from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ENV
    env: str = Field(default="")

    # Slack
    slack_webhook_url: str = Field(default="")


settings = Settings()
