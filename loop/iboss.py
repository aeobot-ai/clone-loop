"""Parse i-boss pages from their HTML (fetched with a Chrome TLS fingerprint, see loop.web)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup

BASE = "https://www.i-boss.co.kr/"
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


@dataclass(frozen=True)
class LeadCard:
    title: str
    url: str
    summary: str
    closed: bool
    budget: str
    industry: str
    date: str


def _int(s: str) -> int:
    digits = re.sub(r"[^\d]", "", s or "")
    return int(digits) if digits else 0


def _text(node) -> str:
    return re.sub(r"\s+", " ", node.get_text(" ", strip=True)).strip() if node else ""


def _post_url(href: str) -> str:
    """'ab-6141-72783&tag=AEO+GEO' → 'https://www.i-boss.co.kr/ab-6141-72783'."""
    return urljoin(BASE, re.match(r"/?(ab-[\d-]+)", href).group(1))


def parse_post_stats(html: str) -> PostStats | None:
    state = BeautifulSoup(html, "html.parser").select_one(".article-state")
    if state is None:
        return None
    found = dict(re.findall(r"(조회수|좋아요|댓글)\s*([\d,]+)", _text(state)))
    if len(found) < 3:
        return None
    return PostStats(_int(found["조회수"]), _int(found["좋아요"]), _int(found["댓글"]))


def parse_board_rows(html: str) -> list[BoardRow]:
    rows = []
    for tr in BeautifulSoup(html, "html.parser").select("tr._t"):
        link = tr.select_one("a.mb_subject")
        if link is None or not re.match(r"/?ab-\d+-\d+", link.get("href", "")):
            continue
        rows.append(BoardRow(
            title=link.get("title") or _text(link),
            url=_post_url(link["href"]),
            date=_text(tr.select_one("td.DateTime")),
            views=_int(_text(tr.select_one("td.ViewCount"))),
            likes=_int(_text(tr.select_one("td.voteCount"))),
            comments=_int(_text(tr.select_one(".AB-comm"))),
        ))
    return rows


def is_relevant(title: str) -> bool:
    t = title.lower()
    return any(k.lower() in t for k in KEYWORDS)


def parse_lead_cards(html: str) -> list[LeadCard]:
    cards = []
    for box in BeautifulSoup(html, "html.parser").select(".bd_open, .bd_closed"):
        link = box.select_one(".txt a[href*='ab-1958-']")
        if link is None:
            continue
        subject = box.select_one(".subject")
        closed_tag = subject.select_one("em.closed") if subject else None
        if closed_tag:
            closed_tag.extract()
        budget = box.select_one(".budget em")
        cards.append(LeadCard(
            title=_text(subject),
            url=_post_url(link["href"]),
            summary=_text(box.select_one(".comment_1")),
            closed="bd_closed" in box.get("class", []),
            budget=_text(budget).replace(" ", "", 1) if budget else "",
            industry=_text(box.select_one(".BDU_tob em")),
            date=_text(box.select_one(".sign_date em")),
        ))
    return cards


def post_body(html: str) -> str:
    """Plain text of the article body, without the site menu around it."""
    return _text(BeautifulSoup(html, "html.parser").select_one(".ABA-view-body"))
