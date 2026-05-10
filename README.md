# Physics App Backend

物理添削AIサービスのバックエンドAPIです。

## 技術スタック

- **FastAPI** - WebAPIフレームワーク
- **MySQL** - データベース（Docker）
- **SQLAlchemy** - ORM
- **Poetry** - パッケージ管理
- **Claude API** - AI回答生成
- **ChromaDB** - ベクトルDB
- **sentence-transformers** - テキストのベクトル化

## サービス概要

生徒が物理の問題を投稿すると、RAGを用いてAIが自分の物理教材を参照しながら一次回答を生成します。AIで解決しない場合は講師が対応する非同期型の物理添削サービスです。

## セットアップ

### 前提条件

- WSL2 / Ubuntu
- Docker Desktop
- Poetry

### 環境変数

`.env.example` をコピーして `.env` を作成してください：

```bash
cp .env.example .env
```

`.env` に以下を設定してください：
DATABASE_URL=mysql+pymysql://physics_user:physics_password@localhost:3306/physics_app
ANTHROPIC_API_KEY=your_api_key
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_DATABASE=physics_app
MYSQL_USER=physics_user
MYSQL_PASSWORD=physics_password

### 起動方法

```bash
# MySQLを起動
docker compose up -d

# 依存パッケージをインストール
poetry install

# 教材をベクトルDBに登録
poetry run python scripts/index_documents.py

# サーバーを起動
poetry run uvicorn app.main:app --reload
```

## APIエンドポイント

| メソッド | URL | 説明 |
|------|------|------|
| POST | /auth/register | ユーザー登録 |
| POST | /auth/login | ログイン（JWT発行） |
| POST | /auth/questions | 問題投稿（AI回答自動生成） |
| GET | /auth/questions | 問題一覧取得 |

## 詰まったポイント

### 1. bcryptとpasslibの互換性エラー
bcrypt 5.x系はpasslibと互換性がないため、bcrypt 4.0.1に固定することで解決。

```bash
poetry add "bcrypt==4.0.1"
```

### 2. GitHubへのpushが拒否された
リポジトリ作成時にLICENSEファイルが追加されたため、ローカルとリモートの履歴が異なり競合が発生。以下で解決：

```bash
git pull --rebase origin main --allow-unrelated-histories
git push -u origin main
```

### 3. Dockerビルド時のPoetryエラー
Poetry 2.x系では `--no-dev` オプションが廃止され `--only main --no-root` に変更。

```bash
poetry install --only main --no-root
```