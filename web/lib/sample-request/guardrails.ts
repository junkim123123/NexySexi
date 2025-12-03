import { NexSupplyLeadAnalysis, SampleRequestPayload } from "./schema";
import { analyzeEmail } from "./emailIntel";

const EMOTIONAL_WORDS = [
  "desperate",
  "desperately",
  "dream",
  "passion",
  "freedom",
];

const TACTICAL_WORDS = [
  "units",
  "sku",
  "skus",
  "container",
  "containers",
  "factory",
  "factories",
  "3pl",
  "hs code",
  "hts",
  "moq",
];

function wordCount(text: string): number {
  return text.trim().split(/\s+/).length;
}

function containsAny(text: string, candidates: string[]): boolean {
  const lowerText = text.toLowerCase();
  return candidates.some((candidate) => lowerText.includes(candidate));
}

function isGenericCompanyName(company: string): boolean {
  const lower = company.trim().toLowerCase();
  return (
    lower.length < 3 ||
    ["n/a", "na", "none", "self"].includes(lower) ||
    lower === ""
  );
}

export function applyLeadGuardrails(
  payload: SampleRequestPayload,
  analysis: NexSupplyLeadAnalysis
): NexSupplyLeadAnalysis {
  // Clone the analysis object to avoid mutation
  const guarded = JSON.parse(JSON.stringify(analysis)) as NexSupplyLeadAnalysis;

  // Integrate Email Intelligence
  const emailIntel = analyzeEmail(payload.workEmail);
  guarded.lead_profile.email_type ??= emailIntel.emailType;
  guarded.lead_profile.email_local_part_type ??= emailIntel.localPartType;

  // 1. Insufficient data guardrail
  if (
    wordCount(payload.useCase) < 5 &&
    isGenericCompanyName(payload.company)
  ) {
    guarded.qualification_engine.opportunity_score = Math.min(
      guarded.qualification_engine.opportunity_score,
      20
    );
    guarded.qualification_engine.data_completeness = "insufficient";
  }

  // 2. Domain authority override & Disposable check
  if (guarded.lead_profile.email_type === "business") {
    if (guarded.qualification_engine.opportunity_score < 60) {
      guarded.qualification_engine.opportunity_score = 60;
    }
  } else if (guarded.lead_profile.email_type === "disposable_or_risky") {
    guarded.qualification_engine.opportunity_score = Math.min(
      Math.max(guarded.qualification_engine.opportunity_score, 0),
      25
    );
    if (wordCount(payload.useCase) > 10) {
      guarded.qualification_engine.data_completeness = "partial";
    } else {
      guarded.qualification_engine.data_completeness = "insufficient";
    }
  }

  // 3. Prosumer + high-intent text
  const highIntentCount = guarded.qualification_engine.intent_signals?.high_intent_tags?.length ?? 0;
  if (guarded.lead_profile.email_type === "prosumer" && highIntentCount >= 3) {
    if (guarded.qualification_engine.opportunity_score < 50) {
      guarded.qualification_engine.opportunity_score = 50;
    }
  }

  // 4. Emotional but not tactical
  const isEmotional = containsAny(payload.useCase, EMOTIONAL_WORDS);
  const isTactical = containsAny(payload.useCase, TACTICAL_WORDS);

  if (isEmotional && !isTactical) {
    // Existing v1 rule
    guarded.lead_profile.technical_sophistication_score = Math.min(
      guarded.lead_profile.technical_sophistication_score,
      3
    );
    if (guarded.qualification_engine.opportunity_score > 70) {
      guarded.qualification_engine.opportunity_score = 40;
    }

    // New v2 rule: Emotional + Free Email
    if (guarded.lead_profile.email_type === "free") {
      guarded.lead_profile.technical_sophistication_score = Math.min(
        guarded.lead_profile.technical_sophistication_score,
        2
      );
      guarded.qualification_engine.opportunity_score = Math.min(
        guarded.qualification_engine.opportunity_score,
        30
      );
    }
  }

  // 5. Unknown industry handling
  const industry = guarded.firmographics.industry_vertical?.trim();
  if (
    !industry ||
    ["unknown", "n/a", "na", ""].includes(industry.toLowerCase())
  ) {
    guarded.firmographics.industry_vertical = "Unknown";
  }

  return guarded;
}