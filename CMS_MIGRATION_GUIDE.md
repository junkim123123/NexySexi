# CMS 전환 가이드 (Sanity → 다른 CMS)

## 개요

다른 CMS(예: Contentful, Strapi, Payload CMS 등)로 전환할 때 개발팀이 수행해야 할 작업을 정리한 문서입니다.

---

## 1. 기존 Sanity 코드 제거

### 1.1 패키지 제거

```bash
cd web
npm uninstall @sanity/client @sanity/image-url
```

**제거할 패키지:**
- `@sanity/client`
- `@sanity/image-url`
- (선택) `sanity` (Studio 관련, 이미 설치되어 있지 않을 수 있음)

### 1.2 파일 삭제

다음 파일/폴더를 삭제합니다:

```
web/lib/sanity/
  ├── client.ts          # Sanity 클라이언트 설정
  └── content.ts         # 콘텐츠 가져오기 함수들 (있는 경우)

web/app/studio/          # Studio 페이지 (있는 경우)
sanity/                  # Sanity Studio 설정 폴더 (전체)
```

### 1.3 환경 변수 제거

`.env.local`에서 다음 변수 제거:

```env
# 제거할 변수
NEXT_PUBLIC_SANITY_PROJECT_ID=
NEXT_PUBLIC_SANITY_DATASET=
SANITY_API_TOKEN=
```

---

## 2. 새 CMS 환경 설정

### 2.1 새 CMS SDK 설치

**예시: Contentful**

```bash
cd web
npm install contentful
```

**예시: Strapi**

```bash
cd web
npm install @strapi/strapi
```

**예시: Payload CMS**

```bash
cd web
npm install payload
```

### 2.2 환경 변수 추가

`.env.local`에 새 CMS 관련 변수 추가:

**Contentful 예시:**
```env
NEXT_PUBLIC_CONTENTFUL_SPACE_ID=your_space_id
NEXT_PUBLIC_CONTENTFUL_ACCESS_TOKEN=your_access_token
CONTENTFUL_PREVIEW_TOKEN=your_preview_token  # 선택사항
```

**Strapi 예시:**
```env
NEXT_PUBLIC_STRAPI_API_URL=http://localhost:1337
STRAPI_API_TOKEN=your_api_token
```

### 2.3 클라이언트 설정 파일 생성

새 파일 생성: `web/lib/cms/client.ts` (또는 CMS 이름에 맞게)

**Contentful 예시:**
```typescript
import { createClient } from 'contentful';

export const contentfulClient = createClient({
  space: process.env.NEXT_PUBLIC_CONTENTFUL_SPACE_ID!,
  accessToken: process.env.NEXT_PUBLIC_CONTENTFUL_ACCESS_TOKEN!,
});
```

**Strapi 예시:**
```typescript
const STRAPI_URL = process.env.NEXT_PUBLIC_STRAPI_API_URL || 'http://localhost:1337';

export async function fetchStrapiData(endpoint: string) {
  const res = await fetch(`${STRAPI_URL}/api${endpoint}`, {
    headers: {
      'Authorization': `Bearer ${process.env.STRAPI_API_TOKEN}`,
    },
  });
  return res.json();
}
```

---

## 3. 콘텐츠 모델 재정의

### 3.1 현재 Sanity 스키마 구조

현재 Sanity에서 정의된 콘텐츠 모델:

#### 싱글톤 페이지 (각각 하나만)
1. **Site Settings** (`siteSettings`)
   - `brandName`, `mainNav`, `footerIntro`, `footerColumns`, `contactEmail`, `disclaimer`

2. **Home Page** (`homePage`)
   - `heroTitle`, `heroSubtitle`, `heroCtaLabel`, `heroBadge`
   - `highlights[]` (서비스 카드)
   - `reviewsTitle`, `reviews[]` (후기)
   - `benefitsTitle`, `benefits[]` (혜택)
   - `trustedTitle`, `trustedLogos[]` (신뢰 로고)
   - `impactTitle`, `impactBody`, `impactStatLabel`, `impactStatBody`, `impactCtaLabel`, `impactCtaUrl`
   - `categoriesTitle`, `categories[]`
   - `faqTeaserTitle`, `faqTeaserBody`, `faqItems[]`

