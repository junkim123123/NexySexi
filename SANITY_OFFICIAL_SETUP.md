# Sanity 공식 가이드에 따른 Studio 설정

## Sanity 공식 가이드

Sanity 웹사이트에서 제공하는 공식 가이드를 따르세요:

### 1단계: Studio 생성

루트 디렉토리(`C:\Users\kmyun\OneDrive\바탕 화면\nexi.ai`)에서 다음 명령어를 실행하세요:

```bash
npm create sanity@latest -- --project m4g1dr67 --dataset production --template clean --typescript --output-path studio-nexi.ai
```

이 명령어는:
- 프로젝트 ID: `m4g1dr67`
- Dataset: `production`
- 템플릿: `clean`
- TypeScript 사용
- 출력 경로: `studio-nexi.ai` (루트에 생성)

### 2단계: Studio 디렉토리로 이동

```bash
cd studio-nexi.ai
```

### 3단계: 개발 서버 실행

```bash
npm run dev
```

### 4단계: 브라우저에서 접근

브라우저에서 `http://localhost:3333` 접속

로그인 화면이 나타나면, Sanity CLI에 로그인할 때 사용한 것과 동일한 서비스(Google, GitHub, 또는 이메일)로 로그인하세요.

## 현재 상황

- ✅ 프로젝트 ID: `m4g1dr67`
- ✅ Dataset: `production`
- ⚠️ `web/studio-nexi.ai` 폴더가 있지만, 공식 가이드는 루트에 생성하라고 합니다
- ⚠️ 루트에 `studio-nexi.ai` 폴더가 없으면 생성해야 합니다

## 권장 사항

1. **루트에 새로 생성** (공식 가이드 따름)
   - 루트에서 `npm create sanity@latest` 명령어 실행
   - `web/studio-nexi.ai`는 무시하거나 삭제

2. **기존 `web/studio-nexi.ai` 사용** (대안)
   - `web/studio-nexi.ai` 폴더로 이동
   - `npm install` 실행 (의존성 설치)
   - `npm run dev` 실행

## 참고

- 공식 가이드는 루트에 `studio-nexi.ai`를 생성하도록 권장합니다
- 기존 `web/studio-nexi.ai`는 Next.js 통합용으로 생성된 것일 수 있습니다
- 루트에 새로 생성하는 것이 가장 안정적입니다

