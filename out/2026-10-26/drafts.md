# 초안 2026-10-26
> 학습 반영: (1) 오늘 받은 대행의뢰 리드 4건 모두에 무료 진단 제안 회신을 쓰고, 게시 뒤 `lead-reply`로 기록해 리드 상태가 new에서 넘어가게 했습니다. (2) 게시판 글에 무료 진단 권유를 넣으면 "가입 초기 홍보 금지" 규칙과 부딪혀서 넣지 않았습니다. 대신 글 끝에 실무자가 답하기 쉬운 질문을 두어 댓글을 먼저 노렸고, 이미 올린 h-supplements-best5-1 글을 고치는 일은 사람 판단으로 남겼습니다.

## 1. 오픈채팅방 메시지

### room-ai
AI로 콘텐츠 초안을 쓸 때 숫자 검증을 어디까지 하시나요? 전기요 질문 10개를 AI 5곳에 3번씩 물어 답변 135건을 봤습니다. 같은 Gemini가 같은 질문에 EMF 인증 기준을 한 번은 "전기장 10V/m 이하"로 맞게, 다른 한 번은 "30V/m 이하"로 다르게 답했습니다. Gemini는 "전기요 추천해줘" 같은 평범한 질문 30건 중 5건을 거절하기도 했는데, 같은 질문을 다시 물으면 브랜드를 꼽아 답한 적이 있었습니다. 업무에 AI 답변을 쓰실 때 같은 질문을 여러 번 돌려 보시는지, 아니면 공식 자료로 바로 확인하시는지 궁금합니다.

### room-content
블로그 콘텐츠를 기획할 때 "AI가 이 글을 인용할까"도 따져 보시나요? 커피 프랜차이즈 질문으로 AI 답변을 모아 인용 출처 도메인을 세 보니 네이버 블로그(32회)와 유튜브(29회)가 가장 많았고, 네이버 카페(19회)가 뒤를 이었습니다. 브랜드 공식 사이트는 상위 10개에 없었습니다. 리포트마다 상위 10개 도메인만 집계한 값이라 전체 인용 수는 아닙니다. 브랜드 블로그를 운영하시는 분들은 공식 채널과 블로그 체험단 콘텐츠 사이에서 비중을 어떻게 나누고 계신지 궁금합니다.
측정 방법 원문: https://aeobot.ai/blog/korea-coffee-brands-ai/?utm_source=iboss&utm_medium=room-content&utm_campaign=korea-coffee-brands-ai&utm_content=h-korea-coffee-brands-ai-1

## 2. 게시판 글

### board-aeo
**제목: 전기요를 AI 5곳에 물었더니 네이버 AI 브리핑은 절반 넘게 브랜드를 꼽지 않았습니다 (답변 135건 관찰)**

날이 추워지면서 "전기요 추천해줘" 같은 질문이 늘고 있어서, AI 답변에 어떤 브랜드가 나오는지 직접 확인해 봤습니다. 제품을 평가하는 글이 아니라 답변에 무엇이 나왔는지를 적은 관찰 기록입니다.

**측정 방법**
- 2026년 10월 25~26일에 ChatGPT, Perplexity, Gemini, Google AI 개요, 네이버 AI 브리핑에 물었습니다.
- 질문 10개를 AI마다 3번씩 물어 답변 135건을 분석했습니다.
- 로그인하지 않은 환경에서 물었습니다.

**관찰한 것**
1. **상위 브랜드는 두 곳으로 모였습니다.** 답변 135건에 브랜드 25곳이 나왔고, 그중 12곳은 답변 한 건에만 나왔습니다. 한일의료기는 62건(46%), 보국전자는 59건(44%)에 나왔습니다.
2. **그다음 순위는 AI마다 달랐습니다.** 이메텍은 Google AI 개요 답변 27건 중 16건(59%)에 나왔지만, ChatGPT에서는 14%, Perplexity에서는 13%였고 네이버 AI 브리핑에는 한 번도 나오지 않았습니다. 답변 맨 앞에 놓인 브랜드도 AI마다 달랐습니다.
3. **네이버 AI 브리핑은 브랜드 대신 고르는 기준을 줬습니다.** 브랜드를 물은 질문의 답변 21건 중 12건이 브랜드 없이 소비전력, 자동 전원 차단, EMF 인증 같은 기준만 정리했습니다.
4. **AI는 질문 범위를 넓혀 답했습니다.** 135건 중 104건이 탄소매트를 함께 다뤘습니다. 그래서 다나와 '전기요' 인기상품순 상위 29개에 없는 경동나비엔과 귀뚜라미도 자주 나왔습니다. 반대로 다나와 상위에 있던 위켄드하우스, 크리벨, 엔뚜마노는 AI 답변에 한 번도 나오지 않았습니다.

