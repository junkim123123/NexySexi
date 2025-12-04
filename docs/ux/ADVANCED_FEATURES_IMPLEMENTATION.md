# Advanced Features Implementation Guide

이 문서는 세 가지 고급 기능 구현에 대한 가이드입니다:
1. 카테고리별 맞춤 질문 (Grace를 위해)
2. 리포트 저장/공유 기능 (Ashley/Ethan을 위해)
3. 전문가용 고급 분석 뷰 (Ethan을 위해)

## 1. 카테고리별 맞춤 질문

### 목표
분석 결과에서 카테고리를 식별한 후, 해당 카테고리에 특화된 추가 질문을 물어봅니다.

### 구현 방법
- 분석 결과에서 `compliance_hints?.id`로 카테고리 추출
- 카테고리별 질문 템플릿을 JSON 파일에 저장
- Copilot에서 분석 완료 후 카테고리별 질문을 추가로 제시
- 사용자가 답변하면 더 정확한 분석 가능

### 파일 구조
- `web/lib/ai/categoryQuestions.ts` - 카테고리별 질문 로직
- `web/data/category-questions.json` - 카테고리별 질문 템플릿
- `web/app/copilot/page.tsx` - Copilot UI에 통합

## 2. 리포트 저장/공유 기능

### 목표
분석 리포트를 PDF로 저장하거나 공유 가능한 링크로 생성합니다.

### 구현 방법
- PDF 생성: 클라이언트 측에서 리포트를 HTML로 렌더링 후 PDF 변환
- 공유 링크: URL에 분석 결과를 인코딩하거나, 서버에 임시 저장 후 링크 생성
- ProductAnalysisCard에 "Save as PDF" 및 "Share" 버튼 추가

### 파일 구조
- `web/lib/utils/pdfExport.ts` - PDF 생성 유틸리티
- `web/lib/utils/shareReport.ts` - 공유 링크 생성 유틸리티
- `web/components/ReportActions.tsx` - 저장/공유 버튼 컴포넌트
- `web/components/ProductAnalysisCard.tsx` - 버튼 통합

## 3. 전문가용 고급 분석 뷰

### 목표
더 상세한 분석 정보를 보여주는 확장 뷰를 제공합니다.

### 구현 방법
- ProductAnalysisCard에 "Advanced View" 토글 추가
- 확장 시 표시되는 정보:
  - 모든 가정 (assumptions)
  - 신뢰도 점수 및 설명
  - 누락된 정보 (missing_info)
  - 상세한 규제 추론 (regulation_reasoning)
  - 초기 주문 비용 상세 (initial_order_cost)

### 파일 구조
- `web/components/ProductAnalysisCard.tsx` - 토글 및 확장 뷰 추가
- `web/components/AdvancedAnalysisView.tsx` - 고급 뷰 컴포넌트 (선택사항)

---

**구현 순서:**
1. 카테고리별 맞춤 질문 (가장 직접적)
2. 전문가용 고급 분석 뷰 (기존 데이터 활용)
3. 리포트 저장/공유 기능 (외부 라이브러리 필요 가능)

