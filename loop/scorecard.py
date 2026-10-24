"""Turn the ledger, metrics, leads and rubric verdicts into the day's scorecard (markdown)."""

from __future__ import annotations

from collections import Counter, defaultdict

from loop.store import LedgerRow

# Ledger kinds that are outcomes, not things we posted. 7-day goals (submitted 2026-10-24) for the conversions.
OUTCOMES = ("response", "diagnosis", "paid")
GOAL_DIAGNOSIS, GOAL_PAID = 5, 1


def _latest_two(metrics: list[dict]) -> dict[str, list[dict]]:
    by_url: dict[str, list[dict]] = defaultdict(list)
    for m in sorted(metrics, key=lambda m: m["date"]):
        by_url[m["url"]].append(m)
    return {u: rows[-2:] for u, rows in by_url.items()}


def _table(title: str, key, ledger: list[LedgerRow], latest: dict[str, list[dict]]) -> list[str]:
    groups: dict[str, list[LedgerRow]] = defaultdict(list)
    for r in ledger:
        if r.kind not in (*OUTCOMES, "chat"):
            groups[key(r)].append(r)
    lines = [f"### {title}", "", "| 이름 | 게시 수 | 조회 | 좋아요 | 댓글 | 전날 대비 조회 |", "|---|---|---|---|---|---|"]
    for name, rows in sorted(groups.items()):
        views = likes = comments = delta = 0
        for url in {r.url for r in rows}:  # a thread logged twice (post + reply) is still one page
            hist = latest.get(url, [])
            if not hist:
                continue
            views += hist[-1]["views"]
            likes += hist[-1]["likes"]
            comments += hist[-1]["comments"]
            delta += hist[-1]["views"] - (hist[0]["views"] if len(hist) == 2 else 0)
        lines.append(f"| {name} | {len(rows)} | {views} | {likes} | {comments} | {delta:+d} |")
    return lines + [""]


def build_scorecard(ledger: list[LedgerRow], metrics: list[dict], leads: list[dict], targets: list[dict], today: str) -> str:
    responses = sum(r.kind == "response" for r in ledger)
    passed = sum(bool(t.get("pass")) for t in targets)
    out = [
        f"# 스코어카드 {today}",
        "",
        "## North Star",
        "",
        f"진짜 고객 반응: **{responses}** (고객 체크리스트를 통과한 마케터의 댓글·쪽지·의뢰 회신 누적)",
        "",
        f"체크리스트 통과 {passed} / 판정 {len(targets)} (수집한 글·리드 누적)",
        "",
    ]
    diagnosis = [r for r in ledger if r.kind == "diagnosis"]
    paid = [r for r in ledger if r.kind == "paid"]
    by_channel = Counter(r.channel for r in diagnosis + paid)
    out += [
        "## 전환",
        "",
        f"무료 진단 신청: **{len(diagnosis)}** / 목표 {GOAL_DIAGNOSIS}",
        "",
        f"유료 전환: **{len(paid)}** / 목표 {GOAL_PAID}",
        "",
        "경로: " + (" · ".join(f"{c} {n}" for c, n in sorted(by_channel.items())) or "아직 없음"),
        "",
    ]
    posted = [r for r in ledger if r.kind not in OUTCOMES]
    if not posted:
        return "\n".join(out + ["아직 게시 기록 없음", ""])
    latest = _latest_two(metrics)
    out += _table("채널별", lambda r: r.channel, posted, latest)
    out += _table("훅별", lambda r: r.hook or "-", posted, latest)
    chats = Counter(r.channel for r in ledger if r.kind == "chat")
    if chats:
        out += ["### 오픈채팅", "", ", ".join(f"{c} {n}회" for c, n in sorted(chats.items())) + " — 조회수 측정 불가, UTM(GA4) 연결 전", ""]
    status = Counter(l.get("status", "new") for l in leads)
    out += ["### 대행의뢰 리드", "", " · ".join(f"{s} {n}" for s, n in sorted(status.items())) or "없음", ""]
    return "\n".join(out)
