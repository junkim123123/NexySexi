import {
  type SampleRequestPayload,
  type NexSupplyLeadAnalysis,
  NexSupplyLeadAnalysisSchema,
} from "../sample-request/schema";

async function getApiKey(): Promise<string> {
  if (typeof process === 'undefined' || !process.env.GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY is not configured.");
  }
  return process.env.GEMINI_API_KEY;
}

const BACKEND_PROMPT = `
Role: You are the Chief Intelligence Officer for NexSupply, an AI-powered global sourcing platform. Your expertise covers international trade law, logistics, Amazon FBA mechanics, and manufacturing supply chains.

Objective: Analyze the provided User Input to determine commercial viability, sourcing maturity, and immediate needs. You must output your analysis in strictly valid JSON format adhering to the provided schema.

Input Data:
- User Name: {name}
- User Email: {workEmail}
- Company: {company}
- Use Case: {useCase}

---

### 1. Scoring Logic (0-100)

You must compute four sub-scores and then a final opportunity_score.

1.  **intent_score_0_to_100 (35% weight)**
    *   **High-intent patterns (80-100):**
        *   Financial: "landed cost", "EBITDA", "contribution margin", "net margin"
        *   Compliance: "HTS code", "HS code", "Section 301", "customs bond", "DDP"
        *   Logistics: "FCL", "40HQ", "3PL", "stockout risk", "inventory turns"
        *   Amazon: "ASIN", "FBA fees", "IPI score", "storage limits"
        *   Product: "private label", "OEM", "BOM", "CAD files", "GSM"
        *   Specifics: Concrete numbers ("5,000 units/month"), deadlines ("Q4 launch")
    *   **Mixed (50-79):** Some serious terms, but vague on volume/timeline.
    *   **Low-intent patterns (0-49):**
        *   "make money online", "passive income", "side hustle"
        *   "I want to start a business", "looking for ideas"
        *   "retail arbitrage", "dropshipping", "AliExpress"
        *   Extremely vague requests with no product details.

2.  **fit_score_0_to_100 (30% weight)**
    *   How well the industry/role matches NexSupply ICP (High-volume importers, FBA sellers, DTC brands).

3.  **authority_score_0_to_100 (20% weight)**
    *   **80-100:** Business domain + person name.
    *   **60-80:** Business domain + role-based (info@, sales@).
    *   **40-70:** Free domain + strong high-intent text.
    *   **0-30:** Free domain + low-intent text.
    *   **0-10:** Disposable domain.

4.  **engagement_score_0_to_100 (15% weight)**
    *   Based on text length, detail, and context provided.

**Final Opportunity Score Calculation:**
opportunity_score = round(0.35 * intent + 0.30 * fit + 0.20 * authority + 0.15 * engagement)

---

### 2. Email Classification

Classify the email into:
*   **email_type:** "business" (custom domain), "prosumer" (personal brand domain), "free" (gmail, yahoo, etc.), or "disposable_or_risky".
*   **email_local_part_type:** "role_based" (admin@, info@), "person_name", or "suspicious" (random digits).

---

### 3. SLA / Tier Guidelines (for reasoning)

*   **Tier A (Strategic Enterprise):** Corporate email, high intent, clear pain/volume. Target < 15 min response.
*   **Tier B (Serious Scaler):** Good fit, clear need. Target < 2 hours response.
*   **Tier C (Standard Operator):** Legitimate but exploratory. Target < 24 hours.
*   **Tier D (Nurture):** Students, vague, disposable. No guaranteed human response.

---

### 4. Output Rules

*   **Return RAW JSON only.** No markdown fences.
*   **Fill reasoning fields FIRST** in natural language, then compute numeric scores.
*   **Be conservative:** If uncertain, lower the score.
*   **Infer 'Unknown'** if data is missing.

`;

