"""
NexSupply Result Builder
Combines rule-based cost calculations with AI-generated insights
into a unified JSON structure for the dashboard.

Architecture:
- Numbers come from cost_calculator (deterministic, ±20-25% accuracy)
- Text/insights come from Gemini AI (qualitative analysis)
- This module merges both into final result JSON
"""

from datetime import datetime, timezone
from typing import Dict, Any, Optional, List
import uuid

from utils.cost_calculator import (
    OrderParams, 
    compute_landed_cost, 
    compute_sensitivity,
    format_for_pie_chart,
    format_for_cost_table
)
from utils.cost_tables import get_category_config, classify_category
from utils.config import Config


def generate_analysis_id() -> str:
    """Generate unique analysis ID."""
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    short_uuid = str(uuid.uuid4())[:8]
    return f"nex-{timestamp}-{short_uuid}"


def build_nexsupply_result(
    user_query: str,
    units: int = None,
    route: str = None,
    target_market: str = None,
    channel: str = None,
    retail_price: Optional[float] = None,
    ai_insights: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Build the complete NexSupply result JSON.
    
    Args:
        user_query: Original user input
        units: Order quantity (defaults to AppSettings.DEFAULT_VOLUME_UNITS)
        route: Shipping route (defaults to AppSettings.DEFAULT_ROUTE)
        target_market: Destination market (defaults to AppSettings.DEFAULT_TARGET_MARKET)
        channel: Sales channel (defaults to AppSettings.DEFAULT_CHANNEL)
        retail_price: Expected retail price for margin calculation
        ai_insights: AI-generated qualitative insights (optional)
    
    Returns:
        Complete result dictionary matching the NexSupply JSON schema
    """
    from utils.config import AppSettings
    
    # Use defaults from AppSettings if not provided
    units = units or AppSettings.DEFAULT_VOLUME_UNITS
    route = route or AppSettings.DEFAULT_ROUTE
    target_market = target_market or AppSettings.DEFAULT_TARGET_MARKET
    channel = channel or AppSettings.DEFAULT_CHANNEL
    
    # Default AI insights if not provided
    if ai_insights is None:
        ai_insights = get_default_ai_insights()
    
    # ===========================================
    # STEP 1: CLASSIFY CATEGORY
    # ===========================================
    category_id = classify_category(user_query)
    cfg = get_category_config(category_id)
    
    # ===========================================
    # STEP 2: COMPUTE LANDED COST (RULE-BASED)
    # ===========================================
    order = OrderParams(
        category_id=category_id,
        units=units,
        route=route,
        incoterm=AppSettings.DEFAULT_INCOTERM,
        retail_price_per_unit=retail_price
    )
    
    lc = compute_landed_cost(order)
    sensitivity = compute_sensitivity(order, lc)
    
    # ===========================================
    # STEP 3: BUILD META SECTION
    # ===========================================
    meta = {
        "analysis_id": generate_analysis_id(),
        "timestamp_utc": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
        "product_raw_input": user_query,
        "product_name": ai_insights.get("product_name", f"{cfg['label']} product"),
        "parsed_category_id": category_id,
        "parsed_category_label": cfg["label"],
        "calculation_method": "hybrid",
        "cost_accuracy": "±20-25% (rule-based)",
        "insight_source": "AI-assisted",
        "source": {
            "text": True,
            "image": ai_insights.get("has_image", False),
            "image_refs": ai_insights.get("image_refs", [])
        }
    }
    
    # ===========================================
    # STEP 4: BUILD ASSUMPTIONS SECTION
    # ===========================================
    # Calculate reliability based on category data coverage
    reliability_score = 0.80 if category_id != "generic_consumer_product" else 0.60
    reliability_level = "High" if reliability_score >= 0.75 else "Medium" if reliability_score >= 0.55 else "Low"
    
    assumptions = {
        "target_market": target_market,
        "channel": channel,
        "volume_units": units,
        "incoterm": AppSettings.DEFAULT_INCOTERM,
        "route": route,
        "route_display": AppSettings.get_route_display(route),
        "currency": AppSettings.DEFAULT_CURRENCY,
        "reliability_level": reliability_level,
        "reliability_score": reliability_score,
        "reliability_range": f"~{int(reliability_score*100-10)}–{int(reliability_score*100+5)}%",
        "data_coverage_notes": ai_insights.get(
            "data_coverage_notes",
            f"Based on {cfg['label']} category data with typical volume ranges."
        )
    }
    
    # ===========================================
    # STEP 5: BUILD MARKET SNAPSHOT
    # ===========================================
    # Use AI insights for qualitative market data
    margin_benchmarks = cfg.get("margin_benchmarks", {})
    typical_margin_low = int(margin_benchmarks.get("low", 0.15) * 100)
    typical_margin_high = int(margin_benchmarks.get("high", 0.50) * 100)
    
    market_snapshot = {
        "demand": {
            "level": ai_insights.get("demand_level", "Medium"),
            "score": ai_insights.get("demand_score", 0.6),
            "change_vs_last_quarter_percent": ai_insights.get("demand_change", 0),
            "notes": ai_insights.get("demand_notes", "Moderate demand with seasonal variations.")
        },
        "margin": {
            "estimated_range_percent": [typical_margin_low + 5, typical_margin_high - 5],
            "category_typical_range_percent": [typical_margin_low, typical_margin_high],
            "notes": ai_insights.get("margin_notes", f"Based on landed cost estimate and typical retail pricing for {cfg['label']}.")
        },
        "competition": {
            "level": ai_insights.get("competition_level", "Medium"),
            "score": ai_insights.get("competition_score", 0.6),
            "estimated_active_listings": ai_insights.get("active_listings", 10),
            "notes": ai_insights.get("competition_notes", "Moderate competition with established players.")
        }
    }
    
    # ===========================================
    # STEP 6: BUILD LANDED COST SECTION
    # ===========================================
    # Format components for display
    components = []
    label_map = {
        "product": "Manufacturing",
        "packing": "Packing",
        "shipping": "Freight & Logistics",
        "handling": "Handling & QC",
        "duty_and_tax": "Customs & Duty"
    }
    
    for key, amount in lc["components_usd"].items():
        components.append({
            "key": key,
            "label": label_map.get(key, key.replace("_", " ").title()),
            "amount_usd": amount,
            "share_percent": lc["components_share_percent"].get(key, 0)
        })
    
    # Build sensitivity scenarios
    sensitivity_scenarios = []
    for scenario in sensitivity.get("scenarios", []):
        sensitivity_scenarios.append({
            "scenario_id": scenario["name"].lower().replace(" ", "_").replace("%", "pct"),
            "title": scenario["name"],
            "description": scenario["trigger"],
            "margin_impact": scenario["margin_impact"],
            "new_margin": scenario["new_margin"],
            "recommendation": scenario["recommendation"]
        })
    
    landed_cost = {
        "order": {
            "units": lc["units"],
            "total_weight_kg": lc["total_weight_kg"],
            "total_cbm": lc["total_cbm"],
            "total_cartons": lc.get("total_cartons", 0)
        },
        "totals": {
            "total_landed_cost_usd": lc["total_landed_cost_usd"],
            "landed_cost_per_unit_usd": lc["landed_cost_per_unit_usd"]
        },
        "components": components,
        "detailed_breakdown": lc.get("cost_breakdown_detailed", {}),
        "current_margin_estimate": sensitivity.get("base_margin", "25-40%"),
        "sensitivity": sensitivity_scenarios,
        "hidden_cost_alerts": ai_insights.get("hidden_cost_alerts", get_default_hidden_costs(cfg))
    }
    
    # Add margin estimate if available
    if "margin_estimate" in lc:
        landed_cost["margin_estimate"] = lc["margin_estimate"]
    
    # ===========================================
    # STEP 7: BUILD SUPPLIERS SECTION
    # ===========================================
    suppliers = ai_insights.get("suppliers", get_default_suppliers(cfg))
    
    # ===========================================
    # STEP 8: BUILD RISK OVERVIEW
    # ===========================================
    risk_overview = ai_insights.get("risk_overview", {
        "overall_level": "Medium",
        "axes": {
            "quality": "Medium",
            "compliance": "Medium",
            "lead_time": "Medium",
            "financial": "Low",
            "geopolitical": "Medium"
        },
        "comments": [
            f"Standard risk profile for {cfg['label']} category.",
            "China-based suppliers with established export experience."
        ]
    })
    
    # ===========================================
    # STEP 9: BUILD NEXT ACTIONS
    # ===========================================
    next_actions = [
        {
            "action_id": "refine_assumptions",
            "label": "Refine Analysis",
            "description": "Adjust volume, market, or requirements and rerun.",
            "cta_type": "rerun_analysis",
            "icon": "🔄"
        },
        {
            "action_id": "export_report",
            "label": "Export Report",
            "description": "Download as PDF or spreadsheet.",
            "cta_type": "export_pdf",
            "icon": "📄"
        },
        {
            "action_id": "run_risk_check",
            "label": "Deep Risk Check",
            "description": "Detailed supplier verification and compliance audit.",
            "cta_type": "open_risk_module",
            "icon": "🔍"
        }
    ]
    
    # ===========================================
    # STEP 10: BUILD CONSULTING OFFER
    # ===========================================
    consulting_offer = {
        "is_recommended": True,
        "headline": "Ready to make it real?",
        "case_summary": f"Landed cost ~${lc['landed_cost_per_unit_usd']:.2f}/unit · Margin {typical_margin_low+5}–{typical_margin_high-5}% · {len(suppliers)} vetted suppliers",
        "reason_summary": ai_insights.get(
            "consulting_reason",
            "This analysis provides structure and insights. When you're ready, let us handle factory visits, negotiations, and quality control."
        ),
        "suggested_scope": ["factory_sourcing", "sample_qc", "logistics"],
        "contact_email": Config.get_consultation_email(),
        "response_time": "24 hours"
    }
    
    # ===========================================
    # FINAL ASSEMBLY
    # ===========================================
    result = {
        "meta": meta,
        "assumptions": assumptions,
        "market_snapshot": market_snapshot,
        "landed_cost": landed_cost,
        "suppliers": suppliers,
        "risk_overview": risk_overview,
        "next_actions": next_actions,
        "consulting_offer": consulting_offer
    }
    
    return result


def get_default_ai_insights() -> Dict[str, Any]:
    """Default AI insights when Gemini is not called."""
    return {
        "product_name": "Consumer Product",
        "demand_level": "Medium",
        "demand_score": 0.6,
        "demand_change": 0,
        "demand_notes": "Moderate market demand with stable trends.",
        "competition_level": "Medium",
        "competition_score": 0.6,
        "active_listings": 10,
        "competition_notes": "Fragmented market with multiple suppliers.",
        "margin_notes": "Typical margins for this category.",
        "data_coverage_notes": "Based on public trade data and category benchmarks.",
        "consulting_reason": "Expert support recommended for supplier verification and negotiation."
    }


def get_default_hidden_costs(cfg: Dict[str, Any]) -> List[str]:
    """Generate category-appropriate hidden cost alerts."""
    category = cfg.get("label", "product").lower()
    
    base_alerts = [
        "Raw material price fluctuations may affect FOB pricing.",
        "Port congestion or delays may incur demurrage/detention fees.",
        "Quality control inspection fees for pre-shipment verification."
    ]
    
    if "candy" in category or "food" in category:
        base_alerts.extend([
            "Food safety testing costs (heavy metals, microbiological).",
            "FDA registration and import compliance fees."
        ])
    elif "toy" in category:
        base_alerts.extend([
            "CPSIA compliance testing for children's products.",
            "Third-party safety certification costs."
        ])
    elif "electronic" in category:
        base_alerts.extend([
            "FCC/CE certification and testing requirements.",
            "Potential warranty and return handling costs."
        ])
    
    base_alerts.append("Potential changes in import tariffs or trade policy.")
    
    return base_alerts[:5]  # Limit to 5 alerts


def get_default_suppliers(cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Generate example suppliers based on category."""
    category = cfg.get("label", "Product")
    moq = cfg.get("moq_units", 5000)
    lead_time = cfg.get("typical_lead_time_days", 25)
    
    return [
        {
            "supplier_id": "sup_001",
            "display_name": f"Guangdong {category} Manufacturing Co. (Example)",
            "location": {
                "city": "Guangzhou",
                "province": "Guangdong",
                "country": "China"
            },
            "supplier_type": "Manufacturer",
            "tier": "Tier-1",
            "verified": True,
            "experience_years": 15,
            "certifications": ["ISO 9001", "BSCI"],
            "moq_units": moq,
            "price_band_fob_usd": "$0.15–$0.25",
            "lead_time_days": f"{lead_time}–{lead_time+10}",
            "response_time": "< 48h",
            "rating_score": 4.5,
            "quality_tier": "High",
            "specialization_notes": f"Specialized in {category} for international markets.",
            "risk_summary": "Established manufacturer with good track record.",
            "risk_tags": [],
            "trade_assurance": True
        },
        {
            "supplier_id": "sup_002",
            "display_name": f"Zhejiang {category} Trading Co. (Example)",
            "location": {
                "city": "Ningbo",
                "province": "Zhejiang", 
                "country": "China"
            },
            "supplier_type": "Trading Company",
            "tier": "Tier-2",
            "verified": True,
            "experience_years": 8,
            "certifications": ["ISO 9001"],
            "moq_units": int(moq * 0.5),
            "price_band_fob_usd": "$0.18–$0.30",
            "lead_time_days": f"{lead_time+5}–{lead_time+15}",
            "response_time": "< 24h",
            "rating_score": 4.2,
            "quality_tier": "Medium",
            "specialization_notes": "Flexible MOQ and quick response.",
            "risk_summary": "Lower MOQ but verify factory source.",
            "risk_tags": ["verify_factory"],
            "trade_assurance": True
        },
        {
            "supplier_id": "sup_003",
            "display_name": f"Fujian {category} Industrial Ltd. (Example)",
            "location": {
                "city": "Xiamen",
                "province": "Fujian",
                "country": "China"
            },
            "supplier_type": "Manufacturer",
            "tier": "Tier-2",
            "verified": True,
            "experience_years": 12,
            "certifications": ["ISO 9001", "ISO 14001"],
            "moq_units": int(moq * 0.8),
            "price_band_fob_usd": "$0.16–$0.28",
            "lead_time_days": f"{lead_time}–{lead_time+12}",
            "response_time": "< 48h",
            "rating_score": 4.3,
            "quality_tier": "Medium",
            "specialization_notes": "Good balance of price and quality.",
            "risk_summary": "Reliable for medium-volume orders.",
            "risk_tags": [],
            "trade_assurance": False
        }
    ]


# =============================================================================
# CONVERSION HELPERS FOR EXISTING DASHBOARD
# =============================================================================

def _calculate_lead_time(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Calculate consistent lead time from result data.
    Ensures Market Snapshot and Lead Time section show the same values.
    
    Returns:
        Dict with production_days, shipping_days, customs_days, buffer_days, total_days
    """
    # Try to get from suppliers first
    suppliers = result.get("suppliers", [])
    if suppliers:
        lead_time_str = suppliers[0].get("lead_time_days", "25-35")
        # Parse "25-35" or "25–35" format
        if isinstance(lead_time_str, str):
            if "–" in lead_time_str:
                production_days = int(lead_time_str.split("–")[0].strip())
            elif "-" in lead_time_str:
                production_days = int(lead_time_str.split("-")[0].strip())
            else:
                try:
                    production_days = int(lead_time_str)
                except ValueError:
                    production_days = 30
        else:
            production_days = int(lead_time_str)
    else:
        production_days = 30
    
    # Standard shipping and customs times
    shipping_days = 28  # Sea freight: 18-25 days average, use 28 for buffer
    customs_days = 5    # Customs clearance
    buffer_days = 7     # Port congestion and safety buffer
    
    # Calculate total
    total_days = production_days + shipping_days + customs_days + buffer_days
    
    return {
        "production_days": production_days,
        "shipping_days": shipping_days,
        "customs_days": customs_days,
        "buffer_days": buffer_days,
        "total_days": total_days,
        "safety_stock_days": 14
    }


def convert_to_dashboard_format(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert the new result format to match existing dashboard expectations.
    This ensures backward compatibility during migration.
    """
    lc = result["landed_cost"]
    market = result["market_snapshot"]
    
    # Build format expected by current render_results_page()
    dashboard_data = {
        "product_info": {
            "name": result["meta"]["product_name"],
            "category": result["meta"]["parsed_category_label"]
        },
        "analysis_confidence": result["assumptions"]["reliability_score"],
        "market_snapshot": {
            "demand": market["demand"]["level"],
            "demand_change": f"+{market['demand']['change_vs_last_quarter_percent']}%",
            "demand_description": market["demand"]["notes"],
            "margin": f"{market['margin']['estimated_range_percent'][0]}–{market['margin']['estimated_range_percent'][1]}%",
            "margin_description": market["margin"]["notes"],
            "competition": market["competition"]["level"],
            "competition_description": market["competition"]["notes"]
        },
        "landed_cost": {
            "cost_per_unit_usd": lc["totals"]["landed_cost_per_unit_usd"],
            "total_cost_usd": lc["totals"]["total_landed_cost_usd"],
            "components": {
                comp["key"]: comp["amount_usd"] 
                for comp in lc["components"]
            },
            "components_percent": {
                comp["key"]: comp["share_percent"]
                for comp in lc["components"]
            },
            "hidden_cost_warnings": lc["hidden_cost_alerts"]
        },
        "suppliers": [
            {
                "name": s["display_name"],
                "location": f"{s['location']['city']}, {s['location']['country']}",
                "rating": s.get("rating_score", 4.0),
                "min_order": f"{s.get('moq_units', 1000):,} units",
                "price_range": s.get("price_band_fob_usd", "Contact"),
                "verified": s.get("verified", False),
                "response_time": s.get("response_time", "< 48h"),
                "certifications": s.get("certifications", []),
                "years_in_business": s.get("experience_years", 0),
                "factory_grade": s.get("tier", "Unknown"),
                "trade_assurance": s.get("trade_assurance", False),
                "quality_tier": s.get("quality_tier", "Medium"),
                "risk_notes": s.get("risk_summary", "")
            }
            for s in result["suppliers"]
        ],
        "risk_analysis": result["risk_overview"],
        "lead_time": _calculate_lead_time(result),
        # New fields for enhanced transparency
        "calculation_method": result["meta"]["calculation_method"],
        "cost_accuracy": result["meta"]["cost_accuracy"],
        "assumptions": result["assumptions"],  # Use 'assumptions' key for consistency
        "assumptions_display": result["assumptions"],  # Keep for backward compatibility
        "sensitivity": lc.get("sensitivity", []),
        "consulting_offer": result["consulting_offer"]
    }
    
    return dashboard_data

