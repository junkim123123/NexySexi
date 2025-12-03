import dotenv from 'dotenv';
import path from 'path';

// Load environment variables BEFORE importing modules that use them
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

import { sendAdminNotificationEmail, sendUserConfirmationEmail } from "../lib/email/sampleRequestMailer";
import { SampleRequestPayload, NexSupplyLeadAnalysis } from "../lib/sample-request/schema";
import { LeadRoutingDecision } from "../lib/sample-request/routing";

const mockPayload: SampleRequestPayload = {
  name: "Test User",
  workEmail: "outreach@nexsupply.net", // Send to self to verify
  company: "Test Corp",
  useCase: "Testing email functionality",
};

const mockAnalysis: NexSupplyLeadAnalysis = {
  lead_profile: {
    inferred_role: "Unknown",
    buyer_persona_tag: "Tire Kicker",
    technical_sophistication_score: 5,
    email_type: "business",
    email_local_part_type: "person_name"
  },
  firmographics: {
    industry_vertical: "Test Industry",
    supply_chain_complexity: "Low",
    estimated_annual_volume: "Unknown",
  },
  qualification_engine: {
    _reasoning_trace: "This is a test run.",
    opportunity_score: 50,
    urgency_signal: "Low",
    routing_destination: "Standard_queue",
    data_completeness: "sufficient",
    intent_score_0_to_100: 50,
    fit_score_0_to_100: 50,
    authority_score_0_to_100: 50,
    engagement_score_0_to_100: 50,
    intent_signals: {
        high_intent_tags: [],
        low_intent_tags: [],
        summary: "Test summary"
    }
  },
  content_generation: {
    admin_battlecard_html: "<li>Test battlecard</li>",
    user_email_subject: "Test Subject",
    user_email_opening_hook: "This is a test email.",
    preview_dashboard_headline: "Test Headline",
    preview_key_insight: "Test Insight",
  },
};

const mockRouting: LeadRoutingDecision = {
  tier: "C",
  label: "Standard Operator",
  slaHours: 24,
  queue: "standard",
  reasonSummary: "Test reasoning",
};

async function testEmail() {
  console.log("Sending test emails...");
  try {
    await sendAdminNotificationEmail(mockPayload, mockAnalysis, mockRouting);
    console.log("Admin email sent successfully.");
    
    await sendUserConfirmationEmail(mockPayload, mockAnalysis, mockRouting);
    console.log("User email sent successfully.");
  } catch (error) {
    console.error("Failed to send emails:", error);
  }
}

testEmail();