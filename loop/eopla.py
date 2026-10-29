"""Parse EO planet (eopla.net) pages. Magazine pages show likes and comments but no view count;
the home page's "오늘 많이 본 아티클" ranking is the only public signal of views."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE = "https://eopla.net/"
HOME = BASE


@dataclass(frozen=True)
class MagazineStats:
    likes: int
    comments: int


def is_eopla(url: str) -> bool:
    return url.startswith(BASE)


def _int(node) -> int | None:
    digits = re.sub(r"[^\d]", "", node.get_text()) if node else ""
    return int(digits) if digits else None


def parse_magazine_stats(html: str, url: str) -> MagazineStats | None:
    soup = BeautifulSoup(html, "html.parser")
    serial = url.rstrip("/").rsplit("/", 1)[-1]
    likes = _int(soup.select_one(f"button.magazine-like[data-likable-id='{serial}'] .like-count"))
    comments = _int(soup.select_one(".comments-section .comments-count"))
    if likes is None or comments is None:
        return None
    return MagazineStats(likes, comments)


def parse_popular(html: str) -> list[str]:
    """Magazine URLs in "오늘 많이 본 아티클" order (rank 1 first)."""
    box = BeautifulSoup(html, "html.parser").select_one(".popular-article-container")
    if box is None:
        return []
    ranked = []
    for item in box.select(".magazine-container"):
        number, link = item.select_one(".number"), item.select_one("a[href^='/magazines/']")
        if number and link:
            ranked.append((_int(number), urljoin(BASE, link["href"])))
    return [u for _, u in sorted(ranked)]
