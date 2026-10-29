# 초안 2026-10-29
> 학습 반영: ① 대행의뢰 리드 4건에 모두 무료 진단 제안 회신을 쓰고, 5번에 리드별 `lead-reply` 기록 명령을 넣어 상태 변화가 스코어카드에 보이게 했다. 오늘 받은 리드는 4건이라 노트에 적힌 나머지 1건은 ledger에서 확인해야 한다. ② board-aeo 글은 마케터가 자기 경험으로 답할 수 있는 질문으로 끝냈고, 무료 진단 안내는 넣지 않았다. 주제는 h-supplements-best5-1과 같은 "추천 브랜드 목록" 형식을 따랐다. 다만 영양제 글 본문이 오늘 입력에 없어서 숫자는 쓸 수 없고, 롱패딩 글(아직 board-aeo에 안 올림)로 대신했다. **게시 첫날에는 댓글을 확인하고 바로 답글을 달아야 한다.**

## 1. 오픈채팅방 메시지

### room-ai
3D 프린터 질문 10개를 AI 5곳에 3번씩 물어 봤는데, 답변이 인용한 출처 가운데 두 번째로 많은 곳이 뱀부랩 한국 공식 스토어(50번)였습니다. "A1 mini 공식 스토어 약 30만 원대부터" 같은 문장이 답변에 거의 그대로 들어갔습니다. 반면 Perplexity는 같은 스토어를 인용하면서도 A1을 "약 46만 9천 원부터"라고 했는데, 측정 당일 스토어 정가는 41만 9천 원이었습니다. 예전 가격이 남아 있던 것으로 보입니다. 혹시 AI가 자사몰이나 상품 페이지를 읽어 간다는 것을 전제로 페이지 업데이트 주기를 바꾸신 분 계신가요? 측정 기록은 여기 있습니다: https://aeobot.ai/blog/3d-printer-ai/?utm_source=iboss&utm_medium=room-ai&utm_campaign=3d-printer-ai&utm_content=h-3d-printer-ai-1

### room-content
롱패딩 질문을 AI 5곳에 물어 봤는데, Google AI 개요 답변 30건 중 6건이 2025년 12월에 쓰인 네이버 블로그 글 하나를 출처로 달았습니다. "판매량·검색량·재구매율 기준 객관적 랭킹"이라는 제목인데 숫자는 하나도 없는 글이었습니다. 그런데 그 글의 "3년 연속 롱패딩 판매 상위권" 같은 표현이 답변에 거의 그대로 옮겨졌습니다. 네이버 데이터랩으로 보면 그 글이 1위로 꼽은 브랜드는 검색 관심도에서 비교한 13곳 중 9위여서, "검색량 1위"라는 말과는 맞지 않았습니다. 순위형 콘텐츠를 만드실 때 기준과 근거 숫자를 본문에 어디까지 밝히시나요? https://aeobot.ai/blog/long-padding-ai/?utm_source=iboss&utm_medium=room-content&utm_campaign=long-padding-ai&utm_content=h-long-padding-ai-2

## 2. 게시판 글

### board-aeo
**제목: 롱패딩 추천을 AI 5곳에 물었더니, 검색 관심도 1~6% 수준의 SPA 브랜드가 아웃도어보다 자주 나왔습니다**

겨울 시즌 브랜드를 맡고 계신 분들께 참고가 될까 싶어 측정 기록을 공유합니다.

**측정 방법**
- 10월 28일, "롱패딩 추천해줘", "20대 여자", "10만원대", "노스페이스랑 디스커버리 중 뭐가 나아?" 등 실제로 물어볼 법한 질문 10개
- ChatGPT, Perplexity, Gemini, Google AI 개요, 네이버 AI 브리핑에 각각 3번씩 물어 답변 136건 수집
- 브랜드 비율은 브랜드 추천을 물은 질문 8개의 답변 106건 기준

**AI가 자주 꺼낸 브랜드**
- 노스페이스 64%, 디스커버리 60%, K2 47%
- 그 바로 뒤에 무신사 스탠다드 46%, 스파오 44%, 탑텐 42%
- 아이더 25%, 코오롱스포츠 16%, 네파 16%

무신사 스탠다드, 스파오, 탑텐은 네이버 데이터랩 검색 관심도가 노스페이스의 1~6% 수준입니다. 그런데도 가성비를 묻지 않은 질문(79건)에서 무신사 스탠다드는 39%, 스파오는 37%, 탑텐은 32%에 나왔습니다. 아이더(24%)와 네파(14%)보다 많습니다.

