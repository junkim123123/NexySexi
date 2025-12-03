# services module - All API calls (Gemini, Database, Email, Analytics)

from services.gemini_service import (
    GeminiService,
    get_gemini_service,
    get_gemini_api_key,
    configure_gemini,
    detect_analysis_mode,
)

from services.email_service import (
    send_email_report,
    send_internal_notification,
    request_consultation,
    render_email_report_form,
    render_consultation_cta,
    CONSULTATION_EMAIL,
)

from services.data_logger import (
    log_analysis,
    log_mode_usage,
    log_consultation_request,
    get_top_queries,
    get_mode_distribution,
    get_category_trends,
    get_risk_trends,
    get_daily_stats,
    get_conversion_funnel,
    render_analytics_dashboard,
)

__all__ = [
    # Gemini Service
    "GeminiService",
    "get_gemini_service",
    "get_gemini_api_key",
    "configure_gemini",
    "detect_analysis_mode",
    # Email Service
    "send_email_report",
    "send_internal_notification",
    "request_consultation",
    "render_email_report_form",
    "render_consultation_cta",
    "CONSULTATION_EMAIL",
    # Data Logger / Analytics
    "log_analysis",
    "log_mode_usage",
    "log_consultation_request",
    "get_top_queries",
    "get_mode_distribution",
    "get_category_trends",
    "get_risk_trends",
    "get_daily_stats",
    "get_conversion_funnel",
    "render_analytics_dashboard",
]
