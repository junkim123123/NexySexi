# Contentful 설정 가이드

## 1단계: Contentful 계정 생성 및 Space 설정

### 1.1 Contentful 계정 생성
1. https://www.contentful.com 접속
2. "Get started for free" 클릭하여 계정 생성
3. 이메일 인증 완료

### 1.2 Space 생성
1. 로그인 후 "Create space" 클릭
2. Space 이름 입력 (예: "NexSupply")
3. Space ID 확인 (예: `abc123xyz`)

### 1.3 API 키 생성
1. Space 대시보드에서 **Settings** → **API keys** 이동
2. **Content delivery / preview tokens** 섹션에서
3. **Add API key** 클릭
4. 이름 입력 (예: "NexSupply Web")
5. **Generate** 클릭
6. **Space ID**와 **Content Delivery API - access token** 복사

---

## 2단계: 환경 변수 설정

`.env.local` 파일에 다음 변수 추가:

```env
NEXT_PUBLIC_CONTENTFUL_SPACE_ID=your_space_id_here
NEXT_PUBLIC_CONTENTFUL_ACCESS_TOKEN=your_access_token_here
```

**중요:** 
- `your_space_id_here`를 실제 Space ID로 교체
- `your_access_token_here`를 실제 Access Token으로 교체
- `.env.local`은 `.gitignore`에 포함되어 있어야 합니다

---

## 3단계: Contentful에서 콘텐츠 모델 생성

### 3.1 Content Model 생성

Contentful 대시보드에서 **Content model** → **Add content type** 클릭

#### A. Site Settings (Single Type)
1. **Display name**: `Site Settings`
2. **API Identifier**: `siteSettings`
3. **Settings** → **Single entry** 체크
4. 필드 추가:
   - `brandName` (Short text)
   - `mainNav` (JSON Object) - 또는 Reference로 처리
   - `footerIntro` (Long text)
   - `contactEmail` (Short text)
   - `disclaimer` (Long text)

#### B. Home Page (Single Type)
1. **Display name**: `Home Page`
2. **API Identifier**: `homePage`
3. **Settings** → **Single entry** 체크
4. 필드 추가:
   - `heroTitle` (Short text)
   - `heroSubtitle` (Long text)
   - `heroCtaLabel` (Short text)
   - `heroBadge` (Short text)
   - `highlights` (JSON Object) - 또는 Reference로 처리
   - `reviewsTitle` (Short text)
   - `benefitsTitle` (Short text)
   - `trustedTitle` (Short text)
   - `categoriesTitle` (Short text)
   - `faqTeaserTitle` (Short text)
   - `faqTeaserBody` (Long text)

#### C. How It Works Page (Single Type)
1. **Display name**: `How It Works Page`
2. **API Identifier**: `howItWorksPage`
3. **Settings** → **Single entry** 체크
4. 필드 추가:
   - `title` (Short text)
   - `subtitle` (Long text)
   - `steps` (JSON Object)
   - `ctaTitle` (Short text)
   - `ctaButtonLabel` (Short text)
   - `ctaButtonUrl` (Short text)

#### D. Use Cases Page (Single Type)
1. **Display name**: `Use Cases Page`
2. **API Identifier**: `useCasesPage`
3. **Settings** → **Single entry** 체크
4. 필드 추가:
   - `title` (Short text)
   - `subtitle` (Long text)
   - `useCases` (JSON Object)
   - `ctaTitle` (Short text)
   - `ctaBody` (Long text)
   - `ctaButtonLabel` (Short text)
   - `ctaButtonUrl` (Short text)

### 3.2 콘텐츠 입력

각 Content Type을 생성한 후:
1. **Content** 탭으로 이동
2. 각 페이지에 해당하는 Entry 생성
3. 필드에 데이터 입력
4. **Publish** 클릭

---

## 4단계: Next.js 코드 확인

코드가 자동으로 Contentful에서 데이터를 가져오도록 설정되어 있습니다.

### 테스트
```bash
cd web
npm run dev
```

브라우저에서 `http://localhost:3000` 접속하여 Contentful 데이터가 표시되는지 확인하세요.

---

## 문제 해결

### 환경 변수가 인식되지 않는 경우
1. `.env.local` 파일이 `web/` 폴더에 있는지 확인
2. 개발 서버 재시작 (`Ctrl+C` 후 `npm run dev`)

### 데이터가 표시되지 않는 경우
1. Contentful에서 Entry가 **Published** 상태인지 확인
2. Space ID와 Access Token이 올바른지 확인
3. 브라우저 콘솔에서 에러 메시지 확인

### 타입 오류가 발생하는 경우
1. `web/lib/contentful/types.ts` 파일 확인
2. Contentful의 필드 이름이 코드와 일치하는지 확인

