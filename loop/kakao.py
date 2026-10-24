"""Send today's open-chat drafts to my own KakaoTalk ("나에게 보내기"), ready to copy into each room.

Kakao has no API for posting into open chat rooms, so a person still pastes them. The default text
template caps text at 200 chars, so each room arrives as 2-3 paste-ready parts, the first tagged with its room.
"""

from __future__ import annotations

import json
import os
import re
from urllib.parse import urlencode

import requests

AUTHORIZE_URL = "https://kauth.kakao.com/oauth/authorize"
TOKEN_URL = "https://kauth.kakao.com/oauth/token"
MEMO_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
TEXT_LIMIT = 200
LINK = "https://aeobot.ai"  # tap target; must be a web domain registered on the Kakao app to open
_ROOMS = re.compile(r"^## 1\..*?$(.*?)(?=^## |\Z)", re.M | re.S)
_SENTENCE = re.compile(r"(?<=[.!?])\s+")


def _ok(r: requests.Response) -> dict:
    if r.status_code >= 400:  # Kakao's own error code says why (KOE…); the body holds no secrets on error
        try:
            b = r.json()
        except ValueError:
            b = {}
        raise RuntimeError(f"kakao {r.status_code}: {b.get('error_code', '')} {b.get('error', '')} {b.get('error_description', b.get('msg', ''))}".strip())
    return r.json()


def room_messages(drafts: str) -> list[tuple[str, str]]:
    m = _ROOMS.search(drafts)
    if not m:
        return []
    rooms = []
    for section in re.split(r"^### +", m.group(1), flags=re.M)[1:]:
        channel, _, body = section.partition("\n")
        body = body.strip()
        if body and "보내지 않음" not in body:
            rooms.append((channel.strip(), body))
    return rooms


def _parts(text: str) -> list[str]:
    words = []  # sentences, or words of a sentence too long for one memo
    for s in _SENTENCE.split(text):
        words += [s] if len(s) <= TEXT_LIMIT else s.split(" ")
    parts, cur = [], ""
    for w in words:
        for piece in [w[i:i + TEXT_LIMIT] for i in range(0, len(w), TEXT_LIMIT)]:
            if cur and len(cur) + 1 + len(piece) > TEXT_LIMIT:
                parts.append(cur)
                cur = piece
            else:
                cur = f"{cur} {piece}" if cur else piece
    return parts + [cur] if cur else parts


def memos(rooms: list[tuple[str, str]]) -> list[str]:
    out = []
    for channel, body in rooms:
        out += _parts(f"[{channel}] {body}")
    return out


def send_day(day_dir, send) -> int:
    """Send one day's open-chat drafts again, e.g. after a failed run or as a demo."""
    texts = memos(room_messages((day_dir / "drafts.md").read_text(encoding="utf-8")))
    for text in texts:
        send(text)
    return len(texts)


class Sender:
    def __init__(self, rest_key: str, refresh_token: str, client_secret: str = ""):
        self.rest_key, self.refresh_token, self.client_secret = rest_key, refresh_token, client_secret
        self.token, self.renewed = "", False

    def _access_token(self) -> str:
        if not self.token:
            data = {"grant_type": "refresh_token", "client_id": self.rest_key, "refresh_token": self.refresh_token}
            if self.client_secret:
                data["client_secret"] = self.client_secret
            body = _ok(requests.post(TOKEN_URL, data=data, timeout=30))
            self.token = body["access_token"]
            self.renewed = "refresh_token" in body  # only issued when the old one has under a month left
        return self.token

    def __call__(self, text: str) -> None:
        template = {"object_type": "text", "text": text, "link": {"web_url": LINK, "mobile_web_url": LINK}}
        r = requests.post(MEMO_URL, headers={"Authorization": f"Bearer {self._access_token()}"},
                          data={"template_object": json.dumps(template, ensure_ascii=False)}, timeout=30)
        code = _ok(r).get("result_code")
        if code != 0:
            raise RuntimeError(f"kakao memo: result_code {code}")


def authorize_url(rest_key: str, redirect_uri: str) -> str:
    q = {"client_id": rest_key, "redirect_uri": redirect_uri, "response_type": "code", "scope": "talk_message"}
    return f"{AUTHORIZE_URL}?{urlencode(q)}"


def exchange_code(rest_key: str, redirect_uri: str, code: str, client_secret: str = "") -> str:
    data = {"grant_type": "authorization_code", "client_id": rest_key, "redirect_uri": redirect_uri, "code": code}
    if client_secret:
        data["client_secret"] = client_secret
    return _ok(requests.post(TOKEN_URL, data=data, timeout=30))["refresh_token"]


def sender_from_env() -> Sender | None:
    key, refresh = os.environ.get("KAKAO_REST_API_KEY"), os.environ.get("KAKAO_REFRESH_TOKEN")
    if not key or not refresh:
        return None
    return Sender(key, refresh, os.environ.get("KAKAO_CLIENT_SECRET", ""))
