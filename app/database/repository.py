from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from typing import Any
from sqlalchemy.orm import Session

from .connection import get_session
from .models import Article, DailyDigest, Source, Subscriber


class Repository:
    def __init__(self, session: Session | None = None):
        self.session = session or get_session()

    def upsert_source(self, source: dict[str, Any]) -> Source:
        existing = self.session.query(Source).filter_by(id=source["id"]).first()
        if existing:
            existing.name = source["name"]
            existing.url = source["url"]
            existing.rss_url = source.get("rss_url")
            existing.channel_id = source.get("channel_id")
            existing.source_type = source["source_type"]
            existing.is_active = source.get("is_active", True)
            self.session.commit()
            return existing

        model = Source(**source)
        self.session.add(model)
        self.session.commit()
        return model
    
    def upsert_article(self, article: dict[str, Any]) -> Article:
        existing = self.session.query(Article).filter_by(id=article["id"]).first()
        if existing:
            existing.raw_content = article.get("raw_content")
            existing.extracted_content = article.get("extracted_content")
            self.session.commit()
            return existing
        model = Article(**article)
        self.session.add(model)
        self.session.commit()
        return model

    def get_articles_for_period(self, hours: int = 24) -> list[Article]:
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=hours)
        return (
            self.session.query(Article)
            .filter(Article.published_at >= cutoff)
            .order_by(Article.published_at.desc())
            .all()
        )

    def get_articles_without_summary(self, limit: int | None = None) -> list[Article]:
        query = (
            self.session.query(Article)
            .filter(Article.summary_status != "completed")
            .order_by(Article.published_at.desc())
        )
        if limit:
            query = query.limit(limit)
        return query.all()

    def set_article_summary(self, article_id: str, summary: str) -> None:
        article = self.session.query(Article).filter_by(id=article_id).first()
        if not article:
            return
        article.summary = summary
        article.summary_status = "completed"
        self.session.commit()

    def create_or_update_daily_digest(
        self,
        digest_date: date,
        period_hours: int,
        title: str,
        summary: str,
        email_sent_to: str | None = None,
    ) -> DailyDigest:
        digest = self.session.query(DailyDigest).filter_by(digest_date=digest_date).first()
        if digest:
            digest.summary = summary
            digest.title = title
            digest.period_hours = str(period_hours)
            if email_sent_to:
                digest.email_sent_to = email_sent_to
            self.session.commit()
            return digest

        digest = DailyDigest(
            id=f"digest:{digest_date.isoformat()}",
            digest_date=digest_date,
            period_hours=str(period_hours),
            title=title,
            summary=summary,
            email_sent_to=email_sent_to,
        )
        self.session.add(digest)
        self.session.commit()
        return digest

    def get_recent_digests(self, days: int = 7) -> list[DailyDigest]:
        cutoff = date.today() - timedelta(days=days)
        return (
            self.session.query(DailyDigest)
            .filter(DailyDigest.digest_date >= cutoff)
            .order_by(DailyDigest.digest_date.desc())
            .all()
        )

    def get_recent_articles(self, limit: int = 200) -> list[Article]:
        return (
            self.session.query(Article)
            .order_by(Article.published_at.desc())
            .limit(limit)
            .all()
        )

    def subscribe_user(self, name: str, email: str) -> Subscriber:
        existing = self.session.query(Subscriber).filter_by(email=email).first()
        if existing:
            existing.name = name
            existing.is_active = True
            self.session.commit()
            return existing

        subscriber = Subscriber(
            id=f"subscriber:{email.lower()}",
            name=name,
            email=email.lower(),
            is_active=True,
        )
        self.session.add(subscriber)
        self.session.commit()
        return subscriber

    def unsubscribe_user(self, email: str) -> bool:
        existing = self.session.query(Subscriber).filter_by(email=email.lower()).first()
        if not existing:
            return False
        existing.is_active = False
        self.session.commit()
        return True

    def get_active_subscribers(self) -> list[Subscriber]:
        return (
            self.session.query(Subscriber)
            .filter(Subscriber.is_active.is_(True))
            .order_by(Subscriber.created_at.desc())
            .all()
        )