**답변이 인용한 출처**
쇼핑몰 무신사가 89번으로 네이버 블로그 다음으로 많았습니다. 노스페이스 공식몰이 77번, LF몰이 69번이었고 다나와는 14번이었습니다. 무신사는 무신사 스탠다드를 직접 파는 곳이기도 합니다. 가습기를 측정했을 때는 한국소비자원 비교시험 자료가 브랜드 목록을 크게 좌우했는데, 롱패딩에서는 쇼핑몰과 공식몰이 그 역할을 하는 것으로 보였습니다.

**한계**
- 하루, 로그인하지 않은 환경에서 한 번 측정한 결과입니다. AI 답변은 날마다 바뀔 수 있습니다.
- 검색 관심도는 상대 지수이고 검색량이 아닙니다. 쇼핑몰 안에서 바로 검색하는 비중이 크면 실제보다 낮게 잡힐 수 있습니다.

전체 기록: https://aeobot.ai/blog/long-padding-ai/?utm_source=iboss&utm_medium=board-aeo&utm_campaign=long-padding-ai&utm_content=h-long-padding-ai-1

**여쭤보고 싶은 것**
담당하시는 업종에서 AI 답변이 인용한 출처를 직접 따라가 보신 적이 있다면, 어디가 가장 많았나요? 쇼핑몰, 공식몰, 블로그, 공공기관 자료 가운데 업종마다 다를 것 같아서 경험을 듣고 싶습니다.

## 3. 답글
없음 (오늘 체크리스트를 통과한 답글 후보 글이 없음)

## 4. 의뢰 응답

### 통검 영역 웹사이트 seo 작업 가능한 곳 찾습니다
https://www.i-boss.co.kr/ab-1958-88939

안녕하세요, aeobot입니다. 먼저 솔직히 말씀드리면, 저희는 웹사이트 SEO 작업을 대행하는 곳이 아닙니다. ChatGPT·Gemini·Google AI 개요·네이버 AI 브리핑 답변에 브랜드와 사이트가 어떻게 나오는지 측정하는 서비스입니다. 그래서 요청하신 단가나 노출 소요 기간 같은 항목에는 답을 드릴 수 없습니다.

