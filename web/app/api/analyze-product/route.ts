import { NextResponse } from "next/server";
import { getServerSession } from "next-auth/next";
import { analyzeProduct } from "@/lib/ai/productAnalysis";
import { incrementUsage } from "@/lib/usage/limit";
import { headers } from "next/headers";

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

    const { count, limit } = incrementUsage(identifier, isAuthenticated);
    if (count > limit) {
      return NextResponse.json(
        {
          ok: false,
          error: "quota_exceeded",
          reason: isAuthenticated ? 'authenticated_daily_limit' : 'anonymous_daily_limit',
          message: "You have exceeded the number of free analyses for today.",
        },
        { status: 429 }
      );
    }
    
    const formData = await req.formData();
    const input = formData.get('input') as string;
    const imageFile = formData.get('image') as File | null;

    if (!input) {
      return NextResponse.json(
        { ok: false, error: "Input is required." },
        { status: 400 }
      );
    }

    let imageBase64: string | undefined = undefined;
    if (imageFile) {
      const buffer = await imageFile.arrayBuffer();
      imageBase64 = Buffer.from(buffer).toString('base64');
    }

    console.log("[AnalyzeProduct] Incoming request for:", input.substring(0, 50) + "...");

    const analysis = await analyzeProduct(input, imageBase64);

    return NextResponse.json(
      {
        ok: true,
        analysis,
      },
      { status: 200 }
    );
  } catch (err) {
    console.error("[AnalyzeProduct] Unexpected server error", err);
    return NextResponse.json(
      {
        ok: false,
        error: "Something went wrong while analyzing the product.",
      },
      { status: 500 }
    );
  }
}