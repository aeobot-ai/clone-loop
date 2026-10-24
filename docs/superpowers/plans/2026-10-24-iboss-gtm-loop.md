# aeobot 아이보스 GTM 루프 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 매일 한 번 aeobot 블로그 글과 아이보스 게시판을 읽어 초안을 만들고, 사람이 올린 게시물의 반응을 재서 `learnings.md`로 다음 초안을 개선하는 루프.

**Architecture:** 작은 Python 패키지 `loop/`. 웹 읽기는 Firecrawl REST(아이보스는 Cloudflare가 일반 요청을 403으로 막음), 초안·학습은 headless `claude -p`(blogs-gen과 같은 방식, API 키 불필요). 순수 함수(파서·UTM·스코어카드)는 단위 테스트, 네트워크·LLM은 주입 가능한 함수로 분리. 산출물은 레포 안 파일로 커밋.

**Tech Stack:** Python 3.12, uv, requests, pytest.

**Spec:** `docs/superpowers/specs/2026-10-24-iboss-gtm-loop-design.md`

## Global Constraints

- 마감: 2026-10-24 17:30 KST에 레포 제출. 이후 7일(~10-31) 매일 1회 실행.
- 아이보스 자동 게시 금지. 루프는 읽기·초안·측정·학습만 한다.
- 비밀값은 환경변수: `FIRECRAWL_API_KEY`(필수), `GA4_PROPERTY_ID`/`GOOGLE_APPLICATION_CREDENTIALS`(선택, 이번 범위 밖). 비밀값을 파일·로그에 쓰지 않는다.
- UTM 형식: `utm_source=iboss&utm_medium=<채널>&utm_campaign=<블로그 slug>&utm_content=<훅 id>`.
- 초안 톤: 블로그와 같은 관찰 기록 톤, 블로그에 없는 수치 금지, "노출 보장" 류 표현 금지. 새 계정 첫 3일(10-24~10-26)은 답글·정보 공유만, 홍보 게시판 글 금지.

- 대표 지표(North Star): **루브릭을 통과한 마케터에게서 받은 반응 수**(내 게시물·답글에 달린 댓글, 쪽지, 의뢰 회신). ledger `kind=response` 행으로 기록, 스코어카드 맨 위에 표시.
- 진짜 고객 루브릭: `rubric.md`의 예/아니오 항목. 수집한 글·리드마다 LLM이 판정하고, 통과한 것에만 답글·제안 초안을 쓴다.
- 마감 정정: 제출 링크는 17:38에 닫힌다.

## 고정 값

- 블로그 RSS: `https://aeobot.ai/blog/rss.xml`
- 감시 게시판(Firecrawl markdown):
  - AEO·GEO `https://www.i-boss.co.kr/ab-6140?tag=AEO+GEO`
  - 블로그 마케팅 `https://www.i-boss.co.kr/ab-74613`
  - 질문답변 `https://www.i-boss.co.kr/ab-2109`
  - 병의원 `https://www.i-boss.co.kr/ab-7055`
  - AI `https://www.i-boss.co.kr/ab-6140?tag=AI`
- 대행의뢰(리드): `https://www.i-boss.co.kr/ab-1957&category_1=SEO`, `https://www.i-boss.co.kr/ab-1957&category_1=AI`
- 관련 키워드: `AEO, GEO, AI 검색, AI 브리핑, 챗GPT, ChatGPT, 제미나이, Gemini, 퍼플렉시티, Perplexity, 블로그 노출, 통검, 블탭, 상위노출, SEO, 검색최적화`
- 오픈채팅방 채널 id: `room-hospital, room-beauty, room-agency, room-inhouse, room-viral, room-content`

## 파일 구조

