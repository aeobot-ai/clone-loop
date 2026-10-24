"""Network adapters. i-boss sits behind Cloudflare, which answers plain requests with 403, so it goes through Firecrawl."""

from __future__ import annotations

import os
import time

import requests

FIRECRAWL = "https://api.firecrawl.dev/v2/scrape"
RETRIES = 4
UA = {"User-Agent": "Mozilla/5.0 (clone-loop; +https://aeobot.ai)"}


def scrape(url: str) -> str:
    for attempt in range(RETRIES):
        r = requests.post(
            FIRECRAWL,
            headers={"Authorization": f"Bearer {os.environ['FIRECRAWL_API_KEY']}"},
            json={"url": url, "formats": ["markdown"], "onlyMainContent": False, "maxAge": 0},
            timeout=90,
        )
        if r.status_code != 429 or attempt == RETRIES - 1:
            break
        time.sleep(15 * (attempt + 1))  # rate limited: back off and retry
    r.raise_for_status()
    body = r.json()
    if not body.get("success"):
        raise RuntimeError(f"firecrawl: {body.get('error', 'failed')}")
    return body["data"]["markdown"]


def get(url: str) -> str:
    r = requests.get(url, headers=UA, timeout=30)
    r.raise_for_status()
    return r.text
