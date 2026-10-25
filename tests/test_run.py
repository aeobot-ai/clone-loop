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
        return (FIX / "html" / "leads.html").read_text()
    if "ab-6141-" in url or "ab-1958-" in url:
        return (FIX / "html" / "post.html").read_text()
    return (FIX / "html" / "board.html").read_text()


def fake_get(url):
    if url.endswith(".xml"):
        return (FIX / "sitemap.xml").read_text()
    return (FIX / "blogpost.html").read_text()


def fake_ask(prompt):
    if "고객 체크리스트로 각 항목" in prompt:
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
    assert "체크리스트 통과" in (out / "scorecard.md").read_text()


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


def test_rerun_same_day_keeps_candidates(tmp_path):
    root = setup_root(tmp_path)
    prompts = []

    def ask(p):
        prompts.append(p)
        return fake_ask(p)

    run_day(TODAY, root, fake_scrape, fake_get, ask)
    run_day(TODAY, root, fake_scrape, fake_get, ask)
    draft_prompts = [p for p in prompts if "사람이 직접 올릴 초안" in p]
    assert "ab-1958-88890" in draft_prompts[-1]  # lead still offered on rerun
    assert "ab-6141-72783" in draft_prompts[-1]  # thread still offered on rerun
    targets = (root / "data/targets.jsonl").read_text().splitlines()
    assert len(targets) == len({json.loads(t)["url"] for t in targets})  # no duplicate verdicts


def test_judge_failure_retries_leads_next_day(tmp_path):
    root = setup_root(tmp_path)

    def judge_down(p):
        if "고객 체크리스트로 각 항목" in p:
            raise RuntimeError("timeout")
        return fake_ask(p)

    run_day(TODAY, root, fake_scrape, fake_get, judge_down)
    prompts = []

    def ask(p):
        prompts.append(p)
        return fake_ask(p)

    run_day("2026-10-25", root, fake_scrape, fake_get, ask)
    judge = [p for p in prompts if "고객 체크리스트로 각 항목" in p][0]
    assert "ab-1958-88890" in judge
    assert judge.count("### https://www.i-boss.co.kr/ab-1958-88890") == 1


def test_threads_spread_across_boards(tmp_path):
    root = setup_root(tmp_path)

    def scrape(url):
        if "ab-6140?tag=AEO" in url:
            return "".join(
                f'<tr class="_t"><td><a href="ab-6141-9{n:03d}&tag=AEO+GEO" title="GEO 글 {n}" class="mb_subject">GEO 글 {n}</a></td>'
                f'<td class="DateTime">10.2{n % 9}</td><td class="ViewCount">1</td><td class="voteCount">0</td></tr>'
                for n in range(10))
        return fake_scrape(url)

    run_day(TODAY, root, scrape, fake_get, fake_ask)
    listing = (root / "out" / TODAY / "threads.md").read_text()
    assert listing.count("(board-aeo)") == 2
    assert "(board-blog)" in listing


def test_own_posts_not_collected(tmp_path):
    root = setup_root(tmp_path)
    append_ledger(root / "data/ledger.csv",
                  LedgerRow(TODAY, "board-blog", "post", "https://www.i-boss.co.kr/ab-6141-72783", "h-x-1", "x", ""))
    run_day(TODAY, root, fake_scrape, fake_get, fake_ask)
    assert "ab-6141-72783" not in (root / "out" / TODAY / "threads.md").read_text()


def test_drafts_sent_to_kakao_once_per_day(tmp_path):
    root = setup_root(tmp_path)
    sent = []

    def ask(p):
        if "사람이 직접 올릴 초안" in p:
            return "# 초안\n## 1. 오픈채팅방 메시지\n### room-beauty\n메시지 {{utm:room-beauty:winter-moisturizer-ai:h-winter-moisturizer-ai-1}}\n## 2. 게시판 글\n"
        return fake_ask(p)

    run_day(TODAY, root, fake_scrape, fake_get, ask, memo=sent.append)
    assert len(sent) == 1 and sent[0].startswith("[room-beauty] ")
    assert "utm_medium=room-beauty" in sent[0]  # UTM filled before sending
    run_day(TODAY, root, fake_scrape, fake_get, ask, memo=sent.append)
    assert len(sent) == 1  # rerun does not resend


def test_kakao_failure_is_reported(tmp_path):
    root = setup_root(tmp_path)

    def boom(text):
        raise RuntimeError("401")

    def ask(p):
        if "사람이 직접 올릴 초안" in p:
            return "# 초안\n## 1. 오픈채팅방 메시지\n### room-beauty\n메시지\n"
        return fake_ask(p)

    out = run_day(TODAY, root, fake_scrape, fake_get, ask, memo=boom)
    assert "kakao" in (out / "errors.md").read_text()
    assert (out / "drafts.md").exists()


def test_drafts_only_for_joined_rooms(tmp_path):
    root = setup_root(tmp_path)
    prompts = []

    def ask(p):
        prompts.append(p)
        return fake_ask(p)

    run_day(TODAY, root, fake_scrape, fake_get, ask)
    draft = [p for p in prompts if "사람이 직접 올릴 초안" in p][-1]
    assert "room-ai" in draft and "room-content" in draft
    assert "https://www.i-boss.co.kr/ab-5545-149" in draft
    for gone in ["room-hospital", "room-beauty", "room-agency", "room-inhouse", "room-viral"]:
        assert gone not in draft
