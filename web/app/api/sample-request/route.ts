import { NextResponse } from "next/server";
import {
  SampleRequestSchema,
  type SampleRequestPayload,
  type NexSupplyLeadAnalysis,
} from "@/lib/sample-request/schema";
import { analyzeSampleRequest } from "@/lib/ai/geminiClient";
import {
  sendAdminNotificationEmail,
  sendUserConfirmationEmail,
} from "@/lib/email/sampleRequestMailer";
import { applyLeadGuardrails } from "@/lib/sample-request/guardrails";
import { deriveLeadRouting } from "@/lib/sample-request/routing";

const ANALYSIS_PREVIEW_PATTERNS = [
  "Preliminary scan: {{qualification_engine.urgency_signal}} urgency detected for {{firmographics.industry_vertical}} sourcing.",
  "Initial finding: {{content_generation.preview_key_insight}}",
  "Analysis in progress for {{lead_profile.buyer_persona_tag}} profile in {{firmographics.industry_vertical}} sector."
];

function getProperty<T, K extends string>(obj: T, path: K): string {
    const keys = path.split('.');
    let current: any = obj;
    for (const key of keys) {
        if (current === null || typeof current !== 'object' || !(key in current)) {
            return '';
        }
        current = current[key];
    }
    return String(current);
}

function renderPreview(analysis: NexSupplyLeadAnalysis): string {
  if (analysis.qualification_engine.data_completeness === "insufficient") {
    return "More Information Needed: Please provide more details about your project for a complete analysis.";
  }

  const pattern = ANALYSIS_PREVIEW_PATTERNS[Math.floor(Math.random() * ANALYSIS_PREVIEW_PATTERNS.length)];
  return pattern.replace(/\{\{([^}]+)\}\}/g, (_, key) => {
    return getProperty(analysis, key.trim() as keyof NexSupplyLeadAnalysis);
  });
}

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

    console.log("[SampleRequest] Incoming payload", {
      name: payload.name,
      email: payload.workEmail,
      company: payload.company,
    });

    // 1. AI Analysis (v2)
    const rawAnalysis = await analyzeSampleRequest(payload);

    // 2. Guardrails & Email Intelligence
    const guardedAnalysis = applyLeadGuardrails(payload, rawAnalysis);

    // 3. Routing & Tiering
    const routing = deriveLeadRouting(guardedAnalysis);

    // 4. Send Emails (Fire & Forget in parallel)
    await Promise.all([
      sendAdminNotificationEmail(payload, guardedAnalysis, routing),
      sendUserConfirmationEmail(payload, guardedAnalysis, routing),
    ]);

    // 5. Response
    const analysisPreview = renderPreview(guardedAnalysis);

    return NextResponse.json(
      {
        ok: true,
        analysisPreview,
        tier: routing.tier,
        slaHours: routing.slaHours,
      },
      { status: 200 }
    );
  } catch (err) {
    console.error("[SampleRequest] Unexpected server error", err);
    return NextResponse.json(
      {
        ok: false,
        error: "Something went wrong while processing your request.",
      },
      { status: 500 }
    );
  }
}