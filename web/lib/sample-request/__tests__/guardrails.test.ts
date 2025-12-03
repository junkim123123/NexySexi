import { describe, it, expect } from 'vitest';
import { applyLeadGuardrails } from '../guardrails';
import { NexSupplyLeadAnalysis, SampleRequestPayload } from '../schema';

// Helper to create a base analysis object
const createBaseAnalysis = (overrides: Partial<NexSupplyLeadAnalysis> = {}): NexSupplyLeadAnalysis => ({
  lead_profile: {
    inferred_role: 'Unknown',
    buyer_persona_tag: 'Tire Kicker',
    technical_sophistication_score: 1,
    ...overrides.lead_profile,
  },
  firmographics: {
    industry_vertical: 'Unknown',
    supply_chain_complexity: 'Low',
    estimated_annual_volume: 'Unknown',
    ...overrides.firmographics,
  },
  qualification_engine: {
    _reasoning_trace: 'Test reasoning',
    opportunity_score: 50,
    urgency_signal: 'Low',
    routing_destination: 'Ignore_or_nurture',
    data_completeness: 'sufficient',
    intent_signals: {
        high_intent_tags: [],
        low_intent_tags: [],
        summary: ''
    },
    ...overrides.qualification_engine,
  },
  content_generation: {
    admin_battlecard_html: '',
    user_email_subject: '',
    user_email_opening_hook: '',
    preview_dashboard_headline: '',
    preview_key_insight: '',
    ...overrides.content_generation,
  },
});

describe('guardrails', () => {
  it('bumps business email score to at least 60', () => {
    const payload: SampleRequestPayload = {
      name: 'CEO',
      workEmail: 'ceo@acmecorp.com',
      company: 'Acme Corp',
      useCase: 'Need sourcing help',
    };
    const analysis = createBaseAnalysis({
      qualification_engine: { opportunity_score: 40 } as any
    });

    const result = applyLeadGuardrails(payload, analysis);
    expect(result.qualification_engine.opportunity_score).toBe(60);
    expect(result.lead_profile.email_type).toBe('business');
  });

  it('caps disposable email score at 25', () => {
    const payload: SampleRequestPayload = {
      name: 'Spam',
      workEmail: 'spam@mailinator.com',
      company: 'Spam Co',
      useCase: 'send prices',
    };
    const analysis = createBaseAnalysis({
      qualification_engine: { opportunity_score: 80 } as any
    });

    const result = applyLeadGuardrails(payload, analysis);
    expect(result.qualification_engine.opportunity_score).toBe(25);
    expect(result.lead_profile.email_type).toBe('disposable_or_risky');
  });

  it('caps emotional + free email score at 30', () => {
    const payload: SampleRequestPayload = {
      name: 'Dreamer',
      workEmail: 'dreamer@gmail.com',
      company: 'Dream Co',
      useCase: 'I am desperate for freedom and passion. No tactical words here.',
    };
    const analysis = createBaseAnalysis({
      qualification_engine: { opportunity_score: 80 } as any,
      lead_profile: { technical_sophistication_score: 8 } as any
    });

    const result = applyLeadGuardrails(payload, analysis);
    expect(result.qualification_engine.opportunity_score).toBe(30);
    expect(result.lead_profile.technical_sophistication_score).toBe(2);
  });

  it('preserves high score for prosumer email with high intent', () => {
    // "a.co" length is 4, triggers prosumer logic
    const payload: SampleRequestPayload = {
        name: "Pro",
        workEmail: "me@a.co",
        company: "A Co",
        useCase: "Need MOQ and BOM for my SKU."
    };

    const analysis = createBaseAnalysis({
      qualification_engine: { 
          opportunity_score: 40,
          intent_signals: { high_intent_tags: ['MOQ', 'BOM', 'SKU'] } 
      } as any
    });

    const result = applyLeadGuardrails(payload, analysis);
    expect(result.lead_profile.email_type).toBe('prosumer');
    expect(result.qualification_engine.opportunity_score).toBe(50);
  });

  it('caps insufficient data score at 20', () => {
    const payload: SampleRequestPayload = {
      name: 'Lazy',
      workEmail: 'lazy@gmail.com',
      company: 'N/A',
      useCase: 'hi', // word count < 5
    };
    const analysis = createBaseAnalysis({
      qualification_engine: { opportunity_score: 80 } as any
    });

    const result = applyLeadGuardrails(payload, analysis);
    expect(result.qualification_engine.opportunity_score).toBe(20);
    expect(result.qualification_engine.data_completeness).toBe('insufficient');
  });
});