```
pyproject.toml
loop/__init__.py
loop/__main__.py      # CLI: run | log
loop/iboss.py         # 아이보스 markdown 파서 (순수)
loop/blog.py          # RSS 파서 (순수)
loop/utm.py           # UTM 붙이기 (순수)
loop/store.py         # ledger.csv / metrics.jsonl / leads.csv 읽기·쓰기
loop/web.py           # Firecrawl scrape, RSS GET
loop/llm.py           # claude -p 호출
loop/scorecard.py     # 채널·훅별 집계 → markdown (순수)
loop/run.py           # 하루 한 바퀴 조립
prompts/drafts.md     # 초안 프롬프트 템플릿
prompts/learn.md      # 학습 프롬프트 템플릿
learnings.md
data/ledger.csv  data/metrics.jsonl  data/leads.csv
out/YYYY-MM-DD/{drafts.md,scorecard.md,threads.md}
tests/fixtures/{post.md,board.md,rss.xml}
tests/test_*.py
scripts/daily.sh      # cron/launchd 진입점
README.md
```

## Review Focus

1. Firecrawl 실패(타임아웃·403·크레딧 소진) → 그 소스만 건너뛰고 나머지 단계는 계속, `out/<date>/errors.md`에 기록. (Task 4 테스트)
2. 숫자에 쉼표("1,896") → 정수 1896. (Task 1 테스트)
3. 같은 날 두 번 실행 → metrics는 (date,url) 중복 없이, 초안 파일은 덮어쓰기. (Task 3·4 테스트)
4. ledger가 비어 있는 첫날 → 스코어카드는 "아직 게시 기록 없음"을 출력하고 실패하지 않음. (Task 3 테스트)
5. `claude` CLI 실패 → 초안 단계에 오류를 남기고 측정·스코어카드는 저장. (Task 4 테스트)

---

### Task 1: 순수 파서 (아이보스·RSS·UTM)

**Files:** Create `pyproject.toml`, `loop/__init__.py`, `loop/iboss.py`, `loop/blog.py`, `loop/utm.py`, `tests/fixtures/post.md`, `tests/fixtures/board.md`, `tests/fixtures/rss.xml`, `tests/test_parsers.py`

**Interfaces — Produces:**
- `PostStats(views: int, likes: int, comments: int)` dataclass; `parse_post_stats(md: str) -> PostStats | None` — 본문의 `조회수 N`, `좋아요 N`, `댓글 N` 첫 등장값.
- `BoardRow(title: str, url: str, date: str, views: int, likes: int)`; `parse_board_rows(md: str) -> list[BoardRow]` — `| 분류 [제목](https://www.i-boss.co.kr/ab-…) N | 작성자 | MM.DD | 조회 | 좋아요 |` 형태의 표 행.
- `is_relevant(title: str) -> bool` — 고정 키워드 중 하나 포함(대소문자 무시).
- `BlogPost(slug: str, title: str, url: str, published: str, description: str)`; `parse_rss(xml: str) -> list[BlogPost]` 최신순.
- `with_utm(url: str, medium: str, campaign: str, content: str) -> str` — 기존 쿼리 보존.

- [ ] Step 1: 픽스처 저장. `post.md`는 Firecrawl로 받은 `ab-6141-72783` 본문 일부(“조회수 1,896 / 좋아요 13 / 댓글 20” 포함), `board.md`는 같은 페이지 하단 표 3행, `rss.xml`은 `curl https://aeobot.ai/blog/rss.xml`.
- [ ] Step 2: 테스트 작성
  - `parse_post_stats(post) == PostStats(1896, 13, 20)`; `parse_post_stats("no stats") is None`
  - `parse_board_rows(board)[0]` 의 `url` 이 `https://www.i-boss.co.kr/ab-6141-` 로 시작하고 `views` 가 int
  - `is_relevant("블로그 노출 현황들 여쭙습니다")` True, `is_relevant("치이카와는 왜 인기")` False, `is_relevant("perplexity 인용")` True
  - `parse_rss(rss)` 길이 ≥ 1, 첫 항목 `url` 이 `https://aeobot.ai/blog/` 로 시작, `slug` 가 URL 마지막 경로
  - `with_utm("https://aeobot.ai/blog/x/", "room-beauty", "x", "h1")` 에 네 파라미터 모두 포함, `with_utm("https://a.b/?q=1", …)` 에 `q=1` 보존
