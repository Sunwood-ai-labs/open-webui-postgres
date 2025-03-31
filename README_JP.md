<div align="center">

![Image](https://github.com/user-attachments/assets/6ec3c160-a607-42ec-97b9-c47a604bbd68)

<h1>Open WebUI with PostgreSQL</h1>

<a href="README_JP.md"><img src="https://img.shields.io/badge/ドキュメント-日本語-white.svg" alt="JA doc"/></a>
<a href="README.md"><img src="https://img.shields.io/badge/english-document-white.svg" alt="EN doc"></a>

<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker"/>
<img src="https://img.shields.io/badge/OpenWebUI-FF6B6B?style=for-the-badge&logo=html5&logoColor=white" alt="Open WebUI"/>

</div>

このリポジトリは、Docker Composeを使用してOpen WebUIをPostgreSQLデータベースと連携させるための設定ファイル一式です。

## 🔧 コンポーネント

- **PostgreSQL**: Open WebUIのデータを保存するデータベースサーバー
- **Ollama**: ローカルで動作する大規模言語モデルサーバー
- **Open WebUI**: Ollamaモデルと対話するためのWebインターフェース

## 🚀 使い方

1. システムにDockerとDocker Composeがインストールされていることを確認してください。
2. 必要に応じて`docker-compose.yml`の環境変数をカスタマイズしてください。
3. 以下のコマンドを実行して、すべてのサービスを起動します：

```bash
docker-compose up -d
```

4. ブラウザで http://localhost:3000 にアクセスして、Open WebUIを使用できます。

## ⚙️ 設定

### PostgreSQL

- デフォルトユーザー: `openwebui`
- デフォルトパスワード: `openwebui`
- デフォルトデータベース: `openwebui`
- ポート: `5432` (ホストからアクセス可能)

これらの設定は`docker-compose.yml`ファイルで変更できます。初回実行後に変更する場合は、変更を適用するためにボリュームを削除する必要がある場合があります：

```bash
docker-compose down
docker volume rm open-webui-postgres_postgres-data
docker-compose up -d
```

### 🔒 セキュリティ

本番環境では以下の対策を推奨します：

1. PostgreSQLのデフォルトユーザー名とパスワードを変更する
2. `WEBUI_SECRET_KEY`を安全なランダム文字列に置き換える
3. 機密性の高い設定値については`.env`ファイルの使用を検討する

## 📦 ボリューム

- `postgres-data`: PostgreSQLデータベースファイルを保存
- `ollama-data`: Ollamaモデルと設定を保存
- `open-webui-data`: データベースに保存されないOpen WebUIデータを保存

## 🔍 トラブルシューティング

- Open WebUIがPostgreSQLに接続できない場合は、`DATABASE_URL`環境変数を確認してください。
- PostgreSQL接続の問題については、直接データベースに接続して確認できます：

```bash
docker exec -it postgres psql -U openwebui -d openwebui
```

- ログを表示するには：

```bash
docker-compose logs -f
```

## 🛠 カスタマイズ

`.env.example`ファイルを`.env`にコピーして編集することで、環境変数を簡単に設定できます：

```bash
cp .env.example .env
# .envファイルを編集してから
docker-compose up -d
```

## 📝 初期化スクリプト

`init-scripts`ディレクトリには、PostgreSQLの初回起動時に実行されるSQLスクリプトが含まれています。必要に応じてカスタムスキーマやデータを追加できます。
