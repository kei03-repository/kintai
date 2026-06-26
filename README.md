# 勤怠管理アプリ

## 構成

- `backend/`: FastAPI バックエンド
- `frontend/`: Vite + React + TypeScript フロントエンド
- `db/attendance.db`: SQLite データベース
- `業務進捗報告_島.xlsx`: Excel テンプレート（`backend/` 隣に配置）

## バックエンドの起動

1. Python 環境を準備する
2. 依存関係をインストールする

```bash
cd "c:\Users\20013\OneDrive\デスクトップ\開発App"
python -m pip install -r backend/requirements.txt
```

Windows 環境で `python` がない場合：

```powershell
cd "c:\Users\20013\OneDrive\デスクトップ\開発App"
& "C:\Users\20013\AppData\Local\Programs\Python\Python313\python.exe" -m pip install -r backend/requirements.txt
```

3. サーバーを起動する

```bash
cd "c:\Users\20013\OneDrive\デスクトップ\開発App\backend"
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Windows 環境で `python` がない場合：

```
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

バックエンド API は `http://localhost:8000/api` で利用できます。

## フロントエンドの起動

1. `frontend` に移動して依存関係をインストールする

```bash
cd "c:\Users\20013\OneDrive\デスクトップ\開発App\frontend"
npm install
```

2. 開発サーバーを起動する

Windows 環境では次のコマンドで起動します（`npm` が PATH に無い場合）。

```
`npm run dev` が使えます。
```

3. ブラウザで `http://localhost:5173` を開きます。

## 動作確認

1. フロントエンドから勤怠入力を保存する
2. 月一覧が表示される
3. `Excel 出力` ボタンでバックエンドが `excel_output` にコピー済みファイルを作成し、ダウンロードする

## Docker 3コンテナ構成（frontend / backend / db）

このリポジトリには以下の Docker ファイルを追加済みです。

- `docker-compose.yml`
- `backend/Dockerfile`
- `frontend/Dockerfile`
- `frontend/nginx.conf`
- `.env.example`

### 1. 環境変数ファイルを作る

```powershell
cd "c:\Users\20013\OneDrive\デスクトップ\kintai"
copy .env.example .env
```

必要に応じて `.env` の値（特に `POSTGRES_PASSWORD`）を変更します。

S3 のテンプレートを使う場合は、`.env` に `TEMPLATE_SOURCE` を設定します。

```env
TEMPLATE_SOURCE=arn:aws:s3:::dev--kintai--s3-709147558067-ap-northeast-1-an/業務進捗報告_島.xlsx
AWS_REGION=ap-northeast-1
```

`backend` は `TEMPLATE_SOURCE` が `arn:aws:s3:::` または `s3://` のとき、S3 からテンプレートをダウンロードしてから Excel を出力します。

必要な権限（IAM）:

- `s3:GetObject`（対象キー）
- 必要なら `s3:ListBucket`（運用ポリシー次第）

ローカル Docker Compose で IAM ロールを使えない場合は、`.env` に `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY`（必要なら `AWS_SESSION_TOKEN`）を設定してください。

### 環境変数ファイルを安全に使うポイント

1. `.env` は Git にコミットしない（このリポジトリでは `.gitignore` で除外済み）。
2. 共有は `.env.example` のみ使う（本番値や実パスワードは書かない）。
3. 強い秘密情報を使う（`POSTGRES_PASSWORD` は長くランダムにする）。
4. 値をログ出力しない（`echo` やデバッグログに秘密情報を出さない）。
5. 定期ローテーションする（漏えい疑いがあれば即再発行）。

PowerShell でランダム文字列を作る例:

```powershell
[Convert]::ToBase64String((1..48 | ForEach-Object {Get-Random -Maximum 256} | ForEach-Object {[byte]$_}))
```

誤って `.env` をコミットした場合の初動:

1. その値を即無効化（DBパスワード変更、キー再発行）
2. Git 履歴から削除（`git filter-repo` など）
3. 影響範囲を確認（CIログ、共有チャット、成果物）

