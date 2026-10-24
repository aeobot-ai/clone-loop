"""One turn of the loop: measure → collect → judge → scorecard → learn → drafts."""

from __future__ import annotations

import json
import re
import traceback
from pathlib import Path
from typing import Callable

from loop import web
from loop.blog import SITEMAP, parse_post_page, parse_sitemap
from loop.iboss import is_relevant, parse_board_rows, parse_lead_cards, parse_post_stats, post_body
from loop.llm import ask as claude_ask
from loop.scorecard import build_scorecard
from loop.store import append_metrics, read_leads, read_ledger, read_metrics, upsert_leads
from loop.utm import with_utm

BOARDS = {
    "board-aeo": "https://www.i-boss.co.kr/ab-6140?tag=AEO+GEO",
    "board-blog": "https://www.i-boss.co.kr/ab-74613",
    "board-qna": "https://www.i-boss.co.kr/ab-2109",
    "board-hospital": "https://www.i-boss.co.kr/ab-7055",
    "board-ai": "https://www.i-boss.co.kr/ab-6140?tag=AI",
}
LEAD_BOARDS = {
    "SEO": "https://www.i-boss.co.kr/ab-1957&category_1=SEO",
    "AI": "https://www.i-boss.co.kr/ab-1957&category_1=AI",
}
WARMUP_UNTIL = "2026-10-27"  # new i-boss account: replies and info-sharing only before this date
MAX_THREADS = 6
PER_BOARD = 2  # AEO·GEO alone would fill every slot, mostly with competitors' posts
THREAD_CHARS = 1500
TOP_POSTS = 3
_UTM = re.compile(r"\{\{utm:([\w-]+):([\w-]+):([\w-]+)\}\}")


def _fill_utm(text: str) -> str:
    def sub(m: re.Match) -> str:
        channel, slug, hook = m.groups()
        base = "https://aeobot.ai/" if slug == "home" else f"https://aeobot.ai/blog/{slug}/"
        return with_utm(base, channel, slug, hook)

    return _UTM.sub(sub, text)


def _read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def _parse_verdicts(text: str) -> list[dict]:
    out = []
    for line in text.splitlines():
        line = line.strip().strip("`")
        if line.startswith("{"):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


