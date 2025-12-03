import {
  type ProductAnalysis,
  ProductAnalysisSchema,
} from "../product-analysis/schema";

async function getApiKey(): Promise<string> {
  if (typeof process === 'undefined' || !process.env.GEMINI_API_KEY) {
    throw new Error("GEMINI_API_KEY is not configured.");
  }
  return process.env.GEMINI_API_KEY;
}

const PRODUCT_ANALYSIS_PROMPT = `
Role: You are a Senior Sourcing Expert at NexSupply. Your job is to provide a quick, "80% accurate" estimation of landed cost and risk for a given product to help a buyer decide if they should proceed.

Objective: Analyze the User Input (which may be a product description, a messy title, a URL, and/or an image) and generate a Landed Cost + Risk Report.

User Input: {input}

---

### Instructions:

1.  **Identify the Product:**
    *   Infer the product type from the input text, URL structure, and/or the provided image.
    *   If an image is provided, use it to infer category, rough dimensions, material, and packaging type.
    *   Estimate the likely HTS/HS code.

2.  **Estimate Landed Cost (Unit Economics):**
    *   Assume a standard "Minimum Order Quantity" (MOQ) scenario (e.g., 500-1000 units) for a generic version of this product sourced from China to the US.
    *   **FOB Price:** Estimate a realistic factory price.
    *   **Freight:** Estimate ocean freight per unit.
    *   **Duty:** Estimate duty rate based on HTS and Section 301 tariffs (if applicable).
    *   **Total Landed Cost:** Sum of the above.

3.  **Assess Risk:**
    *   **Compliance:** Are there safety standards (UL, CE, FDA), restricted materials, or high tariffs?
    *   **Supplier:** Is this a commodity with many suppliers (Low Risk) or a specialized/IP-heavy product (High Risk)?
    *   **Logistics:** Is it bulky/heavy (High Freight Risk) or small/light?

4.  **Recommendation:**
    *   Give a candid "Should you proceed?" summary. Be opinionated.

---

### Output Format:

You must return a strictly valid JSON object matching this structure:

{
  "product_name": "Short descriptive name",
  "hts_code": "Estimated HTS Code",
  "landed_cost_breakdown": {
    "fob_price": "$X.XX",
    "freight_cost": "$X.XX",
    "duty_rate": "X%",
    "duty_cost": "$X.XX",
    "landed_cost": "$X.XX"
  },
  "risk_assessment": {
    "overall_score": number (0-100, 100 = safest),
    "compliance_risk": "Low" | "Medium" | "High",
    "supplier_risk": "Low" | "Medium" | "High",
    "logistics_risk": "Low" | "Medium" | "High",
    "summary": "Short explanation of the risks."
  },
  "recommendation": "1-2 sentences on whether to proceed and what to watch out for."
}
`;

export async function analyzeProduct(input: string, image?: string): Promise<ProductAnalysis> {
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
    const prompt = PRODUCT_ANALYSIS_PROMPT.replace('{input}', input);
    const parts: any[] = [
      { text: prompt },
    ];

    if (image) {
      parts.push({
        inlineData: {
          mimeType: 'image/jpeg',
          data: image,
        },
      });
    }
    const result = await model.generateContent(parts);
    const text = result.response.text();
    console.log("[ProductAnalysis][Gemini] Raw response:", text);

    const cleaned = text.replace(/```json|```/g, "").trim();
    const parsed = JSON.parse(cleaned);

    const validation = ProductAnalysisSchema.safeParse(parsed);
    if (validation.success) {
      return validation.data;
    } else {
      console.error("[ProductAnalysis][Gemini] Zod validation failed", validation.error);
      // In a real app, we might fallback or throw. For now, return a safe error object or throw.
      throw new Error("Failed to parse AI response");
    }
  } catch (error) {
    console.error("[ProductAnalysis][Gemini] Failed to analyze product", error);
    // Return a fallback/error state
    return {
      product_name: "Analysis Failed",
      hts_code: "N/A",
      landed_cost_breakdown: {
        fob_price: "$0.00",
        freight_cost: "$0.00",
        duty_rate: "0%",
        duty_cost: "$0.00",
        landed_cost: "$0.00",
      },
      risk_assessment: {
        overall_score: 0,
        compliance_risk: "High",
        supplier_risk: "High",
        logistics_risk: "High",
        summary: "We could not analyze this product. Please try a different description.",
      },
      recommendation: "Please try again with a clearer product description.",
    };
  }
}