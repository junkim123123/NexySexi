/**
 * API route for submitting contact lead information
 * 
 * Receives contact form data along with project context from onboarding
 * and logs it for now. Later this will integrate with CRM/email system.
 */

import { NextResponse } from 'next/server';

export async function POST(req: Request) {
  try {
    const body = await req.json();
    
    // Log the submission for now
    console.log('[ContactLead] New contact submission:', JSON.stringify(body, null, 2));
    
    // TODO: Integrate with CRM/email system
    // TODO: Send notification to NexSupply team
    // TODO: Store in database
    
    return NextResponse.json({ ok: true });
  } catch (error) {
    console.error('[ContactLead] Error processing request:', error);
    return NextResponse.json(
      { error: 'Failed to process request' },
      { status: 500 }
    );
  }
}

// Only allow POST method
export async function GET() {
  return NextResponse.json(
    { error: 'Method not allowed' },
    { status: 405 }
  );
}

