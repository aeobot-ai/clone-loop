from pathlib import Path

from loop.blog import parse_post_page, parse_sitemap
from loop.eopla import MagazineStats, parse_magazine_stats, parse_popular
from loop.iboss import BoardRow, PostStats, is_relevant, parse_board_rows, parse_post_stats
from loop.utm import with_utm

FIX = Path(__file__).parent / "fixtures"
HTML = FIX / "html"  # i-boss pages as fetched (curl_cffi), 2026-10-25


def test_post_stats_parses_comma_numbers():
    assert parse_post_stats((HTML / "post.html").read_text()) == PostStats(1981, 13, 20)


def test_post_stats_missing():
    assert parse_post_stats("no stats here") is None


def test_board_rows():
    rows = parse_board_rows((HTML / "board.html").read_text())
    assert len(rows) >= 20
    by_url = {r.url: r for r in rows}
    assert by_url["https://www.i-boss.co.kr/ab-6141-72783"] == BoardRow(
        "블로그 노출 현황들 여쭙습니다,,,", "https://www.i-boss.co.kr/ab-6141-72783", "10.20", 1982, 13, 20)
    assert any(r.comments == 0 for r in rows)


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

    cards = parse_lead_cards((HTML / "leads.html").read_text())
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

    body = post_body((HTML / "post.html").read_text())
    assert body.startswith("요즘 네이버 통검")
    assert "통합검색" not in body and "<" not in body
    assert post_body("<p>no article body</p>") == ""


def test_board_row_posted_today_shows_time():
    html = ('<tr class="_t"><td><div class="articleSubject"><a href="ab-6141-72900&tag=AEO+GEO" title="강남 피부과" '
            'class="mb_subject like_0">강남 피부과</a></div></td><td><p class="mb_writer"><span>aeobot</span></p></td>'
            '<td class="DateTime font_num"><strong>16:07</strong></td><td class="ViewCount font_num">1</td>'
            '<td class="voteCount">0</td></tr>')
    rows = parse_board_rows(html)
    assert rows and rows[0].date == "16:07"


def test_eopla_magazine_stats():
    html = (HTML / "eopla_magazine.html").read_text()  # eopla.net, 2026-10-30
    assert parse_magazine_stats(html, "https://eopla.net/magazines/48458") == MagazineStats(0, 0)
    assert parse_magazine_stats("no stats here", "https://eopla.net/magazines/48458") is None


def test_eopla_popular_in_rank_order():
    ranked = parse_popular((HTML / "eopla_home.html").read_text())
    assert ranked[:2] == ["https://eopla.net/magazines/48458", "https://eopla.net/magazines/48409"]
    assert len(ranked) == 9
