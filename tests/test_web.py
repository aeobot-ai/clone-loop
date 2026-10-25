from loop import web


class Resp:
    def __init__(self, status, text=""):
        self.status_code, self.text = status, text

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


def test_scrape_uses_chrome_fingerprint_and_retries_rate_limits(monkeypatch):
    calls = []

    def get(url, **kw):
        calls.append(kw)
        return Resp(429) if len(calls) < 3 else Resp(200, "<html>ok</html>")

    monkeypatch.setattr(web.cffi, "get", get)
    monkeypatch.setattr(web.time, "sleep", lambda s: None)
    assert web.scrape("https://www.i-boss.co.kr/ab-1") == "<html>ok</html>"
    assert len(calls) == 3
    assert calls[0]["impersonate"] == "chrome"


def test_scrape_raises_on_block(monkeypatch):
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    monkeypatch.setattr(web.cffi, "get", lambda url, **kw: Resp(403))
    monkeypatch.setattr(web.time, "sleep", lambda s: None)
    try:
        web.scrape("https://www.i-boss.co.kr/ab-1")
    except RuntimeError as e:
        assert "403" in str(e)
    else:
        raise AssertionError("expected a 403 error")


def test_blocked_request_falls_back_to_firecrawl_raw_html(monkeypatch):
    monkeypatch.setattr(web.cffi, "get", lambda url, **kw: Resp(403))
    monkeypatch.setattr(web.time, "sleep", lambda s: None)
    monkeypatch.setenv("FIRECRAWL_API_KEY", "fc-test")
    sent = {}

    class FC:
        status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return {"success": True, "data": {"rawHtml": "<html>via firecrawl</html>"}}

    def post(url, **kw):
        sent.update(kw["json"])
        return FC()

    monkeypatch.setattr(web.requests, "post", post)
    assert web.scrape("https://www.i-boss.co.kr/ab-1") == "<html>via firecrawl</html>"
    assert sent["formats"] == ["rawHtml"]


def test_no_firecrawl_key_keeps_the_block_error(monkeypatch):
    monkeypatch.setattr(web.cffi, "get", lambda url, **kw: Resp(403))
    monkeypatch.setattr(web.time, "sleep", lambda s: None)
    monkeypatch.delenv("FIRECRAWL_API_KEY", raising=False)
    try:
        web.scrape("https://www.i-boss.co.kr/ab-1")
    except RuntimeError as e:
        assert "403" in str(e)
    else:
        raise AssertionError("expected a 403 error")
