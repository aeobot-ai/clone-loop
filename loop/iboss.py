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
    r"\|[^|]*\|\s*\*{0,2}(?P<date>[\d.:]+)\*{0,2}\s*\|\s*(?P<views>[\d,]+)\s*\|\s*(?P<likes>[\d,]+)\s*\|",
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


@dataclass(frozen=True)
class LeadCard:
    title: str
    url: str
    summary: str
    closed: bool
    budget: str
    industry: str
    date: str


_CARD = re.compile(
    r"\[(?P<closed>_\\\[마감\\\]_ )?(?P<title>[^\[\]\\]+?)\\\\\n\\\\\n(?P<summary>[^\]]*)\]"
    r"\((?P<url>https://www\.i-boss\.co\.kr/ab-1958-\d+)\)"
    r"(?:\s*\n\s*\[[^\]]+\]\([^)]+\) 예산 _(?P<budget>[^_]*)_업종 _(?P<industry>[^_]*)_등록일 _(?P<date>[^_]*)_)?",
)


def parse_lead_cards(md: str) -> list[LeadCard]:
    return [
        LeadCard(m["title"].strip(), m["url"], m["summary"].strip(), bool(m["closed"]),
                 m["budget"] or "", m["industry"] or "", m["date"] or "")
        for m in _CARD.finditer(md)
    ]


def post_body(md: str) -> str:
    """Firecrawl's full-page markdown starts with ~10 KB of site menu; return from the post's own heading."""
    i = md.find("\n조회수 ")
    start = md.rfind("\n# ", 0, i) if i > 0 else md.find("\n# ")
    return md[start + 1:] if start >= 0 else md
