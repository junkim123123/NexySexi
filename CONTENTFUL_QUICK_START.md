# Contentful 빠른 시작 가이드

## ✅ 완료된 작업

1. ✅ Contentful SDK 설치 (`contentful` 패키지)
2. ✅ Contentful 클라이언트 설정 (`web/lib/contentful/client.ts`)
3. ✅ 타입 정의 생성 (`web/lib/contentful/types.ts`)
4. ✅ 데이터 가져오기 함수 생성 (`web/lib/contentful/queries.ts`)
5. ✅ 마케팅 페이지 코드 교체 완료
   - `web/app/(marketing)/page.tsx`
   - `web/app/(marketing)/how-it-works/page.tsx`
   - `web/app/(marketing)/use-cases/page.tsx`

## 🔧 다음 단계: Contentful 설정

### 1단계: Contentful 계정 및 Space 생성

1. **Contentful 계정 생성**
   - https://www.contentful.com 접속
   - "Get started for free" 클릭
   - 이메일 인증 완료

2. **Space 생성**
   - 로그인 후 "Create space" 클릭
   - Space 이름: `NexSupply` (또는 원하는 이름)
   - Space ID 확인 (예: `abc123xyz`)

3. **API 키 생성**
   - Space 대시보드 → **Settings** → **API keys**
   - **Content delivery / preview tokens** 섹션
   - **Add API key** 클릭
   - 이름: `NexSupply Web`
   - **Generate** 클릭
   - **Space ID**와 **Content Delivery API - access token** 복사

### 2단계: 환경 변수 설정

`web/.env.local` 파일을 열고 다음 변수를 추가하세요:

```env
# Contentful 설정
NEXT_PUBLIC_CONTENTFUL_SPACE_ID=your_space_id_here
NEXT_PUBLIC_CONTENTFUL_ACCESS_TOKEN=your_access_token_here
```

**중요:**
- `your_space_id_here`를 실제 Space ID로 교체
- `your_access_token_here`를 실제 Access Token으로 교체
- `.env.local` 파일은 `.gitignore`에 포함되어 있어야 합니다

### 3단계: Contentful에서 콘텐츠 모델 생성

Contentful 대시보드에서 다음 Content Type을 생성하세요:

#### A. Site Settings (Single Entry)

1. **Content model** → **Add content type**
2. **Display name**: `Site Settings`
3. **API Identifier**: `siteSettings` (자동 생성됨)
4. **Settings** → **Single entry** 체크
5. 필드 추가:
   - `brandName` (Short text, single line)
   - `footerIntro` (Long text, multiple lines)
   - `contactEmail` (Short text, single line)
   - `disclaimer` (Long text, multiple lines)

#### B. Home Page (Single Entry)

1. **Content model** → **Add content type**
2. **Display name**: `Home Page`
3. **API Identifier**: `homePage`
4. **Settings** → **Single entry** 체크
5. 필드 추가:
   - `heroTitle` (Short text)
   - `heroSubtitle` (Long text)
   - `heroCtaLabel` (Short text)
   - `heroBadge` (Short text)
   - `reviewsTitle` (Short text)
   - `benefitsTitle` (Short text)
   - `trustedTitle` (Short text)
   - `categoriesTitle` (Short text)
   - `faqTeaserTitle` (Short text)
   - `faqTeaserBody` (Long text)

**복잡한 필드 (JSON Object):**
- `highlights`, `reviews`, `benefits`, `trustedLogos`, `categories`, `faqItems`는 Contentful에서 **JSON Object** 필드 타입으로 생성하거나, 나중에 Reference로 변경할 수 있습니다.

**간단한 방법 (초기):**
- 이 필드들은 일단 **Long text**로 생성하고, JSON 형식으로 입력하세요.
- 예: `highlights` 필드에 다음 JSON 입력:
```json
[
  {
    "title": "Use one box to test demand",
    "body": "Ship a few master cartons DDP into your warehouse...",
    "ctaLabel": "Learn more",
    "ctaUrl": "/how-it-works"
  }
]
```

#### C. How It Works Page (Single Entry)

1. **Content model** → **Add content type**
2. **Display name**: `How It Works Page`
3. **API Identifier**: `howItWorksPage`
4. **Settings** → **Single entry** 체크
5. 필드 추가:
   - `title` (Short text)
   - `subtitle` (Long text)
   - `steps` (Long text - JSON 형식으로 입력)
   - `ctaTitle` (Short text)
   - `ctaButtonLabel` (Short text)
   - `ctaButtonUrl` (Short text)

#### D. Use Cases Page (Single Entry)

1. **Content model** → **Add content type**
2. **Display name**: `Use Cases Page`
3. **API Identifier**: `useCasesPage`
4. **Settings** → **Single entry** 체크
5. 필드 추가:
   - `title` (Short text)
   - `subtitle` (Long text)
   - `useCases` (Long text - JSON 형식으로 입력)
   - `ctaTitle` (Short text)
   - `ctaBody` (Long text)
   - `ctaButtonLabel` (Short text)
   - `ctaButtonUrl` (Short text)

### 4단계: 콘텐츠 입력

1. **Content** 탭으로 이동
2. 각 페이지에 해당하는 Entry 생성
3. 필드에 데이터 입력
4. **Publish** 클릭 (중요!)

### 5단계: 테스트

1. 개발 서버 재시작:
```bash
cd web
npm run dev
```

2. 브라우저에서 확인:
   - `http://localhost:3000` - 홈 페이지
   - `http://localhost:3000/how-it-works` - How It Works 페이지
   - `http://localhost:3000/use-cases` - Use Cases 페이지

3. Contentful 데이터가 표시되는지 확인

## 🔍 문제 해결

### 환경 변수가 인식되지 않는 경우
- `.env.local` 파일이 `web/` 폴더에 있는지 확인
- 개발 서버 재시작 (`Ctrl+C` 후 `npm run dev`)

### 데이터가 표시되지 않는 경우
- Contentful에서 Entry가 **Published** 상태인지 확인
- Space ID와 Access Token이 올바른지 확인
- 브라우저 콘솔(F12)에서 에러 메시지 확인
- 터미널에서 에러 메시지 확인

### 타입 오류가 발생하는 경우
- `web/lib/contentful/types.ts` 파일 확인
- Contentful의 필드 이름이 코드와 일치하는지 확인

## 📝 참고사항

- Contentful의 무료 플랜은 충분히 사용 가능합니다
- 콘텐츠는 즉시 반영됩니다 (개발 서버 재시작 불필요)
- JSON 필드는 나중에 Reference로 변경하여 더 구조화할 수 있습니다