**한계**
- 이틀 동안 한 번 측정한 결과이고, AI 답변은 날마다 바뀔 수 있습니다.
- 다나와 순위는 10월 25일 밤 한 시점의 한 쇼핑몰 순위라서 전체 시장 점유율이 아닙니다.

브랜드 담당자 입장에서 보면 3번이 가장 고민되는 부분입니다. 네이버 AI 브리핑에는 브랜드명이 없고 기준만 나오면, 그 답변에 "나왔다"고 볼지 "안 나왔다"고 볼지부터 애매합니다. 클라이언트나 윗선에 AI 노출을 보고하실 때 이런 답변은 어떻게 분류하고 계신지 의견 듣고 싶습니다.

(질문 목록과 AI별 상세 수치: https://aeobot.ai/blog/electric-blanket-ai/?utm_source=iboss&utm_medium=board-aeo&utm_campaign=electric-blanket-ai&utm_content=h-electric-blanket-ai-1)

## 3. 답글
없음 (체크리스트를 통과한 답글 후보가 없습니다)

## 4. 의뢰 응답
※ 학습 노트에는 new 리드가 5건으로 적혀 있지만, 오늘 입력에 들어온 리드는 4건입니다. 나머지 1건은 스코어카드에서 URL을 확인해야 합니다.

### 통검 영역 웹사이트 seo 작업 가능한 곳 찾습니다
https://www.i-boss.co.kr/ab-1958-88939

안녕하세요, AI 검색 노출을 측정하는 aeobot입니다.
먼저 솔직하게 말씀드리면, 저희는 웹사이트 SEO를 직접 작업하는 업체가 아닙니다. 그래서 요청하신 단가, 노출 기간, A/S 항목에는 답을 드릴 수 없습니다.

다만 통검이 불안정하다고 하셔서 함께 보시면 좋을 부분을 말씀드립니다. 지금 네이버는 통검 위에 AI 브리핑이 뜨는 경우가 있습니다. 저희가 전기요 질문으로 측정해 보니, 네이버 AI 브리핑은 브랜드를 물은 답변 21건 중 12건에서 업체명 없이 고르는 기준만 정리했습니다. 업종마다 결과가 다르기 때문에 집수리·인테리어 키워드에서 AI 브리핑이 업체를 꼽는지, 꼽는다면 어떤 출처를 인용하는지 먼저 보시면 SEO 업체를 고를 때 판단 근거가 됩니다.

원하시면 집수리·인테리어 대표 질문 몇 개로 네이버 AI 브리핑, Google AI 개요, ChatGPT 답변을 무료로 진단해 드리겠습니다. 측정 날짜와 환경도 함께 적어 드립니다. 노출을 약속드리는 서비스는 아니고, 현재 상태를 기록해 드리는 것입니다.
측정 사례: https://aeobot.ai/blog/electric-blanket-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=electric-blanket-ai&utm_content=h-electric-blanket-ai-2

### 구글 SEO·네이버 검색노출·백링크 구축 및 월 관리 가능한 전문 업체 찾습니다
https://www.i-boss.co.kr/ab-1958-88835

안녕하세요, AI 검색 노출을 측정하는 aeobot입니다. 저희는 SEO 작업이나 백링크 구축, CPC 운영을 하지 않습니다. 대신 사이트를 여러 개 운영하실 계획이라면 월 관리 성과를 볼 때 참고하실 만한 내용을 말씀드립니다.

구글 검색 결과 위에는 Google AI 개요가 뜨고, 같은 질문이라도 AI마다 꺼내는 이름이 다릅니다. 저희 측정에서 한 브랜드가 Google AI 개요 답변에는 59% 나왔지만 ChatGPT와 Perplexity에서는 13~14%였고, 네이버 AI 브리핑에서는 0%였습니다. 커피 프랜차이즈 측정에서는 AI가 인용한 출처 상위 10개에 브랜드 공식 사이트가 없었고, 네이버 블로그와 유튜브가 가장 많았습니다. 백링크와 SEO 작업이 AI 답변까지 이어지는지는 따로 측정해야 확인할 수 있습니다.

원하시면 운영 중인 사이트의 핵심 질문으로 Google AI 개요, 네이버 AI 브리핑, ChatGPT 답변을 무료로 진단해 드리겠습니다. 업체를 맡기시기 전 기준점으로 쓰실 수 있습니다.
측정 사례: https://aeobot.ai/blog/korea-coffee-brands-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=korea-coffee-brands-ai&utm_content=h-korea-coffee-brands-ai-2

### SEO/GEO/유튜브숏츠검색노출 건기식/화장품 실행사 찾습니다
https://www.i-boss.co.kr/ab-1958-88771

안녕하세요, aeobot입니다. 저희는 GEO 답변 작업을 하는 실행사가 아니라, ChatGPT 같은 AI 답변에 브랜드가 어떻게 나오는지 측정하는 쪽입니다. 그래서 실행사를 고르실 때와 작업 효과를 확인하실 때 쓰실 수 있는 기준을 드릴 수 있습니다.

ChatGPT 답변은 같은 질문을 다시 물어도 자주 바뀝니다. 커피 브랜드 측정에서 AI와 질문 조합 26개 중 세 번 모두 같은 브랜드가 맨 앞에 나온 경우는 13개였고, 상위 3개가 세 번 모두 같았던 경우는 7개뿐이었습니다. 그래서 실행사가 보여 주는 화면 한 장으로는 작업 효과를 판단하기 어렵고, 같은 질문을 여러 번 물어 작업 전후를 비교해야 합니다.

건기식·화장품 대표 질문으로 ChatGPT를 포함한 AI 답변에서 브랜드와 경쟁사가 어떻게 나오는지 무료로 진단해 드리겠습니다. 실행사 미팅 전에 기준점으로 쓰실 수 있습니다. 미팅도 가능합니다.
측정 사례: https://aeobot.ai/blog/korea-coffee-brands-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=korea-coffee-brands-ai&utm_content=h-korea-coffee-brands-ai-3

### 구글검색작업 가능하신분 연락 부탁드립니다
https://www.i-boss.co.kr/ab-1958-88762

안녕하세요, aeobot입니다. 저희는 구글 검색 작업 실행사가 아니라서 후불 작업은 맡을 수 없습니다. 다만 노출 후 결제로 진행하신다면 "노출"을 어떻게 확인할지가 중요해서 말씀드립니다.

구글 검색 결과 위에 뜨는 Google AI 개요는 같은 질문에도 다른 AI와 결과가 꽤 다릅니다. 저희 전기요 측정에서 Google AI 개요는 답변 하나에 모델명을 평균 1.8개 적었고, 특정 브랜드를 다른 AI보다 4배 넘게 자주 꺼냈습니다. 고객사에 노출을 보고하실 때 일반 검색 결과와 AI 개요를 나눠 보여 주시면 정산 기준이 더 분명해집니다.

필요하시면 맡고 계신 고객사 키워드 몇 개로 Google AI 개요와 다른 AI 답변을 무료로 진단해 드리겠습니다. 고객사 보고 자료로 쓰실 수 있게 측정일과 환경도 함께 적어 드립니다.
측정 사례: https://aeobot.ai/blog/electric-blanket-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=electric-blanket-ai&utm_content=h-electric-blanket-ai-3

## 5. 오늘 기록할 것
- `uv run python -m loop log --channel room-ai --kind chat --url https://www.i-boss.co.kr/ab-5545-149 --hook h-electric-blanket-ai-4 --campaign electric-blanket-ai`
- `uv run python -m loop log --channel room-content --kind chat --url https://www.i-boss.co.kr/ab-5545-146 --hook h-korea-coffee-brands-ai-1 --campaign korea-coffee-brands-ai`
- `uv run python -m loop log --channel board-aeo --kind post --url <게시한 URL> --hook h-electric-blanket-ai-1 --campaign electric-blanket-ai`
- `uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88939 --hook h-electric-blanket-ai-2 --campaign electric-blanket-ai`
- `uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88835 --hook h-korea-coffee-brands-ai-2 --campaign korea-coffee-brands-ai`
- `uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88771 --hook h-korea-coffee-brands-ai-3 --campaign korea-coffee-brands-ai`
- `uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88762 --hook h-electric-blanket-ai-3 --campaign electric-blanket-ai`
