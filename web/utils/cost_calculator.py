"""
NexSupply Cost Calculator - Rule-based landed cost computation
This replaces LLM-generated cost estimates with deterministic calculations.

Accuracy: ±15-25% (vs LLM's ±30-50%)
Use case: Early screening, not final PO quotes

SECURITY NOTE: This module contains proprietary calculation logic.
Do not expose calculation formulas or coefficients to client-side code.
"""

from dataclasses import dataclass
from typing import Dict, Any, Optional
from utils.cost_tables import COST_TABLES, classify_category, get_category_config


@dataclass
class OrderParams:
    """Parameters for landed cost calculation."""
    category_id: str
    units: int
    route: str = None
    incoterm: str = None
    retail_price_per_unit: Optional[float] = None
    custom_unit_weight_kg: Optional[float] = None  # Override default
    
    def __post_init__(self):
        """Set defaults from AppSettings if not provided."""
        from utils.config import AppSettings
        if self.route is None:
            self.route = AppSettings.DEFAULT_ROUTE
        if self.incoterm is None:
            self.incoterm = AppSettings.DEFAULT_INCOTERM
    

def compute_landed_cost(order: OrderParams) -> Dict[str, Any]:
    """
    Compute landed cost breakdown using rule-based tables.
    
    Returns a structured dictionary with:
    - Total cost and per-unit cost
    - Component breakdown (product, packing, shipping, handling, duty)
    - Percentage shares for visualization
    - Margin estimates (if retail price provided)
    - Assumptions and metadata
    """
    cfg = get_category_config(order.category_id)
    
    units = order.units
    unit_weight = order.custom_unit_weight_kg or cfg["default_unit_weight_kg"]
    units_per_carton = cfg["default_units_per_carton"]
    cartons_per_cbm = cfg["default_cartons_per_cbm"]
    
    # ===========================================
    # BASIC CALCULATIONS
    # ===========================================
    total_weight_kg = units * unit_weight
    total_cartons = units / units_per_carton
    total_cbm = total_cartons / cartons_per_cbm
    
    # ===========================================
    # PRODUCT COST (FOB)
    # ===========================================
    product_cost = total_weight_kg * cfg["base_fob_cost_per_kg"]
    
    # ===========================================
    # PACKING COSTS
    # ===========================================
    packing_cost = total_cartons * cfg["packing_cost_per_carton_usd"]
    inner_carton_cost = total_cartons * cfg["inner_carton_cost_usd"]
    total_packing = packing_cost + inner_carton_cost
    
    # ===========================================
    # FREIGHT & LOGISTICS
    # ===========================================
    # Get freight profile for the route
    freight_cfg = cfg["freight_profile"].get(
        order.route, 
        cfg["freight_profile"]["cn_to_us_west_coast"]  # Fallback
    )
    handling_cfg = cfg["handling_profile"]
    
    sea_freight = total_cbm * freight_cfg["sea_freight_per_cbm_usd"]
    origin_charges = total_cbm * freight_cfg["origin_charges_per_cbm_usd"]
    destination_charges = total_cbm * freight_cfg["destination_charges_per_cbm_usd"]
    total_shipping = sea_freight + origin_charges + destination_charges
    
    # ===========================================
    # HANDLING & FIXED COSTS
    # ===========================================
    docs_and_broker = handling_cfg["docs_and_broker_per_shipment_usd"]
    port_misc = handling_cfg["port_misc_per_shipment_usd"]
    qc_cost = cfg["qc_cost_per_order_usd"]
    cert_cost = cfg["cert_cost_per_sku_usd"]
    total_handling = docs_and_broker + port_misc + qc_cost + cert_cost
    
    # ===========================================
    # DUTY & TAXES
    # ===========================================
    # Dutiable value = FOB + Freight (simplified)
    dutiable_base = product_cost + sea_freight
    duty = dutiable_base * cfg["duty_rate_percent"] / 100.0
    extra_taxes = dutiable_base * cfg["extra_taxes_percent"] / 100.0
    total_duty = duty + extra_taxes
    
    # ===========================================
    # TOTAL LANDED COST
    # ===========================================
    total_cost = (
        product_cost
        + total_packing
        + total_shipping
        + total_handling
        + total_duty
    )
    
    cost_per_unit = total_cost / units
    
    # ===========================================
    # COMPONENT BREAKDOWN
    # ===========================================
    components = {
        "product": product_cost,
        "packing": total_packing,
        "shipping": total_shipping,
        "handling": total_handling,
        "duty_and_tax": total_duty,
    }
    
    # Calculate percentage shares (for pie chart)
    cost_share_percent = {
        name: (value / total_cost * 100.0) if total_cost > 0 else 0
        for name, value in components.items()
    }
    
    # ===========================================
    # BUILD RESULT
    # ===========================================
    result = {
        "calculation_method": "rule_based",
        "accuracy_estimate": "±20-25%",
        "units": units,
        "total_weight_kg": round(total_weight_kg, 2),
        "total_cbm": round(total_cbm, 3),
        "total_cartons": round(total_cartons, 1),
        "total_landed_cost_usd": round(total_cost, 2),
        "landed_cost_per_unit_usd": round(cost_per_unit, 4),
        "components_usd": {k: round(v, 2) for k, v in components.items()},
        "components_share_percent": {k: round(v, 1) for k, v in cost_share_percent.items()},
        "cost_breakdown_detailed": {
            "product_fob": round(product_cost, 2),
            "packing_outer": round(packing_cost, 2),
            "packing_inner": round(inner_carton_cost, 2),
            "sea_freight": round(sea_freight, 2),
            "origin_charges": round(origin_charges, 2),
            "destination_charges": round(destination_charges, 2),
            "customs_broker": round(docs_and_broker, 2),
            "port_misc": round(port_misc, 2),
            "qc_inspection": round(qc_cost, 2),
            "certification": round(cert_cost, 2),
            "import_duty": round(duty, 2),
            "extra_taxes": round(extra_taxes, 2),
        },
        "assumptions": {
            "category": cfg["label"],
            "category_id": order.category_id,
            "route": order.route,
            "incoterm": order.incoterm,
            "unit_weight_kg": unit_weight,
            "duty_rate_percent": cfg["duty_rate_percent"],
            "hs_code_hint": cfg.get("hs_code_hint", "N/A"),
        },
        "benchmarks": {
            "moq_units": cfg.get("moq_units", 1000),
            "typical_lead_time_days": cfg.get("typical_lead_time_days", 25),
            "margin_low": cfg.get("margin_benchmarks", {}).get("low", 0.15),
            "margin_typical": cfg.get("margin_benchmarks", {}).get("typical", 0.30),
            "margin_high": cfg.get("margin_benchmarks", {}).get("high", 0.50),
        }
    }
    
    # ===========================================
    # MARGIN ESTIMATE (if retail price provided)
    # ===========================================
    if order.retail_price_per_unit is not None and order.retail_price_per_unit > 0:
        margin = order.retail_price_per_unit - cost_per_unit
        margin_pct = (margin / order.retail_price_per_unit) * 100.0
        
        # Compare to benchmarks
        margin_benchmarks = cfg.get("margin_benchmarks", {})
        if margin_pct < margin_benchmarks.get("low", 0.15) * 100:
            margin_assessment = "Below typical - consider negotiating costs"
        elif margin_pct > margin_benchmarks.get("high", 0.50) * 100:
            margin_assessment = "Strong margin - good opportunity"
        else:
            margin_assessment = "Within typical range for this category"
        
        result["margin_estimate"] = {
            "retail_price_per_unit_usd": round(order.retail_price_per_unit, 2),
            "gross_margin_per_unit_usd": round(margin, 4),
            "gross_margin_percent": round(margin_pct, 1),
            "assessment": margin_assessment,
        }
    
    return result


