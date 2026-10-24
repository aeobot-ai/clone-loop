from loop.store import (
    LedgerRow, append_ledger, append_metrics, read_ledger, read_leads, read_metrics, upsert_leads,
)


def test_empty_ledger(tmp_path):
    assert read_ledger(tmp_path / "ledger.csv") == []


def test_ledger_roundtrip(tmp_path):
    p = tmp_path / "ledger.csv"
    row = LedgerRow("2026-10-24", "board-aeo", "reply", "https://www.i-boss.co.kr/ab-6141-1", "h-x-1", "x", "")
    append_ledger(p, row)
    append_ledger(p, row)
    assert read_ledger(p) == [row, row]


def test_metrics_dedupe_by_date_url(tmp_path):
    p = tmp_path / "metrics.jsonl"
    rows = [{"date": "2026-10-24", "url": "u", "views": 1, "likes": 0, "comments": 0}]
    assert append_metrics(p, rows) == 1
    assert append_metrics(p, rows) == 0
    assert read_metrics(p) == rows


def test_leads_only_new(tmp_path):
    p = tmp_path / "leads.csv"
    lead = {"found": "2026-10-24", "url": "u1", "title": "SEO/AEO 의뢰", "category": "SEO"}
    new = upsert_leads(p, [lead])
    assert new[0]["status"] == "new"
    assert upsert_leads(p, [lead]) == []
    assert len(read_leads(p)) == 1
