from datetime import datetime
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Source(Base):
    __tablename__ = "sources"

    id = Column(String, primary_key=True)
    source_type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    url = Column(String, nullable=False)
    rss_url = Column(String, nullable=True)
    channel_id = Column(String, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    articles = relationship("Article", back_populates="source")


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True)
    source_id = Column(String, ForeignKey("sources.id"), nullable=False)
    published_at = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    external_id = Column(String, nullable=True)
    raw_content = Column(Text, nullable=True)
    extracted_content = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    summary_status = Column(String, nullable=False, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    source = relationship("Source", back_populates="articles")


class DailyDigest(Base):
    __tablename__ = "digests"

    id = Column(String, primary_key=True)
    digest_date = Column(Date, nullable=False, unique=True)
    period_hours = Column(String, nullable=False)
    title = Column(String, nullable=False)
    summary = Column(Text, nullable=False)
    email_sent_to = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

