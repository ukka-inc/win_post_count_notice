import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from settings import settings


class Slack:
    client_web: WebClient

    def __init__(self):
        self.client = WebClient(token=settings.slack_bot_token)

    def _gen_unix_time(self) -> float:
        now = datetime.datetime.now()
        six_days_ago = now - datetime.timedelta(days=6)
        return six_days_ago.timestamp()

    def _gen_post_message(self, win_count: int) -> str:
        now = datetime.datetime.now()
        now_date = now.strftime("%Y/%m/%d")
        six_days_ago = now - datetime.timedelta(days=6)
        six_days_ago_date = six_days_ago.strftime("%Y/%m/%d")

        return f"""
今週もお疲れ様でし！
{six_days_ago_date}から{now_date}のwin数は{win_count}件でした！
18:00からのwin-session盛り上がっていきましょう！

本投稿後以降の駆け込みwinはカウントから除きますmm
"""

    def fetch_post_history(self) -> list[str]:
        unix_6days_ago = self._gen_unix_time()

        try:
            response = self.client.conversations_history(
                oldest=unix_6days_ago,
                channel=settings.slack_channel_id,
                limit=100,
            )
            return response["messages"]

        except SlackApiError as e:
            print(f"Error fetching history: {e}")

    def post_message(self, post_history: list[str]):
        win_count = len(post_history)

        message = self._gen_post_message(win_count=win_count)

        try:
            self.client.chat_postMessage(
                channel=settings.slack_channel_id,
                text=message,
            )

        except SlackApiError as e:
            print(f"Error posting message: {e}")
