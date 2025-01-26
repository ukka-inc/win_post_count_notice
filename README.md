## 使用技術一覧
<img src="https://img.shields.io/badge/-Python-F2C63C.svg?logo=python&style=for-the-badge">

## プロジェクト名
win投稿カウントSlack App

## プロジェクト概要
win-sessionが始まる5分前に今週1週間分(前週土曜から今週金曜のSlack App投稿)のwin投稿数をカウントして通知するSlack App

## 環境
パッケージバージョン等は pyproject.toml と pyproject を確認してください

## 開発環境構築
### local構築
1. 当リポジトリをClone
1. プロジェクトのルートディレクトリで poetry install 実行

### 環境変数
- SLACK_BOT_TOKEN="" * Slack Appページから確認すること
- SLACK_CHANNEL_ID="" * 実行するSlackのChannel Id

### local動作確認
- make run-local