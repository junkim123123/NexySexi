import nodemailer from "nodemailer";
import {
  type SampleRequestPayload,
  type NexSupplyLeadAnalysis,
} from "../sample-request/schema";
import { type LeadRoutingDecision, formatSlaLabel } from "../sample-request/routing";

const systemFrom = process.env.SYSTEM_EMAIL_FROM ?? "NexSupply <no-reply@nexsupply.net>";

let transporter: nodemailer.Transporter | null = null;

function getTransporter() {
  if (transporter) return transporter;

  const smtpHost = process.env.SMTP_HOST;
  const smtpPort = parseInt(process.env.SMTP_PORT || "465", 10);
  const smtpUser = process.env.SMTP_USER;
  const smtpPass = process.env.SMTP_PASS;

  if (smtpHost && smtpUser && smtpPass) {
    transporter = nodemailer.createTransport({
      host: smtpHost,
      port: smtpPort,
      secure: smtpPort === 465,
      auth: {
        user: smtpUser,
        pass: smtpPass,
      },
    });
  }
  return transporter;
}

function getProperty<T, K extends string>(obj: T, path: K): string {
    const keys = path.split('.');
    let current: any = obj;
    for (const key of keys) {
        if (current === null || typeof current !== 'object' || !(key in current)) {
            return '';
        }
        current = current[key];
    }
    return String(current);
}

function renderTemplate(template: string, payload: SampleRequestPayload, analysis: NexSupplyLeadAnalysis, routing: LeadRoutingDecision): string {
    return template.replace(/\{\{([^}]+)\}\}/g, (_, key) => {
        const trimmedKey = key.trim();
        if (trimmedKey === "slaLabel") {
            return formatSlaLabel(routing.slaHours);
        }
        if (trimmedKey.startsWith("routing.")) {
            return getProperty(routing, trimmedKey.replace("routing.", "") as keyof LeadRoutingDecision);
        }
        if (trimmedKey in payload) {
            return getProperty(payload, trimmedKey as keyof SampleRequestPayload);
        }
        return getProperty(analysis, trimmedKey as keyof NexSupplyLeadAnalysis);
    });
}

const ADMIN_EMAIL_HTML_TEMPLATE = `
<!DOCTYPE html>
<html>
<head>
<style>
.score-badge { padding: 5px 10px; border-radius: 4px; font-weight: bold; color: white; display: inline-block; }
.tier-badge { padding: 5px 10px; border-radius: 4px; font-weight: bold; color: white; display: inline-block; margin-right: 10px; }
.tier-A { background-color: #8e44ad; }
.tier-B { background-color: #2980b9; }
.tier-C { background-color: #27ae60; }
.tier-D { background-color: #7f8c8d; }
.high { background-color: #27ae60; }
.med { background-color: #f39c12; }
.low { background-color: #c0392b; }
.battlecard { background-color: #f8f9fa; border-left: 5px solid #2980b9; padding: 15px; margin: 20px 0; }
.snapshot { background-color: #fff; border: 1px solid #eee; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
 li { margin-bottom: 5px; }
</style>
</head>
<body style="font-family: Arial, sans-serif; color: #333;">
  <h2>🚨 New Lead Analysis Complete</h2>

  <div style="margin-bottom: 20px;">
    <span class="tier-badge tier-{{routing.tier}}">
      Tier {{routing.tier}}: {{routing.label}}
    </span>
    <span style="font-size: 14px; color: #666; margin-left: 10px;">
      Queue: <strong>{{routing.queue}}</strong> | SLA: <strong>{{slaLabel}}</strong>
    </span>
  </div>

  <div class="snapshot">
    <h3 style="margin-top: 0; border-bottom: 1px solid #eee; padding-bottom: 10px;">🚦 Lead Snapshot</h3>
    <ul style="list-style: none; padding: 0;">
      <li><strong>Score:</strong> {{qualification_engine.opportunity_score}}/100</li>
      <li><strong>Intent:</strong> {{qualification_engine.intent_signals.summary}}</li>
      <li><strong>Authority:</strong> {{lead_profile.email_type}} / {{lead_profile.email_local_part_type}}</li>
      <li><strong>Risks:</strong>
        <ul>
           <li>Fit: {{qualification_engine.fit_score_0_to_100}}</li>
           <li>Completeness: {{qualification_engine.data_completeness}}</li>
        </ul>
      </li>
    </ul>
  </div>

  <table width="100%" cellpadding="10" cellspacing="0" border="1" style="border-collapse: collapse; border-color: #eee;">
    <tr>
      <td width="30%" bgcolor="#f9f9f9"><strong>Name:</strong></td>
      <td>{{name}} ({{lead_profile.inferred_role}})</td>
    </tr>
    <tr>
      <td bgcolor="#f9f9f9"><strong>Company:</strong></td>
      <td>{{company}} ({{firmographics.supply_chain_complexity}} Complexity)</td>
    </tr>
    <tr>
      <td bgcolor="#f9f9f9"><strong>Vertical:</strong></td>
      <td>{{firmographics.industry_vertical}}</td>
    </tr>
    <tr>
      <td bgcolor="#f9f9f9"><strong>Use Case:</strong></td>
      <td><em>"{{useCase}}"</em></td>
    </tr>
  </table>

  <div class="battlecard">
    <h3 style="margin-top: 0; color: #2980b9;">⚔️ Sales Battlecard</h3>
    <ul style="padding-left: 20px;">
      {{content_generation.admin_battlecard_html}}
    </ul>
    
    <hr style="border: 0; border-top: 1px solid #ddd; margin: 15px 0;">
    
    <p><strong>AI Reasoning Trace:</strong><br>
    <small style="color: #666;">{{qualification_engine._reasoning_trace}}</small></p>
    
    <p><strong>Recommended Action:</strong> <strong style="text-transform: uppercase;">{{qualification_engine.routing_destination}}</strong></p>
  </div>

  <p style="font-size: 12px; color: #999;">Generated by NexSupply Intelligence Engine v2.</p>
</body>
</html>
`;

