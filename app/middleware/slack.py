from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from settings import settings


class Slack:
    client_web: WebClient

    def __init__(self):
        self.client = WebClient(token=settings.slack_bot_token)

    def post_message(self):
        text = "テスト投稿"
        try:
            self.client.chat_postMessage(
                channel=settings.slack_channel_id,
                text=text,
            )

        except SlackApiError as e:
            print(f"Error posting message: {e}")
