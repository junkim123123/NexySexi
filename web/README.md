# NexSupply - B2B Sourcing Platform

AI-powered B2B sourcing intelligence platform that provides cost analysis, supplier verification, and market insights for global sourcing decisions.

## Features

- 🤖 **AI-Powered Analysis**: Gemini 2.5 Pro for intelligent sourcing insights
- 💰 **Landed Cost Calculator**: Accurate cost breakdown with hidden cost alerts
- ✅ **Product Analysis**: Quick scan and conversational copilot for sourcing analysis
- 📊 **Risk Assessment**: Comprehensive risk scoring and recommendations
- ⏱️ **Lead Intelligence**: Automated lead routing and prioritization
- 🔐 **Authentication**: NextAuth.js with Google OAuth and Email magic links

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **AI Model**: Google Gemini 2.5 Pro
- **Authentication**: NextAuth.js
- **Database**: PostgreSQL (via Prisma, optional)
- **Styling**: Tailwind CSS
- **Deployment**: Render

## Quick Start

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd nexsupply-platform/web
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Set up environment variables**
   - Copy `.env.example` to `.env.local` (if exists)
   - Add your environment variables (see [Environment Variables](#environment-variables) section)

4. **Run the development server**
   ```bash
   npm run dev
   ```

5. **Open your browser**
   - Navigate to [http://localhost:3000](http://localhost:3000)

### Package Manager

This project uses **npm** as the package manager. All build and start commands use npm.

- Build: `npm run build`
- Start: `npm run start`
- Dev: `npm run dev`

## Deployment

### Deploy on Render (GitHub 연동)

이 레포는 이미 GitHub에 있으므로, Render 대시보드에서 기존 GitHub 레포를 선택하기만 하면 됩니다.

#### 방법 1: render.yaml 파일 사용 (권장)

1. **GitHub에 코드 푸시**
   ```bash
   git add .
   git commit -m "Ready for Render deployment"
   git push origin main
   ```

2. **Render에 로그인**
   - [Render.com](https://render.com) 접속
   - GitHub 계정으로 로그인
   - GitHub 저장소 연결 승인

3. **새 Web Service 생성**
   - Dashboard → **New +** → **Web Service** 클릭
   - **Connect GitHub** 버튼 클릭
   - 저장소 선택: 이 레포 선택
   - 브랜치 선택: `main` (또는 기본 브랜치)

4. **자동 설정**
   - Render가 `render.yaml` 파일을 자동으로 감지합니다
   - 다음 설정이 자동으로 적용됩니다:
     - **Environment**: Node
     - **Build Command**: `npm install && npm run build`
     - **Start Command**: `npm run start`
     - **Health Check Path**: `/api/health`

5. **환경 변수 설정**
   - **Settings** → **Environment** 섹션으로 이동
   - 아래 [Environment Variables](#environment-variables) 표를 참고하여 모든 변수 추가
   - 각 변수의 실제 값을 입력 (표에는 예시만 표시)

6. **서비스 생성**
   - **Create Web Service** 버튼 클릭
   - 배포가 자동으로 시작됩니다
   - 빌드 로그를 확인하여 오류가 없는지 확인

7. **배포 완료**
   - 배포 완료 후 Render가 자동으로 URL 생성: `https://서비스이름.onrender.com`
   - 해당 URL로 접속하여 애플리케이션 확인

#### 방법 2: render.yaml 없이 UI에서 직접 설정

`render.yaml` 파일을 사용하지 않고 Render 대시보드에서 직접 설정할 수도 있습니다:

1. **새 Web Service 생성** (위와 동일)

2. **수동 설정**
   - **Environment**: `Node`
   - **Build Command**: `npm install && npm run build`
   - **Start Command**: `npm run start`
   - **Health Check Path**: `/api/health` (선택사항)

3. **환경 변수 추가** (위와 동일)

4. **서비스 생성** (위와 동일)

#### Environment Variables

Render 대시보드의 **Settings → Environment**에서 다음 환경 변수들을 설정해야 합니다:

| 변수명 | 설명 | 필수 | 예시 값 |
|--------|------|------|---------|
| `GEMINI_API_KEY` | Google Gemini API 키 | ✅ 필수 | (실제 API 키) |
| `NEXTAUTH_SECRET` | NextAuth 세션 암호화 키 | ✅ 필수 | (openssl rand -base64 32로 생성) |
| `NEXTAUTH_URL` | 애플리케이션 공개 URL | 권장 | `https://nexsupply-web.onrender.com` |
| `GOOGLE_CLIENT_ID` | Google OAuth 클라이언트 ID | 선택 | (Google Cloud Console에서 생성) |
| `GOOGLE_CLIENT_SECRET` | Google OAuth 클라이언트 Secret | 선택 | (Google Cloud Console에서 생성) |
| `EMAIL_SERVER` | Email 서버 설정 | 선택 | `smtp://smtp.gmail.com:587` |
| `EMAIL_FROM` | 발신자 이메일 주소 | 선택 | `noreply@nexsupply.net` |
| `DATABASE_URL` | PostgreSQL 연결 문자열 | 선택 | (Prisma 사용 시) |
| `RESEND_API_KEY` | Resend API 키 | 선택 | (이메일 발송용) |
| `SMTP_HOST` | SMTP 호스트 | 선택 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 포트 | 선택 | `465` |
| `SMTP_USER` | SMTP 사용자명 | 선택 | (이메일 주소) |
| `SMTP_PASS` | SMTP 비밀번호 | 선택 | (앱 비밀번호) |
| `SYSTEM_EMAIL_FROM` | 시스템 발신자 이메일 | 선택 | `system@nexsupply.net` |
| `ADMIN_EMAIL` | 관리자 이메일 | 선택 | `admin@nexsupply.net` |
| `NEXT_PUBLIC_GOOGLE_ENABLED` | Google 로그인 활성화 | 선택 | `true` |
| `NEXT_PUBLIC_EMAIL_ENABLED` | Email 로그인 활성화 | 선택 | `true` |

**중요 사항:**
- 필수 변수 (`GEMINI_API_KEY`, `NEXTAUTH_SECRET`)는 반드시 설정해야 합니다
- `NEXTAUTH_SECRET` 생성 방법:
  ```bash
  openssl rand -base64 32
  ```
- `NEXTAUTH_URL`은 배포 후 실제 Render URL로 업데이트해야 합니다
- 선택적 변수는 해당 기능을 사용할 때만 설정하면 됩니다

### Health Check

애플리케이션은 `/api/health` 엔드포인트를 제공합니다. Render 대시보드에서 Health Check Path로 설정할 수 있습니다.

```bash
curl https://your-app.onrender.com/api/health
```

응답 예시:
```json
{
  "ok": true,
  "status": "healthy",
  "timestamp": "2024-01-01T00:00:00.000Z",
  "environment": "production",
  "environmentVariables": {
    "GEMINI_API_KEY": true,
    "NEXTAUTH_SECRET": true
  }
}
```

## Project Structure

```
web/
├── app/                      # Next.js App Router
│   ├── api/                  # API routes
│   │   ├── analyze-product/  # Product analysis endpoints
│   │   ├── auth/             # NextAuth.js routes
│   │   ├── events/           # Analytics endpoints
│   │   ├── feedback/         # Feedback endpoint
│   │   ├── health/           # Health check endpoint
│   │   └── sample-request/   # Lead generation endpoints
│   ├── (sections)/           # Landing page sections
│   └── page.tsx              # Main landing page
├── components/               # React components
│   ├── ui/                   # UI components (Button, Card, etc.)
│   └── ...                   # Other components
├── lib/                      # Utility libraries
│   ├── ai/                   # AI service integrations
│   ├── analytics/            # Analytics utilities
│   ├── auth.ts               # Authentication helpers
│   ├── config/               # Configuration (env validation)
│   └── ...                   # Other utilities
├── prisma/                   # Prisma schema (optional)
│   └── schema.prisma
├── next.config.js            # Next.js configuration
├── render.yaml               # Render deployment config
└── package.json              # Dependencies and scripts
```

## Environment Variables

로컬 개발 시 `.env.local` 파일을 생성하고 다음 변수들을 설정하세요:

```env
# 필수
GEMINI_API_KEY=your-gemini-api-key
NEXTAUTH_SECRET=your-nextauth-secret

# 권장
NEXTAUTH_URL=http://localhost:3000

# 선택 (기능 사용 시)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
EMAIL_SERVER=smtp://smtp.gmail.com:587
EMAIL_FROM=noreply@nexsupply.net
DATABASE_URL=postgresql://user:password@host:5432/dbname
```

전체 환경 변수 목록은 [Environment Variables](#environment-variables) 섹션을 참고하세요.

## Build & Start Commands

- **Development**: `npm run dev`
- **Build**: `npm run build`
- **Start** (Production): `npm run start`

## Security

- ✅ API keys stored in environment variables
- ✅ No hardcoded credentials
- ✅ Environment variable validation on startup
- ✅ NextAuth.js for secure authentication
- ✅ Error handling with generic error codes
- ✅ Sensitive files excluded from Git (`.env.local`, `.env`)

## Troubleshooting

### Health Check 실패
- 환경 변수가 올바르게 설정되었는지 확인
- Render 대시보드의 로그 확인

### 배포 실패
- `npm install`이 성공하는지 로컬에서 확인
- `npm run build`가 성공하는지 로컬에서 확인
- Render 빌드 로그에서 에러 메시지 확인

### 환경 변수 에러
- 필수 환경 변수 (`GEMINI_API_KEY`, `NEXTAUTH_SECRET`)가 설정되었는지 확인
- 변수명 오타 확인
- Render 대시보드에서 환경 변수가 올바르게 저장되었는지 확인

## License

© 2017 NexSupply. All rights reserved.