- [ ] Step 3: `uv run pytest tests/test_parsers.py` → FAIL 확인 → 구현 → PASS
- [ ] Step 4: Commit `feat: i-boss/RSS parsers and UTM helper`

### Task 2: 저장소 (ledger·metrics·leads)

**Files:** Create `loop/store.py`, `tests/test_store.py`, `data/ledger.csv`(헤더만), `data/leads.csv`(헤더만), `data/metrics.jsonl`(빈 파일)

**Interfaces — Produces:**
- ledger 헤더: `date,channel,kind,url,hook,campaign,note` (`kind` ∈ `post|reply|chat|lead-reply`; 오픈채팅은 `url` 빈칸)
- `LedgerRow` dataclass(위 필드); `read_ledger(path) -> list[LedgerRow]`; `append_ledger(path, row) -> None`
- `append_metrics(path, rows: list[dict]) -> int` — 각 row 는 `{date, url, views, likes, comments}`; 같은 `(date,url)` 이 이미 있으면 건너뜀, 추가한 수 반환. `read_metrics(path) -> list[dict]`
- leads 헤더: `found,url,title,category,status`; `upsert_leads(path, rows: list[dict]) -> list[dict]` — url 기준 신규만 추가하고 신규 목록 반환(`status` 기본 `new`).

- [ ] Step 1: 테스트 — `append_metrics` 두 번 같은 입력 → 두 번째 반환 0; `upsert_leads` 같은 url 두 번 → 두 번째 반환 `[]`; 빈 ledger 읽기 → `[]`.
- [ ] Step 2: FAIL → 구현(csv, json 표준 라이브러리) → PASS
- [ ] Step 3: Commit `feat: ledger, metrics and leads storage`

### Task 3: 스코어카드

**Files:** Create `loop/scorecard.py`, `tests/test_scorecard.py`

**Interfaces — Consumes:** `LedgerRow`, metrics dict. **Produces:** `build_scorecard(ledger: list[LedgerRow], metrics: list[dict], leads: list[dict], today: str) -> str` (markdown).

내용: (1) 채널별 표 `채널 | 게시 수 | 최신 조회 합 | 좋아요 합 | 댓글 합` — url 별 가장 최근 metrics 사용, (2) 훅별 같은 표, (3) 어제 대비 조회 증가(url 별 최신 − 직전), (4) 리드 수 `new/replied/meeting` 별 개수, (5) 오픈채팅(`kind=chat`) 은 게시 수만 표시하고 "UTM(GA4) 연결 전" 메모.

- [ ] Step 1: 테스트 — 빈 입력 → 결과에 `아직 게시 기록 없음`; ledger 2행(같은 채널) + metrics 3행(한 url 이틀치) → 채널 행에 게시 수 2, 조회 합은 최신값 기준; leads 2건(new 1, replied 1) → `new 1`, `replied 1` 포함.
- [ ] Step 2: FAIL → 구현 → PASS
- [ ] Step 3: Commit `feat: daily scorecard`

### Task 4: 웹·LLM 어댑터와 하루 실행

**Files:** Create `loop/web.py`, `loop/llm.py`, `loop/run.py`, `loop/__main__.py`, `prompts/drafts.md`, `prompts/learn.md`, `learnings.md`, `tests/test_run.py`