const USER_EMAIL_HTML_TEMPLATE_TIER_AB = `
<!DOCTYPE html>
<html>
<body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #2c3e50; max-width: 600px; margin: 0 auto;">
  <div style="padding: 30px 20px;">
    <p>Hi {{name}},</p>
    
    <p>I see you're sourcing <strong>{{firmographics.industry_vertical}}</strong> products for {{company}}. Based on your request, I'm running a landed cost and tariff exposure check focusing on:</p>
    <p style="background-color: #f8f9fa; padding: 10px; border-left: 3px solid #007bff;"><em>{{qualification_engine._reasoning_trace}}</em></p>

    <p><strong>Early Scan Insight:</strong></p>
    <p>{{content_generation.preview_key_insight}}</p>

    <p>You’ll receive your full analysis by <strong>{{slaLabel}}</strong>.</p>
    
    <p>If this is urgent, you can also <a href="https://calendly.com/nexsupply/strategy">book a 15-minute review call here</a>.</p>
  </div>
</body>
</html>
`;

const USER_EMAIL_HTML_TEMPLATE_TIER_CD = `
<!DOCTYPE html>
<html>
<body style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; line-height: 1.6; color: #2c3e50; max-width: 600px; margin: 0 auto;">
  <div style="padding: 30px 20px;">
    <p>Hi {{name}},</p>
    
    <p>Thanks for your interest in NexSupply. We have received your request regarding <strong>{{firmographics.industry_vertical}}</strong> sourcing.</p>

    <p>Our system is currently reviewing your details. {{content_generation.preview_key_insight}}</p>

    <p>In the meantime, you might find our <a href="https://nexsupply.net/academy">Sourcing Academy</a> helpful for understanding global trade logistics.</p>
    
    <p>We will be in touch shortly.</p>
  </div>
</body>
</html>
`;

export async function sendAdminNotificationEmail(
  payload: SampleRequestPayload,
  analysis: NexSupplyLeadAnalysis,
  routing: LeadRoutingDecision
): Promise<void> {
  const mailer = getTransporter();
  const adminEmail = process.env.ADMIN_EMAIL;

  if (!mailer || !adminEmail) {
    console.warn("[Email][SampleRequest][Admin] Email service not configured, skipping email.");
    return;
  }

  try {
    const subject = `[Tier ${routing.tier}] New Lead: ${payload.company} (Score: ${analysis.qualification_engine.opportunity_score})`;
    const html = renderTemplate(ADMIN_EMAIL_HTML_TEMPLATE, payload, analysis, routing);
    await mailer.sendMail({ from: systemFrom, to: adminEmail, subject, html });
  } catch (error) {
    console.error("[Email][SampleRequest][Admin] Failed to send", error);
  }
}

export async function sendUserConfirmationEmail(
  payload: SampleRequestPayload,
  analysis: NexSupplyLeadAnalysis,
  routing: LeadRoutingDecision
): Promise<void> {
  const mailer = getTransporter();

  if (!mailer) {
    console.warn("[Email][SampleRequest][User] Email service not configured, skipping email.");
    return;
  }

  try {
    let subject = "";
    let template = "";

    if (routing.tier === "A" || routing.tier === "B") {
      subject = `Your NexSupply Sourcing Audit is Running`;
      template = USER_EMAIL_HTML_TEMPLATE_TIER_AB;
    } else {
      subject = `We’re Reviewing Your NexSupply Request`;
      template = USER_EMAIL_HTML_TEMPLATE_TIER_CD;
    }

    const html = renderTemplate(template, payload, analysis, routing);
    await mailer.sendMail({ from: systemFrom, to: payload.workEmail, subject, html });
  } catch (error) {
    console.error("[Email][SampleRequest][User] Failed to send", error);
  }
}