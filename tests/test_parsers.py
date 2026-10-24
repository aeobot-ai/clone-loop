from pathlib import Path

from loop.blog import parse_post_page, parse_sitemap
from loop.iboss import BoardRow, PostStats, is_relevant, parse_board_rows, parse_post_stats
from loop.utm import with_utm

FIX = Path(__file__).parent / "fixtures"


def test_post_stats_parses_comma_numbers():
    assert parse_post_stats((FIX / "post.md").read_text()) == PostStats(1896, 13, 20)


def test_post_stats_missing():
    assert parse_post_stats("no stats here") is None


def test_board_rows():
    rows = parse_board_rows((FIX / "board.md").read_text())
    assert len(rows) == 3
    assert rows[1] == BoardRow("블로그 노출 현황들 여쭙습니다,,,", "https://www.i-boss.co.kr/ab-6141-72783", "10.20", 1897, 13, 20)
    assert rows[2].comments == 0


def test_is_relevant():
    assert is_relevant("블로그 노출 현황들 여쭙습니다")
    assert is_relevant("perplexity 인용 구조")
    assert not is_relevant("치이카와는 왜 인기가 많을까")


def test_sitemap_skips_index():
    urls = parse_sitemap((FIX / "sitemap.xml").read_text())
    assert "https://aeobot.ai/blog/" not in urls
    assert "https://aeobot.ai/blog/winter-moisturizer-ai/" in urls


def test_post_page_meta():
    p = parse_post_page((FIX / "blogpost.html").read_text(), "https://aeobot.ai/blog/winter-moisturizer-ai/")
    assert p.slug == "winter-moisturizer-ai"
    assert p.title.startswith("겨울 수분크림")
    assert "AEOBOT 인사이트" not in p.title
    assert p.published == "2026-10-23"
    assert "올리브영" in p.text


def test_with_utm():
    u = with_utm("https://aeobot.ai/blog/x/", "room-beauty", "x", "h-x-1")
    for part in ["utm_source=iboss", "utm_medium=room-beauty", "utm_campaign=x", "utm_content=h-x-1"]:
        assert part in u
    assert "q=1" in with_utm("https://a.b/?q=1", "m", "c", "h")


def test_lead_cards():
    from loop.iboss import parse_lead_cards

    cards = parse_lead_cards((FIX / "leads.md").read_text())
    by_url = {c.url: c for c in cards}
    aeo = by_url["https://www.i-boss.co.kr/ab-1958-88890"]
    assert aeo.title == "안녕하세요 AEO ㆍGEO 문의 드립니다."
    assert "광고 대행사" in aeo.summary
    assert not aeo.closed
    place = by_url["https://www.i-boss.co.kr/ab-1958-88896"]
    assert place.closed
    assert place.industry == "병원"
    assert place.budget.startswith("월간최소 10만원")


def test_post_body_skips_site_menu():
    from loop.iboss import post_body

    md = "[메뉴](https://x)\n" * 800 + (FIX / "post.md").read_text()
    assert post_body(md).startswith("# 블로그 노출 현황들 여쭙습니다")
    assert post_body("no heading at all") == "no heading at all"
