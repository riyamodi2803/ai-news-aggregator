# AI News Aggregator MVP

Python backend + server-rendered dashboard that ingests AI news daily from YouTube and blog/RSS sources, stores in PostgreSQL, summarizes with OpenAI, and generates a daily digest.

## Features

- Unified schema: `sources`, `articles`, `digests`
- Daily ingestion pipeline for OpenAI, Anthropic, and YouTube RSS sources
- Full-page context capture (`raw_content`) + extracted text (`extracted_content`)
- Per-article OpenAI summaries and daily digest generation
- Dashboard with historical digests and article list
- Gmail SMTP digest email support

## Quick Start

1. Install dependencies:

```bash
uv sync
```

2. Configure environment (`.env`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=admin
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=news_db

OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o-mini

SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_gmail_app_password
DIGEST_EMAIL_TO=your_email@gmail.com
```

3. Start PostgreSQL:

```bash
docker compose -f docker/postgres/docker-compose.yml up -d
```

4. Run one daily pipeline:

```bash
python main.py
```

5. Start dashboard:

```bash
uvicorn app.web.server:app --reload
```

Open `http://127.0.0.1:8000/dashboard`.