**Interfaces:**
- `scrape(url: str) -> str` — POST `https://api.firecrawl.dev/v2/scrape` body `{"url", "formats":["markdown"], "onlyMainContent": false, "maxAge": 0}`, 헤더 `Authorization: Bearer $FIRECRAWL_API_KEY`, 타임아웃 90s, `data.markdown` 반환; 실패 시 예외.
- `get(url: str) -> str` — RSS 용 requests GET.
- `ask(prompt: str) -> str` — `subprocess.run(["claude","-p",prompt], timeout=600)` stdout; 비정상 종료 시 예외.
- `run_day(today: str, root: Path, scrape=scrape, get=get, ask=ask) -> Path` — 단계 순서:
  1. measure: ledger 의 `url` 있는 행마다 `parse_post_stats(scrape(url))` → `append_metrics`
  2. collect: `parse_rss(get(RSS))` 상위 3개; 감시 게시판마다 `parse_board_rows` → `is_relevant` 필터 → `out/<date>/threads.md`; 대행의뢰 2개 URL 의 `parse_board_rows` 를 `is_relevant` 필터 없이 `upsert_leads`(category 는 URL 의 `category_1`)
  3. scorecard: `build_scorecard` → `out/<date>/scorecard.md`
  4. learn: `prompts/learn.md` 에 scorecard·현재 learnings 를 넣어 `ask` → 결과로 `learnings.md` 덮어쓰기(ledger 가 비면 건너뜀)
  5. drafts: `prompts/drafts.md` 에 블로그 글, threads, 신규 leads, learnings, today, 첫 3일 여부를 넣어 `ask` → `out/<date>/drafts.md`. 초안의 모든 aeobot 링크는 프롬프트가 `{{utm:<채널>:<slug>:<훅id>}}` 토큰으로 쓰게 하고, `run_day` 가 `with_utm` 으로 치환.
  - 각 단계 예외는 잡아서 `out/<date>/errors.md` 에 `단계: 메시지` 로 남기고 다음 단계 진행.
- CLI: `python -m loop run [--date YYYY-MM-DD]`; `python -m loop log --channel C --kind K [--url U] --hook H --campaign S [--note N]` → `append_ledger`(date=오늘 KST).

`prompts/drafts.md` 필수 내용: 대상(대기업 인하우스 마케터, 블로그 대행사 담당자), 채널별 출력 섹션(오픈채팅방 6개 각 1개, 게시판 글 1개, 고민 글 답글 상위 3개, 신규 리드별 의뢰 응답), 훅 id 규칙(`h-<slug>-<n>`), Global Constraints 의 톤·금지 규칙, 첫 3일 규칙, learnings 반영 지시.
`prompts/learn.md` 필수 내용: 스코어카드 숫자만 근거로, "잘 된 것 / 안 된 것 / 내일 바꿀 것 1~2개 / 근거 숫자" 형식, 근거 없는 추측 금지.

- [ ] Step 1: 테스트(가짜 scrape/get/ask 주입, tmp_path 루트)
  - 정상: `run_day` 후 `out/<date>/{drafts.md,scorecard.md,threads.md}` 존재, drafts 에 `{{utm:` 토큰이 남지 않고 `utm_source=iboss` 포함
  - scrape 가 항상 예외 → `errors.md` 존재, `scorecard.md` 와 `drafts.md` 는 여전히 생성
  - ask 가 예외 → `errors.md` 에 `drafts` 포함, `scorecard.md` 생성
  - 같은 날 두 번 실행 → metrics 줄 수 변화 없음
- [ ] Step 2: FAIL → 구현 → PASS (`uv run pytest`)
- [ ] Step 3: Commit `feat: daily run with firecrawl and claude adapters`

### Task 5: 실제 1회 실행·스케줄·README·제출

**Files:** Create `scripts/daily.sh`, `README.md`; 생성물 `out/2026-10-24/*`

- [ ] Step 1: `FIRECRAWL_API_KEY=… uv run python -m loop run` 실제 실행 → `out/2026-10-24/` 세 파일 생성, `errors.md` 없거나 원인 기록 확인.
- [ ] Step 2: `scripts/daily.sh` — 레포로 cd, `.env` 로드, `uv run python -m loop run`, `git add data out learnings.md && git commit -m "loop: <date>" && git push`. crontab 예시 `0 9 * * *` 를 README 에 기재(설치는 사용자 확인 후).
- [ ] Step 3: README — 루프 다이어그램, 매일 사람이 할 일(초안 확인 → 게시 → `python -m loop log …`), 7일 지표 정의, 안 하는 것(자동 게시).
- [ ] Step 4: Commit, GitHub 레포 생성·push(공개 여부 사용자 확인), Discord 제출 링크 전달.