def run_day(
    today: str,
    root: Path,
    scrape: Callable[[str], str] = web.scrape,
    get: Callable[[str], str] = web.get,
    ask: Callable[[str], str] = claude_ask,
) -> Path:
    data, out = root / "data", root / "out" / today
    out.mkdir(parents=True, exist_ok=True)
    (out / "errors.md").unlink(missing_ok=True)
    errors: list[str] = []

    def step(name: str, fn: Callable[[], object]):
        try:
            return fn()
        except Exception as e:  # one broken source must not stop the day
            errors.append(f"- {name}: {type(e).__name__}: {e}")
            (out / "errors.md").write_text("# 오류\n\n" + "\n".join(errors) + "\n", encoding="utf-8")
            traceback.print_exc()
            return None

    ledger = read_ledger(data / "ledger.csv")

    def measure():
        rows = []
        for url in sorted({r.url for r in ledger if r.url}):
            stats = step(f"measure {url}", lambda u=url: parse_post_stats(scrape(u)))
            if stats:
                rows.append({"date": today, "url": url, "views": stats.views, "likes": stats.likes, "comments": stats.comments})
        return append_metrics(data / "metrics.jsonl", rows)

    step("measure", measure)

    def blog_posts():
        posts = [parse_post_page(get(u), u) for u in parse_sitemap(get(SITEMAP))]
        return sorted(posts, key=lambda p: p.published, reverse=True)[:TOP_POSTS]

    posts = step("blog", blog_posts) or []

    targets_path = data / "targets.jsonl"
    all_targets = _read_jsonl(targets_path)
    judged = {t["url"] for t in all_targets if t["date"] != today} | {r.url for r in ledger if r.url}  # skip our own posts
    verdicts: dict[str, dict] = {t["url"]: t for t in all_targets if t["date"] == today}

    def threads():
        found = []
        for channel, url in BOARDS.items():
            rows = step(f"board {channel}", lambda u=url: parse_board_rows(scrape(u))) or []
            found += [(channel, r) for r in rows if is_relevant(r.title) and r.url not in judged][:PER_BOARD]
        seen, uniq = set(), []
        for channel, r in found:
            if r.url not in seen:
                seen.add(r.url)
                uniq.append((channel, r))
        picked = uniq[:MAX_THREADS]
        items = []
        for channel, r in picked:
            body = post_body(step(f"thread {r.url}", lambda u=r.url: scrape(u)) or "")
            items.append({"kind": "thread", "channel": channel, "url": r.url, "title": r.title,
                          "views": r.views, "comments": r.comments, "body": body[:THREAD_CHARS]})
        return items

    thread_items = step("threads", threads) or []

    def leads():
        cards = []
        for cat, url in LEAD_BOARDS.items():
            cards += [(cat, c) for c in (step(f"leads {cat}", lambda u=url: parse_lead_cards(scrape(u))) or []) if not c.closed]
        upsert_leads(data / "leads.csv", [
            {"found": today, "url": c.url, "title": c.title, "category": cat} for cat, c in cards
        ])
        # Offer every open lead not judged on an earlier day, so a failed judge/drafts day is retried.
        items, seen = [], set()
        for _, c in cards:
            if c.url in judged or c.url in seen:
                continue
            seen.add(c.url)
            items.append({"kind": "lead", "channel": "lead", "url": c.url, "title": c.title, "body": c.summary,
                          "budget": c.budget, "industry": c.industry})
        return items

    lead_items = step("leads", leads) or []

    (out / "threads.md").write_text(
        "# 수집 " + today + "\n\n" + "\n".join(
            f"- [{i['kind']}] [{i['title']}]({i['url']}) ({i['channel']})" for i in thread_items + lead_items
        ) + "\n", encoding="utf-8")

    rubric = (root / "rubric.md").read_text(encoding="utf-8")

    def judge():
        items = [i for i in thread_items + lead_items if i["url"] not in verdicts]
        if not items:
            return
        listing = "\n\n".join(f"### {i['url']}\n제목: {i['title']}\n{i['body']}" for i in items)
        prompt = (root / "prompts/judge.md").read_text(encoding="utf-8").format(rubric=rubric, items=listing)
        kinds = {i["url"]: i["kind"] for i in items}
        with targets_path.open("a", encoding="utf-8") as f:
            for v in _parse_verdicts(ask(prompt)):
                if v.get("url") in kinds and v["url"] not in verdicts:
                    verdicts[v["url"]] = v
                    f.write(json.dumps({"date": today, "kind": kinds[v["url"]], **v}, ensure_ascii=False) + "\n")

    step("judge", judge)

    scorecard = build_scorecard(ledger, read_metrics(data / "metrics.jsonl"), read_leads(data / "leads.csv"),
                                _read_jsonl(targets_path), today)
    (out / "scorecard.md").write_text(scorecard, encoding="utf-8")

    learnings_path = root / "learnings.md"

    def learn():
        if not ledger:
            return
        prompt = (root / "prompts/learn.md").read_text(encoding="utf-8").format(
            scorecard=scorecard, learnings=learnings_path.read_text(encoding="utf-8"))
        learnings_path.write_text(ask(prompt) + "\n", encoding="utf-8")

    step("learn", learn)

    def drafts():
        passed = lambda items: [i for i in items if verdicts.get(i["url"], {}).get("pass")]
        fmt = lambda items: "\n\n".join(
            f"### {i['title']}\nURL: {i['url']}\n채널: {i['channel']}\n판정: {verdicts[i['url']].get('why', '')}\n{i['body']}"
            for i in items) or "없음"
        phase_rule = ("가입 초기(신뢰 쌓기) 기간이다: 답글·정보 공유만 쓰고 홍보 게시판 글과 직접적인 제품 홍보는 쓰지 않는다."
                      if today < WARMUP_UNTIL else "정회원이면 마케팅 서비스 게시판 홍보 글도 하나 쓸 수 있다.")
        prompt = (root / "prompts/drafts.md").read_text(encoding="utf-8").format(
            today=today, rubric=rubric, phase_rule=phase_rule,
            learnings=learnings_path.read_text(encoding="utf-8"),
            posts="\n\n".join(f"### {p.title} (slug: {p.slug}, {p.published})\n{p.text}" for p in posts) or "없음",
            threads=fmt(passed(thread_items)), leads=fmt(passed(lead_items)))
        (out / "drafts.md").write_text(_fill_utm(ask(prompt)) + "\n", encoding="utf-8")

    step("drafts", drafts)
    return out
