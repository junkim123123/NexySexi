# Git 푸시 전 체크리스트

## ✅ 완료된 사항

### 1. 빌드 오류 수정
- ✅ `web/app/api/analyze-product/route.ts` 문법 오류 수정 (중괄호, imageBase64 변수 선언)
- ✅ `web/components/ui/card.tsx`에 CardHeader, CardTitle, CardContent 추가

### 2. .gitignore 업데이트
- ✅ `.sanity/` 폴더 추가
- ✅ `studio-nexi.ai/` 폴더 추가
- ✅ `logs/` 및 `*.ndjson` 파일 추가

### 3. 민감한 정보 확인
- ✅ `.env`, `.env.local` 파일은 `.gitignore`에 포함됨
- ✅ API 키들은 환경 변수로 관리됨 (하드코딩 없음)
- ⚠️ Sanity Project ID (`m4g1dr67`)는 public이므로 하드코딩되어 있어도 괜찮음

## ⚠️ 주의사항

### 1. 빌드 경고 (빌드는 성공)
- `web/app/api/sample-request/debug/route.ts`에서 `analyzeSampleRequest` import 오류
- 이는 경고이므로 빌드는 성공하지만, 나중에 수정 권장

### 2. 커밋 전 확인할 파일들
다음 파일들이 새로 추가되었으니 확인하세요:
- `studio-nexi.ai/` - Sanity Studio 설정 (프로젝트 ID 포함, public이므로 OK)
- `web/.sanity/` - Sanity 캐시 (`.gitignore`에 추가됨)
- 여러 문서 파일들 (`SANITY_*.md`, `CONTENTFUL_*.md` 등)

### 3. 환경 변수 확인
다음 환경 변수들이 `.env.local`에 설정되어 있는지 확인:
- `GEMINI_API_KEY`
- `SANITY_API_TOKEN`
- `NEXT_PUBLIC_SANITY_PROJECT_ID`
- `NEXT_PUBLIC_SANITY_DATASET`
- `NEXTAUTH_SECRET`

## 📝 푸시 전 최종 확인

1. **민감한 정보 확인**
   ```bash
   git status
   git diff
   ```
   - `.env*` 파일이 커밋 목록에 없는지 확인
   - API 키나 토큰이 하드코딩된 파일이 없는지 확인

2. **빌드 테스트**
   ```bash
   cd web
   npm run build
   ```
   - 빌드가 성공하는지 확인 (경고는 괜찮음)

3. **린터 확인**
   ```bash
   cd web
   npm run lint
   ```
   - 린터 오류가 없는지 확인

4. **커밋 메시지 작성**
   - 변경 사항을 명확하게 설명하는 커밋 메시지 작성

## 🚀 푸시 명령어

```bash
# 변경 사항 확인
git status

# 변경 사항 추가
git add .

# 커밋
git commit -m "Your commit message"

# 푸시
git push origin main
```

## 📌 참고사항

- Sanity Project ID (`m4g1dr67`)는 public 정보이므로 커밋해도 안전합니다
- 모든 API 키와 토큰은 환경 변수로 관리되고 있습니다
- `.gitignore`가 올바르게 설정되어 있습니다

