import json
import shutil
from pathlib import Path

from loop.run import run_day
from loop.store import LedgerRow, append_ledger, read_metrics

FIX = Path(__file__).parent / "fixtures"
REPO = Path(__file__).parent.parent
TODAY = "2026-10-24"


def setup_root(tmp_path):
    for name in ["rubric.md", "learnings.md"]:
        shutil.copy(REPO / name, tmp_path / name)
    shutil.copytree(REPO / "prompts", tmp_path / "prompts")
    return tmp_path


def fake_scrape(url):
    if "ab-1957" in url:
        return (FIX / "leads.md").read_text()
    if "ab-6141-" in url or "ab-1958-" in url:
        return (FIX / "post.md").read_text()
    return (FIX / "board.md").read_text()


def fake_get(url):
    if url.endswith(".xml"):
        return (FIX / "sitemap.xml").read_text()
    return (FIX / "blogpost.html").read_text()


def fake_ask(prompt):
    if "루브릭으로 각 항목" in prompt:
        urls = [l[4:].strip() for l in prompt.splitlines() if l.startswith("### https://")]
        return "\n".join(json.dumps({"url": u, "pass": True, "why": "test"}) for u in urls)
    if "학습 노트를 새로 쓴다" in prompt:
        return "# 학습 노트\n\n## 근거 숫자\n- test"
    return "# 초안\n링크: {{utm:room-beauty:winter-moisturizer-ai:h-winter-moisturizer-ai-1}}"


def test_happy_path(tmp_path):
    root = setup_root(tmp_path)
    out = run_day(TODAY, root, fake_scrape, fake_get, fake_ask)
    for name in ["drafts.md", "scorecard.md", "threads.md"]:
        assert (out / name).exists()
    drafts = (out / "drafts.md").read_text()
    assert "{{utm:" not in drafts
    assert "utm_source=iboss" in drafts and "utm_medium=room-beauty" in drafts
    assert not (out / "errors.md").exists()
    targets = (root / "data/targets.jsonl").read_text().splitlines()
    assert any('"kind": "lead"' in t for t in targets)
    assert "루브릭 통과" in (out / "scorecard.md").read_text()


def test_scrape_failure_keeps_going(tmp_path):
    root = setup_root(tmp_path)

    def boom(url):
        raise RuntimeError("403")

    out = run_day(TODAY, root, boom, fake_get, fake_ask)
    assert (out / "errors.md").exists()
    assert (out / "scorecard.md").exists()
    assert (out / "drafts.md").exists()


def test_llm_failure_keeps_scorecard(tmp_path):
    root = setup_root(tmp_path)

    def boom(prompt):
        raise RuntimeError("claude down")

    out = run_day(TODAY, root, fake_scrape, fake_get, boom)
    assert "drafts" in (out / "errors.md").read_text()
    assert (out / "scorecard.md").exists()


def test_rerun_same_day_no_duplicates(tmp_path):
    root = setup_root(tmp_path)
    append_ledger(root / "data/ledger.csv",
                  LedgerRow(TODAY, "board-aeo", "reply", "https://www.i-boss.co.kr/ab-6141-72783", "h-x-1", "x", ""))
    run_day(TODAY, root, fake_scrape, fake_get, fake_ask)
    run_day(TODAY, root, fake_scrape, fake_get, fake_ask)
    assert len(read_metrics(root / "data/metrics.jsonl")) == 1
    assert (root / "learnings.md").read_text().startswith("# 학습 노트")
