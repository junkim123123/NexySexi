# -*- coding: utf-8 -*-
"""
NexSupply Email Service - Consultation Handover System
Sends analysis reports to customers with CC to internal consultation team.

Business Goal: "AI for insight, human for execution"
When customer sends report → Internal team gets full context for high-value consultation.
"""

import os
import json
import smtplib
import ssl
import unicodedata
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
from email.utils import formataddr
from typing import Dict, Optional, List
from datetime import datetime

import streamlit as st

from state.session_state import get_sourcing_state
from services.data_logger import log_consultation_request, init_database
import logging

# Configure logger
logger = logging.getLogger(__name__)

# =============================================================================
# COMMON ERROR HANDLERS
# =============================================================================

def handle_email_error(
    error: Exception,
    error_code: str,
    log_message: str = None,
    include_retry: bool = True
) -> Dict[str, str]:
    """
    Centralized error handler for email operations.
    
    Args:
        error: The exception that occurred
        error_code: Error code to display to user (e.g., "E-203")
        log_message: Custom log message (defaults to error code)
        include_retry: Whether to include "try again" in message
        
    Returns:
        Dictionary with success=False and user-friendly error message
    """
    # Get consultation email (may change, so get fresh)
    consultation_email = get_consultation_email()
    
    # Log error internally (not shown to user)
    log_msg = log_message or f"Email error (code {error_code})"
    logger.error(f"{log_msg}: {str(error)}", exc_info=True)
    
    # Build user-friendly message
    retry_text = "Please try again or " if include_retry else ""
    message = (
        f"⚠️ **Email Failed. (Error Code: {error_code})**\n\n"
        f"{retry_text}contact us directly at {consultation_email}"
    )
    
    return {
        "success": False,
        "message": message
    }


# =============================================================================
# CONFIGURATION
# =============================================================================

def get_consultation_email() -> str:
    """Get consultation email from config (secure)."""
    from utils.config import Config
    return Config.get_consultation_email()

# Consultation team email - receives all reports for follow-up
# Use function to get from config (can be overridden via environment/secrets)
CONSULTATION_EMAIL = get_consultation_email()


# =============================================================================
# UTF-8 SAFETY HELPERS
# =============================================================================

def safe_utf8_string(text: str, max_length: int = None) -> str:
    """
    Ensure string is UTF-8 safe and handle any encoding issues.
    Normalizes unicode and ensures the string can be safely encoded to UTF-8.
    """
    if not text:
        return ""
    
    try:
        # First, ensure it's a proper string
        if isinstance(text, bytes):
            text = text.decode('utf-8', errors='replace')
        
        # Normalize unicode characters (e.g., replace fancy quotes with regular ones)
        # NFKC normalization helps with compatibility characters
        text = unicodedata.normalize('NFKC', text)
        
        # Test if it can be encoded to UTF-8 (this is what we need)
        # If encoding fails, replace problematic characters
        try:
            text.encode('utf-8')
            # UTF-8 encoding successful, string is safe
            result = text
        except UnicodeEncodeError:
            # If encoding fails (shouldn't happen with proper UTF-8, but be safe)
            # Replace problematic characters
            result = text.encode('utf-8', errors='replace').decode('utf-8', errors='replace')
        
        # Apply length limit if specified
        if max_length:
            result = result[:max_length]
        
        return result
        
    except (UnicodeDecodeError, UnicodeEncodeError, AttributeError) as e:
        # Fallback: use UTF-8 with error replacement
        try:
            if isinstance(text, bytes):
                result = text.decode('utf-8', errors='replace')
            else:
                result = str(text).encode('utf-8', errors='replace').decode('utf-8', errors='replace')
            if max_length:
                result = result[:max_length]
            return result
        except:
            # Last resort: return empty string or truncated safe version
            return str(text)[:max_length] if max_length else str(text)


def safe_email_header(text: str, max_length: int = 50) -> str:
    """Create a safe email header value that won't cause encoding errors."""
    return safe_utf8_string(text, max_length)

# SMTP Configuration (using environment variables for security)
def get_smtp_config() -> Dict:
    """Get SMTP configuration from secrets or environment."""
    from dotenv import load_dotenv
    load_dotenv(override=True)
    
    # Try st.secrets first, then environment variables
    def get_config_value(key: str, default: str = "") -> str:
        # Try streamlit secrets
        try:
            if hasattr(st, 'secrets') and key in st.secrets:
                return st.secrets[key]
        except:
            pass
        # Fallback to environment
        return os.getenv(key, default)
    
    password = get_config_value("SMTP_PASSWORD", "")
    # Remove spaces from app password (Gmail format)
    password = password.replace(" ", "")
    
    return {
        "server": get_config_value("SMTP_SERVER", "smtp.gmail.com"),
        "port": int(get_config_value("SMTP_PORT", "465")),  # Default to 465 (SMTP_SSL)
        "username": get_config_value("SMTP_USERNAME", ""),
        "password": password,
        "from_email": get_config_value("SMTP_FROM_EMAIL", "outreach@nexsupply.net"),
        "from_name": "NexSupply AI Reports"
    }


# =============================================================================
# EMAIL TEMPLATES
# =============================================================================

