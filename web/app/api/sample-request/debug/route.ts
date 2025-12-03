import { NextResponse } from "next/server";
import {
  SampleRequestSchema,
  type SampleRequestPayload,
} from "@/lib/sample-request/schema";
import { analyzeSampleRequest } from "@/lib/ai/geminiClient";
import { applyLeadGuardrails } from "@/lib/sample-request/guardrails";
import { deriveLeadRouting } from "@/lib/sample-request/routing";

export async function POST(req: Request) {
  try {
    const json = await req.json();
    const result = SampleRequestSchema.safeParse(json);

    if (!result.success) {
      return NextResponse.json(
        {
          ok: false,
          error: "Invalid input.",
          details: result.error.flatten().fieldErrors,
        },
        { status: 400 }
      );
    }

    const payload: SampleRequestPayload = result.data;

    // 1. AI Analysis (v2)
    const rawAnalysis = await analyzeSampleRequest(payload);

    // 2. Guardrails & Email Intelligence
    const guardedAnalysis = applyLeadGuardrails(payload, rawAnalysis);

    // 3. Routing & Tiering
    const routing = deriveLeadRouting(guardedAnalysis);

    return NextResponse.json(
      {
        rawAnalysis,
        guardedAnalysis,
        routing,
      },
      { status: 200 }
    );
  } catch (err) {
    console.error("[SampleRequest][Debug] Unexpected server error", err);
    return NextResponse.json(
      {
        ok: false,
        error: "Something went wrong while processing your request.",
      },
      { status: 500 }
    );
  }
}