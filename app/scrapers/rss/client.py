from datetime import datetime
import feedparser


def parse_feed(rss_url: str, source_id: str) -> list[dict]:
    feed = feedparser.parse(rss_url)
    entries = []
    for entry in feed.entries:
        published = getattr(entry, "published_parsed", None)
        if not published:
            continue
        published_at = datetime(*published[:6])
        link = entry.get("link", "")
        external_id = entry.get("id", link)
        entries.append(
            {
                "id": f"{source_id}:{external_id}",
                "source_id": source_id,
                "external_id": external_id,
                "title": entry.get("title", "Untitled"),
                "url": link,
                "published_at": published_at,
                "raw_content": entry.get("summary", ""),
            }
        )
    return entries
