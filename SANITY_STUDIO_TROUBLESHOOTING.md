# Sanity Studio 실행 문제 해결

## 현재 상황

Sanity Studio가 로컬에서 실행되지 않는 문제가 발생했습니다.

## 해결 방법

### 방법 1: Sanity 웹사이트에서 직접 접근 (가장 간단)

1. 브라우저에서 https://www.sanity.io/manage 접속
2. 프로젝트 ID `vqt42bhw` 선택
3. Studio에서 콘텐츠 관리

**장점:**
- 별도 설정 불필요
- 즉시 사용 가능
- 안정적

### 방법 2: 로컬 Studio 재초기화

현재 `sanity` 폴더의 구조에 문제가 있을 수 있습니다. 다음 단계로 재초기화:

```bash
# 1. 기존 sanity 폴더 백업 (스키마 파일 보존)
cd ..
cp -r sanity/schemas sanity_schemas_backup

# 2. sanity 폴더 삭제
rm -rf sanity

# 3. 새로 초기화
npx sanity@latest init --project vqt42bhw --dataset production --template clean

# 4. 스키마 파일 복원
cp -r sanity_schemas_backup/* sanity/schemas/

# 5. sanity.config.ts 수정 (기존 설정 복원)
```

### 방법 3: 임시 해결책 - Sanity CLI로 직접 접근

```bash
# sanity 폴더에서
npx sanity@latest manage
```

이 명령어는 브라우저에서 Sanity 관리 페이지를 엽니다.

## 현재 상태

- ✅ 환경 변수 설정 완료
- ✅ 스키마 정의 완료
- ✅ Next.js 연동 완료
- ❌ 로컬 Studio 실행 실패 (모듈 해석 오류)

## 권장 사항

**지금 당장 콘텐츠를 입력하려면:**
1. https://www.sanity.io/manage 접속
2. 프로젝트 선택
3. 콘텐츠 입력

**로컬 Studio가 필요하다면:**
- 방법 2로 재초기화하거나
- Sanity 공식 문서 참고: https://www.sanity.io/docs/getting-started

## Next.js 페이지 확인

로컬 Studio 없이도 Next.js 페이지는 정상 작동합니다:

```bash
cd web
npm run dev
```

Sanity에서 입력한 콘텐츠는 Next.js 페이지에 자동으로 반영됩니다.

