from loop import kakao

DRAFTS = """# 초안 2026-10-25
> 학습 반영: test

## 1. 오픈채팅방 메시지

### room-hospital
병원 마케팅 하시는 분들께 공유드려요. 강남 피부과를 측정해 보니 네이버 지도 상위 10위에 든 54곳 중 AI 답변에 나온 곳은 4곳(7%)이었습니다. 지도 1위 병원은 한 번도 나오지 않았습니다. 미국 로펌 1,000곳을 다룬 논문에서도 지도 관리가 충실한 곳이 AI 언급은 오히려 적게 받았다는, 같은 패턴이 나와서 같이 정리해 봤습니다. 지도 관리와 AI 노출을 따로 보셔야 하는 이유가 궁금하시면 참고해 보세요. https://aeobot.ai/blog/ai-citation-gap/?utm_source=iboss&utm_medium=room-hospital&utm_campaign=ai-citation-gap&utm_content=h-ai-citation-gap-1

### room-beauty
짧은 메시지입니다.

### room-viral
오늘은 보내지 않음. 맞는 글이 없습니다.

## 2. 게시판 글

### board-aeo
게시판 글은 보내지 않는다.
"""


def test_room_messages_skips_not_sent_and_other_sections():
    rooms = kakao.room_messages(DRAFTS)
    assert [c for c, _ in rooms] == ["room-hospital", "room-beauty"]
    assert rooms[1][1] == "짧은 메시지입니다."


def test_memos_fit_limit_and_keep_text():
    rooms = kakao.room_messages(DRAFTS)
    memos = kakao.memos(rooms)
    assert all(len(m) <= kakao.TEXT_LIMIT for m in memos)
    hospital = rooms[0][1]
    parts = memos[:memos.index(next(m for m in memos if "room-beauty" in m))]
    assert parts[0].startswith("[room-hospital] ")  # room tag rides on the first part, no separate header
    assert " ".join(parts) == "[room-hospital] " + hospital  # pasted back together, nothing lost
    assert any(p.endswith("utm_content=h-ai-citation-gap-1") for p in parts)  # URL never split
    assert memos[-1] == "[room-beauty] 짧은 메시지입니다."


def test_no_rooms_no_memos():
    assert kakao.memos(kakao.room_messages("# 초안\n## 2. 게시판 글\n### board-aeo\n본문")) == []


class Resp:
    def __init__(self, body, status_code=200):
        self._body, self.status_code = body, status_code

    def raise_for_status(self):
        pass

    def json(self):
        return self._body


def test_sender_refreshes_once_and_sends_memo(monkeypatch):
    calls = []

    def post(url, data=None, headers=None, timeout=None):
        calls.append((url, data, headers))
        if "kauth" in url:
            return Resp({"access_token": "at", "refresh_token": "new"})
        return Resp({"result_code": 0})

    monkeypatch.setenv("KAKAO_REST_API_KEY", "key")
    monkeypatch.setenv("KAKAO_REFRESH_TOKEN", "rt")
    monkeypatch.delenv("KAKAO_CLIENT_SECRET", raising=False)
    monkeypatch.setattr(kakao.requests, "post", post)
    send = kakao.sender_from_env()
    send("하나")
    send("둘")
    assert [c[0] for c in calls] == [kakao.TOKEN_URL, kakao.MEMO_URL, kakao.MEMO_URL]
    assert calls[0][1] == {"grant_type": "refresh_token", "client_id": "key", "refresh_token": "rt"}
    assert calls[1][2] == {"Authorization": "Bearer at"}
    assert '"text": "하나"' in calls[1][1]["template_object"]
    assert send.renewed  # Kakao issued a new refresh token: the old one expires within a month


def test_sender_off_without_env(monkeypatch):
    monkeypatch.delenv("KAKAO_REST_API_KEY", raising=False)
    monkeypatch.delenv("KAKAO_REFRESH_TOKEN", raising=False)
    assert kakao.sender_from_env() is None


def test_memo_error_raises(monkeypatch):
    monkeypatch.setattr(kakao.requests, "post",
                        lambda url, **k: Resp({"access_token": "at"} if "kauth" in url else {"result_code": -1}))
    send = kakao.Sender("key", "rt")
    try:
        send("x")
    except RuntimeError as e:
        assert "result_code" in str(e)
    else:
        raise AssertionError("expected RuntimeError")


def test_login_url_and_code_exchange(monkeypatch):
    url = kakao.authorize_url("key", "https://localhost")
    assert url.startswith("https://kauth.kakao.com/oauth/authorize?") and "scope=talk_message" in url
    seen = {}

    def post(u, data=None, timeout=None):
        seen.update(data)
        return Resp({"access_token": "at", "refresh_token": "rt"})

    monkeypatch.setattr(kakao.requests, "post", post)
    assert kakao.exchange_code("key", "https://localhost", "c0de") == "rt"
    assert seen == {"grant_type": "authorization_code", "client_id": "key",
                    "redirect_uri": "https://localhost", "code": "c0de"}


def test_token_error_shows_kakao_code(monkeypatch):
    monkeypatch.setattr(kakao.requests, "post", lambda url, **k: Resp(
        {"error": "invalid_grant", "error_description": "authorization code not found", "error_code": "KOE320"}, 400))
    try:
        kakao.Sender("key", "rt")("x")
    except RuntimeError as e:
        assert "KOE320" in str(e) and "invalid_grant" in str(e)
    else:
        raise AssertionError("expected RuntimeError")


def test_send_day_resends_drafts(tmp_path, monkeypatch):
    day = tmp_path / "out" / "2026-10-25"
    day.mkdir(parents=True)
    (day / "drafts.md").write_text(DRAFTS, encoding="utf-8")
    sent = []
    assert kakao.send_day(day, sent.append) == len(sent) > 0
    assert "room-hospital" in sent[0]
