import { z } from "zod";

export const SampleRequestSchema = z.object({
  name: z.string().min(1, "Name is required."),
  workEmail: z.string().email("A valid email is required."),
  company: z.string().min(1, "Company is required."),
  useCase: z.string().min(10, "Please provide at least a few words about your use case."),
  leadSource: z.string().optional(),
});

export type SampleRequestPayload = z.infer<typeof SampleRequestSchema>;

export interface NexSupplyLeadAnalysis {
  lead_profile: {
    inferred_role: 'Founder' | 'Owner' | 'Operations Manager' | 'Supply Chain Manager' | 'Procurement Manager' | 'Solo Seller' | 'Unknown';
    buyer_persona_tag: 'Anxious Scaler' | 'Established Enterprise' | 'Tire Kicker' | 'Brand Builder' | 'Arbitrage Seller';
    technical_sophistication_score: number; // 1-10
    email_type?: "business" | "prosumer" | "free" | "disposable_or_risky";
    email_local_part_type?: "role_based" | "person_name" | "suspicious";
  };
  firmographics: {
    industry_vertical: string;
    supply_chain_complexity: 'Low' | 'Medium' | 'High' | 'Enterprise';
    estimated_annual_volume: string;
  };
  qualification_engine: {
    _reasoning_trace: string;
    opportunity_score: number; // 0-100
    urgency_signal: 'Low' | 'Medium' | 'High';
    routing_destination: 'Ignore_or_nurture' | 'Standard_queue' | 'Priority_queue' | 'Executive_hand_off';
    data_completeness?: 'insufficient' | 'partial' | 'sufficient';
    intent_score_0_to_100?: number;
    fit_score_0_to_100?: number;
    authority_score_0_to_100?: number;
    engagement_score_0_to_100?: number;
    intent_signals?: {
      high_intent_tags?: string[];
      low_intent_tags?: string[];
      summary?: string;
    };
  };
  content_generation: {
    admin_battlecard_html: string;
    user_email_subject: string;
    user_email_opening_hook: string;
    preview_dashboard_headline: string;
    preview_key_insight: string;
  };
}

export const NexSupplyLeadAnalysisSchema = z.object({
  lead_profile: z.object({
    inferred_role: z.enum(['Founder', 'Owner', 'Operations Manager', 'Supply Chain Manager', 'Procurement Manager', 'Solo Seller', 'Unknown']),
    buyer_persona_tag: z.enum(['Anxious Scaler', 'Established Enterprise', 'Tire Kicker', 'Brand Builder', 'Arbitrage Seller']),
    technical_sophistication_score: z.number().min(1).max(10),
    email_type: z.enum(["business", "prosumer", "free", "disposable_or_risky"]).optional(),
    email_local_part_type: z.enum(["role_based", "person_name", "suspicious"]).optional(),
  }),
  firmographics: z.object({
    industry_vertical: z.string(),
    supply_chain_complexity: z.enum(['Low', 'Medium', 'High', 'Enterprise']),
    estimated_annual_volume: z.string(),
  }),
  qualification_engine: z.object({
    _reasoning_trace: z.string(),
    opportunity_score: z.number().min(0).max(100),
    urgency_signal: z.enum(['Low', 'Medium', 'High']),
    routing_destination: z.enum(['Ignore_or_nurture', 'Standard_queue', 'Priority_queue', 'Executive_hand_off']),
    data_completeness: z.enum(['insufficient', 'partial', 'sufficient']).optional(),
    intent_score_0_to_100: z.number().min(0).max(100).optional(),
    fit_score_0_to_100: z.number().min(0).max(100).optional(),
    authority_score_0_to_100: z.number().min(0).max(100).optional(),
    engagement_score_0_to_100: z.number().min(0).max(100).optional(),
    intent_signals: z.object({
      high_intent_tags: z.array(z.string()).optional(),
      low_intent_tags: z.array(z.string()).optional(),
      summary: z.string().optional(),
    }).optional(),
  }),
  content_generation: z.object({
    admin_battlecard_html: z.string(),
    user_email_subject: z.string(),
    user_email_opening_hook: z.string(),
    preview_dashboard_headline: z.string(),
    preview_key_insight: z.string(),
  }),
});