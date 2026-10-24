"""Files the loop keeps in git: the posting ledger, daily metrics, i-boss leads."""

from __future__ import annotations

import csv
import json
from dataclasses import astuple, dataclass, fields
from pathlib import Path

LEAD_FIELDS = ["found", "url", "title", "category", "status"]


@dataclass(frozen=True)
class LedgerRow:
    date: str
    channel: str
    kind: str  # post | reply | chat | lead-reply | response
    url: str
    hook: str
    campaign: str
    note: str


LEDGER_FIELDS = [f.name for f in fields(LedgerRow)]


def _read_csv(path: Path) -> list[dict]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def _append_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    new = not path.exists() or path.stat().st_size == 0
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(header)
        w.writerows(rows)


def read_ledger(path: Path) -> list[LedgerRow]:
    return [LedgerRow(**{k: r.get(k, "") or "" for k in LEDGER_FIELDS}) for r in _read_csv(path)]


def append_ledger(path: Path, row: LedgerRow) -> None:
    _append_csv(path, LEDGER_FIELDS, [list(astuple(row))])


def read_metrics(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_metrics(path: Path, rows: list[dict]) -> int:
    seen = {(r["date"], r["url"]) for r in read_metrics(path)}
    fresh = [r for r in rows if (r["date"], r["url"]) not in seen]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for r in fresh:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return len(fresh)


def read_leads(path: Path) -> list[dict]:
    return _read_csv(path)


def upsert_leads(path: Path, rows: list[dict]) -> list[dict]:
    known = {r["url"] for r in read_leads(path)}
    fresh = []
    for r in rows:
        if r["url"] in known:
            continue
        known.add(r["url"])
        fresh.append({**{k: "" for k in LEAD_FIELDS}, "status": "new", **r})
    _append_csv(path, LEAD_FIELDS, [[r[k] for k in LEAD_FIELDS] for r in fresh])
    return fresh
