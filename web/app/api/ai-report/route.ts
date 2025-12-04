import { NextResponse } from 'next/server';
import { generateAIReportV2 } from '@/lib/ai/aiReportV2';
import { getLeadData, getAIReportFromLead, saveLead } from '@/lib/storage/leads';
import type { NexSupplyAIReportV2 } from '@/lib/types/ai-report';

interface GetAIReportResponse {
  leadId: string;
  aiReport: NexSupplyAIReportV2;
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

    // Try to get lead data
    const leadData = getLeadData(leadId);
    
    if (!leadData) {
      return NextResponse.json(
        { ok: false, error: 'Lead not found.' },
        { status: 404 }
      );
    }

    // Check if we already have an AI report stored
    let aiReport = getAIReportFromLead(leadId);
    
    // If no stored report, generate a new one
    if (!aiReport) {
      const reportContext = {
        businessType: leadData.businessType,
        productCategory: leadData.productCategory,
        productDescription: leadData.productDescription,
        targetMarket: leadData.targetMarket,
        volumePlan: leadData.volumePlan,
        extraNote: leadData.extraNote,
      };

      try {
        aiReport = await generateAIReportV2(reportContext);
        // Store the generated report with the lead
        leadData.aiReportV2 = aiReport;
        saveLead(leadId, leadData);
      } catch (error) {
        console.error('[GetAIReport] Failed to generate report:', error);
        return NextResponse.json(
          { ok: false, error: 'Failed to generate AI report.' },
          { status: 500 }
        );
      }
    }

    const response: GetAIReportResponse = {
      leadId,
      aiReport,
    };

    return NextResponse.json({ ok: true, ...response }, { status: 200 });
  } catch (error) {
    console.error('[GetAIReport] Server error:', error);
    return NextResponse.json(
      { ok: false, error: 'Failed to retrieve AI report.' },
      { status: 500 }
    );
  }
}

