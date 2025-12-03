import { NexSupplyLeadAnalysis } from "./schema";

export type LeadTier = "A" | "B" | "C" | "D";

export interface LeadRoutingDecision {
  tier: LeadTier;
  label: string;
  slaHours: number;
  queue: "priority" | "standard" | "nurture";
  reasonSummary: string;
}

export function formatSlaLabel(slaHours: number): string {
  if (slaHours < 1) return `${Math.round(slaHours * 60)} min`;
  return `${slaHours} h`;
}

export function deriveLeadRouting(
  analysis: NexSupplyLeadAnalysis
): LeadRoutingDecision {
  const score = analysis.qualification_engine.opportunity_score;
  const tech = analysis.lead_profile.technical_sophistication_score;
  const urgency = analysis.qualification_engine.urgency_signal;

  let tier: LeadTier = "C";
  let label = "Standard Operator";
  let slaHours = 4; // Default Tier C
  let queue: LeadRoutingDecision["queue"] = "standard";

  if (score >= 90 && tech >= 8) {
    tier = "A";
    label = "Strategic Enterprise";
    slaHours = urgency === "High" ? 5 / 60 : 15 / 60; // 5-15 min
    queue = "priority";
  } else if (score >= 70) {
    tier = "B";
    label = "Serious Scaler";
    slaHours = urgency === "High" ? 0.5 : 2; // 30 min - 2 hours
    queue = "priority";
  } else if (score < 40) {
    tier = "D";
    label = "Nurture / Low Intent";
    slaHours = 24; // No guaranteed quick response
    queue = "nurture";
  }

  const reasonSummary =
    analysis.qualification_engine._reasoning_trace ?? "";

  return { tier, label, slaHours, queue, reasonSummary };
}