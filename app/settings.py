import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    openai_api_key = os.getenv("OPENAI_API_KEY", "")
    openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    app_base_url = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000")
    digest_email_to = os.getenv("DIGEST_EMAIL_TO", os.getenv("MY_EMAIL", ""))
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "465"))
    smtp_user = os.getenv("SMTP_USER", os.getenv("MY_EMAIL", ""))
    smtp_password = os.getenv("SMTP_PASSWORD", os.getenv("APP_PASSWORD", ""))


settings = Settings()