3. **How It Works Page** (`howItWorksPage`)
   - `title`, `subtitle`
   - `steps[]` (단계별 설명)
   - `ctaTitle`, `ctaLines[]`, `ctaButtonLabel`, `ctaButtonUrl`

4. **Use Cases Page** (`useCasesPage`)
   - `title`, `subtitle`
   - `useCases[]` (사용 사례)
   - `ctaTitle`, `ctaBody`, `ctaButtonLabel`, `ctaButtonUrl`

#### 재사용 가능한 문서
- **Testimonial** (`testimonial`)
- **FAQ** (`faq`)
- **Use Case** (`useCase`)

### 3.2 새 CMS에서 모델 정의

선택한 CMS의 관리 인터페이스에서 위 구조와 동일하게 콘텐츠 모델을 정의합니다.

**Contentful 예시:**
- Content Model에서 "Site Settings", "Home Page" 등을 Content Type으로 생성
- 각 필드 타입을 Contentful의 타입에 맞게 매핑 (Text, Rich Text, Media, Reference 등)

**Strapi 예시:**
- Content-Type Builder에서 Collection Type 또는 Single Type 생성
- 각 필드를 Strapi의 필드 타입에 맞게 설정

---

## 4. 페이지 연동 코드 수정

### 4.1 현재 Sanity 사용 페이지

다음 페이지에서 Sanity 코드를 제거하고 새 CMS 코드로 교체해야 합니다:

1. `web/app/(marketing)/page.tsx` (홈 페이지)
2. `web/app/(marketing)/how-it-works/page.tsx`
3. `web/app/(marketing)/use-cases/page.tsx`

### 4.2 수정 작업

#### Step 1: Import 문 변경

**기존 (Sanity):**
```typescript
import { getHomePage, getSiteSettings } from '@/lib/sanity/client';
import type { HomePage } from '@/lib/sanity/client';
```

**새 CMS (Contentful 예시):**
```typescript
import { getHomePage, getSiteSettings } from '@/lib/cms/contentful';
import type { HomePage } from '@/lib/cms/types';
```

#### Step 2: 데이터 가져오기 함수 교체

**기존 (Sanity):**
```typescript
export default async function HomePage() {
  const [site, page] = await Promise.all([
    getSiteSettings(),
    getHomePage(),
  ]);
  // ...
}
```

**새 CMS (Contentful 예시):**
```typescript
export default async function HomePage() {
  const [site, page] = await Promise.all([
    getSiteSettings(),  // 새 CMS 함수
    getHomePage(),      // 새 CMS 함수
  ]);
  // ...
}
```

#### Step 3: 이미지 처리 변경

**기존 (Sanity):**
```typescript
import { urlFor } from '@/lib/sanity/client';
const imageUrl = urlFor(page.heroImage).width(800).url();
```

**새 CMS (Contentful 예시):**
```typescript
const imageUrl = `https:${page.heroImage.fields.file.url}`;
```

### 4.3 새 CMS 헬퍼 함수 생성

새 파일 생성: `web/lib/cms/queries.ts` (또는 CMS 이름에 맞게)

**Contentful 예시:**
```typescript
import { contentfulClient } from './client';

export async function getSiteSettings() {
  const entry = await contentfulClient.getEntry('siteSettings');
  return entry.fields;
}

export async function getHomePage() {
  const entry = await contentfulClient.getEntry('homePage');
  return entry.fields;
}
```

**Strapi 예시:**
```typescript
import { fetchStrapiData } from './client';

export async function getSiteSettings() {
  const data = await fetchStrapiData('/site-setting?populate=*');
  return data.data;
}

export async function getHomePage() {
  const data = await fetchStrapiData('/home-page?populate=*');
  return data.data;
}
```

---

## 5. 타입 정의 업데이트

### 5.1 새 타입 파일 생성

새 파일: `web/lib/cms/types.ts`

**Contentful 예시:**
```typescript
export interface SiteSettings {
  brandName?: string;
  mainNav?: Array<{ label: string; href: string }>;
  footerIntro?: string;
  // ... 기존과 동일한 구조
}

export interface HomePage {
  heroTitle?: string;
  heroSubtitle?: string;
  // ... 기존과 동일한 구조
}
```

**중요:** 타입 구조는 기존 Sanity 타입과 동일하게 유지하여 페이지 컴포넌트 코드 변경을 최소화합니다.

