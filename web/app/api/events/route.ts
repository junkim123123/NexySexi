import { NextResponse } from 'next/server';
import { getServerSession } from "next-auth/next";
import { headers } from "next/headers";
import { addEvent } from '@/lib/analytics/events';

export async function POST(req: Request) {
  try {
    const session = await getServerSession();
    const isAuthenticated = !!session?.user;
    
    let identifier: string;
    if (isAuthenticated) {
      identifier = session.user!.email!;
    } else {
      const ip = headers().get('x-forwarded-for') || 'unknown';
      const userAgent = headers().get('user-agent') || 'unknown';
      identifier = `${ip}-${userAgent}`;
    }

    const { name, payload, timestamp } = await req.json();
    addEvent(identifier, { type: name, timestamp, metadata: payload });
    console.log('[Event]', timestamp, name, payload);
    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error('[Event API] Error:', error);
    return NextResponse.json(
      { ok: false, error: 'Internal Server Error' },
      { status: 500 }
    );
  }
}