# NexSupply Conversational Sourcing Copilot v3
## 설계 통합본

지금까지 정리한

* Landed Cost + Risk Report v1
* Lead Intelligence Engine v2.1
* Conversational Copilot 리서치
* bdb 스타일 대화형 흐름 설명
* Rule based vs LLM 기반 설명

전부 합쳐서 한 번에 쓸 수 있는 버전으로 정리한 문서야.
Roo한테 줄 개발 브리프까지 포함해 둠.

---

## 1) 제품 정체성과 목표

**한 문장 정의**
NexSupply는 아시아 발주를 위한
AI 기반 소싱 인텔리전스 코파일럿이자
Tech 기반 에이전시의 두뇌다.

**역할**

1. 사용자가
   링크·텍스트·사진 중 어느 것으로든 제품을 입력하면
   관세와 물류비를 포함한 Landed Cost와
   카테고리별 Risk를 계산해 준다.
2. 대화형 Copilot이 몇 가지 질문을 통해
   수입 국가·채널·물량·타임라인·리스크 우선순위를
   자연스럽게 끌어낸다.
3. 뒤에서는 Lead Intelligence Engine이
   이 리드를 점수화하고
   진짜 발주 가능성이 있는 사람만
   에이전시로 라우팅한다.

**비즈니스 관점 핵심**

* 앱 자체가 최종 상품이 아니라
  발주를 만들어 내는 퍼널의 앞단이다.
* Quick Scan과 Conversational Copilot은
  전부
  아버지 인프라로 이어지는 발주 엔진에 먹이를 주는 장치다.

---

## 2) 과거 챗봇 vs NexSupply 방식

### 과거 방식  Rule based 챗봇

* 미리 만든 질문 트리
  예를 들어
  가격 관련 질문이면 준비된 멘트를 그대로 출력
* 사용자가 의도 밖 질문을 하면
  이해하지 못했습니다 같은 답만 반복
* 스크립트가 조금만 복잡해지면
  유지보수와 확장이 힘듦

### NexSupply 방식  LLM 기반 하이브리드

* 실시간 LLM을 사용하지만
  완전 자유가 아니라
  시스템 프롬프트와 가이드라인 안에서 움직이게 만든다.
* 구조는 다음 세 가지가 핵심

  1. 준비된 목표와 규칙
     시스템 프롬프트에서
     꼭 알아내야 하는 정보와 질문 스타일을 정의
  2. 실시간 Reasoning
     어떤 질문을 언제 할지
     어떤 말투로 답할지
     LLM이 문맥을 보고 스스로 판단
  3. 함수 호출  Function Calling
     대화 도중에
     필요한 정보를 백엔드 구조체로 추출하고
     우측 패널 Landed Cost와 Risk 패널을 계속 업데이트

이 구조 덕분에
사용자가 갑자기
관세가 너무 무서워요 같은 딴소리를 해도

* 예전 챗봇은
  물량을 먼저 입력해 주세요 같은 딱딱한 답만 했을 것
* NexSupply Copilot은
  관세 걱정이 크시군요
  대략 몇 개 정도 수량을 생각하고 계신지 알려주시면
  관세까지 포함해서 실제 도착 단가를 계산해 볼게요

이렇게 사람처럼 받으면서도
우리가 원하는 정보 수집 로직을 깨지 않는다.

---

## 3) 전체 UX 플로우  Quick Scan에서 Copilot까지

### Step 1  Quick Scan

* 입력
  하나의 텍스트 필드
  Paste a product link or description
* 처리
  기존 Landed Cost + Risk Report API 호출
* 결과
  제품 타입·HTS 코드 후보·비용 분해·리스크 스코어를
  카드 형태로 보여줌

여기까지가 유입과 첫 번째 마법 순간
사용자가
와 이 정도면 진짜 계산 잘해 주네
를 느끼는 지점.

### Step 2  Copilot로 초대

Report 카드 아래에
버튼 하나

