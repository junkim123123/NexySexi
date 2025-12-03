# utils module - Configuration and helpers

from utils.config import Config, AppSettings
from utils.i18n import t, get_current_language, render_language_selector_minimal
from utils.cost_tables import (
    COST_TABLES,
    CATEGORY_KEYWORDS,
    MARKET_DATA,
    classify_category,
    get_category_config,
    list_available_categories,
    list_available_routes,
    get_confidence_level,
    get_lead_time_estimate,
    get_hidden_cost_estimate,
)
from utils.cost_calculator import OrderParams, compute_landed_cost
from utils.result_builder import build_nexsupply_result, convert_to_dashboard_format
from utils.prompts import (
    SYSTEM_INSTRUCTION,
    build_analysis_prompt,
    build_image_analysis_prompt,
    build_hybrid_prompt,
    HYBRID_SYSTEM_PROMPT,
)
from utils.validation import (
    validate_query,
    validate_context,
    validate_email,
    validate_name,
    validate_message,
    validate_uploaded_file,
    validate_analysis_input,
    validate_consultation_input,
)
from utils.logger import (
    log_structured,
    log_error,
    log_warning,
    log_info,
    build_analysis_context,
    build_email_context,
    build_db_context,
)

__all__ = [
    # Config
    "Config",
    "AppSettings",
    # i18n
    "t",
    "get_current_language",
    "render_language_selector_minimal",
    # Cost Tables
    "COST_TABLES",
    "CATEGORY_KEYWORDS",
    "MARKET_DATA",
    "classify_category",
    "get_category_config",
    "list_available_categories",
    "list_available_routes",
    "get_confidence_level",
    "get_lead_time_estimate",
    "get_hidden_cost_estimate",
    # Cost Calculator
    "OrderParams",
    "compute_landed_cost",
    # Result Builder
    "build_nexsupply_result",
    "convert_to_dashboard_format",
    # Prompts
    "SYSTEM_INSTRUCTION",
    "build_analysis_prompt",
    "build_image_analysis_prompt",
    "build_hybrid_prompt",
    "HYBRID_SYSTEM_PROMPT",
    # Validation
    "validate_query",
    "validate_context",
    "validate_email",
    "validate_name",
    "validate_message",
    "validate_uploaded_file",
    "validate_analysis_input",
    "validate_consultation_input",
    # Structured Logging
    "log_structured",
    "log_error",
    "log_warning",
    "log_info",
    "build_analysis_context",
    "build_email_context",
    "build_db_context",
]
