import argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path

from loop.run import run_day
from loop.store import LedgerRow, append_ledger

ROOT = Path(__file__).resolve().parent.parent
KST = timezone(timedelta(hours=9))


def main() -> None:
    p = argparse.ArgumentParser(prog="loop")
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="하루 한 바퀴 실행")
    r.add_argument("--date")
    lg = sub.add_parser("log", help="게시·반응 한 줄 기록")
    lg.add_argument("--channel", required=True)
    lg.add_argument("--kind", required=True, choices=["post", "reply", "chat", "lead-reply", "response"])
    lg.add_argument("--url", default="")
    lg.add_argument("--hook", default="")
    lg.add_argument("--campaign", default="")
    lg.add_argument("--note", default="")
    a = p.parse_args()
    today = getattr(a, "date", None) or datetime.now(KST).date().isoformat()
    if a.cmd == "run":
        print(run_day(today, ROOT))
    else:
        append_ledger(ROOT / "data/ledger.csv", LedgerRow(today, a.channel, a.kind, a.url, a.hook, a.campaign, a.note))
        print("기록했습니다")


if __name__ == "__main__":
    main()