* Ask NexSupply Copilot
  또는
* Make this estimate more accurate

를 배치한다.

버튼을 누르면 화면이 확장된다.

### Step 3  Split UI  좌측 채팅  우측 라이브 리포트

* 왼쪽
  NexSupply Analyst와 사용자 채팅 인터페이스
  말풍선 형태
* 오른쪽
  Live Landed Cost + Risk Panel
  이미 나온 견적에 대해

  * 사용자가 답을 줄수록
    confidence 퍼센트가 올라간다.
  * missing info 목록과
    assumptions 목록도 함께 보인다.

예시 흐름

1. Copilot
   지금까지 입력해 주신 내용 기준으로
   미국 FBA 기준 대략 이런 비용 구조가 예상됩니다.
   몇 가지 더 여쭤보면
   정확도가 올라가요.
   먼저 수입 국가는 어디인가요
2. 유저
   미국이에요.
3. Copilot
   미국 FBA 입점이 목표군요
   첫 발주 수량은 어느 정도 생각하고 계신가요
   500개 1000개 같은 대략 숫자로 말씀해 주셔도 괜찮아요

같은 식으로 항상 한 번에 질문 하나만 던진다.

### Step 4  사진·링크·텍스트 유연 처리

사용자는 항상 이런 상태일 수 있다.

* 링크만 있고 사진 없음
* 사진만 있고 정확한 텍스트 설명 없음
* 아무것도 준비되지 않고 그냥
  곰돌이 젤리 같은 제품 하고 싶어요
  수준으로 들어옴

Copilot 규칙

* 사진이나 링크가 없으면
  없다고 해도 된다고 먼저 안심시킨다.
  예시
  사진이나 링크 없어도 괜찮아요
  그냥 대략 어떤 제품인지만 설명해 주셔도 됩니다.
* 이미지가 올라오면
  Vision 모델로 카테고리·재질·패키징 힌트를 뽑고
  리포트를 업데이트
* 링크가 있으면
  기존 Quick Scan 분석 결과를
  컨텍스트로 사용

### Step 5  대화 종료와 CTA

어느 정도 정보가 쌓이면 Copilot이

1. 대화 요약
2. Proceed  Proceed with caution  Not recommended 중 하나의 Verdict
3. 다음 액션을 제안

을 해 준다.

예시

* 요약
  미국 FBA로 스테인리스 텀블러를
  처음 1000개 정도 테스트 발주하려고 하시고
  관세와 품질 리스크를 가장 걱정하고 계십니다.
* Verdict
  현 시점 estimate 기준으로는
  관세와 물류비 포함 Landed Cost가 이 정도
  품질 리스크는 공장 검증 여부에 따라 꽤 달라질 수 있어서
  proceed with caution에 가깝습니다.
* CTA
  이 조건 기준으로
  실제 공장 리스트와 견적을 받아 보고 싶으시면
  이름과 이메일만 남겨 주시면
  저희 팀이 맞는 공장을 찾아 드릴 수 있어요.

이 단계에서 수집되는 리드는
Lead Intelligence Engine으로 바로 들어간다.

---

## 4) 아키텍처 개요  세 단계 엔진

### A  시스템 프롬프트  브레인 매뉴얼

AI에게 단순 질문 목록이 아니라
역할과 목표를 넘긴다.

예시 개념

* 너는 NexSupply의 소싱 컨설턴트

* 반드시 알아내야 하는 정보

  * 수입 국가
  * 판매 채널
  * 예상 첫 발주 수량 또는 예산 범위
  * 목표 타임라인
  * 사용자가 가장 걱정하는 리스크

* 한 번에 질문 하나

* 사용자가 모른다고 하면
  그대로 인정하고 보수적인 가정으로 처리

이 지침을 기반으로
LLM이 매 턴마다 어떤 질문을 할지 스스로 고른다.

### B  LLM API 호출  실시간 Reasoning

프론트에서 오는 정보