def generate_customer_email_html(
    product_name: str,
    user_query: str,
    analysis_data: Dict,
    include_json: bool = False
) -> str:
    """Generate HTML email for customer with analysis summary."""
    
    # Escape all user input for HTML safety
    safe_product_name = html_escape(product_name)
    safe_user_query = html_escape(user_query[:500])  # Limit length
    
    # Extract key data
    market = analysis_data.get("market_snapshot", {})
    landed_cost = analysis_data.get("landed_cost", {})
    suppliers = analysis_data.get("suppliers", [])
    confidence = analysis_data.get("analysis_confidence", 0.75)
    
    # Format supplier list with escaped data
    supplier_rows = ""
    for idx, s in enumerate(suppliers[:3], 1):
        supplier_name = html_escape(str(s.get('name', 'Unknown')))
        supplier_location = html_escape(str(s.get('location', 'N/A')))
        supplier_price = html_escape(str(s.get('price_range', 'Contact')))
        supplier_grade = html_escape(str(s.get('factory_grade', 'N/A')))
        supplier_rows += f"""
        <tr>
            <td style="padding: 12px; border-bottom: 1px solid #E5E7EB;">{idx}. {supplier_name}</td>
            <td style="padding: 12px; border-bottom: 1px solid #E5E7EB;">{supplier_location}</td>
            <td style="padding: 12px; border-bottom: 1px solid #E5E7EB;">{supplier_price}</td>
            <td style="padding: 12px; border-bottom: 1px solid #E5E7EB;">{supplier_grade}</td>
        </tr>
        """
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: 'Inter', -apple-system, sans-serif; line-height: 1.6; color: #1F2937; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%); color: white; padding: 30px; border-radius: 12px 12px 0 0; text-align: center; }}
            .content {{ background: #FFFFFF; padding: 30px; border: 1px solid #E5E7EB; }}
            .section {{ margin-bottom: 24px; }}
            .section-title {{ font-size: 1.1rem; font-weight: 600; color: #0F172A; margin-bottom: 12px; border-bottom: 2px solid #0EA5E9; padding-bottom: 8px; }}
            .metric-row {{ display: flex; gap: 16px; margin-bottom: 16px; }}
            .metric-box {{ flex: 1; background: #F8FAFC; padding: 16px; border-radius: 8px; text-align: center; }}
            .metric-value {{ font-size: 1.5rem; font-weight: 700; color: #0EA5E9; }}
            .metric-label {{ font-size: 0.85rem; color: #64748B; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: #F1F5F9; padding: 12px; text-align: left; font-weight: 600; }}
            .cta-section {{ background: #FEF3C7; border: 1px solid #FDE68A; border-radius: 8px; padding: 20px; margin-top: 24px; text-align: center; }}
            .cta-button {{ display: inline-block; background: #0EA5E9; color: white; padding: 12px 24px; border-radius: 8px; text-decoration: none; font-weight: 600; }}
            .footer {{ background: #F8FAFC; padding: 20px; border-radius: 0 0 12px 12px; text-align: center; font-size: 0.85rem; color: #64748B; }}
            .query-box {{ background: #F1F5F9; padding: 16px; border-radius: 8px; border-left: 4px solid #0EA5E9; margin-bottom: 20px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0; font-size: 1.5rem;">📊 NexSupply Analysis Report</h1>
                <p style="margin: 10px 0 0 0; opacity: 0.9;">{safe_product_name}</p>
            </div>
            
            <div class="content">
                <!-- User Query -->
                <div class="section">
                    <div class="section-title">🔍 Your Request</div>
                    <div class="query-box">
                        {safe_user_query}
                    </div>
                </div>
                
                <!-- Market Snapshot -->
                <div class="section">
                    <div class="section-title">📈 Market Snapshot</div>
                    <table>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Market Demand:</strong></td>
                            <td style="padding: 8px 0;">{market.get('demand', 'Medium')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Est. Margin:</strong></td>
                            <td style="padding: 8px 0;">{market.get('margin', '25%')}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px 0;"><strong>Competition:</strong></td>
                            <td style="padding: 8px 0;">{market.get('competition', 'Medium')}</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Landed Cost -->
                <div class="section">
                    <div class="section-title">💰 Landed Cost Estimate</div>
                    <div style="text-align: center; padding: 20px; background: #F0F9FF; border-radius: 8px;">
                        <div style="font-size: 2rem; font-weight: 700; color: #0EA5E9;">
                            ${landed_cost.get('cost_per_unit_usd', 0):.2f}
                        </div>
                        <div style="color: #64748B;">Per Unit (DDP)</div>
                    </div>
                </div>
                
                <!-- Verified Suppliers -->
                <div class="section">
                    <div class="section-title">✓ Verified Suppliers ({len(suppliers)} found)</div>
                    <table>
                        <tr>
                            <th>Supplier</th>
                            <th>Location</th>
                            <th>Price Range</th>
                            <th>Grade</th>
                        </tr>
                        {supplier_rows if supplier_rows else '<tr><td colspan="4" style="padding: 12px; text-align: center;">No suppliers matched criteria</td></tr>'}
                    </table>
                </div>
                
                <!-- Confidence -->
                <div class="section">
                    <div style="text-align: center; padding: 12px; background: #F8FAFC; border-radius: 8px;">
                        <span style="font-weight: 600;">Analysis Confidence:</span>
                        <span style="color: {'#10B981' if confidence >= 0.7 else '#F59E0B'}; font-weight: 700;">
                            {int(confidence * 100)}%
                        </span>
                    </div>
                </div>
                
                <!-- CTA -->
                <div class="cta-section">
                    <p style="margin: 0 0 16px 0; font-weight: 600; color: #92400E;">
                        🔥 Ready to move forward?
                    </p>
                    <p style="margin: 0 0 16px 0; font-size: 0.9rem; color: #78350F;">
                        This analysis provides structure and insights. When you're ready,<br>
                        let us handle factory visits, negotiations, and quality control.
                    </p>
                    <a href="mailto:{CONSULTATION_EMAIL}?subject=Consultation Request: {safe_product_name}" class="cta-button">
                        📧 Talk to a Sourcing Expert
                    </a>
                </div>
            </div>
            
            <div class="footer">
                <p>Generated by NexSupply AI · {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}</p>
                <p style="font-size: 0.75rem; color: #9CA3AF;">
                    This is an AI-generated estimate for planning purposes.<br>
                    Contact our team for verified quotes and supplier due diligence.
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


def html_escape(text: str) -> str:
    """Escape HTML special characters to prevent injection and encoding issues."""
    if not text:
        return ""
    if isinstance(text, bytes):
        text = text.decode('utf-8', errors='replace')
    # HTML escape
    text = str(text).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
    return text


def generate_internal_email_html(
    product_name: str,
    user_query: str,
    user_email: str,
    analysis_data: Dict
) -> str:
    """Generate detailed HTML email for internal consultation team."""
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')
    
    # Escape all user input for HTML safety - with additional encoding safety
    try:
        safe_product_name = html_escape(str(product_name))
        safe_user_query = html_escape(str(user_query))
        safe_user_email = html_escape(str(user_email))
        
        # Ensure all escaped strings are UTF-8 safe
        safe_product_name = safe_product_name.encode('utf-8', errors='replace').decode('utf-8')
        safe_user_query = safe_user_query.encode('utf-8', errors='replace').decode('utf-8')
        safe_user_email = safe_user_email.encode('utf-8', errors='replace').decode('utf-8')
    except Exception:
        # If escaping fails, use ASCII fallback
        safe_product_name = str(product_name).encode('ascii', errors='replace').decode('ascii')
        safe_user_query = str(user_query).encode('ascii', errors='replace').decode('ascii')
        safe_user_email = str(user_email).encode('ascii', errors='replace').decode('ascii')
    
    # Full JSON for internal team - ensure it's UTF-8 safe
    try:
        json_formatted = json.dumps(analysis_data, indent=2, ensure_ascii=False, default=str)
        # Ensure JSON is UTF-8 safe before escaping
        json_formatted = json_formatted.encode('utf-8', errors='replace').decode('utf-8')
        # Escape JSON for HTML embedding
        json_formatted = html_escape(json_formatted)
    except (TypeError, ValueError, UnicodeEncodeError, UnicodeDecodeError) as e:
        # If JSON serialization fails, use safe fallback
        try:
            json_formatted = html_escape(str(analysis_data).encode('utf-8', errors='replace').decode('utf-8'))
        except Exception:
            json_formatted = "Analysis data unavailable"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: monospace; line-height: 1.4; color: #1F2937; background: #F8FAFC; }}
            .container {{ max-width: 800px; margin: 0 auto; padding: 20px; }}
            .header {{ background: #DC2626; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
            .content {{ background: white; padding: 24px; border: 1px solid #E5E7EB; }}
            .section {{ margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #E5E7EB; }}
            .label {{ font-weight: 700; color: #374151; margin-bottom: 8px; }}
            .value {{ background: #F1F5F9; padding: 12px; border-radius: 6px; }}
            pre {{ background: #1F2937; color: #10B981; padding: 16px; border-radius: 8px; overflow-x: auto; font-size: 0.8rem; max-height: 400px; overflow-y: auto; }}
            .priority {{ display: inline-block; background: #FEE2E2; color: #DC2626; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin: 0;">🚨 New Consultation Lead</h1>
                <p style="margin: 8px 0 0 0; opacity: 0.9;">Timestamp: {timestamp}</p>
            </div>
            
            <div class="content">
                <!-- Priority Indicator -->
                <div style="margin-bottom: 20px;">
                    <span class="priority">⚡ HOT LEAD - User requested analysis report</span>
                </div>
                
                <!-- User Info -->
                <div class="section">
                    <div class="label">👤 Customer Email:</div>
                    <div class="value">{safe_user_email}</div>
                </div>
                
                <!-- Product -->
                <div class="section">
                    <div class="label">📦 Product/Query:</div>
                    <div class="value">{safe_product_name}</div>
                </div>
                
                <!-- User's Full Query -->
                <div class="section">
                    <div class="label">📝 Customer's Original Input:</div>
                    <div class="value" style="white-space: pre-wrap;">{safe_user_query}</div>
                </div>
                
                <!-- Quick Stats -->
                <div class="section">
                    <div class="label">📊 Quick Summary:</div>
                    <table style="width: 100%;">
                        <tr>
                            <td style="padding: 8px; background: #F8FAFC;"><strong>Est. Landed Cost:</strong></td>
                            <td style="padding: 8px;">${analysis_data.get('landed_cost', {}).get('cost_per_unit_usd', 0):.2f}/unit</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; background: #F8FAFC;"><strong>Suppliers Found:</strong></td>
                            <td style="padding: 8px;">{len(analysis_data.get('suppliers', []))}</td>
                        </tr>
                        <tr>
                            <td style="padding: 8px; background: #F8FAFC;"><strong>Confidence:</strong></td>
                            <td style="padding: 8px;">{int(analysis_data.get('analysis_confidence', 0.75) * 100)}%</td>
                        </tr>
                    </table>
                </div>
                
                <!-- Full JSON Data -->
                <div class="section" style="border-bottom: none;">
                    <div class="label">🔧 Full AI Analysis JSON (for consultation prep):</div>
                    <pre>{json_formatted}</pre>
                </div>
                
                <!-- Action Items -->
                <div style="background: #FEF3C7; padding: 16px; border-radius: 8px; margin-top: 16px;">
                    <strong style="color: #92400E;">📋 Recommended Follow-up:</strong>
                    <ol style="margin: 12px 0 0 0; color: #78350F;">
                        <li>Reply within 24 hours acknowledging receipt</li>
                        <li>Review AI analysis for accuracy and gaps</li>
                        <li>Prepare 2-3 specific supplier recommendations</li>
                        <li>Schedule discovery call to understand exact requirements</li>
                    </ol>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    return html


# =============================================================================
# MAIN EMAIL FUNCTIONS
# =============================================================================

def send_email_report(
    recipient_email: str,
    product_name: str,
    user_query: str,
    analysis_data: Optional[Dict] = None,
    cc_internal: bool = True
) -> Dict:
    """
    Send analysis report email to customer with CC to consultation team.
    
    Args:
        recipient_email: Customer's email address
        product_name: Product/query name for subject line
        user_query: The original user input text
        analysis_data: Full analysis result dictionary (from SourcingState.get_result())
        cc_internal: Whether to CC the consultation team (default: True)
    
    Returns:
        Dict with 'success' boolean and 'message' string
    """
    
    # Get analysis data from state if not provided
    if analysis_data is None:
        state = get_sourcing_state()
        analysis_data = state.get_result() or {}
    
    # Get SMTP config
    config = get_smtp_config()
    
    # Validate configuration
    if not config["username"] or not config["password"]:
        # Return mock success for demo/development
        return {
            "success": True,
            "message": "Email queued (SMTP not configured - demo mode)",
            "demo_mode": True
        }
    
    try:
        # Sanitize all input strings to prevent encoding errors
        safe_product_name = safe_utf8_string(product_name, max_length=50)
        safe_user_query = safe_utf8_string(user_query, max_length=1000)
        
        # Create message
        msg = MIMEMultipart('alternative')
        
        # Encode subject properly for non-ASCII characters (UTF-8)
        safe_subject = safe_email_header(f"NexSupply Analysis Report: {safe_product_name}")
        msg['Subject'] = Header(safe_subject, 'utf-8')
        msg['From'] = formataddr((safe_utf8_string(config['from_name']), config['from_email']))
        msg['To'] = recipient_email
        
        # CC consultation team for internal handover
        if cc_internal:
            msg['Cc'] = CONSULTATION_EMAIL
        
        # Generate customer-facing HTML (use safe strings)
        customer_html = generate_customer_email_html(
            product_name=safe_product_name,
            user_query=safe_user_query,
            analysis_data=analysis_data,
            include_json=False
        )
        
        # Attach HTML content with explicit UTF-8 encoding
        html_part = MIMEText(customer_html, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Determine all recipients
        recipients = [recipient_email]
        if cc_internal:
            recipients.append(CONSULTATION_EMAIL)
        
        # Send email with UTF-8 encoding - use Port 465 (SMTP_SSL) for better security
        # SMTP_SSL uses implicit SSL/TLS encryption (no starttls() needed)
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(config["server"], config["port"], context=context, timeout=10) as server:
            # No server.ehlo() or server.starttls() needed - SMTP_SSL handles encryption implicitly
            server.login(config["username"], config["password"])
            # Use as_string() and encode explicitly for better control
            try:
                email_str = msg.as_string()
                email_bytes = email_str.encode('utf-8', errors='replace')
            except Exception:
                # Fallback to as_bytes() if as_string() fails
                email_bytes = msg.as_bytes()
            server.sendmail(config["from_email"], recipients, email_bytes)
        
        # ALWAYS send notification to outreach@nexsupply.net with user email and content
        # This ensures we capture all user emails and report requests
        try:
            send_user_report_notification(
                user_email=recipient_email,
                product_name=product_name,
                user_query=user_query,
                analysis_data=analysis_data
            )
        except Exception as notify_err:
            # Log but don't fail the main email send
            logger.warning(f"Failed to send notification to outreach: {notify_err}")
        
        # Send separate detailed email to internal team (with full JSON) if requested
        if cc_internal:
            send_internal_notification(
                user_email=recipient_email,
                product_name=product_name,
                user_query=user_query,
                analysis_data=analysis_data
            )
        
        return {
            "success": True,
            "message": f"Report sent to {recipient_email}" + (f" (CC: {CONSULTATION_EMAIL})" if cc_internal else "")
        }
        
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        return handle_email_error(e, "E-203", "Encoding error", include_retry=True)
    except smtplib.SMTPAuthenticationError as e:
        return handle_email_error(e, "E-204", "SMTP authentication failed", include_retry=False)
    except smtplib.SMTPException as e:
        return handle_email_error(e, "E-205", "SMTP error", include_retry=True)
    except Exception as e:
        return handle_email_error(e, "E-206", "Unexpected email error", include_retry=True)


def send_user_report_notification(
    user_email: str,
    product_name: str,
    user_query: str,
    analysis_data: Dict
) -> Dict:
    """
    Send notification to outreach@nexsupply.net when user requests email report.
    Includes user email and report content.
    """
    config = get_smtp_config()
    
    if not config["username"] or not config["password"]:
        return {"success": True, "message": "Notification skipped (demo mode)"}
    
    try:
        # Sanitize all input strings
        safe_product_name = safe_utf8_string(product_name, max_length=50)
        safe_user_email = safe_utf8_string(user_email, max_length=100)
        safe_user_query = safe_utf8_string(user_query, max_length=2000)
        
        msg = MIMEMultipart('alternative')
        safe_subject = safe_email_header(f"📧 Email Report Request: {safe_product_name} from {safe_user_email}")
        msg['Subject'] = Header(safe_subject, 'utf-8')
        msg['From'] = formataddr((safe_utf8_string(config['from_name']), config['from_email']))
        msg['To'] = CONSULTATION_EMAIL  # outreach@nexsupply.net
        
        # Generate notification HTML
        notification_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: #0EA5E9; color: white; padding: 20px; border-radius: 8px 8px 0 0; }}
                .content {{ background: #F8FAFC; padding: 20px; border: 1px solid #E5E7EB; }}
                .section {{ margin-bottom: 20px; }}
                .label {{ font-weight: 600; color: #1F2937; margin-bottom: 8px; }}
                .value {{ color: #4B5563; }}
                .highlight {{ background: #FEF3C7; padding: 12px; border-radius: 6px; margin: 12px 0; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h2 style="margin: 0;">📧 Email Report Request</h2>
                </div>
                <div class="content">
                    <div class="section">
                        <div class="label">👤 User Email:</div>
                        <div class="value highlight">{safe_user_email}</div>
                    </div>
                    
                    <div class="section">
                        <div class="label">📦 Product/Query:</div>
                        <div class="value">{safe_product_name}</div>
                    </div>
                    
                    <div class="section">
                        <div class="label">📝 User's Original Input:</div>
                        <div class="value" style="white-space: pre-wrap; background: white; padding: 12px; border-radius: 6px;">{safe_user_query}</div>
                    </div>
                    
                    <div class="section">
                        <div class="label">📊 Quick Summary:</div>
                        <table style="width: 100%; background: white; border-radius: 6px; padding: 12px;">
                            <tr>
                                <td style="padding: 8px;"><strong>Est. Landed Cost:</strong></td>
                                <td style="padding: 8px;">${analysis_data.get('landed_cost', {}).get('cost_per_unit_usd', 0):.2f}/unit</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px;"><strong>Suppliers Found:</strong></td>
                                <td style="padding: 8px;">{len(analysis_data.get('suppliers', []))}</td>
                            </tr>
                            <tr>
                                <td style="padding: 8px;"><strong>Confidence:</strong></td>
                                <td style="padding: 8px;">{int(analysis_data.get('analysis_confidence', 0.75) * 100)}%</td>
                            </tr>
                        </table>
                    </div>
                    
                    <div class="section" style="background: #F0F9FF; padding: 16px; border-radius: 6px; margin-top: 20px;">
                        <strong style="color: #0369A1;">💡 Action Required:</strong>
                        <p style="margin: 8px 0 0 0; color: #1E40AF;">
                            User has requested the full analysis report via email.<br>
                            Consider following up with personalized consultation offer.
                        </p>
                    </div>
                </div>
            </div>
        </body>
        </html>
        """
        
        html_part = MIMEText(notification_html, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Also attach JSON data
        json_str = json.dumps(analysis_data, indent=2, ensure_ascii=False, default=str)
        json_attachment = MIMEBase('application', 'json')
        json_attachment.set_payload(json_str.encode('utf-8'))
        encoders.encode_base64(json_attachment)
        safe_filename = safe_email_header(f"report_request_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", max_length=100)
        json_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{safe_filename}"'
        )
        msg.attach(json_attachment)
        
        # Send via SMTP_SSL
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(config["server"], config["port"], context=context, timeout=10) as server:
            server.login(config["username"], config["password"])
            try:
                email_str = msg.as_string()
                email_bytes = email_str.encode('utf-8', errors='replace')
            except Exception:
                email_bytes = msg.as_bytes()
            server.sendmail(config["from_email"], [CONSULTATION_EMAIL], email_bytes)
        
        return {"success": True, "message": "Notification sent to outreach team"}
        
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        logger.error(f"Encoding error in user report notification: {e}", exc_info=True)
        return {"success": False, "message": "Notification failed: Encoding error"}
    except smtplib.SMTPException as e:
        logger.error(f"SMTP error in user report notification: {e}", exc_info=True)
        return {"success": False, "message": "Notification failed: SMTP error"}
    except Exception as e:
        logger.error(f"Unexpected error in user report notification: {e}", exc_info=True)
        return {"success": False, "message": "Notification failed"}


def send_internal_notification(
    user_email: str,
    product_name: str,
    user_query: str,
    analysis_data: Dict
) -> Dict:
    """
    Send detailed notification to internal consultation team.
    Includes full JSON data for consultation preparation.
    """
    
    config = get_smtp_config()
    
    if not config["username"] or not config["password"]:
        return {"success": True, "message": "Internal notification skipped (demo mode)"}
    
    try:
        # Sanitize all input strings
        safe_product_name = safe_utf8_string(product_name, max_length=40)
        safe_user_email = safe_utf8_string(user_email, max_length=100)
        safe_user_query = safe_utf8_string(user_query, max_length=2000)
        
        msg = MIMEMultipart('alternative')
        # Use UTF-8 encoding for subject (no ASCII filtering)
        safe_subject = safe_email_header(f"NEW LEAD: {safe_product_name} - {safe_user_email}")
        msg['Subject'] = Header(safe_subject, 'utf-8')
        msg['From'] = formataddr((safe_utf8_string(config['from_name']), config['from_email']))
        msg['To'] = CONSULTATION_EMAIL
        
        # Generate internal HTML with full data (use safe strings)
        internal_html = generate_internal_email_html(
            product_name=safe_product_name,
            user_query=safe_user_query,
            user_email=safe_user_email,
            analysis_data=analysis_data
        )
        
        html_part = MIMEText(internal_html, 'html', 'utf-8')
        msg.attach(html_part)
        
        # Also attach JSON as file with UTF-8 encoding
        json_str = json.dumps(analysis_data, indent=2, ensure_ascii=False, default=str)
        json_attachment = MIMEBase('application', 'json')
        json_attachment.set_payload(json_str.encode('utf-8'))
        encoders.encode_base64(json_attachment)
        safe_filename = safe_email_header(f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", max_length=100)
        json_attachment.add_header(
            'Content-Disposition',
            f'attachment; filename="{safe_filename}"'
        )
        msg.attach(json_attachment)
        
        # Use SMTP_SSL for Port 465 - implicit SSL/TLS encryption
        # No server.ehlo() or server.starttls() needed
        context = ssl.create_default_context()
        
        with smtplib.SMTP_SSL(config["server"], config["port"], context=context, timeout=10) as server:
            server.login(config["username"], config["password"])
            # Use as_string() and encode explicitly for better control
            try:
                email_str = msg.as_string()
                email_bytes = email_str.encode('utf-8', errors='replace')
            except Exception:
                # Fallback to as_bytes() if as_string() fails
                email_bytes = msg.as_bytes()
            server.sendmail(config["from_email"], [CONSULTATION_EMAIL], email_bytes)
        
        return {"success": True, "message": "Internal notification sent"}
        
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        # Don't fail the main flow if internal notification fails
        return {"success": False, "message": "Internal notification failed: Encoding error"}
    except Exception as e:
        # Don't fail the main flow if internal notification fails
        try:
            error_msg = safe_utf8_string(str(e), max_length=200)
        except:
            error_msg = "Internal notification failed"
        return {"success": False, "message": f"Internal notification failed: {error_msg}"}


def request_consultation(
    user_email: str,
    user_name: str = "",
    message: str = "",
    product_name: str = "",
    analysis_data: Optional[Dict] = None
) -> Dict:
    """
    Send a consultation request to the internal team.
    Called when user clicks "Talk to a Sourcing Expert" button.
    
    PRIMARY METHOD: Save to database (always works)
    SECONDARY: Try email (optional, failure doesn't affect success)
    """
    
    if analysis_data is None:
        state = get_sourcing_state()
        analysis_data = state.get_result() or {}
    
    user_query = st.session_state.get("search_query", "")
    
    # STEP 1: Always save to database first (primary method)
    try:
        init_database()  # Ensure database is initialized
        request_id = log_consultation_request(
            user_email=user_email,
            user_name=user_name,
            product_query=user_query or product_name,
            message=message
        )
        
        if request_id:
            # Database save successful - this is our primary method
            db_success = True
        else:
            db_success = False
    except Exception as db_error:
        logger.error(f"Database save failed: {db_error}", exc_info=True)
        db_success = False
    
    # STEP 2: Try email (optional, failure doesn't affect success)
    config = get_smtp_config()
    email_success = False
    
    if not config["username"] or not config["password"]:
        # No email config - database is primary, so return success
        return {
            "success": True,
            "message": "Consultation request received! We'll contact you within 24 hours.",
            "demo_mode": True,
            "saved_to_db": db_success
        }
    
    try:
        # Sanitize all input strings to prevent encoding errors
        safe_product_name = safe_utf8_string(product_name or "Consultation Request", max_length=40)
        safe_user_email = safe_utf8_string(user_email, max_length=100)
        safe_message = safe_utf8_string(message or "", max_length=2000)
        safe_user_query = safe_utf8_string(user_query or "", max_length=2000)
        
        # Ensure all strings are properly encoded before use
        try:
            # Test encoding of all strings
            safe_product_name.encode('utf-8')
            safe_user_email.encode('utf-8')
            safe_message.encode('utf-8')
            safe_user_query.encode('utf-8')
        except UnicodeEncodeError:
            # If any encoding fails, use ASCII fallback
            safe_product_name = safe_product_name.encode('ascii', errors='replace').decode('ascii')
            safe_user_email = safe_user_email.encode('ascii', errors='replace').decode('ascii')
            safe_message = safe_message.encode('ascii', errors='replace').decode('ascii')
            safe_user_query = safe_user_query.encode('ascii', errors='replace').decode('ascii')
        
        msg = MIMEMultipart('alternative')
        # Use UTF-8 encoding for subject - ensure it's safe
        safe_subject = f"CONSULTATION REQUEST: {safe_product_name} - {safe_user_email}"
        # Limit subject length and ensure UTF-8 safe
        safe_subject = safe_subject[:100].encode('utf-8', errors='replace').decode('utf-8')
        msg['Subject'] = Header(safe_subject, 'utf-8')
        
        # Safe from address
        from_name_safe = safe_utf8_string(config['from_name'], max_length=50)
        msg['From'] = formataddr((from_name_safe, config['from_email']))
        msg['To'] = CONSULTATION_EMAIL
        msg['Reply-To'] = safe_user_email
        
        # Generate internal email with UTF-8 safe string concatenation
        # Ensure all parts are safe before concatenation
        try:
            full_query = f"{safe_message}\n\n---\nOriginal Analysis Query:\n{safe_user_query}"
            # Test encoding of concatenated string
            full_query.encode('utf-8')
        except (UnicodeEncodeError, UnicodeDecodeError):
            # Fallback: use ASCII-safe version
            safe_message_ascii = safe_message.encode('ascii', errors='replace').decode('ascii')
            safe_user_query_ascii = safe_user_query.encode('ascii', errors='replace').decode('ascii')
            full_query = f"{safe_message_ascii}\n\n---\nOriginal Analysis Query:\n{safe_user_query_ascii}"
        
        # Ensure analysis_data is JSON-safe before passing to HTML generator
        try:
            # Test if analysis_data can be serialized
            json.dumps(analysis_data, ensure_ascii=False, default=str)
        except (TypeError, ValueError) as e:
            # If JSON serialization fails, use empty dict
            analysis_data = {}
        
        # Generate email content - use simple text first, then try HTML
        # This approach is more reliable for encoding issues
        text_content = f"""Consultation Request

From: {safe_user_email}
Product: {safe_product_name}
Message: {safe_message}
Original Query: {safe_user_query}

---
Analysis Summary:
- Landed Cost: ${analysis_data.get('landed_cost', {}).get('cost_per_unit_usd', 0):.2f}/unit
- Suppliers Found: {len(analysis_data.get('suppliers', []))}
- Confidence: {int(analysis_data.get('analysis_confidence', 0.75) * 100)}%
"""
        
        # Try to create HTML version, but fallback to text if it fails
        html_content = None
        try:
            # Try generating HTML
            internal_html = generate_internal_email_html(
                product_name=safe_product_name,
                user_query=full_query,
                user_email=safe_user_email,
                analysis_data=analysis_data
            )
            # Ensure HTML is UTF-8 safe
            try:
                internal_html.encode('utf-8')
                html_content = internal_html
            except (UnicodeEncodeError, UnicodeDecodeError):
                # If encoding fails, HTML will be None and we'll use text only
                pass
        except Exception as html_error:
            # If HTML generation fails completely, just use text
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"HTML generation failed, using text only: {html_error}")
        
        # Attach content - prefer HTML if available, otherwise text
        try:
            if html_content:
                html_part = MIMEText(html_content, 'html', 'utf-8')
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)  # Add text as fallback
                msg.attach(html_part)  # Add HTML version
            else:
                # Only text version
                text_part = MIMEText(text_content, 'plain', 'utf-8')
                msg.attach(text_part)
        except Exception as attach_error:
            # Last resort: create minimal text message
            logger.warning(f"Content attachment failed, using minimal text: {attach_error}")
            minimal_text = f"Consultation Request\nFrom: {safe_user_email}\nProduct: {safe_product_name}\nMessage: {safe_message}"
            text_part = MIMEText(minimal_text, 'plain', 'utf-8')
            msg.attach(text_part)
        
        # Final safety: use as_string() and encode explicitly
        # This gives us more control over the encoding process
        try:
            email_str = msg.as_string()
            # Ensure the string can be encoded to UTF-8
            email_bytes = email_str.encode('utf-8', errors='replace')
        except Exception as e:
            # If as_string() fails, try as_bytes() as fallback
            try:
                email_bytes = msg.as_bytes()
            except Exception:
                # Last resort: create a simple text message
                simple_msg = f"From: {config['from_email']}\nTo: {CONSULTATION_EMAIL}\nSubject: {safe_subject}\n\nConsultation request from {safe_user_email}\n\nProduct: {safe_product_name}\n\nMessage: {safe_message}"
                email_bytes = simple_msg.encode('utf-8', errors='replace')
        
        # STEP 2: Try email (optional - database is primary)
        # SMTP connection with Port 465 (SMTP_SSL) - implicit SSL/TLS encryption
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL(config["server"], config["port"], context=context, timeout=10) as server:
                server.login(config["username"], config["password"])
                server.sendmail(config["from_email"], [CONSULTATION_EMAIL], email_bytes)
            email_success = True
        except Exception as email_err:
            # Email failed - but database save is primary, so log and continue
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"Email send failed (but saved to DB): {email_err}")
            email_success = False
        
        # Return success if database save worked (primary method)
        if db_success:
            return {
                "success": True,
                "message": "Consultation request received! We'll contact you within 24 hours.",
                "saved_to_db": True,
                "email_sent": email_success
            }
        else:
            # Database save also failed - this is a real error
            return {
                "success": False,
                "message": "⚠️ **Request Failed.**\n\nWe apologize for the issue. Please **refresh the page** or email us directly at {CONSULTATION_EMAIL}"
            }
        
    except (UnicodeEncodeError, UnicodeDecodeError) as e:
        # Handle encoding errors - but check if database save worked
        logger.error(f"Unicode encoding error: {str(e)}", exc_info=True)
        
        # If database save worked, return success
        if db_success:
            return {
                "success": True,
                "message": "Consultation request received! We'll contact you within 24 hours.",
                "saved_to_db": True,
                "email_sent": False
            }
        else:
            return {
                "success": False,
                "message": f"⚠️ **Request Failed. (Error Code: E-201)**\n\nWe apologize for the issue. Please **refresh the page** or email us directly at {CONSULTATION_EMAIL}"
            }
    except Exception as e:
        # Security: Don't expose exception details to users
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Request consultation error: {str(e)}", exc_info=True)
        
        # If database save worked, return success
        if db_success:
            return {
                "success": True,
                "message": "Consultation request received! We'll contact you within 24 hours.",
                "saved_to_db": True,
                "email_sent": False
            }
        else:
            return {
                "success": False,
                "message": f"⚠️ **Request Failed. (Error Code: E-202)**\n\nWe apologize for the issue. Please **refresh the page** or email us directly at {CONSULTATION_EMAIL}"
            }


# =============================================================================
# STREAMLIT UI COMPONENT
# =============================================================================

def render_email_report_form():
    """Render email report form in Streamlit UI."""
    
    st.markdown("### 📧 Get Report via Email")
    
    with st.form("email_report_form"):
        email = st.text_input(
            "Your Email",
            placeholder="your@email.com",
            help="We'll send the full analysis report to this address"
        )
        
        send_copy = st.checkbox(
            "Also notify NexSupply team for consultation",
            value=True,
            help="Our experts can help you with supplier negotiations and quality control"
        )
        
        submitted = st.form_submit_button("📤 Send Report", type="primary", use_container_width=True)
        
        if submitted:
            if not email or "@" not in email:
                st.error("Please enter a valid email address")
            else:
                state = get_sourcing_state()
                result = state.get_result()
                user_query = st.session_state.get("search_query", "")
                product_name = result.get("product_info", {}).get("name", user_query[:50]) if result else user_query[:50]
                
                with st.spinner("Sending report..."):
                    response = send_email_report(
                        recipient_email=email,
                        product_name=product_name,
                        user_query=user_query,
                        analysis_data=result,
                        cc_internal=send_copy
                    )
                
                if response["success"]:
                    st.success(f"✅ {response['message']}")
                    if response.get("demo_mode"):
                        st.info("📝 Note: Email service is in demo mode. In production, you'll receive the full report.")
                else:
                    st.error(f"❌ {response['message']}")


def render_consultation_cta():
    """Render consultation CTA button with email capture."""
    
    st.markdown("""
        <div style="
            background: linear-gradient(135deg, #0EA5E9 0%, #0284C7 100%);
            border-radius: 16px;
            padding: 32px;
            text-align: center;
            margin: 24px 0;
        ">
            <h3 style="color: white; margin: 0 0 12px 0;">🔥 Ready to make it real?</h3>
            <p style="color: rgba(255,255,255,0.9); margin: 0 0 20px 0;">
                This analysis provides structure and insights, not a final answer.<br>
                When you're ready, let us do the legwork — factory visits, negotiations, quality control.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("📧 Request Expert Consultation", expanded=False):
        with st.form("consultation_form"):
            col1, col2 = st.columns(2)
            with col1:
                email = st.text_input("Your Email *", placeholder="your@email.com")
            with col2:
                name = st.text_input("Your Name", placeholder="Optional")
            
            message = st.text_area(
                "Tell us about your project",
                placeholder="Target volume, timeline, specific requirements...",
                height=100
            )
            
            submitted = st.form_submit_button("📤 Request Consultation", type="primary", use_container_width=True)
            
            if submitted:
                # Validate inputs using centralized validation
                from utils.validation import validate_consultation_input
                
                is_valid, error_msg = validate_consultation_input(
                    email=email,
                    name=name if name else None,
                    message=message if message else None
                )
                
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                else:
                    state = get_sourcing_state()
                    result = state.get_result()
                    user_query = st.session_state.get("search_query", "")
                    product_name = result.get("product_info", {}).get("name", user_query[:50]) if result else "Consultation"
                    
                    with st.spinner("Sending request..."):
                        response = request_consultation(
                            user_email=email,
                            user_name=name,
                            message=message,
                            product_name=product_name,
                            analysis_data=result
                        )
                    
                    if response["success"]:
                        st.success(f"✅ {response['message']}")
                        st.balloons()
                    else:
                        st.error(f"❌ {response['message']}")

