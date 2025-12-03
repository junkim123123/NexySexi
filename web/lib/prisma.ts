import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

function createPrismaClient(): PrismaClient | null {
  try {
    // Check if DATABASE_URL is valid
    const dbUrl = process.env.DATABASE_URL;
    if (!dbUrl || dbUrl.trim() === '') {
      console.warn('[Prisma] DATABASE_URL is not set');
      return null;
    }

    // Check if URL is Prisma Dev format (prisma:// or prisma+postgres://)
    // If not, we'll try to use it directly
    const client = new PrismaClient({
      log: process.env.NODE_ENV === 'development' ? ['query', 'error', 'warn'] : ['error'],
    });

    return client;
  } catch (error: any) {
    console.warn('[Prisma] Failed to create Prisma Client:', error?.message || error);
    return null;
  }
}

export const prisma =
  globalForPrisma.prisma ?? createPrismaClient();

if (process.env.NODE_ENV !== 'production' && prisma) {
  globalForPrisma.prisma = prisma;
}

