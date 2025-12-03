"""
NexSupply Cost Tables - Rule-based pricing data
These tables provide realistic baseline values for landed cost calculations.
LLM handles category classification; Python handles the math.

Structure:
- Category ID → Base costs, weights, freight profiles
- Route → Sea freight, origin/destination charges
- Handling → Fixed per-shipment costs

Accuracy target: ±20-25% (vs pure LLM estimates at ±30-50%)

Data Sources (verified Nov 2025):
- Grand View Research - Procurement Software Market
- ISM Survey 2024 - Lead Time Data
- Eyton Lighting 2025 - China Sourcing Cost Breakdown
- Veridion 2025 - Supplier Onboarding Costs
"""

from typing import Dict, Any

# =============================================================================
# COST TABLES BY CATEGORY
# =============================================================================

COST_TABLES: Dict[str, Dict[str, Any]] = {
    
    # -------------------------------------------------------------------------
    # CANDY: Marshmallow on stick (lollipop style)
    # -------------------------------------------------------------------------
    "candy_marshmallow_stick": {
        "label": "Marshmallow on stick / Lollipop",
        "hs_code_hint": "1704.90",
        "default_unit_weight_kg": 0.02,      # 20g per unit
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 20,       # ~2000 units per CBM
        "base_fob_cost_per_kg": 2.1,         # USD/kg FOB China
        "packing_cost_per_carton_usd": 0.35,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 120,
        "cert_cost_per_sku_usd": 600,        # FDA registration, lab tests
        "duty_rate_percent": 10,             # US candy tariff
        "extra_taxes_percent": 0,
        "moq_units": 5000,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 180,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.20,
            "typical": 0.30,
            "high": 0.45
        }
    },
    
    # -------------------------------------------------------------------------
    # CANDY: Gummy / Peelable candy pouch
    # -------------------------------------------------------------------------
    "candy_gummy_peelable": {
        "label": "Peelable gummy / Gummy candy pouch",
        "hs_code_hint": "1704.10",
        "default_unit_weight_kg": 0.015,     # 15g per unit
        "default_units_per_carton": 120,
        "default_cartons_per_cbm": 25,       # ~3000 units per CBM
        "base_fob_cost_per_kg": 3.2,         # Higher due to gelatin
        "packing_cost_per_carton_usd": 0.28,
        "inner_carton_cost_usd": 0.12,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 750,
        "duty_rate_percent": 12,
        "extra_taxes_percent": 0,
        "moq_units": 10000,
        "typical_lead_time_days": 30,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 130,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 100,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 190,
            "port_misc_per_shipment_usd": 130
        },
        "margin_benchmarks": {
            "low": 0.18,
            "typical": 0.28,
            "high": 0.40
        }
    },
    
    # -------------------------------------------------------------------------
    # NOVELTY TOY: Small plastic keychain/toy
    # -------------------------------------------------------------------------
    "novelty_toy_small_plastic": {
        "label": "Small plastic novelty toy / Keychain",
        "hs_code_hint": "9503.00",
        "default_unit_weight_kg": 0.03,      # 30g per unit
        "default_units_per_carton": 200,
        "default_cartons_per_cbm": 30,       # ~6000 units per CBM
        "base_fob_cost_per_kg": 4.5,
        "packing_cost_per_carton_usd": 0.40,
        "inner_carton_cost_usd": 0.18,
        "qc_cost_per_order_usd": 200,
        "cert_cost_per_sku_usd": 1200,       # CPSIA, toy safety tests
        "duty_rate_percent": 5,              # Toy tariff (varies)
        "extra_taxes_percent": 0,
        "moq_units": 3000,
        "typical_lead_time_days": 20,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 125,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 65
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 200,
            "port_misc_per_shipment_usd": 140
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # ELECTRONICS: Small accessory (charger, cable, adapter)
    # -------------------------------------------------------------------------
    "electronics_small_accessory": {
        "label": "Small electronics accessory",
        "hs_code_hint": "8504.40",
        "default_unit_weight_kg": 0.05,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 40,
        "base_fob_cost_per_kg": 8.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 250,
        "cert_cost_per_sku_usd": 1500,       # FCC, CE, UL
        "duty_rate_percent": 0,              # Many electronics duty-free
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 15,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 220,
            "port_misc_per_shipment_usd": 150
        },
        "margin_benchmarks": {
            "low": 0.20,
            "typical": 0.35,
            "high": 0.50
        }
    },
    
    # -------------------------------------------------------------------------
    # APPAREL: T-shirts, basic garments
    # -------------------------------------------------------------------------
    "apparel_tshirt_basic": {
        "label": "Basic T-shirt / Garment",
        "hs_code_hint": "6109.10",
        "default_unit_weight_kg": 0.18,      # 180g per shirt
        "default_units_per_carton": 50,
        "default_cartons_per_cbm": 25,       # ~1250 units per CBM
        "base_fob_cost_per_kg": 8.5,         # Cotton blend
        "packing_cost_per_carton_usd": 0.60,
        "inner_carton_cost_usd": 0.25,
        "qc_cost_per_order_usd": 300,
        "cert_cost_per_sku_usd": 400,        # OEKO-TEX, basic compliance
        "duty_rate_percent": 16.5,           # US apparel tariff (varies)
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 35,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 180,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # APPAREL: Hats / Caps
    # -------------------------------------------------------------------------
    "apparel_hat_cap": {
        "label": "Hat / Cap / Headwear",
        "hs_code_hint": "6505.00",
        "default_unit_weight_kg": 0.08,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 20,
        "base_fob_cost_per_kg": 12.0,
        "packing_cost_per_carton_usd": 0.40,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 300,
        "duty_rate_percent": 7.5,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 170,
            "port_misc_per_shipment_usd": 110
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # BAGS: Tote bags, backpacks
    # -------------------------------------------------------------------------
    "bags_tote_backpack": {
        "label": "Tote bag / Backpack",
        "hs_code_hint": "4202.92",
        "default_unit_weight_kg": 0.35,
        "default_units_per_carton": 30,
        "default_cartons_per_cbm": 15,
        "base_fob_cost_per_kg": 7.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 200,
        "cert_cost_per_sku_usd": 350,
        "duty_rate_percent": 17.6,           # US bag tariff
        "extra_taxes_percent": 0,
        "moq_units": 300,
        "typical_lead_time_days": 30,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 125,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 100,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 190,
            "port_misc_per_shipment_usd": 125
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # HOME & KITCHEN: Food containers, storage
    # -------------------------------------------------------------------------
    "home_food_container": {
        "label": "Food container / Storage",
        "hs_code_hint": "3924.10",
        "default_unit_weight_kg": 0.15,
        "default_units_per_carton": 48,
        "default_cartons_per_cbm": 20,
        "base_fob_cost_per_kg": 4.5,
        "packing_cost_per_carton_usd": 0.35,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 800,        # FDA food contact
        "duty_rate_percent": 3.4,
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 20,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 180,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # HOME & KITCHEN: Utensils, tools
    # -------------------------------------------------------------------------
    "home_kitchen_utensil": {
        "label": "Kitchen utensil / Tool",
        "hs_code_hint": "8215.99",
        "default_unit_weight_kg": 0.08,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 30,
        "base_fob_cost_per_kg": 6.0,
        "packing_cost_per_carton_usd": 0.30,
        "inner_carton_cost_usd": 0.12,
        "qc_cost_per_order_usd": 120,
        "cert_cost_per_sku_usd": 500,
        "duty_rate_percent": 0,              # Many kitchen tools duty-free
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 18,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 170,
            "port_misc_per_shipment_usd": 115
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.45,
            "high": 0.65
        }
    },
    
    # -------------------------------------------------------------------------
    # BEAUTY: Cosmetic bottles, packaging
    # -------------------------------------------------------------------------
    "beauty_cosmetic_packaging": {
        "label": "Cosmetic bottle / Packaging",
        "hs_code_hint": "3923.30",
        "default_unit_weight_kg": 0.05,
        "default_units_per_carton": 200,
        "default_cartons_per_cbm": 40,
        "base_fob_cost_per_kg": 10.0,
        "packing_cost_per_carton_usd": 0.40,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 180,
        "cert_cost_per_sku_usd": 1200,       # FDA, stability testing
        "duty_rate_percent": 3.0,
        "extra_taxes_percent": 0,
        "moq_units": 5000,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 200,
            "port_misc_per_shipment_usd": 130
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # PET: Pet toys, accessories
    # -------------------------------------------------------------------------
    "pet_toy_accessory": {
        "label": "Pet toy / Accessory",
        "hs_code_hint": "4201.00",
        "default_unit_weight_kg": 0.12,
        "default_units_per_carton": 60,
        "default_cartons_per_cbm": 25,
        "base_fob_cost_per_kg": 5.5,
        "packing_cost_per_carton_usd": 0.35,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 600,        # Pet safety testing
        "duty_rate_percent": 2.4,
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 22,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 175,
            "port_misc_per_shipment_usd": 115
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # OUTDOOR: Camping gear, outdoor accessories
    # -------------------------------------------------------------------------
    "outdoor_camping_gear": {
        "label": "Camping gear / Outdoor accessory",
        "hs_code_hint": "6306.22",
        "default_unit_weight_kg": 0.50,
        "default_units_per_carton": 20,
        "default_cartons_per_cbm": 12,
        "base_fob_cost_per_kg": 6.5,
        "packing_cost_per_carton_usd": 0.55,
        "inner_carton_cost_usd": 0.22,
        "qc_cost_per_order_usd": 250,
        "cert_cost_per_sku_usd": 900,        # Fire retardant, safety
        "duty_rate_percent": 8.5,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 30,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 130,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 105,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 210,
            "port_misc_per_shipment_usd": 140
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.45,
            "high": 0.65
        }
    },
    
    # -------------------------------------------------------------------------
    # SPORTS: Fitness equipment, small gear
    # -------------------------------------------------------------------------
    "sports_fitness_equipment": {
        "label": "Fitness equipment / Sports gear",
        "hs_code_hint": "9506.91",
        "default_unit_weight_kg": 0.80,
        "default_units_per_carton": 12,
        "default_cartons_per_cbm": 10,
        "base_fob_cost_per_kg": 4.0,
        "packing_cost_per_carton_usd": 0.60,
        "inner_carton_cost_usd": 0.25,
        "qc_cost_per_order_usd": 200,
        "cert_cost_per_sku_usd": 700,
        "duty_rate_percent": 4.0,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 28,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 135,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 220,
            "port_misc_per_shipment_usd": 145
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # OFFICE: Stationery, office supplies
    # -------------------------------------------------------------------------
    "office_stationery": {
        "label": "Stationery / Office supplies",
        "hs_code_hint": "4820.10",
        "default_unit_weight_kg": 0.06,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 35,
        "base_fob_cost_per_kg": 7.0,
        "packing_cost_per_carton_usd": 0.30,
        "inner_carton_cost_usd": 0.12,
        "qc_cost_per_order_usd": 100,
        "cert_cost_per_sku_usd": 200,
        "duty_rate_percent": 0,              # Most stationery duty-free
        "extra_taxes_percent": 0,
        "moq_units": 2000,
        "typical_lead_time_days": 18,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 160,
            "port_misc_per_shipment_usd": 100
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # AUTOMOTIVE: Car accessories, small parts
    # -------------------------------------------------------------------------
    "automotive_accessory": {
        "label": "Car accessory / Auto parts",
        "hs_code_hint": "8708.99",
        "default_unit_weight_kg": 0.25,
        "default_units_per_carton": 40,
        "default_cartons_per_cbm": 18,
        "base_fob_cost_per_kg": 5.5,
        "packing_cost_per_carton_usd": 0.45,
        "inner_carton_cost_usd": 0.18,
        "qc_cost_per_order_usd": 250,
        "cert_cost_per_sku_usd": 1500,       # FMVSS compliance varies
        "duty_rate_percent": 2.5,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 125,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 100,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 200,
            "port_misc_per_shipment_usd": 130
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # HOME DECOR: Decorative items, wall art
    # -------------------------------------------------------------------------
    "home_decor_decorative": {
        "label": "Home decor / Decorative item",
        "hs_code_hint": "8306.29",
        "default_unit_weight_kg": 0.30,
        "default_units_per_carton": 30,
        "default_cartons_per_cbm": 15,
        "base_fob_cost_per_kg": 6.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 300,
        "duty_rate_percent": 3.7,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 22,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 185,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # LED LIGHTING: LED products, light fixtures
    # -------------------------------------------------------------------------
    "lighting_led_fixture": {
        "label": "LED light / Light fixture",
        "hs_code_hint": "9405.42",
        "default_unit_weight_kg": 0.20,
        "default_units_per_carton": 40,
        "default_cartons_per_cbm": 22,
        "base_fob_cost_per_kg": 9.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 220,
        "cert_cost_per_sku_usd": 1800,       # UL, ETL, DLC certification
        "duty_rate_percent": 3.9,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 20,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 210,
            "port_misc_per_shipment_usd": 140
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # PACKAGING: Boxes, mailers, packaging materials
    # -------------------------------------------------------------------------
    "packaging_boxes_mailers": {
        "label": "Packaging / Boxes / Mailers",
        "hs_code_hint": "4819.10",
        "default_unit_weight_kg": 0.04,
        "default_units_per_carton": 250,
        "default_cartons_per_cbm": 50,
        "base_fob_cost_per_kg": 3.0,
        "packing_cost_per_carton_usd": 0.25,
        "inner_carton_cost_usd": 0.10,
        "qc_cost_per_order_usd": 80,
        "cert_cost_per_sku_usd": 150,
        "duty_rate_percent": 0,              # Paper products often duty-free
        "extra_taxes_percent": 0,
        "moq_units": 5000,
        "typical_lead_time_days": 15,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 65,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 105,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 150,
            "port_misc_per_shipment_usd": 95
        },
        "margin_benchmarks": {
            "low": 0.15,
            "typical": 0.30,
            "high": 0.50
        }
    },
    
    # -------------------------------------------------------------------------
    # JEWELRY: Fashion jewelry, accessories
    # -------------------------------------------------------------------------
    "jewelry_fashion_accessory": {
        "label": "Fashion jewelry / Accessory",
        "hs_code_hint": "7117.19",
        "default_unit_weight_kg": 0.025,
        "default_units_per_carton": 200,
        "default_cartons_per_cbm": 60,
        "base_fob_cost_per_kg": 25.0,
        "packing_cost_per_carton_usd": 0.45,
        "inner_carton_cost_usd": 0.18,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 800,        # Lead/nickel testing
        "duty_rate_percent": 5.5,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 20,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 180,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.45,
            "typical": 0.65,
            "high": 0.85
        }
    },
    
    # -------------------------------------------------------------------------
    # FOOTWEAR: Shoes, sandals, slippers
    # -------------------------------------------------------------------------
    "footwear_shoes_sandals": {
        "label": "Shoes / Sandals / Footwear",
        "hs_code_hint": "6404.19",
        "default_unit_weight_kg": 0.45,
        "default_units_per_carton": 20,
        "default_cartons_per_cbm": 12,
        "base_fob_cost_per_kg": 12.0,
        "packing_cost_per_carton_usd": 0.65,
        "inner_carton_cost_usd": 0.25,
        "qc_cost_per_order_usd": 280,
        "cert_cost_per_sku_usd": 600,
        "duty_rate_percent": 20.0,           # US footwear tariff high
        "extra_taxes_percent": 0,
        "moq_units": 300,
        "typical_lead_time_days": 35,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 130,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 105,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 200,
            "port_misc_per_shipment_usd": 135
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # SUNGLASSES: Eyewear, sunglasses
    # -------------------------------------------------------------------------
    "eyewear_sunglasses": {
        "label": "Sunglasses / Eyewear",
        "hs_code_hint": "9004.10",
        "default_unit_weight_kg": 0.035,
        "default_units_per_carton": 150,
        "default_cartons_per_cbm": 45,
        "base_fob_cost_per_kg": 35.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 180,
        "cert_cost_per_sku_usd": 1000,       # UV protection testing
        "duty_rate_percent": 2.0,
        "extra_taxes_percent": 0,
        "moq_units": 300,
        "typical_lead_time_days": 22,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 175,
            "port_misc_per_shipment_usd": 115
        },
        "margin_benchmarks": {
            "low": 0.50,
            "typical": 0.70,
            "high": 0.85
        }
    },
    
    # -------------------------------------------------------------------------
    # WATCHES: Fashion watches
    # -------------------------------------------------------------------------
    "watches_fashion": {
        "label": "Fashion watch / Wristwatch",
        "hs_code_hint": "9102.12",
        "default_unit_weight_kg": 0.08,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 50,
        "base_fob_cost_per_kg": 50.0,
        "packing_cost_per_carton_usd": 0.60,
        "inner_carton_cost_usd": 0.25,
        "qc_cost_per_order_usd": 200,
        "cert_cost_per_sku_usd": 800,
        "duty_rate_percent": 6.4,
        "extra_taxes_percent": 0,
        "moq_units": 200,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 185,
            "port_misc_per_shipment_usd": 125
        },
        "margin_benchmarks": {
            "low": 0.45,
            "typical": 0.65,
            "high": 0.85
        }
    },
    
    # -------------------------------------------------------------------------
    # BABY: Baby products, infant items
    # -------------------------------------------------------------------------
    "baby_infant_products": {
        "label": "Baby product / Infant item",
        "hs_code_hint": "9503.00",
        "default_unit_weight_kg": 0.15,
        "default_units_per_carton": 50,
        "default_cartons_per_cbm": 20,
        "base_fob_cost_per_kg": 8.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 300,
        "cert_cost_per_sku_usd": 2000,       # CPSIA, EN71, phthalate testing
        "duty_rate_percent": 0,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 28,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 220,
            "port_misc_per_shipment_usd": 145
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # TOOLS: Hand tools, hardware
    # -------------------------------------------------------------------------
    "tools_hand_hardware": {
        "label": "Hand tools / Hardware",
        "hs_code_hint": "8205.59",
        "default_unit_weight_kg": 0.30,
        "default_units_per_carton": 30,
        "default_cartons_per_cbm": 18,
        "base_fob_cost_per_kg": 4.5,
        "packing_cost_per_carton_usd": 0.45,
        "inner_carton_cost_usd": 0.18,
        "qc_cost_per_order_usd": 180,
        "cert_cost_per_sku_usd": 500,
        "duty_rate_percent": 0,              # Many hand tools duty-free
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 22,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 135,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 190,
            "port_misc_per_shipment_usd": 125
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # MEDICAL: Health supplies, first aid
    # -------------------------------------------------------------------------
    "medical_health_supplies": {
        "label": "Health supplies / Medical",
        "hs_code_hint": "9018.90",
        "default_unit_weight_kg": 0.05,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 40,
        "base_fob_cost_per_kg": 15.0,
        "packing_cost_per_carton_usd": 0.55,
        "inner_carton_cost_usd": 0.22,
        "qc_cost_per_order_usd": 350,
        "cert_cost_per_sku_usd": 3000,       # FDA 510(k), ISO 13485
        "duty_rate_percent": 0,              # Most medical duty-free
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 30,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 250,
            "port_misc_per_shipment_usd": 160
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # SEASONAL: Holiday, seasonal items
    # -------------------------------------------------------------------------
    "seasonal_holiday_items": {
        "label": "Holiday / Seasonal items",
        "hs_code_hint": "9505.10",
        "default_unit_weight_kg": 0.12,
        "default_units_per_carton": 60,
        "default_cartons_per_cbm": 25,
        "base_fob_cost_per_kg": 5.0,
        "packing_cost_per_carton_usd": 0.40,
        "inner_carton_cost_usd": 0.15,
        "qc_cost_per_order_usd": 150,
        "cert_cost_per_sku_usd": 400,
        "duty_rate_percent": 0,              # Festive articles often duty-free
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 175,
            "port_misc_per_shipment_usd": 115
        },
        "margin_benchmarks": {
            "low": 0.40,
            "typical": 0.60,
            "high": 0.80
        }
    },
    
    # -------------------------------------------------------------------------
    # PROMOTIONAL: Promo products, giveaways
    # -------------------------------------------------------------------------
    "promotional_products": {
        "label": "Promotional product / Giveaway",
        "hs_code_hint": "3926.90",
        "default_unit_weight_kg": 0.05,
        "default_units_per_carton": 200,
        "default_cartons_per_cbm": 40,
        "base_fob_cost_per_kg": 6.0,
        "packing_cost_per_carton_usd": 0.30,
        "inner_carton_cost_usd": 0.12,
        "qc_cost_per_order_usd": 100,
        "cert_cost_per_sku_usd": 250,
        "duty_rate_percent": 5.3,
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 18,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 160,
            "port_misc_per_shipment_usd": 105
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # GARDEN: Garden tools, lawn products
    # -------------------------------------------------------------------------
    "garden_lawn_products": {
        "label": "Garden / Lawn product",
        "hs_code_hint": "8201.90",
        "default_unit_weight_kg": 0.40,
        "default_units_per_carton": 24,
        "default_cartons_per_cbm": 14,
        "base_fob_cost_per_kg": 4.0,
        "packing_cost_per_carton_usd": 0.50,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 180,
        "cert_cost_per_sku_usd": 400,
        "duty_rate_percent": 0,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 130,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 105,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 195,
            "port_misc_per_shipment_usd": 130
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # CRAFT: Craft supplies, DIY materials
    # -------------------------------------------------------------------------
    "craft_diy_supplies": {
        "label": "Craft supplies / DIY materials",
        "hs_code_hint": "3926.90",
        "default_unit_weight_kg": 0.08,
        "default_units_per_carton": 100,
        "default_cartons_per_cbm": 35,
        "base_fob_cost_per_kg": 7.0,
        "packing_cost_per_carton_usd": 0.35,
        "inner_carton_cost_usd": 0.14,
        "qc_cost_per_order_usd": 120,
        "cert_cost_per_sku_usd": 350,
        "duty_rate_percent": 5.3,
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 20,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 75,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 90,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 170,
            "port_misc_per_shipment_usd": 110
        },
        "margin_benchmarks": {
            "low": 0.35,
            "typical": 0.55,
            "high": 0.75
        }
    },
    
    # -------------------------------------------------------------------------
    # PHONE CASES: Phone cases, screen protectors
    # -------------------------------------------------------------------------
    "phone_case_protector": {
        "label": "Phone case / Screen protector",
        "hs_code_hint": "3926.90",
        "default_unit_weight_kg": 0.03,
        "default_units_per_carton": 200,
        "default_cartons_per_cbm": 55,
        "base_fob_cost_per_kg": 12.0,
        "packing_cost_per_carton_usd": 0.35,
        "inner_carton_cost_usd": 0.14,
        "qc_cost_per_order_usd": 100,
        "cert_cost_per_sku_usd": 200,
        "duty_rate_percent": 5.3,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 15,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 70,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 110,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 155,
            "port_misc_per_shipment_usd": 100
        },
        "margin_benchmarks": {
            "low": 0.50,
            "typical": 0.70,
            "high": 0.85
        }
    },
    
    # -------------------------------------------------------------------------
    # TEXTILES: Fabrics, towels, blankets
    # -------------------------------------------------------------------------
    "textiles_fabrics_towels": {
        "label": "Textiles / Towels / Blankets",
        "hs_code_hint": "6302.60",
        "default_unit_weight_kg": 0.25,
        "default_units_per_carton": 40,
        "default_cartons_per_cbm": 18,
        "base_fob_cost_per_kg": 5.5,
        "packing_cost_per_carton_usd": 0.45,
        "inner_carton_cost_usd": 0.18,
        "qc_cost_per_order_usd": 180,
        "cert_cost_per_sku_usd": 450,        # OEKO-TEX
        "duty_rate_percent": 9.3,
        "extra_taxes_percent": 0,
        "moq_units": 500,
        "typical_lead_time_days": 28,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 80,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 120,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 185,
            "port_misc_per_shipment_usd": 120
        },
        "margin_benchmarks": {
            "low": 0.30,
            "typical": 0.50,
            "high": 0.70
        }
    },
    
    # -------------------------------------------------------------------------
    # FURNITURE: Small furniture, storage
    # -------------------------------------------------------------------------
    "furniture_small_storage": {
        "label": "Small furniture / Storage",
        "hs_code_hint": "9403.70",
        "default_unit_weight_kg": 2.5,
        "default_units_per_carton": 4,
        "default_cartons_per_cbm": 5,
        "base_fob_cost_per_kg": 3.0,
        "packing_cost_per_carton_usd": 1.20,
        "inner_carton_cost_usd": 0.50,
        "qc_cost_per_order_usd": 300,
        "cert_cost_per_sku_usd": 800,        # CARB, formaldehyde testing
        "duty_rate_percent": 0,
        "extra_taxes_percent": 0,
        "moq_units": 100,
        "typical_lead_time_days": 35,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 100,
                "origin_charges_per_cbm_usd": 30,
                "destination_charges_per_cbm_usd": 50
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 145,
                "origin_charges_per_cbm_usd": 30,
                "destination_charges_per_cbm_usd": 60
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 115,
                "origin_charges_per_cbm_usd": 30,
                "destination_charges_per_cbm_usd": 70
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 250,
            "port_misc_per_shipment_usd": 180
        },
        "margin_benchmarks": {
            "low": 0.25,
            "typical": 0.40,
            "high": 0.60
        }
    },
    
    # -------------------------------------------------------------------------
    # FOOD/BEVERAGE: Snacks, beverages (non-candy)
    # -------------------------------------------------------------------------
    "food_beverage_snacks": {
        "label": "Food / Beverage / Snacks",
        "hs_code_hint": "1905.90",
        "default_unit_weight_kg": 0.10,
        "default_units_per_carton": 60,
        "default_cartons_per_cbm": 22,
        "base_fob_cost_per_kg": 3.5,
        "packing_cost_per_carton_usd": 0.40,
        "inner_carton_cost_usd": 0.16,
        "qc_cost_per_order_usd": 250,
        "cert_cost_per_sku_usd": 1500,       # FDA, lab testing, FSMA
        "duty_rate_percent": 8,
        "extra_taxes_percent": 0,
        "moq_units": 2000,
        "typical_lead_time_days": 30,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 50
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 125,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 100,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 65
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 220,
            "port_misc_per_shipment_usd": 150
        },
        "margin_benchmarks": {
            "low": 0.20,
            "typical": 0.35,
            "high": 0.55
        }
    },
    
    # -------------------------------------------------------------------------
    # GENERIC: Fallback for uncategorized products
    # -------------------------------------------------------------------------
    "generic_consumer_product": {
        "label": "Generic consumer product",
        "hs_code_hint": "N/A",
        "default_unit_weight_kg": 0.10,
        "default_units_per_carton": 50,
        "default_cartons_per_cbm": 15,
        "base_fob_cost_per_kg": 5.0,
        "packing_cost_per_carton_usd": 0.45,
        "inner_carton_cost_usd": 0.20,
        "qc_cost_per_order_usd": 200,
        "cert_cost_per_sku_usd": 800,
        "duty_rate_percent": 8,
        "extra_taxes_percent": 0,
        "moq_units": 1000,
        "typical_lead_time_days": 25,
        "freight_profile": {
            "cn_to_us_west_coast": {
                "sea_freight_per_cbm_usd": 85,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 45
            },
            "cn_to_us_east_coast": {
                "sea_freight_per_cbm_usd": 125,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 55
            },
            "cn_to_eu": {
                "sea_freight_per_cbm_usd": 95,
                "origin_charges_per_cbm_usd": 25,
                "destination_charges_per_cbm_usd": 60
            }
        },
        "handling_profile": {
            "docs_and_broker_per_shipment_usd": 200,
            "port_misc_per_shipment_usd": 130
        },
        "margin_benchmarks": {
            "low": 0.15,
            "typical": 0.30,
            "high": 0.50
        }
    }
}


# =============================================================================
# CATEGORY KEYWORDS FOR CLASSIFICATION
# =============================================================================

CATEGORY_KEYWORDS: Dict[str, list] = {
    # Candy
    "candy_marshmallow_stick": [
        "marshmallow", "lollipop", "sucker", "candy stick", "pop", 
        "hard candy", "棒棒糖", "롤리팝", "사탕"
    ],
    "candy_gummy_peelable": [
        "gummy", "gummi", "jelly", "peelable", "chewy", "gelatin candy",
        "fruit snack", "젤리", "구미", "软糖"
    ],
    
    # Toys
    "novelty_toy_small_plastic": [
        "keychain", "toy", "figurine", "collectible", "novelty", 
        "plastic toy", "miniature", "키링", "玩具", "小饰品", "finger board",
        "fingerboard", "fidget", "spinner"
    ],
    
    # Electronics
    "electronics_small_accessory": [
        "charger", "cable", "adapter", "usb", "power bank", "earbuds",
        "electronic", "充电器", "数据线", "충전기", "bluetooth", "wireless",
        "phone case", "screen protector", "headphone"
    ],
    
    # Apparel
    "apparel_tshirt_basic": [
        "t-shirt", "tshirt", "shirt", "top", "garment", "clothing",
        "apparel", "cotton", "polo", "tank top", "티셔츠", "衬衫"
    ],
    "apparel_hat_cap": [
        "hat", "cap", "beanie", "headwear", "snapback", "baseball cap",
        "visor", "bucket hat", "모자", "帽子"
    ],
    
    # Bags
    "bags_tote_backpack": [
        "bag", "tote", "backpack", "handbag", "purse", "pouch", "duffel",
        "messenger bag", "shoulder bag", "가방", "包"
    ],
    
    # Home & Kitchen
    "home_food_container": [
        "container", "food storage", "lunch box", "tupperware", "meal prep",
        "storage container", "food container", "용기", "容器"
    ],
    "home_kitchen_utensil": [
        "utensil", "spatula", "spoon", "fork", "knife", "cooking tool",
        "kitchen tool", "kitchenware", "whisk", "ladle", "주방용품", "厨具"
    ],
    
    # Beauty
    "beauty_cosmetic_packaging": [
        "cosmetic", "beauty", "skincare", "bottle", "jar", "pump",
        "dropper", "lipstick", "mascara", "makeup", "화장품", "美容"
    ],
    
    # Pet
    "pet_toy_accessory": [
        "pet", "dog", "cat", "pet toy", "leash", "collar", "pet bed",
        "pet bowl", "pet accessory", "애완동물", "宠物"
    ],
    
    # Outdoor
    "outdoor_camping_gear": [
        "camping", "outdoor", "tent", "sleeping bag", "hiking",
        "camping gear", "backpacking", "hammock", "캠핑", "户外"
    ],
    
    # Sports
    "sports_fitness_equipment": [
        "fitness", "gym", "exercise", "yoga", "dumbbell", "resistance band",
        "workout", "sports", "weight", "운동", "健身"
    ],
    
    # Office
    "office_stationery": [
        "stationery", "pen", "notebook", "planner", "desk", "office",
        "paper", "folder", "binder", "문구", "文具"
    ],
    
    # Automotive
    "automotive_accessory": [
        "car", "auto", "vehicle", "car accessory", "phone mount",
        "car charger", "seat cover", "floor mat", "자동차", "汽车"
    ],
    
    # Home Decor
    "home_decor_decorative": [
        "decor", "decoration", "wall art", "vase", "candle", "frame",
        "mirror", "sculpture", "plant pot", "인테리어", "装饰"
    ],
    
    # LED Lighting
    "lighting_led_fixture": [
        "led", "light", "lamp", "bulb", "lighting", "fixture",
        "desk lamp", "string light", "spotlight", "조명", "灯"
    ],
    
    # Packaging
    "packaging_boxes_mailers": [
        "packaging", "box", "mailer", "carton", "shipping box",
        "gift box", "bubble mailer", "envelope", "포장", "包装"
    ],
    
    # Jewelry
    "jewelry_fashion_accessory": [
        "jewelry", "jewellery", "necklace", "bracelet", "earring", "ring",
        "pendant", "chain", "accessory", "fashion jewelry", "주얼리", "首饰"
    ],
    
    # Footwear
    "footwear_shoes_sandals": [
        "shoe", "shoes", "sandal", "slipper", "sneaker", "boot", "footwear",
        "flip flop", "loafer", "신발", "鞋"
    ],
    
    # Sunglasses/Eyewear
    "eyewear_sunglasses": [
        "sunglasses", "eyewear", "glasses", "shades", "spectacles",
        "reading glasses", "blue light", "선글라스", "眼镜"
    ],
    
    # Watches
    "watches_fashion": [
        "watch", "wristwatch", "smartwatch", "timepiece", "clock",
        "digital watch", "analog watch", "시계", "手表"
    ],
    
    # Baby
    "baby_infant_products": [
        "baby", "infant", "toddler", "newborn", "nursery", "pacifier",
        "bottle", "bib", "diaper", "teether", "아기", "婴儿"
    ],
    
    # Tools
    "tools_hand_hardware": [
        "tool", "tools", "hardware", "screwdriver", "wrench", "pliers",
        "hammer", "drill bit", "socket", "공구", "工具"
    ],
    
    # Medical/Health
    "medical_health_supplies": [
        "medical", "health", "first aid", "bandage", "mask", "thermometer",
        "blood pressure", "healthcare", "의료", "医疗"
    ],
    
    # Seasonal/Holiday
    "seasonal_holiday_items": [
        "christmas", "halloween", "holiday", "easter", "thanksgiving",
        "valentine", "decoration", "festive", "seasonal", "크리스마스", "节日"
    ],
    
    # Promotional
    "promotional_products": [
        "promotional", "promo", "giveaway", "branded", "custom logo",
        "corporate gift", "swag", "merchandise", "판촉", "促销"
    ],
    
    # Garden
    "garden_lawn_products": [
        "garden", "lawn", "plant", "planter", "hose", "sprinkler",
        "gardening", "outdoor", "patio", "정원", "园艺"
    ],
    
    # Craft
    "craft_diy_supplies": [
        "craft", "diy", "art supply", "beads", "yarn", "fabric paint",
        "scrapbook", "sewing", "knitting", "공예", "手工"
    ],
    
    # Phone Cases
    "phone_case_protector": [
        "phone case", "iphone case", "samsung case", "mobile case",
        "screen protector", "phone cover", "폰케이스", "手机壳"
    ],
    
    # Textiles
    "textiles_fabrics_towels": [
        "towel", "blanket", "bedding", "sheet", "pillow", "cushion",
        "fabric", "textile", "linen", "수건", "毛巾"
    ],
    
    # Furniture
    "furniture_small_storage": [
        "furniture", "shelf", "rack", "organizer", "storage bin",
        "cabinet", "drawer", "stand", "가구", "家具"
    ],
    
    # Food/Beverage
    "food_beverage_snacks": [
        "food", "snack", "beverage", "drink", "cookie", "chip",
        "cracker", "nut", "dried fruit", "식품", "食品"
    ]
}


def classify_category(query: str) -> str:
    """
    Simple keyword-based category classification.
    Returns best matching category_id or 'generic_consumer_product'.
    """
    query_lower = query.lower()
    
    scores = {}
    for cat_id, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in query_lower)
        if score > 0:
            scores[cat_id] = score
    
    if scores:
        return max(scores, key=scores.get)
    return "generic_consumer_product"


def get_category_config(category_id: str) -> Dict[str, Any]:
    """Get configuration for a category, with fallback to generic."""
    return COST_TABLES.get(category_id, COST_TABLES["generic_consumer_product"])


def list_available_categories() -> list:
    """List all available category IDs."""
    return list(COST_TABLES.keys())


def list_available_routes() -> list:
    """List common shipping routes."""
    return [
        "cn_to_us_west_coast",
        "cn_to_us_east_coast", 
        "cn_to_eu"
    ]


# =============================================================================
# VERIFIED MARKET DATA (Data-Driven Report Nov 2025)
# =============================================================================

MARKET_DATA = {
    # Source: ISM Survey 2024
    "lead_time_benchmarks": {
        "production_materials_days": {"min": 88, "max": 92, "avg": 90},
        "operational_materials_days": {"min": 40, "max": 50, "avg": 45},
        "capital_goods_days": {"min": 140, "max": 168, "avg": 154},
        "nexsupply_target_days": 74,  # Our optimized estimate
        "data_source": "ISM Manufacturing Survey 2024",
        "confidence": 0.85
    },
    
    # Source: Eyton Lighting 2025
    "landed_cost_ratios": {
        "base_price_percent": {"min": 40, "max": 60},
        "shipping_percent": {"min": 15, "max": 30},
        "customs_percent": {"min": 10, "max": 20},
        "hidden_costs_percent": {"min": 5, "max": 15},
        "total_hidden_increase": {"min": 60, "max": 100},  # % increase from base
        "data_source": "Eyton Lighting 2025 / CrimsonLogic",
        "confidence": 0.80
    },
    
    # Source: Veridion 2025, CAPS Research
    "supplier_onboarding": {
        "manual_cost_usd": 35000,
        "manual_time_months": 6,
        "ai_based_cost_usd": 2400,
        "ai_based_time_days": {"min": 2, "max": 5},
        "cost_reduction_percent": 85,
        "nexsupply_time_minutes": 10,  # Our target
        "data_source": "Veridion 2025, CAPS Research",
        "confidence": 0.90
    },
    
    # Source: Grand View Research, Mordor Intelligence
    "market_size": {
        "global_sourcing_software_2024_usd_b": 9.3,
        "global_sourcing_software_2033_usd_b": 21.2,
        "cagr_percent": 9.7,
        "asia_pacific_cagr_percent": 11.9,
        "sme_segment_cagr_percent": 11.9,
        "data_source": "Grand View Research, Mordor Intelligence",
        "confidence": 0.95
    },
    
    # Source: ChurnFree 2024, Benchmarkit 2025
    "saas_benchmarks": {
        "average_cac_usd": 702,
        "cac_range_usd": {"min": 440, "max": 1290},
        "healthy_ltv_cac_ratio": 3,
        "excellent_ltv_cac_ratio": 5,
        "visitor_to_lead_percent": {"avg": 1.5, "good": 2.5},
        "lead_to_sql_percent": {"avg": 25, "good": 40},
        "data_source": "ChurnFree 2024, Benchmarkit 2025",
        "confidence": 0.85
    }
}


# Detailed hidden cost items (Eyton Lighting breakdown)
HIDDEN_COST_ITEMS = {
    "customs_clearance": {"min_usd": 300, "max_usd": 500},
    "insurance": {"min_usd": 500, "max_usd": 1000},
    "fx_fees": {"min_usd": 250, "max_usd": 400},
    "port_handling": {"min_usd": 200, "max_usd": 300},
    "storage_per_day": {"min_usd": 150, "max_usd": 500},
    "documentation": {"min_usd": 75, "max_usd": 200},
    "inspection": {"min_usd": 250, "max_usd": 350}
}


# Lead time breakdown (verified ISM 2024)
LEAD_TIME_BREAKDOWN = {
    "order_processing": {"min_days": 1, "max_days": 3, "avg_days": 2},
    "raw_material_procurement": {"min_days": 5, "max_days": 15, "avg_days": 10},
    "production": {"min_days": 3, "max_days": 10, "avg_days": 7},
    "quality_control": {"min_days": 1, "max_days": 5, "avg_days": 2},
    "packaging": {"min_days": 1, "max_days": 2, "avg_days": 1.5},
    "sea_freight": {"min_days": 26, "max_days": 30, "avg_days": 28},
    "customs_clearance": {"min_days": 2, "max_days": 5, "avg_days": 3},
    "total": {"min_days": 67, "max_days": 83, "avg_days": 74}
}


def get_confidence_level(confidence_score: float) -> str:
    """Convert confidence score to level string."""
    if confidence_score >= 0.85:
        return "High"
    elif confidence_score >= 0.70:
        return "Medium"
    else:
        return "Low"


def get_lead_time_estimate(category_id: str = None) -> dict:
    """Get lead time estimate with confidence."""
    base = LEAD_TIME_BREAKDOWN["total"].copy()
    base["breakdown"] = LEAD_TIME_BREAKDOWN
    base["confidence"] = 0.85
    base["confidence_level"] = "High"
    base["data_source"] = "ISM Manufacturing Survey 2024"
    return base


def get_hidden_cost_estimate(order_value_usd: float) -> dict:
    """Estimate hidden costs based on order value."""
    # Sum up typical hidden costs
    min_hidden = sum(v["min_usd"] for v in HIDDEN_COST_ITEMS.values())
    max_hidden = sum(v["max_usd"] for v in HIDDEN_COST_ITEMS.values())
    avg_hidden = (min_hidden + max_hidden) / 2
    
    # As percentage of order value
    if order_value_usd > 0:
        percent_of_order = (avg_hidden / order_value_usd) * 100
    else:
        percent_of_order = 15  # Default estimate
    
    return {
        "min_usd": min_hidden,
        "max_usd": max_hidden,
        "avg_usd": avg_hidden,
        "percent_of_order": round(percent_of_order, 1),
        "items": HIDDEN_COST_ITEMS,
        "confidence": 0.80,
        "data_source": "Eyton Lighting 2025"
    }

