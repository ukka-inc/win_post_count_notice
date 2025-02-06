import datetime

from repositories.time_management import gen_time_schedule
from settings import settings
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError


class Slack:
    client_web: WebClient

    def __init__(self):
        self.client = WebClient(token=settings.slack_bot_token)

    def _gen_now_datetime(self) -> datetime.datetime:
        return datetime.datetime.now()

    def _gen_unix_time(self) -> float:
        now = self._gen_now_datetime()
        modified_time = now.replace(hour=19, minute=0, second=0, microsecond=0)
        seven_days_ago = modified_time - datetime.timedelta(days=7)
        return seven_days_ago.timestamp()

    def _gen_opening_message(self, win_count: int) -> str:
        if win_count >= 20:
            return """
:fireworks: :fireworks: :fireworks: :fireworks: :fireworks: :fireworks: :fireworks: :fireworks: :fireworks: :fireworks:

お疲れ様でした！！！！！
"""

        if 10 <= win_count < 20:
            return """
:ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon: :ukaemon:

お疲れ様でした！！！
"""

        if win_count < 10:
            return "お疲れ様でした！"

    def _gen_post_message(self, win_count: int) -> str:
        opening_message = self._gen_opening_message(win_count=win_count)
        now = self._gen_now_datetime()
        now_date = now.strftime("%Y/%m/%d")
        seven_days_ago = now - datetime.timedelta(days=7)
        seven_days_ago_date = seven_days_ago.strftime("%Y/%m/%d")
        time_management = gen_time_schedule(post_count=win_count)

        if not time_management:
            return f"{opening_message}{seven_days_ago_date}から{now_date}の :congratulations: はありませんでした :sob:"

        return f"""
{opening_message}

今週も :tokiwakita:
{seven_days_ago_date}から{now_date}の :congratulations: は *{win_count}件* でした！！！

1投稿あたりの共有目安時間は、{time_management['minutes']}分 {time_management['seconds']}秒です！！！

18:00からのwin-session盛り上がっていきましょう :kinnikun_power:

本投稿後以降の駆け込みwinはカウントから除きますmm
"""

    def fetch_post_history(self) -> list[str]:
        unix_seven_days_ago = self._gen_unix_time()

        try:
            response = self.client.conversations_history(
                oldest=unix_seven_days_ago,
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
