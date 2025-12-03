'use client';

import { useSession } from 'next-auth/react';

export function useAuth() {
  const { data: session, status } = useSession();

  return {
    session,
    isAuthenticated: status === 'authenticated',
    isLoading: status === 'loading',
    userId: session?.user?.email, // Using email as a stable ID
    email: session?.user?.email,
    isAdmin: (session?.user as any)?.isAdmin || false,
    role: (session?.user as any)?.role || 'user',
  };
}