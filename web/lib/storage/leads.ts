/**
 * Shared leads storage (temporary in-memory solution)
 * In production, replace with database
 */

import type { NexSupplyAIReportV2 } from '@/lib/types/ai-report';

export interface StartIntakePayload {
  businessType: string;
  productCategory?: string;
  productDescription?: string;
  targetMarket?: string;
  volumePlan?: string;
  email: string;
  companyName?: string;
  extraNote?: string;
}

export interface StoredLead extends StartIntakePayload {
  aiReportV2?: NexSupplyAIReportV2;
  createdAt: string;
}

const leadsStore = new Map<string, StoredLead>();
let leadCounter = 1;

export function generateLeadId(): string {
  return `lead-${Date.now()}-${leadCounter++}`;
}

export function getLeadData(leadId: string): StoredLead | undefined {
  return leadsStore.get(leadId);
}

export function getAIReportFromLead(leadId: string): NexSupplyAIReportV2 | undefined {
  const lead = leadsStore.get(leadId);
  return lead?.aiReportV2;
}

export function saveLead(leadId: string, lead: StoredLead): void {
  leadsStore.set(leadId, lead);
}

export function getAllLeads(): StoredLead[] {
  return Array.from(leadsStore.values());
}

