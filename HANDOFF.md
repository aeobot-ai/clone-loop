# 이어서 하기 (2026-10-24 16:2x KST 기준)

## 지금 상태
- 루프 구현 완료, 테스트 27개 통과 (`uv run pytest`).
- 10/24 첫 실행 완료: `out/2026-10-24/` (drafts·scorecard·threads). 체크리스트 통과 7 / 판정 11 (게시판 글 2, 대행의뢰 리드 5).
- 관찰: 아이보스 AEO·GEO 게시판 글은 대부분 경쟁 실행사(TheLogic, 소하AI, 온더AI, 오픈타임GEO, 라이즈유마케팅) 홍보 글이라 체크리스트 X1로 탈락. 진짜 고객은 블로그 마케팅 게시판과 대행의뢰에 있다.
- 첫 게시 기록: AEO·GEO 게시판 "강남 피부과, 네이버 지도 1위와 AI가 고르는 병원은 달랐습니다" https://www.i-boss.co.kr/ab-6141-72893 (16:07 게시, UTM 링크 포함, 측정 시점 조회 2).

## 남은 일
1. **제출 (17:38 마감)**: 레포가 비공개이므로 심사 측 GitHub 계정을 협업자로 추가하거나 공개로 바꾼 뒤 Discord에 링크 제출.
2. **매일 실행 (10/25~10/31)**: 매일 09:00 KST에 `uv run python -m loop run` 후 `data/ out/ learnings.md`를 커밋·푸시.
   - 필요한 비밀값: `FIRECRAWL_API_KEY`.
   - LLM 단계는 `claude -p`를 호출한다. 실행 환경에 `claude` CLI가 없으면 판정·학습·초안 단계가 `out/<날짜>/errors.md`에 오류를 남기고 측정·스코어카드만 생성된다. 그 경우 `loop/llm.py`의 `ask()`를 그 환경에서 쓸 수 있는 LLM 호출로 바꾼다.
3. **사람이 매일 할 일**: `out/<오늘>/drafts.md` 확인 → 아이보스에 직접 게시 → `python -m loop log ...`로 기록(README 참고). 반응(댓글·쪽지·의뢰 회신)은 `--kind response`로 기록 — 이것이 North Star.
4. **선택**: GA4 서비스 계정 키·속성 ID를 받으면 UTM 유입을 스코어카드에 추가.
5. **10/31 18:00까지**: Day 1 → Day 7 North Star, 전환(무료 진단 신청 5·유료 1 목표), 체크리스트 통과 수, 채널·훅별 조회 변화, 리드 응답 수, `learnings.md` 이력을 정리해 Discord에 공유.

## 참고
- 설계: `docs/superpowers/specs/2026-10-24-iboss-gtm-loop-design.md`
- 계획: `docs/superpowers/plans/2026-10-24-iboss-gtm-loop.md`
- 아이보스는 Cloudflare가 일반 HTTP를 403으로 막는다 → Firecrawl만 사용. Firecrawl 429는 자동 재시도.
