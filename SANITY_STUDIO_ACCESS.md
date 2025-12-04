# Sanity Studio 접근 방법

## 현재 상황

Sanity 대시보드에서 "Add studio" 모달이 열려 있지만, 로컬 Studio를 등록할 필요가 없습니다.

## 올바른 방법: Sanity에서 제공하는 Studio 사용

### 1. 모달 닫기
"Add studio" 모달의 X 버튼을 클릭하여 닫으세요.

### 2. Studio 생성/접근

Sanity 대시보드에서:

1. **"Getting started"** 탭 클릭
2. 또는 **"Create new studio"** 버튼 클릭 (있는 경우)
3. 또는 직접 Studio URL 접근:
   - `https://vqt42bhw.api.sanity.io/v2024-01-01/studio/desk`

### 3. 또는 Sanity CLI로 Studio 열기

터미널에서:

```bash
cd sanity
npx sanity@latest manage
```

이 명령어는 브라우저에서 Sanity 관리 페이지를 엽니다.

## 로컬 Studio 등록은 불필요합니다

- 로컬 Studio (`localhost:3001`)를 Sanity에 등록할 필요가 없습니다
- Sanity에서 제공하는 웹 기반 Studio를 사용하면 됩니다
- 웹 Studio가 더 안정적이고 설정이 간단합니다

## 콘텐츠 입력

Studio가 열리면:

1. 왼쪽 사이드바에서 문서 타입 선택
2. 새 문서 생성 또는 기존 문서 편집
3. 콘텐츠 입력 후 "Publish" 클릭
4. Next.js 페이지에서 자동으로 반영됨

## 참고

- 로컬 Studio 등록은 고급 사용자를 위한 기능입니다
- 일반적으로는 Sanity에서 제공하는 Studio를 사용하는 것이 권장됩니다
- 콘텐츠는 어디서 입력하든 동일하게 작동합니다

