import { NextResponse } from 'next/server';
import { z } from 'zod';

const feedbackSchema = z.object({
  rating: z.enum(['up', 'down']),
  mode: z.enum(['quick_scan', 'conversational']),
  productSummary: z.string(),
  leadSource: z.string().optional(),
});

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const validation = feedbackSchema.safeParse(body);

    if (!validation.success) {
      return NextResponse.json({ error: validation.error.errors }, { status: 400 });
    }

    // For now, just log the payload on the server.
    // In a real application, this would be stored in a database.
    console.log('[FEEDBACK RECEIVED]', validation.data);

    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error('[API_FEEDBACK_ERROR]', error);
    return NextResponse.json({ error: 'Internal Server Error' }, { status: 500 });
  }
}