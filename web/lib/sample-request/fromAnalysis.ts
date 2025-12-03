import type { ProductAnalysis } from '@/lib/product-analysis/schema';

export type SampleRequestResponseType = {
  ok: boolean;
  analysisPreview?: string;
  tier?: string;
  slaHours?: number;
  error?: string;
};

export async function createLeadFromAnalysis(input: {
  name: string;
  email: string;
  company?: string;
  analysis: ProductAnalysis;
  leadSource?: string;
  userId?: string | null;
}): Promise<SampleRequestResponseType> {
  const { name, email, company, analysis, leadSource, userId } = input;
  
  const finalLeadSource = `${leadSource || 'unknown'}|${userId ? 'authenticated' : 'anonymous'}`;

  const useCase = `
    [Source: ${finalLeadSource}]
    [User ID: ${userId || 'N/A'}]
    Product: ${analysis.product_name}
    Landed Cost: ${analysis.landed_cost_breakdown.landed_cost}
    Risk Score: ${analysis.risk_assessment.overall_score}/100
    Risk Summary: ${analysis.risk_assessment.summary}
    Recommendation: ${analysis.recommendation}
    ---
    Full Analysis:
    ${JSON.stringify(analysis, null, 2)}
  `.trim();

  try {
    const res = await fetch('/api/sample-request', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name,
        workEmail: email,
        company: company || 'Not Provided',
        useCase,
        leadSource: leadSource || 'unknown',
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || 'Failed to submit lead');
    }

    return data;
  } catch (err) {
    console.error('[createLeadFromAnalysis] Error:', err);
    return {
      ok: false,
      error: err instanceof Error ? err.message : 'An unknown error occurred',
    };
  }
}