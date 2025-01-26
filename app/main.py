from middleware.slack import Slack


def main():
    # 初期化
    slack_client = Slack()

    # 投稿取得
    post_history = slack_client.fetch_post_history()

    # カウントしたwinを通知
    slack_client.post_message(post_history)


if __name__ == "__main__":
    main()
