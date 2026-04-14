from datetime import date

from app.database.repository import Repository
from app.llm.summarizer import summarize_daily_digest


def build_daily_digest(hours: int = 24) -> dict:
    repo = Repository()
    articles = repo.get_articles_for_period(hours=hours)
    if not articles:
        summary = "No new articles were found in the selected time window."
    else:
        items = []
        for article in articles:
            item = f"- {article.title} ({article.url})\n  - {article.summary or 'Summary pending'}"
            items.append(item)
        summary = summarize_daily_digest("\n".join(items))

    digest = repo.create_or_update_daily_digest(
        digest_date=date.today(),
        period_hours=hours,
        title=f"AI Daily Digest - Last {hours}h",
        summary=summary,
    )
    return {"id": digest.id, "summary": digest.summary}
