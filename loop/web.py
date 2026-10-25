"""Network adapters. i-boss sits behind Cloudflare, which answers plain HTTP clients (and datacenter IPs)
with 403; a Chrome TLS fingerprint from a home connection gets through. Where that is still blocked
(cloud runners, a cluster), Firecrawl's proxies fetch the same raw HTML if FIRECRAWL_API_KEY is set."""

from __future__ import annotations

import os
import time

import requests
from curl_cffi import requests as cffi

FIRECRAWL = "https://api.firecrawl.dev/v2/scrape"
RETRIES = 4
UA = {"User-Agent": "Mozilla/5.0 (clone-loop; +https://aeobot.ai)"}


def scrape(url: str) -> str:
    for attempt in range(RETRIES):
        r = cffi.get(url, impersonate="chrome", timeout=30)
        if r.status_code not in (429, 503) or attempt == RETRIES - 1:
            break
        time.sleep(15 * (attempt + 1))  # rate limited: back off and retry
    if r.status_code == 403 and os.environ.get("FIRECRAWL_API_KEY"):
        return firecrawl_html(url)
    r.raise_for_status()
    return r.text


def firecrawl_html(url: str) -> str:
    """Same page as the browser sees it, fetched through Firecrawl's proxies (costs a credit)."""
    for attempt in range(RETRIES):
        r = requests.post(
            FIRECRAWL,
            headers={"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"},
            json={"url": url, "formats": ["rawHtml"], "maxAge": 0},
            timeout=90,
        )
        if r.status_code != 429 or attempt == RETRIES - 1:
            break
        time.sleep(15 * (attempt + 1))
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"firecrawl: {body.get('error', 'failed')}")
    return body["data"]["rawHtml"]


def get(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return r.text