def compute_sensitivity(order: OrderParams, base_result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute sensitivity scenarios: what if costs change?
    
    Returns scenarios showing impact of:
    - Shipping cost +20%
    - Duty rate -5 points
    - Product cost +10%
    """
    cfg = get_category_config(order.category_id)
    base_cost = base_result["landed_cost_per_unit_usd"]
    base_margin = base_result.get("margin_estimate", {}).get("gross_margin_percent", 30)
    
    scenarios = []
    
    # Scenario 1: Shipping +20%
    shipping_share = base_result["components_share_percent"].get("shipping", 15)
    shipping_impact_pct = shipping_share * 0.20  # 20% of shipping component
    new_margin_shipping = base_margin - shipping_impact_pct
    scenarios.append({
        "name": "Shipping cost +20%",
        "trigger": "Peak season, port congestion, fuel surcharge",
        "margin_impact": f"-{shipping_impact_pct:.1f}%",
        "new_margin": f"{new_margin_shipping:.1f}%",
        "recommendation": "Consider off-peak shipping or larger batch sizes"
    })
    
    # Scenario 2: Duty reduced by 5 points
    duty_reduction = 5
    duty_impact_pct = (cfg["duty_rate_percent"] - duty_reduction) / cfg["duty_rate_percent"] * base_result["components_share_percent"].get("duty_and_tax", 10) if cfg["duty_rate_percent"] > 0 else 0
    new_margin_duty = base_margin + min(duty_impact_pct, 3)  # Cap at 3% improvement
    scenarios.append({
        "name": "Duty reduced by 5 points",
        "trigger": "Trade agreement, tariff negotiation",
        "margin_impact": f"+{min(duty_impact_pct, 3):.1f}%",
        "new_margin": f"{new_margin_duty:.1f}%",
        "recommendation": "Monitor trade policy changes"
    })
    
    # Scenario 3: Product cost +10%
    product_share = base_result["components_share_percent"].get("product", 50)
    product_impact_pct = product_share * 0.10
    new_margin_product = base_margin - product_impact_pct
    scenarios.append({
        "name": "Product cost +10%",
        "trigger": "Raw material price increase, supplier renegotiation",
        "margin_impact": f"-{product_impact_pct:.1f}%",
        "new_margin": f"{new_margin_product:.1f}%",
        "recommendation": "Lock in pricing with longer contracts"
    })
    
    return {
        "base_margin": f"{base_margin:.1f}%",
        "scenarios": scenarios
    }


def compute_from_query(
    query: str,
    units: int = 5000,
    route: str = "cn_to_us_west_coast",
    retail_price: Optional[float] = None
) -> Dict[str, Any]:
    """
    Convenience function: classify category from query and compute costs.
    
    Args:
        query: User's product description
        units: Order quantity
        route: Shipping route
        retail_price: Expected retail price (for margin calculation)
    
    Returns:
        Complete landed cost analysis
    """
    category_id = classify_category(query)
    
    order = OrderParams(
        category_id=category_id,
        units=units,
        route=route,
        retail_price_per_unit=retail_price
    )
    
    result = compute_landed_cost(order)
    result["sensitivity"] = compute_sensitivity(order, result)
    result["query_parsed"] = {
        "original_query": query,
        "detected_category": category_id,
        "category_label": result["assumptions"]["category"]
    }
    
    return result


# =============================================================================
# FORMAT HELPERS FOR UI
# =============================================================================

def format_for_pie_chart(result: Dict[str, Any]) -> list:
    """Format cost components for Plotly pie chart."""
    components = result.get("components_usd", {})
    labels_map = {
        "product": "Manufacturing",
        "packing": "Packing",
        "shipping": "Freight & Logistics",
        "handling": "Handling & QC",
        "duty_and_tax": "Duty & Taxes"
    }
    
    return [
        {
            "label": labels_map.get(k, k),
            "value": v,
            "percent": result["components_share_percent"].get(k, 0)
        }
        for k, v in components.items()
    ]


def format_for_cost_table(result: Dict[str, Any]) -> list:
    """Format detailed breakdown for table display."""
    detailed = result.get("cost_breakdown_detailed", {})
    labels_map = {
        "product_fob": ("Product (FOB)", "Manufacturing cost at factory"),
        "packing_outer": ("Outer Carton", "Export packing"),
        "packing_inner": ("Inner Packing", "Unit packaging"),
        "sea_freight": ("Sea Freight", "Ocean shipping"),
        "origin_charges": ("Origin Charges", "China port handling"),
        "destination_charges": ("Destination Charges", "US port handling"),
        "customs_broker": ("Customs Broker", "Documentation and clearance"),
        "port_misc": ("Port Miscellaneous", "Terminal handling"),
        "qc_inspection": ("QC Inspection", "Pre-shipment inspection"),
        "certification": ("Certification", "Product testing and compliance"),
        "import_duty": ("Import Duty", "Customs duty"),
        "extra_taxes": ("Additional Taxes", "Other applicable taxes"),
    }
    
    rows = []
    for key, value in detailed.items():
        if value > 0:
            label, desc = labels_map.get(key, (key, ""))
            rows.append({
                "item": label,
                "description": desc,
                "amount": value
            })
    
    return rows

