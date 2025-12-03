"""
Unit tests for result builder.
Tests the result building logic.
"""

import pytest
from utils.result_builder import build_nexsupply_result
from utils.config import AppSettings


def test_build_nexsupply_result_basic():
    """Test basic result building."""
    result = build_nexsupply_result("test product query")
    
    # Check structure (build_nexsupply_result returns new format)
    assert "meta" in result
    assert "landed_cost" in result
    assert "market_snapshot" in result
    assert "assumptions" in result


def test_build_nexsupply_result_with_defaults():
    """Test that result uses AppSettings defaults."""
    result = build_nexsupply_result("test product")
    
    assumptions = result.get("assumptions", {})
    
    # Should use defaults from AppSettings
    assert assumptions.get("target_market") == AppSettings.DEFAULT_TARGET_MARKET
    assert assumptions.get("channel") == AppSettings.DEFAULT_CHANNEL
    assert assumptions.get("incoterm") == AppSettings.DEFAULT_INCOTERM
    assert assumptions.get("currency") == AppSettings.DEFAULT_CURRENCY


def test_build_nexsupply_result_custom_params():
    """Test result building with custom parameters."""
    result = build_nexsupply_result(
        "test product",
        units=10000,
        target_market="EU",
        channel="Retail"
    )
    
    assumptions = result.get("assumptions", {})
    
    # Should use custom values
    assert assumptions.get("volume_units") == 10000
    assert assumptions.get("target_market") == "EU"
    assert assumptions.get("channel") == "Retail"


def test_build_nexsupply_result_has_landed_cost():
    """Test that result includes landed cost data."""
    result = build_nexsupply_result("test product")
    
    landed_cost = result.get("landed_cost", {})
    totals = landed_cost.get("totals", {})
    
    assert "landed_cost_per_unit_usd" in totals
    assert "total_landed_cost_usd" in totals
    assert totals["landed_cost_per_unit_usd"] > 0




