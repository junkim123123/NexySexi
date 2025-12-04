import { NextResponse } from 'next/server';
import { generateAIReportV2 } from '@/lib/ai/aiReportV2';
import type { NexSupplyAIReportV2 } from '@/lib/types/ai-report';
import {
  type StartIntakePayload,
  type StoredLead,
  generateLeadId,
  saveLead,
  getLeadData,
  getAIReportFromLead,
} from '@/lib/storage/leads';

interface StartIntakeResponse {
  leadId: string;
  aiReport: NexSupplyAIReportV2 | null;
}


export async function POST(req: Request) {
  try {
    const body: StartIntakePayload = await req.json();

    // Validate required fields
    if (!body.email || !body.businessType) {
      return NextResponse.json(
        { ok: false, error: 'Email and business type are required.' },
        { status: 400 }
      );
    }

    // Generate lead ID and store lead
    const leadId = generateLeadId();
    const storedLead: StoredLead = {
      ...body,
      createdAt: new Date().toISOString(),
    };
    saveLead(leadId, storedLead);
    console.log('[StartIntake] Lead saved:', leadId, body);

    let aiReport: NexSupplyAIReportV2 | null = null;

    try {
      // Generate AI Report V2
      const reportContext: Parameters<typeof generateAIReportV2>[0] = {
        businessType: body.businessType,
        productCategory: body.productCategory,
        productDescription: body.productDescription,
        targetMarket: body.targetMarket,
        volumePlan: body.volumePlan,
        extraNote: body.extraNote,
      };

      aiReport = await generateAIReportV2(reportContext);
      
      // Store AI report with lead
      storedLead.aiReportV2 = aiReport;
      saveLead(leadId, storedLead);
      
      console.log('[StartIntake] AI report V2 generated:', leadId);
    } catch (aiError) {
      console.error('[StartIntake] AI report generation failed:', aiError);
      // Continue without AI report - lead is still saved
    }

    const response: StartIntakeResponse = {
      leadId,
      aiReport,
    };

    return NextResponse.json({ ok: true, ...response }, { status: 200 });
  } catch (error) {
    console.error('[StartIntake] Server error:', error);
    return NextResponse.json(
      { ok: false, error: 'Failed to process intake request.' },
      { status: 500 }
    );
  }
}

// Helper functions to map start intake values to onboarding context
function mapBusinessTypeToChannel(businessType: string): string {
  const mapping: Record<string, string> = {
    'Amazon FBA private label': 'amazon_fba',
    'Shopify / DTC brand': 'shopify_dtc',
    'Retail / wholesale buyer': 'retail_wholesale',
    'Importer / trading company': 'b2b_distributor',
    'I\'m just exploring': 'not_sure',
  };
  return mapping[businessType] || 'not_sure';
}

function mapMarketToCode(market: string): string {
  const mapping: Record<string, string> = {
    'US – Amazon FBA': 'united_states',
    'US – Retail / wholesale': 'united_states',
    'Korea / Japan': 'japan',
    'Other markets': 'other',
  };
  return mapping[market] || 'united_states';
}

function mapVolumeToPlan(volume?: string): string {
  if (!volume) return 'not_sure';
  const mapping: Record<string, string> = {
    'Under 1 pallet (test only)': 'test',
    '1–3 pallets': 'small_launch',
    '1 container +': 'steady',
    'Not sure yet': 'not_sure',
  };
  return mapping[volume] || 'not_sure';
}


export async function GET(req: Request) {
  try {
    const { searchParams } = new URL(req.url);
    const leadId = searchParams.get('leadId');

    if (!leadId) {
      return NextResponse.json(
        { ok: false, error: 'leadId is required.' },
        { status: 400 }
      );
    }

    const leadData = getLeadData(leadId);
    if (!leadData) {
      return NextResponse.json(
        { ok: false, error: 'Lead not found.' },
        { status: 404 }
      );
    }

    // Return lead data without aiReportV2 (separate endpoint for that)
    const { aiReportV2, ...leadPayload } = leadData;
    return NextResponse.json({ ok: true, lead: leadPayload }, { status: 200 });
  } catch (error) {
    console.error('[StartIntake] GET error:', error);
    return NextResponse.json(
      { ok: false, error: 'Failed to retrieve lead data.' },
      { status: 500 }
    );
  }
}

