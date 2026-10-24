import requests

from loop import web


class Resp:
    def __init__(self, status, body=None):
        self.status_code, self._body = status, body or {}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code}")

    def json(self):
        return self._body


def test_scrape_retries_429(monkeypatch):
    calls = []

    def post(*a, **k):
        calls.append(1)
        return Resp(429) if len(calls) < 3 else Resp(200, {"success": True, "data": {"markdown": "ok"}})

    monkeypatch.setenv("FIRECRAWL_API_KEY", "x")
    monkeypatch.setattr(web.requests, "post", post)
    monkeypatch.setattr(web.time, "sleep", lambda s: None)
    assert web.scrape("https://e.com") == "ok"
    assert len(calls) == 3
