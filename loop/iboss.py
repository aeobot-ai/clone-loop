"""Parse i-boss pages as Firecrawl returns them (markdown)."""

from __future__ import annotations

import re
from dataclasses import dataclass

KEYWORDS = (
    "AEO", "GEO", "AI 검색", "AI 브리핑", "챗GPT", "ChatGPT", "제미나이", "Gemini",
    "퍼플렉시티", "Perplexity", "블로그 노출", "통검", "블탭", "상위노출", "SEO", "검색최적화",
)


@dataclass(frozen=True)
class PostStats:
    views: int
    likes: int
    comments: int


@dataclass(frozen=True)
class BoardRow:
    title: str
    url: str
    date: str
    views: int
    likes: int
    comments: int


def _int(s: str) -> int:
    return int(s.replace(",", ""))


def parse_post_stats(md: str) -> PostStats | None:
    found = {}
    for label in ("조회수", "좋아요", "댓글"):
        m = re.search(rf"^{label}\s+([\d,]+)\s*$", md, re.M)
        if not m:
            return None
        found[label] = _int(m.group(1))
    return PostStats(found["조회수"], found["좋아요"], found["댓글"])


_ROW = re.compile(
    r"^\|[^|\[]*\[(?P<title>[^\]]+)\]\((?P<url>https://www\.i-boss\.co\.kr/ab-[\d-]+)[^)]*\)\s*(?P<cmt>[\d,]*)\s*"
    r"\|[^|]*\|\s*(?P<date>[\d.]+)\s*\|\s*(?P<views>[\d,]+)\s*\|\s*(?P<likes>[\d,]+)\s*\|",
    re.M,
)


def parse_board_rows(md: str) -> list[BoardRow]:
    return [
        BoardRow(m["title"].strip(), m["url"], m["date"], _int(m["views"]), _int(m["likes"]), _int(m["cmt"] or "0"))
        for m in _ROW.finditer(md)
    ]


def is_relevant(title: str) -> bool:
    t = title.lower()
    return any(k.lower() in t for k in KEYWORDS)
