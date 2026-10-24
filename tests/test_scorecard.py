from loop.scorecard import build_scorecard
from loop.store import LedgerRow


def L(channel, kind, url, hook="h-a-1"):
    return LedgerRow("2026-10-24", channel, kind, url, hook, "a", "")


def test_empty():
    out = build_scorecard([], [], [], [], "2026-10-24")
    assert "아직 게시 기록 없음" in out
    assert "North Star" in out


def test_channel_uses_latest_metric_and_delta():
    ledger = [L("board-aeo", "post", "u1"), L("board-aeo", "reply", "u2")]
    metrics = [
        {"date": "2026-10-24", "url": "u1", "views": 10, "likes": 1, "comments": 0},
        {"date": "2026-10-25", "url": "u1", "views": 30, "likes": 2, "comments": 1},
        {"date": "2026-10-25", "url": "u2", "views": 5, "likes": 0, "comments": 0},
    ]
    out = build_scorecard(ledger, metrics, [], [], "2026-10-25")
    assert "| board-aeo | 2 | 35 | 2 | 1 | +25 |" in out


def test_north_star_and_leads_and_targets():
    ledger = [L("board-aeo", "response", ""), L("room-beauty", "chat", ""), L("lead", "response", "")]
    leads = [{"status": "new"}, {"status": "replied"}]
    targets = [{"date": "2026-10-24", "url": "a", "pass": True}, {"date": "2026-10-24", "url": "b", "pass": False}]
    out = build_scorecard(ledger, [], leads, targets, "2026-10-24")
    assert "진짜 고객 반응: **2**" in out
    assert "new 1" in out and "replied 1" in out
    assert "체크리스트 통과 1 / 판정 2" in out
    assert "UTM(GA4) 연결 전" in out


def test_same_url_logged_twice_counted_once():
    ledger = [L("board-aeo", "reply", "u1"), L("board-aeo", "reply", "u1")]
    metrics = [{"date": "2026-10-24", "url": "u1", "views": 10, "likes": 1, "comments": 2}]
    out = build_scorecard(ledger, metrics, [], [], "2026-10-24")
    assert "| board-aeo | 2 | 10 | 1 | 2 | +10 |" in out


def test_conversions_counted_and_kept_out_of_post_tables():
    ledger = [
        L("board-aeo", "post", "u1"),
        L("lead", "diagnosis", ""),
        L("board-aeo", "diagnosis", ""),
        L("lead", "paid", ""),
    ]
    metrics = [{"date": "2026-10-24", "url": "u1", "views": 10, "likes": 0, "comments": 0}]
    out = build_scorecard(ledger, metrics, [], [], "2026-10-24")
    assert "무료 진단 신청: **2** / 목표 5" in out
    assert "유료 전환: **1** / 목표 1" in out
    assert "board-aeo 1 · lead 2" in out
    assert "| board-aeo | 1 | 10 | 0 | 0 | +10 |" in out  # diagnosis rows are not posts
