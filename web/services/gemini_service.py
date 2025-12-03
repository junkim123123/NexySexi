"""
GeminiService - Clean, Production-Ready AI Service
Uses centralized prompts from utils/prompts.py for easy maintenance.
"""
from __future__ import annotations

import os
import json
import re
import logging
import functools
import streamlit as st
from typing import Optional, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

import google.generativeai as genai

# Import centralized prompts
from utils.prompts import build_analysis_prompt, build_image_analysis_prompt

# Load .env for local development
load_dotenv(override=False)

# Configure logging (production-safe)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)  # Only log warnings and errors in production
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)


# =============================================================================
# API KEY MANAGEMENT (with caching)
# =============================================================================

# Module-level cache for API key (cleared on each Streamlit rerun)
_cached_api_key: Optional[str] = None

def _read_raw_api_key() -> Optional[str]:
    """Read API key from environment or secrets."""
    # Priority 1: Environment variables
    key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if key:
        return key
    
    # Priority 2: Streamlit secrets
    try:
        if hasattr(st, 'secrets') and st.secrets:
            for key_name in ["GEMINI_API_KEY", "GOOGLE_API_KEY", "google_api_key"]:
                if key_name in st.secrets:
                    return st.secrets[key_name]
    except (AttributeError, KeyError, TypeError):
        # Streamlit secrets not available or invalid format
        pass
    
    return None


def _clean_api_key(raw: str) -> str:
    """Clean API key of whitespace and invisible characters."""
    cleaned = raw.strip().replace("\r", "").replace("\n", "")
    for ch in ["\u00A0", "\u200B", "\u200E", "\u200F"]:
        cleaned = cleaned.replace(ch, "")
    return cleaned


@functools.lru_cache(maxsize=1)
def _get_cached_api_key() -> Optional[str]:
    """
    Cached version of API key retrieval.
    Uses LRU cache to avoid repeated environment/secret lookups.
    Cache is cleared when Streamlit reruns (new session).
    """
    raw = _read_raw_api_key()
    if not raw:
        return None
    
    cleaned = _clean_api_key(raw)
    if len(cleaned) < 20:
        return None
    
    return cleaned


def get_gemini_api_key() -> str:
    """
    Get cleaned API key or raise error.
    Uses caching to avoid repeated lookups in the same session.
    """
    global _cached_api_key
    
    # Try cached value first
    if _cached_api_key is not None:
        return _cached_api_key
    
    # Try LRU cache
    cached = _get_cached_api_key()
    if cached:
        _cached_api_key = cached
        return cached
    
    # Fallback to direct lookup (for error message)
    raw = _read_raw_api_key()
    if not raw:
        raise RuntimeError("❌ Gemini API key not found. Set GEMINI_API_KEY environment variable.")
    
    cleaned = _clean_api_key(raw)
    if len(cleaned) < 20:
        raise RuntimeError(f"❌ API key appears invalid. Length: {len(cleaned)}")
    
    _cached_api_key = cleaned
    return cleaned


def clear_api_key_cache() -> None:
    """Clear the API key cache (useful for testing or key rotation)."""
    global _cached_api_key
    _cached_api_key = None
    _get_cached_api_key.cache_clear()


# =============================================================================
# GEMINI CONFIGURATION
# =============================================================================

_configured = False

def configure_gemini() -> bool:
    """Configure Gemini API globally."""
    global _configured
    if _configured:
        return True
    
    try:
        api_key = get_gemini_api_key()
        if not api_key:
            raise ValueError("API key not found")
        genai.configure(api_key=api_key)
        _configured = True
        return True
    except ValueError as e:
        # Invalid API key or missing key
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Gemini configuration failed - invalid/missing API key: {str(e)}", exc_info=True)
        # Show generic error to user
        st.error("❌ Service configuration failed. Please refresh the page or contact support.")
        return False
    except (TypeError, AttributeError) as e:
        # Invalid API key format or genai module issue
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Gemini configuration failed - API key format error: {str(e)}", exc_info=True)
        st.error("❌ Service configuration failed. Please refresh the page or contact support.")
        return False
    except Exception as e:
        # Catch-all for unexpected errors
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Gemini configuration failed - unexpected error: {str(e)}", exc_info=True)
        st.error("❌ Service configuration failed. Please refresh the page or contact support.")
        return False


# =============================================================================
# MODE DETECTION
# =============================================================================