다만 통검이 불안정해서 웹사이트로 방향을 바꾸신다면 함께 봐 두실 만한 부분이 있습니다. 저희가 3D 프린터 질문을 AI 5곳에 물어 봤을 때, 답변이 두 번째로 많이 인용한 출처가 한 브랜드의 한국어 공식 스토어(50번)였습니다. 자사 웹페이지 내용이 AI 답변에 그대로 쓰인 사례입니다. (https://aeobot.ai/blog/3d-printer-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=3d-printer-ai&utm_content=h-3d-printer-ai-2)

집수리·인테리어 키워드로 AI 답변에 어떤 업체와 출처가 나오는지 무료 AI 노출 진단을 해 드릴 수 있습니다. SEO 업체를 고르신 뒤 작업 전후를 비교하는 기준 자료로 쓰셔도 됩니다. 필요하시면 대상 키워드 몇 개를 알려 주세요. 노출을 보장해 드리는 것은 아니고, 현재 상태를 측정해서 보여 드리는 것입니다.

### 구글 SEO·네이버 검색노출·백링크 구축 및 월 관리 가능한 전문 업체 찾습니다
https://www.i-boss.co.kr/ab-1958-88835

안녕하세요, aeobot입니다. 저희는 SEO·백링크 실행사가 아니라 AI 검색 답변에 브랜드가 어떻게 나오는지 측정하는 서비스라서, 월 관리 업체로 지원드리기는 어렵습니다.

다만 구글 SEO를 맡기신다면 Google AI 개요도 함께 보시는 게 좋겠습니다. 저희가 롱패딩 질문을 측정했을 때, Google AI 개요 답변 30건 중 6건이 네이버 블로그 글 하나를 출처로 달았고 그 글의 표현이 답변에 거의 그대로 옮겨졌습니다. 어떤 페이지가 출처로 잡히느냐에 따라 답변 내용이 달라질 수 있다는 사례입니다. (https://aeobot.ai/blog/long-padding-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=long-padding-ai&utm_content=h-long-padding-ai-3)

운영 중인 웹사이트와 앱을 대상으로 무료 AI 노출 진단을 해 드릴 수 있습니다. 핵심 키워드로 ChatGPT, Gemini, Google AI 개요, 네이버 AI 브리핑에 현재 어떻게 나오는지 정리해 드립니다. 업체를 선정하신 뒤 월 관리 성과를 확인하는 기준선으로 쓰실 수 있습니다.

### SEO/GEO/유튜브숏츠검색노출 건기식/화장품 실행사 찾습니다
https://www.i-boss.co.kr/ab-1958-88771

안녕하세요, aeobot입니다. 저희는 ChatGPT 답변 작업을 해 드리는 실행사가 아니라, AI 답변에 브랜드가 어떻게 나오는지 측정하는 서비스입니다. 다만 GEO 실행사를 고르시기 전후로 현재 상태를 측정해 두시면 실행사 성과를 판단하는 데 쓰실 수 있어서 연락드립니다.

ChatGPT가 무엇을 근거로 브랜드를 꺼내는지 보여 주는 사례가 있습니다. 가습기 질문을 측정했을 때 ChatGPT는 답변 20건 중 9건에서 한국소비자원 비교시험을 직접 언급했고, 시험 대상이던 쿠쿠를 11건에 꺼냈습니다. 같은 질문을 받은 Gemini와 네이버 AI 브리핑에서는 쿠쿠가 한 번도 나오지 않았습니다. 같은 브랜드라도 AI마다 기대는 자료가 다르다는 뜻입니다. (https://aeobot.ai/blog/humidifier-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=humidifier-ai&utm_content=h-humidifier-ai-2)

건기식·화장품 제품 키워드로 무료 AI 노출 진단을 해 드릴 수 있습니다. ChatGPT를 중심으로, 다른 AI에서는 어떻게 나오는지도 함께 비교해 드립니다. 미팅도 가능합니다. 답변 노출을 보장하는 작업은 하지 않고, 측정 결과와 그 한계를 그대로 보여 드립니다.

### 구글검색작업 가능하신분 연락 부탁드립니다
https://www.i-boss.co.kr/ab-1958-88762

안녕하세요, aeobot입니다. 저희는 구글 검색 작업을 하는 실행사가 아니라서 후불제 실행으로 도와드리기는 어렵습니다. 대신 대행사 입장에서 클라이언트에게 보고하실 때 쓰실 수 있는 부분이 있어 말씀드립니다.

구글 검색 결과 위에 붙는 Google AI 개요는 일반 검색 결과와 다르게 움직이기도 합니다. 저희가 3D 프린터 질문을 측정했을 때, 국내 브랜드는 Google AI 개요의 "브랜드별 장단점 비교" 답변 3건에만 나왔습니다. 판매 순위 상위권인 다른 국내 브랜드는 한 번도 나오지 않았습니다. (https://aeobot.ai/blog/3d-printer-ai/?utm_source=iboss&utm_medium=lead&utm_campaign=3d-printer-ai&utm_content=h-3d-printer-ai-3)

구글 물량을 맡기시는 클라이언트 키워드 중 몇 개로 무료 AI 노출 진단을 해 드릴 수 있습니다. 작업 전 기준선으로 남겨 두시면 클라이언트 보고에 같이 쓰실 수 있습니다.

## 5. 오늘 기록할 것
```
uv run python -m loop log --channel room-ai --kind chat --url https://www.i-boss.co.kr/ab-5545-149 --hook h-3d-printer-ai-1 --campaign 3d-printer-ai
uv run python -m loop log --channel room-content --kind chat --url https://www.i-boss.co.kr/ab-5545-146 --hook h-long-padding-ai-2 --campaign long-padding-ai
uv run python -m loop log --channel board-aeo --kind post --url <게시한 URL> --hook h-long-padding-ai-1 --campaign long-padding-ai
uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88939 --hook h-3d-printer-ai-2 --campaign 3d-printer-ai
uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88835 --hook h-long-padding-ai-3 --campaign long-padding-ai
uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88771 --hook h-humidifier-ai-2 --campaign humidifier-ai
uv run python -m loop log --channel lead --kind lead-reply --url https://www.i-boss.co.kr/ab-1958-88762 --hook h-3d-printer-ai-3 --campaign 3d-printer-ai
```

게시 전에 확인할 것:
- **리드 상태:** `lead-reply`를 기록해도 리드 상태가 new에서 바뀌지 않으면, 스코어카드에 나흘째 같은 숫자가 나온 이유가 기록 누락이 아니라 이 부분일 수 있습니다. 기록한 뒤 ledger에서 상태가 바뀌었는지 확인해 주세요.
- **다섯 번째 리드:** 노트에는 new 리드가 5건인데 오늘 받은 목록은 4건입니다. ledger에서 나머지 1건을 찾아 회신해야 합니다.
- **board-aeo 첫날 댓글:** 학습 노트 2번에 따라, 글을 올린 날 달린 댓글에는 바로 답글을 달아 주세요.
