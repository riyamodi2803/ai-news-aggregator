import requests
from bs4 import BeautifulSoup


def fetch_page_context(url: str) -> tuple[str, str]:
    response = requests.get(url, timeout=20)
    response.raise_for_status()
    raw_html = response.text
    soup = BeautifulSoup(raw_html, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    return raw_html, text[:15000]