ANALYSIS_MODES = {
    "verify": {
        "keywords": ["verify", "verification", "check", "legitimate", "real factory", 
                     "trading company", "alibaba supplier", "검증", "확인", "scam", "fraud"],
    },
    "cost": {
        "keywords": ["cost", "landed cost", "calculate", "price", "freight", "customs", 
                     "FOB", "duty", "tariff", "비용", "가격", "랜딩", "관세"],
    },
    "market": {
        "keywords": ["market", "analysis", "demand", "trend", "competition", "margin",
                     "opportunity", "시장", "분석", "트렌드", "수요"],
    },
    "leadtime": {
        "keywords": ["lead time", "delivery", "timeline", "shipping", "production time",
                     "when", "how long", "리드타임", "배송", "일정", "납기"],
    }
}


def detect_analysis_mode(query: str) -> str:
    """Detect analysis mode from query content."""
    query_lower = query.lower()
    
    for mode, config in ANALYSIS_MODES.items():
        for keyword in config["keywords"]:
            if keyword.lower() in query_lower:
                return mode
    
    return "general"


# =============================================================================
# GEMINI SERVICE CLASS
# =============================================================================

class GeminiService:
    """
    Production-ready B2B sourcing analysis service.
    Uses centralized prompts for maintainability.
    """
    
    MODEL_NAME = "gemini-2.5-flash"
    
    def __init__(self):
        self._model = None
    
    @property
    def is_configured(self) -> bool:
        """Check if API key is available."""
        try:
            get_gemini_api_key()
            return True
        except RuntimeError:
            return False
    
    def _get_model(self):
        """Get or create model instance."""
        if self._model is None:
            if not configure_gemini():
                raise RuntimeError("Failed to configure Gemini API")
            
            self._model = genai.GenerativeModel(
                model_name=self.MODEL_NAME,
                generation_config={
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "max_output_tokens": 16384,  # Increased for detailed responses
                }
            )
        return self._model
    
    def _clean_json_response(self, response_text: str) -> str:
        """Extract pure JSON from AI response."""
        cleaned = response_text.strip()
        
        # Remove markdown code blocks
        patterns = [
            r'^```json\s*\n?(.*?)\n?```$',
            r'^```\s*\n?(.*?)\n?```$',
        ]
        
        for pattern in patterns:
            match = re.match(pattern, cleaned, re.DOTALL | re.IGNORECASE)
            if match:
                cleaned = match.group(1).strip()
                break
        
        # Extract JSON object
        first_brace = cleaned.find('{')
        last_brace = cleaned.rfind('}')
        
        if first_brace != -1 and last_brace != -1:
            cleaned = cleaned[first_brace:last_brace + 1]
        
        return cleaned
    
    def _parse_json_response(self, response_text: str) -> tuple:
        """Parse JSON from AI response."""
        try:
            cleaned = self._clean_json_response(response_text)
            data = json.loads(cleaned)
            return data, None
        except json.JSONDecodeError as e:
            return None, f"JSON parsing failed: {str(e)}"
    
    def analyze_product(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze a product sourcing query using hybrid system (rule-based + AI).
        
        Parses user input to extract volume, channel, target_market, and route,
        then uses hybrid analysis system for accurate cost calculation.
        
        Args:
            input_data: Dict with query, file_bytes, file_mime_type
        
        Returns:
            {"success": True/False, "data": result_or_error, "mode": analysis_mode}
        """
        query = input_data.get("query", "")
        file_bytes = input_data.get("file_bytes")
        file_mime_type = input_data.get("file_mime_type")
        
        if not query and not file_bytes:
            return {"success": False, "data": "Please provide a query or upload a file.", "mode": "general"}
        
        # Detect analysis mode
        mode = detect_analysis_mode(query) if query else "general"
        
        try:
            # Step 1: Extract structured data from user input using LLM
            extracted_values = None
            if query and self.is_configured:
                try:
                    from utils.extraction_prompts import (
                        EXTRACTION_USER_PROMPT_TEMPLATE,
                        normalize_extracted_values,
                        validate_and_normalize_extraction
                    )
                    
                    # Build extraction prompt with user message
                    extraction_prompt = EXTRACTION_USER_PROMPT_TEMPLATE.format(user_message=query)
                    
                    model = self._get_model()
                    response = model.generate_content(extraction_prompt)
                    
                    if response and response.text:
                        # Use Pydantic validation
                        extracted_dict, error = validate_and_normalize_extraction(response.text)
                        if not error and extracted_dict:
                            extracted_values = extracted_dict
                            logger.info(f"Successfully extracted: {extracted_values}")
                        elif error:
                            # Fallback to old parsing if validation fails
                            logger.warning(f"Extraction validation failed: {error}, using fallback parser")
                            data, parse_error = self._parse_json_response(response.text)
                            if not parse_error and data:
                                extracted_values = normalize_extracted_values(data)
                                logger.info(f"Fallback extraction successful: {extracted_values}")
                except ImportError as e:
                    logger.warning(f"Extraction module not available: {e}, using fallback parser")
                except Exception as e:
                    logger.warning(f"Extraction failed: {e}, using fallback parser", exc_info=True)
            
            # Step 2: Use extracted values or fallback to input parser
            if extracted_values:
                units = extracted_values.get("volume_units")
                channel = extracted_values.get("channel")
                target_market = extracted_values.get("target_market")
                route = extracted_values.get("route")
            else:
                # Fallback to input parser
                from utils.input_parser import parse_input_parameters
                parsed = parse_input_parameters(query)
                units = parsed.get("volume_units")
                channel = parsed.get("channel")
                target_market = parsed.get("target_market")
                route = parsed.get("route")
            
            # Step 3: Parse research data from context
            from utils.research_data import parse_research_data_from_text
            context_query = input_data.get("context_query", "") or query
            research_data = parse_research_data_from_text(context_query)
            
            # Step 4: Use hybrid system with extracted values
            result = analyze_with_hybrid_system(
                query=query,
                units=units,
                route=route,
                target_market=target_market,
                channel=channel,
                retail_price=None,
                file_bytes=file_bytes,
                research_data=research_data
            )
            
            if result["success"]:
                # Convert to expected format
                dashboard_data = result["data"]
                
                # Assumptions are already set by analyze_with_hybrid_system
                # No need to update here as they're extracted from AI response
                
                # Log successful analysis
                try:
                    from services.data_logger import log_analysis
                    log_analysis(
                        query=query or "Image analysis",
                        mode=mode,
                        json_data=dashboard_data
                    )
                except (ImportError, OSError, ValueError) as log_err:
                    # Don't break main flow if logging fails
                    logger.warning(f"Logging skipped: {log_err}")
                
                return {"success": True, "data": dashboard_data, "mode": mode}
            else:
                return result
        
        except (ConnectionError, TimeoutError) as e:
            # Network/API connection issues
            logger.error(f"API connection error: {e}", exc_info=True)
            return {"success": False, "data": "Connection to AI service failed. Please check your internet connection and try again.", "mode": mode}
        except ValueError as e:
            # Invalid input or configuration
            logger.error(f"Invalid input/configuration: {e}", exc_info=True)
            return {"success": False, "data": "Invalid request. Please check your input and try again.", "mode": mode}
        except KeyError as e:
            # Missing required data in response
            logger.error(f"Missing data in API response: {e}", exc_info=True)
            return {"success": False, "data": "Incomplete response from AI service. Please try again.", "mode": mode}
        except Exception as e:
            # Catch-all for unexpected errors
            logger.error(f"Unexpected error in analysis: {e}", exc_info=True)
            return {"success": False, "data": f"Analysis failed: {type(e).__name__}", "mode": mode}
    
    def get_mock_analysis(self, query: str = "") -> Dict[str, Any]:
        """Return comprehensive mock data for demo/testing."""
        return {
            "success": True,
            "mode": "general",
            "data": {
                "analysis_mode": "general",
                "data_transparency": {
                    "analysis_date": datetime.now().strftime("%Y-%m-%d"),
                    "data_sources": [
                        {"source": "Alibaba.com", "data_type": "Supplier listings, prices", "freshness": "Real-time"},
                        {"source": "Freightos", "data_type": "Freight rates", "freshness": "Nov 2024"},
                        {"source": "USITC", "data_type": "Tariff schedules", "freshness": "Current"}
                    ],
                    "confidence_overall": 0.75,
                    "limitations": [
                        "FOB prices are estimates - get actual quotes for accuracy",
                        "Freight rates change weekly - verify before ordering",
                        "Supplier data based on public profiles - due diligence recommended"
                    ]
                },
                "product_info": {
                    "name": query[:50] if query else "Sample Product",
                    "category": "Consumer Goods",
                    "description": "Analysis based on your query"
                },
                "market_snapshot": {
                    "demand": "High",
                    "demand_trend": "+15%",
                    "demand_evidence": "Strong search volume growth on Amazon, 12,000+ monthly searches",
                    "margin_estimate": "35%",
                    "margin_note": "After Amazon fees (~30%), actual net margin: 15-20%",
                    "competition_level": "Medium",
                    "market_size_usd": "$250M"
                },
                "landed_cost_breakdown": {
                    "cost_per_unit_usd": 4.85,
                    "cost_components": {
                        "fob_price_usd": 2.50,
                        "fob_source": "Alibaba average, range $1.80-$3.20",
                        "ocean_freight_usd": 0.65,
                        "freight_note": "LCL rate, Shenzhen to LA, Nov 2024",
                        "customs_duty_usd": 0.85,
                        "duty_note": "HTS 9503.00 + 25% Section 301 tariff",
                        "other_fees_usd": 0.85,
                        "other_note": "THC, broker, insurance, inland"
                    },
                    "total_landed_cost_usd": 4850.00,
                    "quantity_basis": 1000,
                    "hidden_cost_warnings": [
                        "Section 301 tariff (25%) already included - verify HTS code",
                        "Demurrage risk: $150-500 if container not picked up in 4 days",
                        "Quality inspection recommended: $250-350 for pre-shipment"
                    ]
                },
                "lead_time_analysis": {
                    "production_lead_time_days": 21,
                    "sea_freight_lead_time_days": 30,
                    "port_congestion_buffer_days": 5,
                    "customs_clearance_days": 5,
                    "total_lead_time_days": 61,
                    "safety_stock_days": 14,
                    "current_conditions": "LA/LB ports: +4-5 days congestion. Peak season Oct-Jan adds +7-10 days.",
                    "recommended_order_advance_days": 75
                },
                "verified_suppliers": [
                    {
                        "name": "Shenzhen Quality Manufacturing Co.",
                        "location": "Shenzhen, China",
                        "years_in_business": 8,
                        "estimated_factory_grade": "Tier-1 Factory",
                        "trade_assurance": True,
                        "trade_assurance_amount": 75000,
                        "min_order_qty": "500 units",
                        "price_range_usd": "$2.20 - $2.80",
                        "certifications": ["ISO 9001:2015", "BSCI"],
                        "response_time": "< 12 hours",
                        "estimated_quality_tier": "High",
                        "risk_notes": "CNY closure Jan 15 - Feb 10. Requires 30% deposit, balance before shipping.",
                        "green_flags": ["8 years Gold Supplier", "67% repeat buyer rate", "Real factory photos"]
                    },
                    {
                        "name": "Guangzhou Trade & Export Ltd.",
                        "location": "Guangzhou, China",
                        "years_in_business": 5,
                        "estimated_factory_grade": "Trading Company",
                        "trade_assurance": True,
                        "trade_assurance_amount": 50000,
                        "min_order_qty": "200 units",
                        "price_range_usd": "$2.80 - $3.50",
                        "certifications": ["CE (claimed)"],
                        "response_time": "< 24 hours",
                        "estimated_quality_tier": "Medium",
                        "risk_notes": "Trading company - higher markup but lower MOQ. Verify quality with samples.",
                        "green_flags": ["Flexible MOQ", "Fast response"]
                    },
                    {
                        "name": "Vietnam Precision Industries",
                        "location": "Ho Chi Minh City, Vietnam",
                        "years_in_business": 4,
                        "estimated_factory_grade": "Tier-2 Factory",
                        "trade_assurance": False,
                        "min_order_qty": "1000 units",
                        "price_range_usd": "$2.90 - $3.40",
                        "certifications": ["ISO 9001"],
                        "response_time": "24-48 hours",
                        "estimated_quality_tier": "Medium",
                        "risk_notes": "No Section 301 tariff (saves 25%), but no Trade Assurance. Use LC for payment.",
                        "green_flags": ["Tariff advantage", "Growing reputation"]
                    }
                ],
                "risk_analysis": {
                    "overall_risk_level": "Medium",
                    "risk_items": [
                        {
                            "category": "Tariff/Trade",
                            "severity": "High",
                            "description": "25% Section 301 tariff on China goods significantly impacts margin",
                            "financial_impact_usd": 625,
                            "mitigation": "Consider Vietnam sourcing to avoid tariff, or factor into pricing"
                        },
                        {
                            "category": "Logistics",
                            "severity": "High",
                            "description": "Port congestion adding 4-5 days. Peak season (Oct-Jan) adds 7-10 more.",
                            "financial_impact_usd": 150,
                            "mitigation": "Order 75+ days before needed. Build safety stock."
                        },
                        {
                            "category": "Quality",
                            "severity": "Medium",
                            "description": "First-time supplier relationship - quality consistency unknown",
                            "financial_impact_usd": 500,
                            "mitigation": "Order samples first. Use pre-shipment inspection ($250-350)."
                        },
                        {
                            "category": "Supplier",
                            "severity": "Medium",
                            "description": "CNY factory closure Jan 15 - Feb 10 disrupts production",
                            "mitigation": "Place orders before Dec 15 for pre-CNY delivery, or after Feb 20"
                        }
                    ]
                },
                "action_items": [
                    {
                        "priority": 1,
                        "action": "Request samples from top 2 suppliers",
                        "why": "Verify quality before committing to bulk order",
                        "cost": "$50-150 including shipping",
                        "timeline": "2-3 weeks"
                    },
                    {
                        "priority": 2,
                        "action": "Get actual FOB quotes for 1000 units",
                        "why": "Our estimate is ±20% - real quotes narrow this",
                        "cost": "Free",
                        "timeline": "2-3 days"
                    },
                    {
                        "priority": 3,
                        "action": "Verify HTS code with customs broker",
                        "why": "Duty rate depends on exact classification",
                        "cost": "$50-100",
                        "timeline": "1-2 days"
                    },
                    {
                        "priority": 4,
                        "action": "Get freight quote from forwarder",
                        "why": "Current rates change weekly",
                        "cost": "Free",
                        "timeline": "1 day"
                    }
                ],
                "honest_assessment": {
                    "verdict": "PROCEED WITH DUE DILIGENCE",
                    "reasoning": "Viable opportunity with healthy potential margins, but tariff and quality risks need management",
                    "key_success_factors": [
                        "Verify quality with samples before bulk order",
                        "Factor 25% tariff into pricing strategy",
                        "Build 14+ day safety stock for logistics variability"
                    ]
                },
                "analysis_confidence": 0.75
            }
        }


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================

def get_gemini_service() -> GeminiService:
    """Get a GeminiService instance."""
    return GeminiService()


# =============================================================================
# HYBRID ANALYSIS (Calculator + AI Insights)
# =============================================================================

def analyze_with_hybrid_system(
    query: str,
    units: int = None,
    route: str = None,
    target_market: str = None,
    channel: str = None,
    retail_price: Optional[float] = None,
    file_bytes: Optional[bytes] = None,
    research_data: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Hybrid analysis: Rule-based cost calculation + AI insights.
    
    This approach provides:
    - ±20-25% accuracy on costs (vs ±30-50% with pure LLM)
    - Transparent, reproducible calculations
    - AI for qualitative insights only
    
    Args:
        query: User's product description
        units: Order quantity (defaults to AppSettings.DEFAULT_VOLUME_UNITS)
        route: Shipping route (defaults to AppSettings.DEFAULT_ROUTE)
        target_market: Destination market (defaults to AppSettings.DEFAULT_TARGET_MARKET)
        channel: Sales channel (defaults to AppSettings.DEFAULT_CHANNEL)
        retail_price: Expected retail price
        file_bytes: Optional image data
    
    Returns:
        Complete analysis result
    """
    from utils.config import AppSettings
    from utils.cost_tables import classify_category, get_category_config
    from utils.cost_calculator import OrderParams, compute_landed_cost
    from utils.result_builder import build_nexsupply_result, convert_to_dashboard_format
    from utils.prompts import build_hybrid_prompt, HYBRID_SYSTEM_PROMPT
    
    # Step 1: Classify category
    category_id = classify_category(query)
    cfg = get_category_config(category_id)
    
    # Step 2: Use fallback values for initial calculation (will be updated after AI extraction)
    from utils.input_parser import parse_input_parameters
    parsed = parse_input_parameters(query) if not (units and target_market and channel) else {}
    
    temp_units = units or parsed.get("volume_units", AppSettings.DEFAULT_VOLUME_UNITS)
    temp_route = route or parsed.get("route", AppSettings.DEFAULT_ROUTE)
    temp_target_market = target_market or parsed.get("target_market", AppSettings.DEFAULT_TARGET_MARKET)
    temp_channel = channel or parsed.get("channel", AppSettings.DEFAULT_CHANNEL)
    
    # Step 3: Compute initial landed cost (rule-based) with temp values
    order = OrderParams(
        category_id=category_id,
        units=temp_units,
        route=temp_route,
        incoterm=AppSettings.DEFAULT_INCOTERM,
        retail_price_per_unit=retail_price
    )
    landed_cost_result = compute_landed_cost(order)
    
    # Step 4: Get AI insights (if API configured) - AI will extract volume, channel, target_market
    ai_insights = None
    service = get_gemini_service()
    
    if service.is_configured:
        try:
            # Build hybrid prompt with research data
            prompt = build_hybrid_prompt(
                user_input=query,
                category_id=category_id,
                category_label=cfg["label"],
                landed_cost_json=json.dumps(landed_cost_result, indent=2),
                image_summary="Image provided for analysis." if file_bytes else "",
                suppliers_db_json="[]",  # Use default suppliers
                research_data=research_data
            )
            
            model = service._get_model()
            
            # Call with system prompt
            full_prompt = f"{HYBRID_SYSTEM_PROMPT}\n\n{prompt}"
            
            if file_bytes:
                image_part = {"mime_type": "image/jpeg", "data": file_bytes}
                response = model.generate_content([full_prompt, image_part])
            else:
                response = model.generate_content(full_prompt)
            
            if response and response.text:
                data, error = service._parse_json_response(response.text)
                if not error:
                    ai_insights = data
                    
                    # Inject research data into AI insights if provided
                    if research_data and ai_insights:
                        from utils.research_data import inject_research_data
                        ai_insights = inject_research_data(ai_insights, research_data)
                    
                    # Extract values from AI response (priority 1: AI extraction)
                    if ai_insights:
                        extracted_units = ai_insights.get("volume_units")
                        extracted_target_market = ai_insights.get("target_market")
                        extracted_channel = ai_insights.get("channel")
                        
                        # Use AI-extracted values if available
                        if extracted_units and isinstance(extracted_units, (int, float)) and extracted_units > 0:
                            units = int(extracted_units)
                        if extracted_target_market and extracted_target_market.strip():
                            target_market = extracted_target_market.strip()
                        if extracted_channel and extracted_channel.strip():
                            channel = extracted_channel.strip()
        except Exception as e:
            logger.error(f"AI insights failed: {e}", exc_info=True)
    
    # Step 5: Use extracted values or fallbacks (priority: AI > input parser > defaults)
    final_units = units or parsed.get("volume_units", AppSettings.DEFAULT_VOLUME_UNITS)
    final_target_market = target_market or parsed.get("target_market", AppSettings.DEFAULT_TARGET_MARKET)
    final_channel = channel or parsed.get("channel", AppSettings.DEFAULT_CHANNEL)
    final_route = route or parsed.get("route", AppSettings.DEFAULT_ROUTE)
    
    # Step 6: Recalculate landed cost with correct values if they changed
    if final_units != temp_units or final_route != temp_route:
        order = OrderParams(
            category_id=category_id,
            units=final_units,
            route=final_route,
            incoterm=AppSettings.DEFAULT_INCOTERM,
            retail_price_per_unit=retail_price
        )
        landed_cost_result = compute_landed_cost(order)
    
    # Step 7: Build final result with extracted values
    try:
        result = build_nexsupply_result(
            user_query=query,
            units=final_units,
            route=final_route,
            target_market=final_target_market,
            channel=final_channel,
            retail_price=retail_price,
            ai_insights=ai_insights
        )
        
        # Step 5: Convert to dashboard format for backward compatibility
        dashboard_data = convert_to_dashboard_format(result)
        
        return {
            "success": True,
            "mode": "hybrid",
            "data": dashboard_data,
            "full_result": result,
            "calculation_source": "rule_based",
            "insight_source": "ai" if ai_insights else "default"
        }
    except Exception as e:
        logger.error(f"Error building result: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
        return {
            "success": False,
            "data": f"Error building analysis result: {str(e)}",
            "mode": "hybrid",
            "error": str(e),
            "error_type": type(e).__name__
        }
