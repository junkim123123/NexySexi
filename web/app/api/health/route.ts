// FILE: app/api/health/route.ts - 헬스 체크 API 엔드포인트
// Render 배포 시 서비스 상태 확인용 엔드포인트
// Render 대시보드에서 Health Check Path로 설정할 수 있습니다 (예: /api/health)

import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic'; // 항상 동적 응답

export async function GET() {
  try {
    // 기본 정보
    const health = {
      ok: true,
      status: 'healthy',
      timestamp: new Date().toISOString(),
      environment: process.env.NODE_ENV || 'unknown',
      version: process.env.npm_package_version || '0.1.0',
    };

    // 필수 환경 변수 체크 (에러는 던지지 않고 상태만 표시)
    const envStatus: Record<string, boolean> = {
      GEMINI_API_KEY: !!process.env.GEMINI_API_KEY,
      NEXTAUTH_SECRET: !!process.env.NEXTAUTH_SECRET,
    };

    // 모든 필수 변수가 설정되어 있으면 healthy, 아니면 degraded
    const allEnvSet = Object.values(envStatus).every(Boolean);
    const status = allEnvSet ? 'healthy' : 'degraded';

    return NextResponse.json(
      {
        ...health,
        status,
        environmentVariables: envStatus,
        // 환경 변수가 모두 설정되어 있지 않으면 경고 추가
        ...(status === 'degraded' && {
          warning: 'Some required environment variables are not set. Please check Render dashboard settings.',
        }),
      },
      {
        status: status === 'healthy' ? 200 : 503, // degraded 상태는 503 반환
        headers: {
          'Cache-Control': 'no-cache, no-store, must-revalidate',
        },
      }
    );
  } catch (error) {
    return NextResponse.json(
      {
        ok: false,
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        error: error instanceof Error ? error.message : 'Unknown error',
      },
      { status: 500 }
    );
  }
}

