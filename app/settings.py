from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ENV
    env: str = Field(default="")

    # Slack
    slack_bot_token: str = Field(default="")
    slack_channel_id: str = Field(default="")


settings = Settings()
