"""Read aeobot blog posts from the sitemap and each post's page."""

from __future__ import annotations

import html
import re
from dataclasses import dataclass

BLOG_ROOT = "https://aeobot.ai/blog/"
SITEMAP = "https://aeobot.ai/blog/sitemap-0.xml"
_TEXT_LIMIT = 6000


@dataclass(frozen=True)
class BlogPost:
    slug: str
    title: str
    url: str
    published: str
    description: str
    text: str


def parse_sitemap(xml: str) -> list[str]:
    return [u for u in re.findall(r"<loc>([^<]+)</loc>", xml) if u.rstrip("/") != BLOG_ROOT.rstrip("/")]


def _meta(page: str, key: str) -> str:
    m = re.search(rf'<meta[^>]+(?:property|name)="{re.escape(key)}"[^>]+content="([^"]*)"', page)
    return html.unescape(m.group(1)) if m else ""


def parse_post_page(page: str, url: str) -> BlogPost:
    title = _meta(page, "og:title").split(" | ")[0]
    body = re.search(r"(?is)<article[^>]*>(.*)</article>", page)
    text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", body.group(1) if body else page)
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", text))).strip()
    return BlogPost(
        slug=url.rstrip("/").rsplit("/", 1)[-1],
        title=title,
        url=url,
        published=_meta(page, "article:published_time")[:10],
        description=_meta(page, "og:description"),
        text=text[:_TEXT_LIMIT],
    )
