// FILE: lib/config/env.ts - 환경 변수 검증 및 관리
// Render 배포 시 필요한 모든 환경 변수를 중앙에서 관리하고 검증합니다.

/**
 * 필수 환경 변수 목록
 * 이 변수들이 없으면 애플리케이션이 시작되지 않습니다.
 */
const REQUIRED_ENV_VARS = [
  'GEMINI_API_KEY',
  'NEXTAUTH_SECRET',
] as const;

/**
 * 선택적 환경 변수 목록
 * 이 변수들이 없어도 애플리케이션이 시작되지만, 일부 기능이 비활성화될 수 있습니다.
 */
const OPTIONAL_ENV_VARS = [
  'NEXTAUTH_URL',
  'GOOGLE_CLIENT_ID',
  'GOOGLE_CLIENT_SECRET',
  'EMAIL_SERVER',
  'EMAIL_FROM',
  'DATABASE_URL',
  'RESEND_API_KEY',
  'SMTP_HOST',
  'SMTP_PORT',
  'SMTP_USER',
  'SMTP_PASS',
  'SYSTEM_EMAIL_FROM',
  'ADMIN_EMAIL',
  'NEXT_PUBLIC_GOOGLE_ENABLED',
  'NEXT_PUBLIC_EMAIL_ENABLED',
] as const;

/**
 * 환경 변수 검증 결과
 */
interface EnvValidationResult {
  isValid: boolean;
  missing: string[];
  warnings: string[];
}

/**
 * 필수 환경 변수가 모두 설정되어 있는지 검증합니다.
 * @returns 검증 결과 객체
 */
export function validateEnv(): EnvValidationResult {
  const missing: string[] = [];
  const warnings: string[] = [];

  // 필수 변수 검증
  for (const key of REQUIRED_ENV_VARS) {
    const value = process.env[key];
    if (!value || value.trim() === '') {
      missing.push(key);
    }
  }

  // 선택적 변수에 대한 경고 (프로덕션 환경에서만)
  if (process.env.NODE_ENV === 'production') {
    // NextAuth URL이 설정되지 않았으면 경고
    if (!process.env.NEXTAUTH_URL) {
      warnings.push('NEXTAUTH_URL is not set. NextAuth may not work correctly in production.');
    }

    // 데이터베이스가 설정되지 않았으면 경고 (Prisma 사용 시)
    if (!process.env.DATABASE_URL) {
      warnings.push('DATABASE_URL is not set. Database features will be disabled.');
    }
  }

  return {
    isValid: missing.length === 0,
    missing,
    warnings,
  };
}

/**
 * 환경 변수를 안전하게 읽습니다.
 * @param key 환경 변수 키
 * @param defaultValue 기본값 (선택적)
 * @returns 환경 변수 값 또는 기본값
 */
export function getEnv(key: string, defaultValue?: string): string {
  const value = process.env[key];
  if (!value && defaultValue === undefined) {
    throw new Error(`Environment variable ${key} is not set and no default value provided.`);
  }
  return value || defaultValue || '';
}

/**
 * 불린 환경 변수를 안전하게 읽습니다.
 * @param key 환경 변수 키
 * @param defaultValue 기본값
 * @returns 불린 값
 */
export function getEnvBool(key: string, defaultValue: boolean = false): boolean {
  const value = process.env[key];
  if (!value) return defaultValue;
  return value.toLowerCase() === 'true' || value === '1';
}

/**
 * 숫자 환경 변수를 안전하게 읽습니다.
 * @param key 환경 변수 키
 * @param defaultValue 기본값
 * @returns 숫자 값
 */
export function getEnvNumber(key: string, defaultValue: number): number {
  const value = process.env[key];
  if (!value) return defaultValue;
  const parsed = parseInt(value, 10);
  if (isNaN(parsed)) {
    console.warn(`Environment variable ${key} is not a valid number, using default value.`);
    return defaultValue;
  }
  return parsed;
}

/**
 * 애플리케이션 시작 시 환경 변수를 검증하고 결과를 출력합니다.
 * 필수 변수가 없으면 에러를 던집니다.
 */
export function validateEnvOnStartup(): void {
  const result = validateEnv();

  if (!result.isValid) {
    const errorMessage = `
❌ Missing required environment variables:
${result.missing.map(key => `  - ${key}`).join('\n')}

Please set these environment variables in Render dashboard:
Settings → Environment → Add Environment Variable

For local development, add them to .env.local file.
`;
    throw new Error(errorMessage);
  }

  // 경고 메시지 출력 (프로덕션에서만)
  if (result.warnings.length > 0 && process.env.NODE_ENV === 'production') {
    console.warn('⚠️ Environment variable warnings:');
    result.warnings.forEach(warning => {
      console.warn(`  - ${warning}`);
    });
  }

  if (process.env.NODE_ENV === 'development') {
    console.log('✅ Environment variables validated successfully');
  }
}

// 프로덕션 환경에서만 시작 시 자동 검증
if (typeof window === 'undefined' && process.env.NODE_ENV === 'production') {
  try {
    validateEnvOnStartup();
  } catch (error) {
    console.error(error);
    // 서버 시작을 막지 않고 경고만 출력 (Render에서 환경 변수를 나중에 설정할 수 있도록)
  }
}

