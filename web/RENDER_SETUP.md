# Render 배포 가이드 - NexSupply Platform

## 사전 준비

1. **GitHub 저장소 준비**
   - 코드가 GitHub에 푸시되어 있어야 합니다
   - `render.yaml` 파일이 루트 디렉토리에 있어야 합니다

2. **환경 변수 준비**
   - GEMINI_API_KEY
   - SMTP_SERVER (선택사항)
   - SMTP_PORT (선택사항, 기본값: 465)
   - SMTP_USERNAME (선택사항)
   - SMTP_PASSWORD (선택사항)
   - SMTP_FROM_EMAIL (선택사항)

## Render 배포 단계

### 1. Render 계정 생성 및 로그인

1. [Render.com](https://render.com) 접속
2. GitHub 계정으로 로그인
3. GitHub 저장소 연결 승인

### 2. 새 Web Service 생성

1. **Dashboard** → **New +** → **Web Service** 클릭
2. **Connect GitHub** 버튼 클릭
3. 저장소 선택: `nexsupply-platform`
4. 브랜치 선택: `main`

### 3. 서비스 설정

Render가 `render.yaml` 파일을 자동으로 감지합니다. 다음 설정이 자동으로 적용됩니다:

- **Name**: `nexsupply-platform`
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`

### 4. 환경 변수 설정

**Settings** → **Environment** 섹션에서 다음 환경 변수를 추가:

```
GEMINI_API_KEY=your-gemini-api-key-here
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=465
SMTP_USERNAME=outreach@nexsupply.net
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=outreach@nexsupply.net
```

**중요**: 
- `GEMINI_API_KEY`는 필수입니다
- SMTP 관련 변수는 이메일 기능을 사용할 때만 필요합니다
- `SMTP_PASSWORD`는 Gmail 앱 비밀번호를 사용해야 합니다

### 5. 배포 시작

1. **Create Web Service** 버튼 클릭
2. 배포가 자동으로 시작됩니다
3. 빌드 로그를 확인하여 오류가 없는지 확인

### 6. 배포 완료 확인

- 배포가 완료되면 Render가 자동으로 URL을 생성합니다
- 예: `https://nexsupply-platform.onrender.com`
- 이 URL로 접속하여 앱이 정상 작동하는지 확인

## 배포 후 확인 사항

1. **홈페이지 접속 확인**
   - 메인 페이지가 정상적으로 로드되는지 확인

2. **AI 분석 기능 테스트**
   - 제품 검색 및 분석이 정상 작동하는지 확인

3. **Analytics 페이지 확인**
   - `https://your-app.onrender.com/analytics?admin=1` 접속
   - 데이터가 정상적으로 표시되는지 확인

## 문제 해결

### 배포 실패 시

1. **빌드 로그 확인**
   - Render Dashboard → 해당 서비스 → **Logs** 탭
   - 에러 메시지 확인

2. **일반적인 문제**
   - `requirements.txt`에 모든 의존성이 포함되어 있는지 확인
   - 환경 변수가 올바르게 설정되었는지 확인
   - Python 버전 호환성 확인 (Python 3.9+ 필요)

### 앱이 시작되지 않는 경우

1. **포트 설정 확인**
   - `$PORT` 환경 변수가 올바르게 사용되고 있는지 확인
   - `--server.address 0.0.0.0`이 포함되어 있는지 확인

2. **환경 변수 확인**
   - `GEMINI_API_KEY`가 설정되어 있는지 확인
   - Secrets 탭에서 환경 변수 재확인

### 데이터베이스 문제

- SQLite 데이터베이스는 Render의 임시 파일 시스템에 생성됩니다
- 서비스 재시작 시 데이터가 초기화될 수 있습니다
- 영구 저장이 필요한 경우 PostgreSQL 서비스를 추가로 생성하세요

## Render 서비스 관리

### 서비스 재시작

- Dashboard → 해당 서비스 → **Manual Deploy** → **Clear build cache & deploy**

### 로그 확인

- Dashboard → 해당 서비스 → **Logs** 탭
- 실시간 로그 확인 가능

### 환경 변수 수정

- Dashboard → 해당 서비스 → **Environment** 탭
- 환경 변수 추가/수정 후 **Save Changes**
- 서비스가 자동으로 재배포됩니다

## 비용 정보

- **Free Tier**: 
  - 서비스가 15분 동안 요청이 없으면 자동으로 sleep 상태로 전환
  - 첫 요청 시 약 30초 정도의 cold start 시간 소요
  - 월 750시간 무료

- **Paid Plans**:
  - 항상 실행 상태 유지
  - 더 빠른 응답 시간
  - 더 많은 리소스 할당

## 추가 리소스

- [Render 공식 문서](https://render.com/docs)
- [Streamlit 배포 가이드](https://docs.streamlit.io/deploy)