### 2. 3コンテナを起動する

```powershell
docker compose up -d --build
```

アクセス先:

- frontend: `http://localhost:5173`
- backend(OpenAPI): `http://localhost:8000/docs`
- db(PostgreSQL): `localhost:5432`

停止:

```powershell
docker compose down
```

DBデータも削除する場合:

```powershell
docker compose down -v
```

## DockerHub にイメージを push

以下ではタグに例として `v1.0.0` を使用します。

```powershell
cd "c:\Users\20013\OneDrive\デスクトップ\kintai"
$TAG="v1.0.0"
$DOCKERHUB_USER="<your-dockerhub-user>"

docker login

docker build -f backend/Dockerfile -t $DOCKERHUB_USER/kintai-backend:$TAG .
docker build -f frontend/Dockerfile -t $DOCKERHUB_USER/kintai-frontend:$TAG .

docker push $DOCKERHUB_USER/kintai-backend:$TAG
docker push $DOCKERHUB_USER/kintai-frontend:$TAG
```

### リリース手順（version + latest 同時更新）

このプロジェクトは compose 側で以下のイメージ名を使います。

- `kintai/backend:${IMAGE_TAG:-latest}`
- `kintai/frontend:${IMAGE_TAG:-latest}`

運用ルール:

- `version` タグ（例: `v1.0.0`）は不変
- `latest` タグは最新リリースに更新

PowerShell 実行例:

```powershell
cd "c:\Users\20013\OneDrive\デスクトップ\kintai"
$VERSION="v1.0.0"

# 1) version タグでビルド
$env:IMAGE_TAG=$VERSION
docker compose build backend frontend

# 2) latest タグを同じ内容で更新
docker tag kintai/backend:$VERSION kintai/backend:latest
docker tag kintai/frontend:$VERSION kintai/frontend:latest

# 3) push（version と latest の両方）
docker push kintai/backend:$VERSION
docker push kintai/backend:latest
docker push kintai/frontend:$VERSION
docker push kintai/frontend:latest
```

補足:

- `docker compose build` はローカルでビルドを実行します（`docker build` を個別に2回書かなくてよいだけ）。
- 完全自動化したい場合は GitHub Actions などの CI で上記手順を実行します。
- `.env` の `IMAGE_TAG` は具体値を設定してください（例: `IMAGE_TAG=v1.0.0`）。`IMAGE_TAG=$VERSION` のような変数参照は Compose で展開されず、`VERSION variable is not set` 警告の原因になります。
- 現在の backend イメージは S3 テンプレート運用を前提に、ビルド時にローカルの `業務進捗報告_島.xlsx` を必須にしていません。ローカルファイル運用をする場合は、`TEMPLATE_SOURCE` をコンテナ内に存在するパスへ設定してください。

## DockerHub イメージを AWS ECR に push

前提: AWS CLI が設定済みで、ECR リポジトリ（例: `kintai-backend`, `kintai-frontend`）が作成済み。

```powershell
$AWS_REGION="ap-northeast-1"
$AWS_ACCOUNT_ID="123456789012"
$TAG="v1.0.0"
$DOCKERHUB_USER="<your-dockerhub-user>"

$ECR_BASE="$AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com"

aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_BASE

docker pull $DOCKERHUB_USER/kintai-backend:$TAG
docker pull $DOCKERHUB_USER/kintai-frontend:$TAG

docker tag $DOCKERHUB_USER/kintai-backend:$TAG $ECR_BASE/kintai-backend:$TAG
docker tag $DOCKERHUB_USER/kintai-frontend:$TAG $ECR_BASE/kintai-frontend:$TAG

docker push $ECR_BASE/kintai-backend:$TAG
docker push $ECR_BASE/kintai-frontend:$TAG
```

補足:

- `db` は `postgres:16-alpine` を利用しているため、通常は ECR へ push せずそのまま利用可能です。
- もし `db` も独自イメージ化したい場合は、`db/Dockerfile` を作成して同様に build/tag/push してください。
