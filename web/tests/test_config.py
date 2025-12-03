"""
Unit tests for configuration management.
Tests AppSettings and Config classes.
"""

import pytest
from utils.config import AppSettings, Config


def test_app_settings_defaults():
    """Test that AppSettings has all required defaults."""
    assert AppSettings.DEFAULT_VOLUME_UNITS == 5000
    assert AppSettings.DEFAULT_TARGET_MARKET == "USA"
    assert AppSettings.DEFAULT_CHANNEL == "Amazon FBA"
    assert AppSettings.DEFAULT_INCOTERM == "DDP"
    assert AppSettings.DEFAULT_CURRENCY == "USD"


def test_app_settings_route_display():
    """Test route display formatting."""
    display = AppSettings.get_route_display("cn_to_us_west_coast")
    assert "China" in display
    assert "US" in display or "West" in display


def test_app_settings_incoterm_display():
    """Test incoterm display formatting."""
    display = AppSettings.get_incoterm_display("DDP", "Los Angeles")
    assert "DDP" in display
    assert "Los Angeles" in display


def test_app_settings_incoterm_display_defaults():
    """Test incoterm display with defaults."""
    display = AppSettings.get_incoterm_display()
    assert AppSettings.DEFAULT_INCOTERM in display
    assert AppSettings.DEFAULT_DESTINATION in display




