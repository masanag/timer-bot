# ベースイメージ
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install -r requirements.txt

# アプリケーションコードをコピー
COPY . .

# デフォルトのコマンド
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
