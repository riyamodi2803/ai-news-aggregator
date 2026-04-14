import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import settings


def send_email(subject: str, body: str, recipients: list[str]) -> bool:
    if not settings.smtp_user or not settings.smtp_password:
        return False
    recipients = [r for r in recipients if r]
    if not recipients:
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = settings.smtp_user
    msg["To"] = ", ".join(recipients)
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as smtp:
        smtp.login(settings.smtp_user, settings.smtp_password)
        smtp.sendmail(settings.smtp_user, recipients, msg.as_string())
    return True


def build_welcome_email(name: str, email: str) -> tuple[str, str]:
    unsubscribe_url = f"{settings.app_base_url.rstrip('/')}/unsubscribe?email={email}"
    subject = "Welcome to AI News Aggregator"
    body = (
        f"Hi {name},\n\n"
        "You're subscribed to AI News Aggregator.\n"
        "You will receive daily summaries with article links.\n\n"
        f"Unsubscribe anytime: {unsubscribe_url}\n"
    )
    return subject, body
