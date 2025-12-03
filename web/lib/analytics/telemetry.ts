import { getSession } from 'next-auth/react';

export async function logEvent(name: string, payload?: Record<string, any>) {
  try {
    const session = await getSession();
    const user = session?.user;

    await fetch('/api/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        payload,
        timestamp: new Date().toISOString(),
        userId: user?.email,
        email: user?.email,
      }),
    });
  } catch (error) {
    // Fire-and-forget, so we ignore failures.
    console.warn('[logEvent] Failed to log event:', error);
  }
}