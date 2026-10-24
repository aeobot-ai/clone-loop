# clone-loop — aeobot 아이보스 GTM 루프

[aeobot](https://aeobot.ai)(AI 답변 엔진 속 브랜드 노출 측정)을 **진짜 고객**인 대기업 인하우스 마케터와 블로그 마케팅 대행사 담당자에게 알리는 Agentic GTM 루프입니다. Clone Loop Day Seoul(2026-10-24) 제출작.

## 왜 아이보스인가

국내 최대 마케터 커뮤니티 [아이보스](https://www.i-boss.co.kr)에는 우리 고객이 이미 모여 있고, 고민도 공개되어 있습니다.
- AEO·GEO 전용 게시판, 네이버 블로그 노출 변동 고민 글("블로그 노출 현황들 여쭙습니다" 조회 1,896·댓글 20)
- **대행의뢰 게시판**: "광고 대행사인데 AEO·GEO를 한 번도 관리해 본 적이 없어 상담을 원합니다" 같은 구매 의도 리드

## 루프 (하루 1회)

```
measure → collect → judge(루브릭) → scorecard → learn → drafts → kakao → (사람이 게시) → log ─┐
   ↑                                                                               │
   └──────────────────────────── 다음 날 ──────────────────────────────────────────┘
```

| 단계 | 하는 일 | 파일 |
|---|---|---|
| measure | 내가 올린 아이보스 글·답글의 조회수·좋아요·댓글을 다시 읽음 | `data/metrics.jsonl` |
| collect | aeobot 최신 블로그 글, 아이보스 5개 게시판의 관련 글, 대행의뢰(SEO·AI) 새 리드 | `out/<날짜>/threads.md`, `data/leads.csv` |
| judge | [`rubric.md`](rubric.md)의 예/아니오 체크리스트로 작성자가 진짜 고객인지 판정 | `data/targets.jsonl` |
| scorecard | North Star와 채널·훅별 성과, 리드 현황 | `out/<날짜>/scorecard.md` |
| learn | 스코어카드 숫자만 근거로 학습 노트 갱신 | [`learnings.md`](learnings.md) |
| drafts | 학습 노트를 반영한 오픈채팅방 메시지·게시판 글·답글·의뢰 응답 초안, 채널·훅별 UTM 링크 | `out/<날짜>/drafts.md` |
| kakao | 오픈채팅방 메시지 초안을 내 카카오톡으로 전송(나에게 보내기). 설정했을 때만 | `out/<날짜>/kakao-sent` |

**North Star:** 루브릭을 통과한 마케터에게서 받은 반응 수(댓글·쪽지·의뢰 회신). 봇이나 엉뚱한 사람에게 닿은 숫자는 세지 않습니다.

## 사람이 하는 일 (하루 5~10분)

아이보스에는 게시 API가 없고, 자동 게시는 스팸·계정 정지 위험이 있어 **등록 버튼만 사람이 누릅니다.**

1. `out/<오늘>/drafts.md`를 읽고 고쳐서 올립니다.
2. 올린 것과 받은 반응을 한 줄씩 기록합니다.

```sh
uv run python -m loop log --channel board-aeo --kind reply --url https://www.i-boss.co.kr/ab-6141-72783 --hook h-winter-moisturizer-ai-1 --campaign winter-moisturizer-ai
uv run python -m loop log --channel room-beauty --kind chat --hook h-winter-moisturizer-ai-1 --campaign winter-moisturizer-ai
uv run python -m loop log --channel lead --kind response --note "대행사 AEO 의뢰자 회신, 미팅 잡음"
```

## 카카오톡으로 초안 받기 (선택)

카카오는 오픈채팅방에 글을 올리는 API를 제공하지 않습니다. 대신 루프가 매일 오픈채팅 초안을 **나에게 보내기**로 보내 주므로, 휴대폰에서 복사해 방에 붙이면 됩니다. 기본 텍스트 템플릿은 200자 제한이 있어서, 방마다 안내 메시지 하나와 이어 붙일 조각 2~3개로 나눠 옵니다.

1. [카카오디벨로퍼스](https://developers.kakao.com/console/app)에서 앱을 만들고 REST API 키를 확인합니다.
2. 앱에서 카카오 로그인을 켜고, 리다이렉트 URI에 `https://localhost`를 등록하고, 동의항목에서 "카카오톡 메시지 전송(talk_message)"을 켭니다. 메시지를 눌렀을 때 aeobot.ai가 열리게 하려면 웹 도메인에 `https://aeobot.ai`도 등록합니다.
3. 리프레시 토큰을 한 번 발급합니다.
   ```sh
   KAKAO_REST_API_KEY=... uv run python -m loop kakao-login             # 출력된 주소를 열어 동의
   KAKAO_REST_API_KEY=... uv run python -m loop kakao-login --code <주소창의 code 값>
   ```
   클라이언트 시크릿을 켰다면 `KAKAO_CLIENT_SECRET`도 함께 넘깁니다.
4. `KAKAO_REST_API_KEY`, `KAKAO_REFRESH_TOKEN`(필요하면 `KAKAO_CLIENT_SECRET`)을 `.env`나 실행 환경의 비밀값에 넣고 `uv run python -m loop kakao-test`로 확인합니다.

리프레시 토큰은 약 2개월 유효합니다. 만료가 한 달 안으로 다가오면 `out/<날짜>/errors.md`에 다시 발급하라는 안내가 남습니다. 같은 날 다시 실행해도 중복 전송하지 않습니다.

## 실행

```sh
uv sync
echo "FIRECRAWL_API_KEY=..." > .env
uv run python -m loop run      # 하루 한 바퀴
uv run pytest                  # 테스트
```

LLM 단계는 headless Claude Code(`claude -p`)를 씁니다. 매일 09:00 KST 자동 실행:

```cron
0 9 * * * /path/to/clone-loop/scripts/daily.sh >> /tmp/clone-loop.log 2>&1
```

## 하지 않는 것

- 아이보스·카카오 오픈채팅 자동 게시
- 블로그에 없는 수치, "노출 보장" 같은 표현
- 새 계정 첫 3일(~10/26)의 홍보 글: 답글과 정보 공유로 신뢰를 먼저 쌓습니다

## 7일 뒤 보고할 숫자 (2026-10-31)

- North Star: 진짜 고객 반응 수, Day 1 → Day 7
- 루브릭 통과 대상 수와 통과율
- 채널·훅별 조회·댓글 변화, 대행의뢰 리드 수·응답 수·회신 수
- `learnings.md` git 이력: 루프가 바꾼 결정들
