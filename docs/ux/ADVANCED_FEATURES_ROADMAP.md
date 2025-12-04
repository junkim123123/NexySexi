# Advanced Features Implementation Roadmap

## 개요

세 가지 고급 기능 구현을 위한 상세 로드맵입니다.

---

## 1. 전문가용 고급 분석 뷰 (Advanced Analysis View)

### 목표
Ethan과 같은 전문가 사용자에게 더 상세한 분석 정보를 제공합니다.

### 구현 단계

#### Phase 1: 기본 구조 (우선 구현)
- [ ] `AdvancedAnalysisView.tsx` 컴포넌트 생성
- [ ] `ProductAnalysisCard.tsx`에 "Show Advanced View" 토글 버튼 추가
- [ ] 확장 시 표시할 기본 정보 섹션들:
  - Estimate Confidence Score
  - Assumptions Made
  - Missing Information

#### Phase 2: 상세 정보 추가
- [ ] Regulation Reasoning 상세 표시
- [ ] Testing Cost Estimate 상세
- [ ] Initial Order Cost Breakdown (if available)

#### Phase 3: UX 개선
- [ ] 애니메이션 (expand/collapse)
- [ ] 프린트 최적화
- [ ] PDF 내보내기 지원

### 파일 구조
```
web/components/
  ├── ProductAnalysisCard.tsx (수정)
  └── AdvancedAnalysisView.tsx (신규)
```

---

## 2. 카테고리별 맞춤 질문 (Category-Specific Questions)

### 목표
Grace와 같은 사용자를 위해 카테고리별로 특화된 추가 질문을 물어봅니다.

### 구현 단계

#### Phase 1: 카테고리 질문 시스템 구축
- [ ] `web/data/category-questions.json` 파일 생성
- [ ] `web/lib/ai/categoryQuestions.ts` 헬퍼 함수 생성
- [ ] 카테고리 ID를 기반으로 질문 로드

#### Phase 2: Copilot 통합
- [ ] 분석 완료 후 카테고리 확인
- [ ] 카테고리별 질문을 선택적으로 표시
- [ ] 사용자 답변 수집

#### Phase 3: 분석 개선
- [ ] 수집한 답변을 다음 분석에 반영
- [ ] 질문-답변 히스토리 저장

### 파일 구조
```
web/data/
  └── category-questions.json (신규)
web/lib/ai/
  └── categoryQuestions.ts (신규)
web/app/copilot/
  └── page.tsx (수정)
```

### 예시: `category-questions.json`
```json
{
  "categories": [
    {
      "id": "baby_teether",
      "questions": [
        {
          "id": "material_type",
          "question": "What materials is the teether made of?",
          "type": "multiple_choice",
          "options": ["Silicone", "Rubber", "Wood", "Other"],
          "importance": "high"
        },
        {
          "id": "target_age",
          "question": "What age group is this product for?",
          "type": "multiple_choice",
          "options": ["0-6 months", "6-12 months", "12-24 months", "24+ months"],
          "importance": "high"
        }
      ]
    }
  ]
}
```

---

## 3. 리포트 저장/공유 기능 (Save & Share Report)

### 목표
Ashley와 Ethan이 리포트를 PDF로 저장하거나 팀과 공유할 수 있게 합니다.

### 구현 단계

#### Phase 1: PDF 생성 (클라이언트 측)
- [ ] `jspdf` 또는 `react-pdf` 라이브러리 선택 및 설치
- [ ] 리포트를 PDF로 변환하는 유틸리티 함수
- [ ] "Save as PDF" 버튼 추가

#### Phase 2: 공유 링크 생성
- [ ] URL에 분석 결과 인코딩 (짧은 링크)
- [ ] 또는 서버에 임시 저장 후 링크 생성
- [ ] "Copy Share Link" 버튼 추가

#### Phase 3: UX 개선
- [ ] 공유 링크 만료 시간 설정
- [ ] 비밀번호 보호 옵션
- [ ] 공유 링크 열람 통계

### 파일 구조
```
web/lib/utils/
  ├── pdfExport.ts (신규)
  └── shareReport.ts (신규)
web/components/
  ├── ReportActions.tsx (신규)
  └── ProductAnalysisCard.tsx (수정)
web/app/api/
  └── share/[id]/route.ts (선택사항 - 서버 저장 시)
```

### 필요한 패키지
```json
{
  "dependencies": {
    "jspdf": "^2.5.1",
    "html2canvas": "^1.4.1"
  }
}
```

---

## 구현 우선순위

### 높은 우선순위 (즉시 시작)
1. ✅ **전문가용 고급 분석 뷰** - 가장 간단하고 기존 데이터 활용
2. ✅ **카테고리별 맞춤 질문** - 중간 복잡도, 사용자 가치 높음

### 중간 우선순위 (다음 스프린트)
3. ⏳ **리포트 저장/공유 기능** - 외부 라이브러리 필요, PDF 생성 복잡

---

## 테스트 계획

### 전문가용 고급 분석 뷰
- [ ] Ethan 페르소나: 확장 뷰에서 모든 상세 정보 확인 가능
- [ ] 모바일 반응형 확인
- [ ] 프린트 시 레이아웃 확인

### 카테고리별 맞춤 질문
- [ ] Grace 페르소나: 베이비 제품 분석 시 추가 질문 표시
- [ ] 질문-답변 플로우 검증
- [ ] 카테고리 없을 때 처리

### 리포트 저장/공유
- [ ] PDF 다운로드 기능 테스트
- [ ] 공유 링크 생성 및 열람 테스트
- [ ] 다양한 브라우저 호환성 확인

---

## 참고사항

- 모든 기능은 **코어 분석 엔진을 변경하지 않고** 프론트엔드에서만 구현
- 기존 API와 스키마는 그대로 유지
- 점진적 배포 가능하도록 각 기능은 독립적으로 동작

