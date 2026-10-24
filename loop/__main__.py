import argparse
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path

from loop import kakao
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
    kl = sub.add_parser("kakao-login", help="카카오 리프레시 토큰 발급 (처음 한 번)")
    kl.add_argument("--redirect-uri", default="https://localhost")
    kl.add_argument("--code", help="로그인 후 주소창의 code 값")
    sub.add_parser("kakao-test", help="나에게 보내기 테스트 메시지")
    ks = sub.add_parser("kakao-send", help="그날 오픈채팅 초안을 나에게 다시 보내기")
    ks.add_argument("--date")
    a = p.parse_args()
    today = getattr(a, "date", None) or datetime.now(KST).date().isoformat()
    if a.cmd == "run":
        print(run_day(today, ROOT))
    elif a.cmd == "kakao-login":
        key = os.environ["KAKAO_REST_API_KEY"]
        if not a.code:
            print("브라우저에서 열고 동의한 뒤, 주소창의 code 값을 --code로 넘기세요:\n" + kakao.authorize_url(key, a.redirect_uri))
        else:
            token = kakao.exchange_code(key, a.redirect_uri, a.code, os.environ.get("KAKAO_CLIENT_SECRET", ""))
            print("KAKAO_REFRESH_TOKEN으로 저장하세요 (약 2개월 유효):\n" + token)
    elif a.cmd == "kakao-send":
        send = kakao.sender_from_env()
        if not send:
            raise SystemExit("KAKAO_REST_API_KEY와 KAKAO_REFRESH_TOKEN이 필요합니다")
        print(f"{kakao.send_day(ROOT / 'out' / today, send)}개 보냈습니다")
    elif a.cmd == "kakao-test":
        send = kakao.sender_from_env()
        if not send:
            raise SystemExit("KAKAO_REST_API_KEY와 KAKAO_REFRESH_TOKEN이 필요합니다")
        send("clone-loop 연결 확인: 내일부터 오픈채팅 초안이 여기로 옵니다.")
        print("보냈습니다")
    else:
        append_ledger(ROOT / "data/ledger.csv", LedgerRow(today, a.channel, a.kind, a.url, a.hook, a.campaign, a.note))
        print("기록했습니다")


if __name__ == "__main__":
    main()
