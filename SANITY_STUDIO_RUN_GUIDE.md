# Sanity Studio 실행 가이드

## 문제

`web/sanity` 폴더에서 `npm run`을 실행했지만 스크립트가 없습니다.

## 해결 방법

### 방법 1: 루트 `sanity/` 폴더에서 실행 (권장)

```bash
# 루트 디렉토리로 이동
cd "C:\Users\kmyun\OneDrive\바탕 화면\nexi.ai"

# sanity 폴더로 이동
cd sanity

# Sanity Studio 실행
npm run dev
```

### 방법 2: `web/` 폴더에서 직접 실행

```bash
# web 폴더로 이동
cd "C:\Users\kmyun\OneDrive\바탕 화면\nexi.ai\web"

# npx로 직접 실행
npx sanity dev
```

### 방법 3: Sanity 웹사이트에서 접근 (가장 안정적)

1. https://www.sanity.io/manage 접속
2. 프로젝트 `m4g1dr67` 선택
3. Studio 열기

## 폴더 구조 설명

- **`sanity/`** (루트) - 독립적인 Sanity Studio 프로젝트
  - `package.json` 있음
  - `sanity.config.ts` 있음
  - `npm run dev` 가능

- **`web/sanity/`** - Next.js와 통합된 Sanity 설정
  - `package.json` 없음
  - Next.js 앱의 일부
  - `npx sanity dev`로 실행

## 현재 위치 확인

터미널에서 현재 위치를 확인하려면:
```bash
pwd  # PowerShell에서는 Get-Location
```

## 권장 실행 순서

1. **루트 `sanity/` 폴더에서 실행** (가장 간단)
   ```bash
   cd sanity
   npm run dev
   ```

2. 또는 **Sanity 웹사이트에서 접근** (가장 안정적)
   - https://www.sanity.io/manage