* message history
* current report 상태
* optional image url
* optional lead analysis 일부

를 LLM으로 보낸다.

LLM은

* 지금까지의 대화를 읽고
* 다음에 어떤 질문을 해야 할지
* 어떤 톤으로 답해야 할지 결정한다.

### C  함수 호출과 상태 업데이트

Backend에서는
LLM이 말한 내용에서 필요한 정보를 추출해
상태 객체를 업데이트한다.

예

* 유저
  한 천 개 정도 생각하고 있어요
* LLM
  지금 대화 안에서
  orderVolumeUnits 1000이라고 판단
* Backend
  update_report 함수 호출

  * Landed Cost 다시 계산
  * Risk Score 보정
  * confidence를 40에서 65로 올림

이 업데이트 결과가
우측 패널에 실시간 반영된다.

---

## 5) 데이터 구조와 API 디자인

### Report State 객체 예시

타입 느낌만 정리

```ts
type ProductAnalysisReport = {
  productName: string
  productCategory: string
  htsCodeGuess: string
  targetMarket: string
  channel: string

  costBreakdown: {
    fobPerUnit: number
    freightPerUnit: number
    dutyPerUnit: number
    extraPerUnit: number
    ddpPerUnit: number
  }

  risk: {
    totalRiskScore_0_100: number
    qualityRisk_0_100: number
    complianceRisk_0_100: number
    logisticsRisk_0_100: number
    notes: string[]
  }

  estimateConfidence_0_100: number
  missingInfo: string[]
  assumptions: string[]

  conversationSummary: string
  lastUpdatedAt: string
}
```

Lead Intelligence Engine 쪽에는
이미 v2.1 스키마가 있으니

* conversationIntentBoost
* conversationNotes

정도만 확장해 붙이면 된다.

### Chat API 설계

엔드포인트

`POST /api/analyze-product/chat`

요청 바디 예시

```ts
{
  sessionId: string
  messages: {
    role: "user" | "assistant" | "system"
    content: string
  }[]
  currentReport?: ProductAnalysisReport
  attachments?: {
    type: "image"
    url: string
  }[]
}
```

응답 바디 예시

```ts
{
  reply: string
  followUpNeeded: boolean
  updatedReport?: ProductAnalysisReport
  updatedLeadAnalysis?: NexSupplyLeadAnalysis
  suggestedNextAction?:
    | "ask_more"
    | "show_summary"
    | "show_cta"
}
```

이미지 업로드는 별도의

`POST /api/upload-image`

에서 url만 받아오고
chat 요청에는 url만 전달.

---

## 6) Copilot 시스템 프롬프트 초안

Roo나 Gemini에 그대로 넣을 수 있는 버전

```text
You are NexSupply's Conversational Sourcing Copilot.

Your role
- Help importers and Amazon or TikTok sellers understand landed costs, compliance risks, and supplier feasibility.
- Collect the minimum information needed to generate a reliable "Landed Cost plus Risk Report".
- Qualify the lead in the background without sounding like a pushy salesperson.

Key goals
- Identify target import country.
- Identify main sales channel such as Amazon FBA, TikTok Shop, Shopify, retail.
- Estimate first order volume or budget range.
- Understand high level timeline.
- Understand which risks they worry about most such as quality, customs, cash flow, logistics.

Tone
- Friendly consultant.
- Short messages.
- One question at a time.
- Always allow the user to say "Not sure yet".

Rules
1) Never ask more than one question in a single turn.

2) Start broad then narrow.
   - First confirm target market and channel.
   - Then ask for rough volume or budget.
   - Then ask about timing.
   - Then ask which risk is most worrying.

3) If the user does not know an answer
   - Accept it without pressure.
   - Make a conservative assumption.
   - Add a short note into an assumptions list.
   - Lower the confidence score slightly.

4) If a photo or link is provided
   - Use it to refine product type, materials, and packaging.
   - Mention briefly how this changes the estimate.

5) After each key answer
   - Confirm your understanding in one sentence.
   - Optionally mention how this changes cost, risk, or confidence.

6) When you have enough information
   - Summarize their situation in three to five bullet points.
   - Recommend one of three verdicts
     "Proceed"
     "Proceed with caution"
     "Not recommended".
   - Offer to send a detailed sourcing quote or connect them with a human expert.

7) Do not output JSON in your messages.
   - The backend will handle structured data.
   - You only speak natural language.
```

