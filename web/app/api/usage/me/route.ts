import { NextResponse } from "next/server";
import { getServerSession } from "next-auth/next";
import { getUsage } from "@/lib/usage/limit";
import { headers } from "next/headers";

export async function GET() {
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

    const usage = getUsage(identifier, isAuthenticated);

    return NextResponse.json(usage, { status: 200 });
  } catch (err) {
    console.error("[UsageMe] Unexpected server error", err);
    return NextResponse.json(
      {
        error: "Something went wrong.",
      },
      { status: 500 }
    );
  }
}