export async function analyzeSampleRequest(
  payload: SampleRequestPayload
): Promise<NexSupplyLeadAnalysis> {
  try {
    const apiKey = await getApiKey();
    const { GoogleGenerativeAI } = await import("@google/generative-ai");

    const genAI = new GoogleGenerativeAI(apiKey);
    const model = genAI.getGenerativeModel({
      model: "gemini-2.5-pro",
      generationConfig: {
        responseMimeType: "application/json",
      },
    });

    const prompt = BACKEND_PROMPT
      .replace('{name}', payload.name)
      .replace('{workEmail}', payload.workEmail)
      .replace('{company}', payload.company)
      .replace('{useCase}', payload.useCase) + `

IMPORTANT: You must return a JSON object that strictly matches this structure:
{
  "lead_profile": {
    "inferred_role": "Founder" | "Owner" | "Operations Manager" | "Supply Chain Manager" | "Procurement Manager" | "Solo Seller" | "Unknown",
    "buyer_persona_tag": "Anxious Scaler" | "Established Enterprise" | "Tire Kicker" | "Brand Builder" | "Arbitrage Seller",
    "technical_sophistication_score": number, // 1-10
    "email_type": "business" | "prosumer" | "free" | "disposable_or_risky",
    "email_local_part_type": "role_based" | "person_name" | "suspicious"
  },
  "firmographics": {
    "industry_vertical": string,
    "supply_chain_complexity": "Low" | "Medium" | "High" | "Enterprise",
    "estimated_annual_volume": string
  },
  "qualification_engine": {
    "_reasoning_trace": string,
    "opportunity_score": number, // 0-100
    "urgency_signal": "Low" | "Medium" | "High",
    "routing_destination": "Ignore_or_nurture" | "Standard_queue" | "Priority_queue" | "Executive_hand_off",
    "data_completeness": "insufficient" | "partial" | "sufficient",
    "intent_score_0_to_100": number,
    "fit_score_0_to_100": number,
    "authority_score_0_to_100": number,
    "engagement_score_0_to_100": number,
    "intent_signals": {
      "high_intent_tags": string[],
      "low_intent_tags": string[],
      "summary": string
    }
  },
  "content_generation": {
    "admin_battlecard_html": string,
    "user_email_subject": string,
    "user_email_opening_hook": string,
    "preview_dashboard_headline": string,
    "preview_key_insight": string
  }
}`;

    const result = await model.generateContent(prompt);
    const text = result.response.text();
    console.log("[SampleRequest][Gemini] Raw response:", text);
    
    // Attempt to parse JSON (handling potential markdown fences if model ignores instruction)
    const cleaned = text.replace(/```json|```/g, "").trim();
    const parsed = JSON.parse(cleaned);

    const validation = NexSupplyLeadAnalysisSchema.safeParse(parsed);
    if (validation.success) {
      return validation.data;
    } else {
      console.error("[SampleRequest][Gemini] Zod validation failed", validation.error);
      // Fallback: try to return parsed object if it has essential fields, otherwise fail
      // For now, we'll log and fall through to the default return
    }
  } catch (error) {
    console.error("[SampleRequest][Gemini] Failed to generate analysis", error);
  }

  return {
    lead_profile: {
      inferred_role: 'Unknown',
      buyer_persona_tag: 'Tire Kicker',
      technical_sophistication_score: 1,
      email_type: 'free',
      email_local_part_type: 'suspicious'
    },
    firmographics: {
      industry_vertical: 'Unknown',
      supply_chain_complexity: 'Low',
      estimated_annual_volume: 'Unknown',
    },
    qualification_engine: {
      _reasoning_trace: 'AI analysis failed. Manual review required.',
      opportunity_score: 0,
      urgency_signal: 'Low',
      routing_destination: 'Ignore_or_nurture',
      data_completeness: 'insufficient',
      intent_score_0_to_100: 0,
      fit_score_0_to_100: 0,
      authority_score_0_to_100: 0,
      engagement_score_0_to_100: 0,
    },
    content_generation: {
      admin_battlecard_html: '<li>Manual review required due to AI analysis failure.</li>',
      user_email_subject: `Your NexSupply request for ${payload.company}`,
      user_email_opening_hook: 'Thank you for your request. Our team is reviewing it and will get back to you shortly.',
      preview_dashboard_headline: 'Analysis Pending',
      preview_key_insight: 'Our team will manually review your request to provide a detailed analysis.',
    },
  };
}