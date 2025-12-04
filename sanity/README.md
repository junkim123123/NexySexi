# NexSupply Sanity Studio

Sanity CMS 관리자 화면입니다. 마케팅 페이지 콘텐츠를 관리할 수 있습니다.

## 시작하기

### 1. 의존성 설치

```bash
npm install
```

### 2. 환경 변수 확인

`.env.local` 파일이 있는지 확인하세요. 없으면 프로젝트 루트의 `web/.env.local`을 참고하세요.

필요한 환경 변수:
- `NEXT_PUBLIC_SANITY_PROJECT_ID=vqt42bhw`
- `NEXT_PUBLIC_SANITY_DATASET=production`

### 3. Sanity Studio 실행

```bash
npm run dev
```

브라우저에서 `http://localhost:3333`로 접속하면 Sanity Studio가 열립니다.

## 콘텐츠 타입

다음 콘텐츠 타입을 관리할 수 있습니다:

### 싱글톤 페이지 (각각 하나만 존재)
- **Site Settings**: 전역 사이트 설정 (네비게이션, 푸터 등)
- **Home Page**: 홈 페이지 콘텐츠
- **How It Works Page**: How It Works 페이지 콘텐츠
- **Use Cases Page**: Use Cases 페이지 콘텐츠

### 재사용 가능한 문서
- **Testimonial**: 고객 후기
- **FAQ**: 자주 묻는 질문
- **Use Case**: 개별 사용 사례

## 배포

Sanity Studio를 배포하려면:

```bash
npm run deploy
```

또는 Sanity 웹사이트에서 직접 접근:
https://www.sanity.io/manage

## 문제 해결

### Studio가 열리지 않는 경우
1. `sanity.config.ts`의 `projectId`와 `dataset` 확인
2. 환경 변수가 올바르게 설정되었는지 확인
3. `npm install`을 다시 실행

### 콘텐츠가 표시되지 않는 경우
1. Next.js 앱의 `.env.local`에 환경 변수가 있는지 확인
2. Sanity 프로젝트에서 데이터가 실제로 저장되었는지 확인
3. Next.js 개발 서버를 재시작

