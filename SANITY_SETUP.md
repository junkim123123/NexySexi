# Sanity CMS 설정 가이드

## 1. Sanity 프로젝트 생성

1. [Sanity.io](https://www.sanity.io)에 가입
2. 새 프로젝트 생성
3. 프로젝트 ID와 Dataset 이름 확인

## 2. 환경 변수 설정

`.env.local` 파일에 다음 변수 추가:

```env
NEXT_PUBLIC_SANITY_PROJECT_ID=your-project-id
NEXT_PUBLIC_SANITY_DATASET=production
SANITY_API_TOKEN=your-api-token  # (선택사항, 쓰기 권한 필요)
```

## 3. Sanity Studio 실행

프로젝트 루트에서:

```bash
npx sanity dev
```

또는 Sanity 웹사이트에서 직접 접근:
- https://www.sanity.io/manage

## 4. 스키마 배포

스키마는 이미 `sanity/schemas/` 폴더에 정의되어 있습니다.

Sanity Studio에서:
1. 프로젝트 설정 → API → Add CORS origin
2. 로컬 개발: `http://localhost:3000` 추가
3. 프로덕션: 실제 도메인 추가

## 5. 콘텐츠 타입

다음 콘텐츠 타입이 정의되어 있습니다:

- **Homepage Hero**: 메인 랜딩 페이지 히어로 섹션
- **Service Card**: 서비스 소개 카드들
- **Testimonial**: 고객 후기/리뷰
- **Benefit Card**: 혜택 카드들
- **FAQ**: 자주 묻는 질문
- **Use Case**: 사용 사례
- **Mission Section**: 미션 섹션
- **Featured On**: "Trusted by" 섹션
- **Category Link**: 카테고리 링크들

## 6. 데이터 가져오기

각 페이지에서 Sanity 데이터를 가져오는 예시:

```typescript
import { fetchSanityData } from '@/lib/sanity/client';
import { HERO_QUERY } from '@/lib/sanity/queries';
import type { HomepageHero } from '@/lib/sanity/schema';

// Server Component에서
const hero = await fetchSanityData<HomepageHero>(HERO_QUERY);
```

## 7. 이미지 사용

```typescript
import { urlFor } from '@/lib/sanity/client';

const imageUrl = urlFor(hero.heroImage)
  .width(800)
  .height(600)
  .url();
```

## 8. 다음 단계

1. Sanity 프로젝트 생성 및 환경 변수 설정
2. Sanity Studio에서 초기 콘텐츠 입력
3. 랜딩 페이지를 Sanity 데이터로 마이그레이션
4. 테스트 및 배포

