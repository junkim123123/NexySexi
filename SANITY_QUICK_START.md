# Sanity CMS 빠른 시작 가이드

## 현재 상황

✅ **완료된 작업:**
- Sanity 프로젝트 설정 완료 (ID: vqt42bhw, Dataset: production)
- 환경 변수 설정 완료
- 스키마 정의 완료
- Next.js 연동 완료 (페이지가 Sanity 데이터 사용)

❌ **문제:**
- 로컬 Sanity Studio 실행 실패 (모듈 해석 오류)
- `next-sanity` 설치 실패 (Next.js 14와 호환 불가)

## 해결 방법: Sanity 웹사이트에서 직접 접근

로컬 Studio 없이도 콘텐츠를 관리할 수 있습니다.

### 1. Sanity Studio 접속

1. 브라우저에서 **https://www.sanity.io/manage** 접속
2. 로그인 (Sanity 계정 필요)
3. 프로젝트 **vqt42bhw** 선택
4. Studio 열기

### 2. 콘텐츠 입력

Studio가 열리면 다음 문서들을 생성하세요:

#### 싱글톤 페이지 (각각 하나만)
1. **Site Settings** - 전역 사이트 설정
2. **Home Page** - 홈 페이지 콘텐츠
3. **How It Works Page** - How It Works 페이지
4. **Use Cases Page** - Use Cases 페이지

#### 재사용 가능한 문서
- **Testimonial** - 고객 후기 (여러 개 가능)
- **FAQ** - 자주 묻는 질문 (여러 개 가능)
- **Use Case** - 개별 사용 사례 (여러 개 가능)

### 3. Next.js에서 확인

```bash
cd web
npm run dev
```

브라우저에서 `http://localhost:3000` (또는 표시된 포트)로 접속하여 Sanity에서 입력한 콘텐츠가 표시되는지 확인하세요.

## 현재 상태

- ✅ Next.js 앱: 정상 작동
- ✅ Sanity 연동: 완료
- ✅ 환경 변수: 설정 완료
- ✅ 스키마: 정의 완료
- ⚠️ 로컬 Studio: 실행 불가 (웹사이트에서 접근 권장)

## 참고

- Sanity 웹사이트에서 입력한 콘텐츠는 즉시 Next.js 페이지에 반영됩니다
- 로컬 Studio가 꼭 필요하지 않습니다
- 웹사이트 Studio가 더 안정적이고 설정이 간단합니다

