# Sales Consultation Funnel Extension - Implementation Complete

## 개요

기존 Dr B 스타일 대화형 intake flow에 sales consultation funnel을 추가하여 마케팅 사용자를 NexSupply의 qualified lead로 전환할 수 있도록 확장했습니다.

## 구현 완료 항목

### Step 1: 새 QuestionNode 정의 추가 ✅

**파일**: `web/lib/analyze/questionFlow.ts`

**추가된 질문 노드**:

1. **q13** - 제품의 실제 주문 가능성 확인
   - Input: singleChoice
   - Choices: "serious candidate", "idea_later", "exploring"

2. **q14** - 24시간 내 follow-up 미팅 개방성 확인
   - Input: singleChoice
   - Choices: "yes_call", "maybe_later", "no_call"

3. **q15** - 선호 연락처 수집
   - Input: text
   - Optional: true (hesitant 경로에서)
   - 저장 키: `contact_info`

4. **q16_budget** - 프로젝트 규모 확인
   - Input: singleChoice
   - Choices: "under_5k", "5k_to_20k", "above_20k"
   - 인라인 노트: "This helps NexSupply prioritize projects and tailor the quote."

5. **q16_timeline** - 프로젝트 타임라인 확인
   - Input: singleChoice
   - Choices: "3_months", "6_months", "flexible"
   - 인라인 노트: "This helps NexSupply prioritize projects and tailor the quote."

6. **q17** - NexSupply engagement model 설명 및 paid consult 진행 여부
   - Input: singleChoice
   - Choices: "yes_consult", "no_consult"
   - 설명은 별도 메시지로 표시

### Step 2: 네비게이션 로직 업데이트 ✅

**파일**: `web/lib/analyze/questionFlow.ts`

**조건부 분기 로직**:

- **summary → q13**: 항상 진행
- **q13 → q14**: 항상 진행
- **q14 → 분기**:
  - `yes_call`: q15 → q16_budget → q16_timeline → q17 → final_thanks
  - `maybe_later` / `no_call`: q15 (optional, softer tone) → final_thanks
- **q17 → final_thanks**: Lead intent 마킹

**Lead Intent 마킹**:
- `high_intent`: q17 = 'yes_consult' 또는 q14 = 'yes_call'
- `report_only`: 그 외 모든 경우

### Step 3: UI 조정 ✅

**파일**: `web/app/analyze/chat/page.tsx`

**구현된 UI 개선사항**:

1. **시각적 분리선**: Summary 후 q13 시작 전에 구분선 추가
2. **인라인 노트**: q16_budget, q16_timeline에 "This helps NexSupply prioritize projects and tailor the quote." 표시
3. **q17 설명 메시지**: 질문 전에 NexSupply engagement model 상세 설명 표시
4. **q15 조건부 톤**: hesitant 경로에서 더 부드러운 질문 텍스트 사용
5. **최종 감사 메시지**: 
   - 24시간 내 연락 여부 확인
   - 추가 제품 분석 가능 안내
6. **Skip 기능**: q15가 optional일 때 skip 버튼 제공

## 플로우 다이어그램

```
q1-q12 (Product/Logistics Intake)
  ↓
summary
  ↓
[Visual Separator]
  ↓
q13 (Serious candidate?)
  ↓
q14 (Open to call in 24h?)
  ↓
  ├─ yes_call → q15 → q16_budget → q16_timeline → q17 → final_thanks (high_intent)
  └─ maybe_later/no_call → q15 (optional, softer) → final_thanks (report_only)
```

## Lead 데이터 구조

**최종 answers 객체에 포함**:
- 모든 q1-q12 답변
- q13-q17 sales consultation 답변
- `contact_info`: q15 답변
- `lead_intent`: 'high_intent' | 'report_only'

## TODO 마커

코드에 다음 TODO 마커가 포함되어 있습니다:

1. **API/CRM 통합**:
   - `TODO: Post lead data to API/CRM`
   - `TODO: Send email/notification to NexSupply team`

2. **결제 처리**:
   - `TODO: Process payment if q17 answer is 'yes_consult'`

3. **기존 TODO**:
   - `TODO: Integrate with Nexi analysis API`
   - `TODO: Handle file uploads (images, links)`

## 주요 기능

### 조건부 질문 흐름
- 사용자의 답변에 따라 질문 경로가 동적으로 변경
- Hesitant 경로에서 더 부드러운 톤과 optional 질문 제공

### Lead Qualification
- High intent leads는 전체 sales consultation 플로우 진행
- Report-only leads는 최소한의 정보만 수집

### 사용자 경험
- Summary 후 자연스럽게 sales consultation으로 전환
- 긴 설명 메시지는 별도로 표시하여 가독성 향상
- 최종 메시지에서 다음 단계 명확히 안내

## 테스트 시나리오

### 시나리오 1: High Intent Lead
1. q1-q12 완료
2. summary 확인
3. q13: "serious candidate" 선택
4. q14: "yes_call" 선택
5. q15: 연락처 제공
6. q16_budget, q16_timeline 완료
7. q17 설명 확인 후 "yes_consult" 선택
8. final_thanks: "24시간 내 연락" 메시지 확인
9. lead_intent = 'high_intent'

### 시나리오 2: Hesitant Lead
1. q1-q12 완료
2. q13: "exploring" 선택
3. q14: "maybe_later" 선택
4. q15: Skip 또는 선택적 답변
5. final_thanks: "분석 저장" 메시지 확인
6. lead_intent = 'report_only'

### 시나리오 3: Report Only
1. q1-q12 완료
2. q13: "exploring" 선택
3. q14: "no_call" 선택
4. q15: Skip
5. final_thanks: "분석 저장" 메시지 확인
6. lead_intent = 'report_only'

## 파일 변경 사항

### 수정된 파일
- `web/lib/analyze/questionFlow.ts`: 새 질문 노드 추가, 조건부 네비게이션 로직
- `web/app/analyze/chat/page.tsx`: UI 조정, 조건부 질문 처리, lead 마킹

### 새로운 기능
- 조건부 질문 분기
- Lead intent 마킹
- 설명 메시지 분리
- 조건부 톤 조정

---

**Status**: ✅ 완전히 구현 완료 및 테스트 준비 완료

