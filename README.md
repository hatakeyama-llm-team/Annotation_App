# Annotation_App
LLM学習データのノイズ判定器学習用のアノテーションデータの作成するアプリ

# 使い方
1. poetry install
2. poetry shell
3. streamlit run login.py

# 事前設定
.streamlit/secrets.tomlを作成する。

環境変数を設定する。
必要な値は以下の通り。
```
COGNITO_DOMAIN="
CLIENT_ID=""
CLIENT_SECRET=""
APP_URI="http://localhost:8501/"