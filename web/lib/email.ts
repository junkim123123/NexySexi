import { Resend } from 'resend';
import type { SampleRequestData } from './validation';

/**
 * @fileoverview Email sending utilities using Resend.
 * @description This module initializes the Resend client and provides
 * functions for sending transactional emails.
 *
 * .env.local example:
 * RESEND_API_KEY="YOUR_RESEND_KEY"
 * ADMIN_EMAIL="outreach@nexsupply.net"
 * SYSTEM_EMAIL_FROM="NexSupply System <system@nexsupply.net>"
 */

const resend = new Resend(process.env.RESEND_API_KEY);

const fromEmail = process.env.SYSTEM_EMAIL_FROM || 'system@nexsupply.net';
const adminEmail = process.env.ADMIN_EMAIL || 'admin@example.com';

/**
 * Sends a notification email to the internal team about a new sample request.
 * @param data The validated sample request data.
 * @param summary The AI-generated summary of the request.
 */
export async function sendAdminNotification(data: SampleRequestData, summary: any) {
  const subject = `New Sample Request from ${data.company || data.name}`;
  const body = `
    <p>A new sample report request has been submitted.</p>
    <h3>Request Details:</h3>
    <ul>
      <li><strong>Name:</strong> ${data.name}</li>
      <li><strong>Email:</strong> ${data.workEmail}</li>
      <li><strong>Company:</strong> ${data.company || 'N/A'}</li>
      <li><strong>Use Case:</strong> ${data.useCase}</li>
    </ul>
    <h3>AI Summary:</h3>
    <pre>${JSON.stringify(summary, null, 2)}</pre>
  `;

  try {
    await resend.emails.send({
      from: fromEmail,
      to: adminEmail,
      subject: subject,
      html: body,
    });
  } catch (error) {
    console.error("Failed to send admin notification email:", error);
    throw new Error("Could not send admin notification.");
  }
}

/**
 * Sends a confirmation email to the user who submitted the request.
 * @param data The validated sample request data.
 */
export async function sendUserConfirmation(data: SampleRequestData) {
  const subject = "Your NexSupply Sample Report Request";
  const body = `
    <h1>Thank you for your request, ${data.name}!</h1>
    <p>We've received your request for a sample NexSupply report and our team will be in touch shortly.</p>
    <p>Here's a summary of the details you provided:</p>
    <ul>
      <li><strong>Name:</strong> ${data.name}</li>
      <li><strong>Email:</strong> ${data.workEmail}</li>
      <li><strong>Company:</strong> ${data.company || 'N/A'}</li>
      <li><strong>Use Case:</strong> ${data.useCase}</li>
    </ul>
    <p>Best,<br>The NexSupply Team</p>
  `;

  try {
    await resend.emails.send({
      from: fromEmail,
      to: data.workEmail,
      subject: subject,
      html: body,
    });
  } catch (error) {
    console.error("Failed to send user confirmation email:", error);
    // Non-critical, so we don't throw an error that would fail the API request
  }
}