---

## 6. 콘텐츠 마이그레이션

### 6.1 데이터 내보내기

Sanity에서 콘텐츠를 JSON으로 내보냅니다:

1. Sanity Studio에서 각 문서를 JSON으로 내보내기
2. 또는 Sanity CLI 사용:
```bash
npx sanity@latest dataset export production backup.json
```

### 6.2 데이터 가져오기

새 CMS의 API 또는 관리 인터페이스를 사용하여 데이터를 가져옵니다.

**Contentful 예시:**
- Contentful Management API 사용
- 또는 수동으로 관리 인터페이스에서 입력

**Strapi 예시:**
- Strapi API를 통해 POST 요청으로 데이터 입력
- 또는 관리 인터페이스에서 수동 입력

---

## 7. 테스트 및 검증

### 7.1 체크리스트

- [ ] 새 CMS에서 모든 콘텐츠 모델이 정의되었는지 확인
- [ ] 환경 변수가 올바르게 설정되었는지 확인
- [ ] 홈 페이지(`/`)가 정상적으로 렌더링되는지 확인
- [ ] How It Works 페이지(`/how-it-works`)가 정상적으로 렌더링되는지 확인
- [ ] Use Cases 페이지(`/use-cases`)가 정상적으로 렌더링되는지 확인
- [ ] 이미지가 올바르게 표시되는지 확인
- [ ] 폴백(fallback) 값이 올바르게 작동하는지 확인

### 7.2 빌드 테스트

```bash
cd web
npm run build
```

빌드 오류가 없는지 확인합니다.

---

## 8. 정리 작업

### 8.1 불필요한 파일 정리

- `sanity/` 폴더 전체 삭제
- `web/app/studio/` 폴더 삭제 (있는 경우)
- Sanity 관련 문서 파일 삭제 (선택사항)

### 8.2 README 업데이트

프로젝트 README에서 Sanity 관련 내용을 제거하고 새 CMS 관련 내용으로 업데이트합니다.

---

## 9. 주의사항

### 9.1 점진적 마이그레이션

- 한 번에 모든 것을 바꾸지 말고, 페이지별로 단계적으로 마이그레이션
- 각 페이지 마이그레이션 후 테스트

### 9.2 타입 호환성

- 타입 구조를 기존과 동일하게 유지하여 페이지 컴포넌트 변경 최소화
- 새 CMS의 데이터 구조가 다를 경우, 헬퍼 함수에서 변환 처리

### 9.3 이미지 처리

- 각 CMS마다 이미지 URL 형식이 다름
- 이미지 최적화가 필요한 경우, Next.js Image 컴포넌트와 함께 사용

### 9.4 환경 변수 보안

- `.env.local`은 `.gitignore`에 포함되어 있는지 확인
- 프로덕션 환경 변수는 배포 플랫폼(Vercel, Netlify 등)에서 설정

---

## 10. 롤백 계획

문제 발생 시 빠르게 롤백할 수 있도록:

1. Sanity 코드를 완전히 삭제하지 말고, 주석 처리하거나 별도 브랜치에 보관
2. Git 커밋을 작은 단위로 나누어 커밋
3. 각 단계마다 테스트 후 커밋

---

## 요약

CMS 전환 시 주요 작업:

1. ✅ **Sanity 코드 제거** - 패키지, 파일, 환경 변수
2. ✅ **새 CMS 설정** - SDK 설치, 환경 변수, 클라이언트 설정
3. ✅ **콘텐츠 모델 재정의** - 새 CMS에서 동일한 구조로 정의
4. ✅ **페이지 연동 코드 수정** - 데이터 가져오기 함수 교체
5. ✅ **타입 정의 업데이트** - 새 CMS에 맞는 타입 정의
6. ✅ **콘텐츠 마이그레이션** - 기존 데이터를 새 CMS로 이동
7. ✅ **테스트 및 검증** - 모든 페이지가 정상 작동하는지 확인
8. ✅ **정리 작업** - 불필요한 파일 제거, 문서 업데이트

---

## 추가 리소스

- [Contentful Migration Guide](https://www.contentful.com/developers/docs/tutorials/general/migrating-to-contentful/)
- [Strapi Migration Guide](https://docs.strapi.io/dev-docs/migration)
- [Payload CMS Documentation](https://payloadcms.com/docs)

