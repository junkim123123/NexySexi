# Sanity Studio 오류 해결

## 문제

`studio-nexi.ai` 폴더에서 Sanity Studio를 실행하려고 할 때 다음 오류가 발생했습니다:
```
Error: Unable to resolve `sanity` module root
```

## 해결 방법

### 1. 올바른 디렉토리에서 실행

`studio-nexi.ai` 폴더가 아닌 `web/` 폴더에서 Sanity Studio를 실행하세요:

```bash
cd web
npx sanity dev
```

또는 루트의 `sanity/` 폴더에서 실행:

```bash
cd sanity
npm run dev
```

### 2. Sanity Studio 웹사이트에서 접근 (권장)

로컬 Studio 대신 Sanity 웹사이트에서 직접 접근하는 것이 가장 안정적입니다:

1. https://www.sanity.io/manage 접속
2. 프로젝트 `m4g1dr67` 선택
3. Studio 열기

### 3. 설정 파일 확인

다음 파일들이 올바르게 설정되어 있습니다:

- `web/sanity.cli.ts` - 프로젝트 ID: `m4g1dr67`
- `web/sanity.config.ts` - Studio 설정
- `web/sanity/schemaTypes/index.ts` - 스키마 연결

## 참고

- `studio-nexi.ai` 폴더는 Sanity가 자동으로 생성한 폴더입니다
- 이 폴더를 사용하지 않고 `web/` 또는 `sanity/` 폴더를 사용하세요
- 환경 변수는 `.env.local` 파일에 설정되어 있습니다

