from app.database.create_tables import create_all_tables
from app.database.repository import Repository
from app.digest.service import build_daily_digest
from app.email.sender import send_email
from app.ingest.pipeline import run_ingestion
from app.llm.summarizer import summarize_article
from app.settings import settings


def _build_digest_email_body(subscriber_name: str, subscriber_email: str, articles: list, hours: int) -> str:
    base = settings.app_base_url.rstrip("/")
    unsubscribe_url = f"{base}/unsubscribe?email={subscriber_email}"
    lines = [
        f"Hi {subscriber_name},",
        "",
        f"Here is your AI digest for the last {hours} hours:",
        "",
    ]
    for idx, article in enumerate(articles, 1):
        lines.append(f"{idx}. {article.title}")
        lines.append(f"   Date: {article.published_at}")
        lines.append(f"   Summary: {article.summary or 'Summary pending'}")
        lines.append(f"   Link: {article.url}")
        lines.append("")
    lines.append(f"Unsubscribe: {unsubscribe_url}")
    return "\n".join(lines)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    create_all_tables()
    repo = Repository()

    ingest_result = run_ingestion(hours=hours)
    for article in repo.get_articles_without_summary(limit=200):
        content = article.extracted_content or article.raw_content or article.title
        summary = summarize_article(article.title, content)
        repo.set_article_summary(article.id, summary)

    digest = build_daily_digest(hours=hours)
    recent_articles = repo.get_articles_for_period(hours=hours)[:top_n]
    subscribers = repo.get_active_subscribers()
    email_sent_count = 0
    for subscriber in subscribers:
        body = _build_digest_email_body(
            subscriber_name=subscriber.name,
            subscriber_email=subscriber.email,
            articles=recent_articles,
            hours=hours,
        )
        if send_email(
            subject=f"AI Daily Digest (last {hours}h)",
            body=body,
            recipients=[subscriber.email],
        ):
            email_sent_count += 1

    if not subscribers and settings.digest_email_to:
        fallback_body = _build_digest_email_body(
            subscriber_name="there",
            subscriber_email=settings.digest_email_to,
            articles=recent_articles,
            hours=hours,
        )
        if send_email(
            subject=f"AI Daily Digest (last {hours}h)",
            body=fallback_body,
            recipients=[settings.digest_email_to],
        ):
            email_sent_count = 1

    return {
        "success": True,
        "ingestion": ingest_result,
        "digest_id": digest["id"],
        "email_sent": email_sent_count > 0,
        "recipient_count": max(len(subscribers), 1 if settings.digest_email_to and not subscribers else 0),
        "email_sent_count": email_sent_count,
        "top_n": top_n,
    }


if __name__ == "__main__":
    run_daily_pipeline(hours=24, top_n=10)
