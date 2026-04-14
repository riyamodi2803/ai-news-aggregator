from pathlib import Path

from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.daily_runner import run_daily_pipeline
from app.database.create_tables import create_all_tables
from app.database.repository import Repository
from app.email.sender import build_welcome_email, send_email

app = FastAPI(title="AI News Aggregator")
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.on_event("startup")
def startup() -> None:
    create_all_tables()


@app.get("/")
def root() -> RedirectResponse:
    return RedirectResponse(url="/dashboard")


@app.get("/dashboard")
def dashboard(request: Request):
    repo = Repository()
    digests = repo.get_recent_digests(days=14)
    articles = repo.get_recent_articles(limit=100)
    subscribers = repo.get_active_subscribers()
    message = request.query_params.get("message", "")
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "digests": digests,
            "articles": articles,
            "subscribers": subscribers,
            "message": message,
        },
    )


@app.post("/run-daily")
def run_daily():
    return run_daily_pipeline(hours=24, top_n=10)


@app.post("/subscribe")
def subscribe(name: str = Form(...), email: str = Form(...)):
    repo = Repository()
    clean_name = name.strip()
    clean_email = email.strip().lower()
    repo.subscribe_user(name=clean_name, email=clean_email)
    subject, body = build_welcome_email(clean_name, clean_email)
    send_email(subject=subject, body=body, recipients=[clean_email])
    return RedirectResponse(url="/dashboard?message=Subscribed+successfully", status_code=303)


@app.post("/unsubscribe")
def unsubscribe(email: str = Form(...)):
    repo = Repository()
    repo.unsubscribe_user(email=email.strip().lower())
    return RedirectResponse(url="/dashboard?message=Unsubscribed+successfully", status_code=303)


@app.get("/unsubscribe")
def unsubscribe_link(email: str):
    repo = Repository()
    repo.unsubscribe_user(email=email.strip().lower())
    return RedirectResponse(url="/dashboard?message=Unsubscribed+successfully", status_code=303)