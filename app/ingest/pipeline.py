from datetime import datetime, timedelta

from app.database.repository import Repository
from app.scrapers.rss.client import parse_feed
from app.scrapers.web.fetcher import fetch_page_context
from app.sources.registry import DEFAULT_SOURCES


def run_ingestion(hours: int = 24) -> dict:
    repo = Repository()
    cutoff = datetime.utcnow() - timedelta(hours=hours)
    created = 0

    for source in DEFAULT_SOURCES:
        repo.upsert_source(source)
        if not source.get("rss_url"):
            continue
        entries = parse_feed(source["rss_url"], source["id"])
        for item in entries:
            if item["published_at"] < cutoff:
                continue
            try:
                raw_html, extracted = fetch_page_context(item["url"])
            except Exception:
                raw_html = item.get("raw_content", "")
                extracted = item.get("raw_content", "")
            repo.upsert_article(
                {
                    "id": item["id"],
                    "source_id": item["source_id"],
                    "published_at": item["published_at"],
                    "title": item["title"],
                    "url": item["url"],
                    "external_id": item.get("external_id"),
                    "raw_content": raw_html,
                    "extracted_content": extracted,
                }
            )
            created += 1

    return {"created_or_updated": created}
