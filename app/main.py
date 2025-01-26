from settings import settings
from middleware.slack import Slack


def main():
    # 初期化
    slack_client = Slack()

    slack_client.post_message()


if __name__ == "__main__":
    main()
