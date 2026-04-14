from openai import OpenAI

from app.agent.prompts import BASE_SYSTEM_PROMPT, USER_INSIGHTS_PROMPT, DIGEST_PROMPT_TEMPLATE
from app.settings import settings


def _client() -> OpenAI:
    return OpenAI(api_key=settings.openai_api_key)


def summarize_article(title: str, content: str) -> str:
    if not settings.openai_api_key:
        return "OpenAI key not configured. Summary unavailable."
    client = _client()
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "system", "content": USER_INSIGHTS_PROMPT},
            {"role": "user", "content": f"Title: {title}\n\nContent:\n{content[:12000]}"},
        ],
    )
    return response.output_text.strip()


def summarize_daily_digest(items_markdown: str) -> str:
    if not settings.openai_api_key:
        return items_markdown
    client = _client()
    response = client.responses.create(
        model=settings.openai_model,
        input=[
            {"role": "system", "content": BASE_SYSTEM_PROMPT},
            {"role": "system", "content": DIGEST_PROMPT_TEMPLATE},
            {"role": "user", "content": items_markdown[:20000]},
        ],
    )
    return response.output_text.strip()