---

## 7) Roo용 구현 브리프

Roo에게 그대로 전달할 수 있는 개발 요청서 버전

```text
Goal
Implement a v3 "Conversational Sourcing Copilot" on top of the existing NexSupply Quick Scan flow.

Tech context
- Next.js app router under `web`.
- Already available
  - `ProductAnalyzer` section with a single input and instant Landed Cost plus Risk Report using `POST /api/analyze-product`.
  - Lead Intelligence Engine v2.1 with intent, fit, authority, engagement scoring and tiered routing.

Scope

1) UI
- On the main landing page under `web/app/page.tsx`, keep the existing Quick Scan section.
- Under the report card, add a button such as "Ask NexSupply Copilot".
- When clicked, show a split layout
  - Left side
    - Chat interface with message history and an input box.
  - Right side
    - Live report panel that shows
      - Landed Cost breakdown
      - Risk scores
      - Estimate confidence progress bar
      - Missing info and assumptions lists.

- Add an optional image upload in the chat area
  - Simple file input with `accept="image/*"` and `capture="environment"` for mobile.

2) API
- Create `POST /api/analyze-product/chat`.
- Request body
  - `sessionId`
  - `messages` list
  - optional `currentReport`
  - optional `attachments` such as image urls.
- Response body
  - `reply` for the assistant message.
  - `followUpNeeded` flag.
  - optional `updatedReport`.
  - optional `updatedLeadAnalysis`.
  - optional `suggestedNextAction` enum.

3) State management
- On the client maintain
  - `sessionId` generated once per user session.
  - `messages` array.
  - `currentReport`.
  - loading flags.

- On each user message
  - Append the user message to `messages`.
  - Call the chat API.
  - Append the assistant reply.
  - If `updatedReport` exists, replace the local report and re render the right panel.

4) AI integration
- Under `web/lib/ai`, create `conversationalCopilot.ts`.
- This module should
  - Wrap `gemini-2.5-pro` with the system prompt provided in my message.
  - Send
    - message history
    - current report
    - image urls if present.
  - Receive
    - assistant reply text
    - structured fields for updated report
      - including confidence, missing info, assumptions.

- Reuse the existing product analysis functions whenever possible
  - do not duplicate landed cost calculation logic.

5) Lead Intelligence integration
- When the chat response sets `suggestedNextAction` to `"show_summary"` or `"show_cta"`
  - Call the existing Lead Intelligence Engine with
    - the conversation summary
    - the final product report
    - original user input.
  - Use the returned analysis to
    - create or update the lead in the existing pipeline.
    - populate any badges in the UI if needed later.

6) Non goals for now
- Do not build WebSocket based real time sync between desktop and mobile.
- Do not implement a full CRM interface.
- Keep visuals consistent with the current dark theme and card styles already used in NexSupply.

Testing
- After implementation, we should be able to
  - run Quick Scan on a simple keyword such as "gaming mouse"
  - open the Copilot
  - answer three to five questions
  - see the report confidence go up
  - and confirm that the final summary and lead record are created without errors.
```

---

이 버전 그냥 통째로
Notion이나 `docs/copilot-v3-spec.md` 같은 데 박아두고

* 위쪽 절반은 기획 설명
* 아래 Roo 브리프는 코드 구현용

으로 쓰면 될 것 같다.
다음에 원하면 이걸 더 줄여서
투자자용 한 페이지 버전으로도 정리해 줄 수 있어.