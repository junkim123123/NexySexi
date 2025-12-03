"""
Pydantic Models for NexSupply Extraction
Validates and normalizes LLM-extracted structured data.
"""

from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, Dict, Any
from enum import Enum


# =============================================================================
# ENUMS - Allowed Values (must match system prompt exactly)
# =============================================================================

class ChannelType(str, Enum):
    """Allowed sales channel values."""
    CONVENIENCE_STORE = "Convenience Store"
    AMAZON_FBA = "Amazon FBA"
    ECOMMERCE_D2C = "eCommerce D2C"
    WHOLESALE_DISTRIBUTOR = "Wholesale Distributor"
    OFFLINE_RETAIL = "Offline Retail"
    OTHER = "Other"


class TargetMarketType(str, Enum):
    """Allowed target market values."""
    USA = "USA"
    EU = "EU"
    KOREA = "Korea"
    JAPAN = "Japan"
    GLOBAL = "Global"
    OTHER = "Other"


class DeliveryTimelineType(str, Enum):
    """Allowed delivery timeline categories."""
    URGENT = "Urgent (under 1 week)"
    SHORT_TERM = "Short-term (1-4 weeks)"
    MEDIUM_TERM = "Medium-term (1-3 months)"
    LONG_TERM = "Long-term (over 3 months)"
    OTHER = "Other"


# =============================================================================
# MAIN EXTRACTION MODEL
# =============================================================================

class PriceRange(BaseModel):
    """Price range structure."""
    min: Optional[float] = Field(default=None, description="Minimum price")
    max: Optional[float] = Field(default=None, description="Maximum price")
    currency: Optional[str] = Field(default=None, description="Currency code (USD, KRW, etc.)")
    
    @field_validator('currency')
    @classmethod
    def validate_currency(cls, v):
        """Normalize currency codes."""
        if v is None:
            return None
        v_upper = v.upper()
        if v_upper in ['USD', 'US$', '$', '달러', 'DOLLAR']:
            return 'USD'
        elif v_upper in ['KRW', '원', 'WON', 'W']:
            return 'KRW'
        return v


class SourcingIntents(BaseModel):
    """
    Extracted sourcing requirements from user input.
    Validates LLM output against defined schema.
    """
    
    # Volume fields
    volume: Optional[int] = Field(
        default=None,
        ge=0,
        description="Normalized order quantity (integer, must be >= 0)"
    )
    volume_raw: Optional[str] = Field(
        default=None,
        description="Original user text for volume"
    )
    
    # Channel fields
    channel: ChannelType = Field(
        default=ChannelType.OTHER,
        description="Normalized sales channel"
    )
    channel_raw: Optional[str] = Field(
        default=None,
        description="Original user text for channel"
    )
    
    # Target market fields
    target_market: TargetMarketType = Field(
        default=TargetMarketType.OTHER,
        description="Normalized target market"
    )
    target_market_raw: Optional[str] = Field(
        default=None,
        description="Original user text for target market"
    )
    
    # Optional fields (for future expansion)
    price_range: Optional[PriceRange] = Field(
        default=None,
        description="Target price range"
    )
    price_range_raw: Optional[str] = Field(
        default=None,
        description="Original user text for price"
    )
    
    delivery_timeline: Optional[DeliveryTimelineType] = Field(
        default=None,
        description="Delivery timeline category"
    )
    delivery_timeline_raw: Optional[str] = Field(
        default=None,
        description="Original user text for delivery timeline"
    )
    
    moq: Optional[int] = Field(
        default=None,
        ge=0,
        description="Minimum order quantity mentioned by user"
    )
    moq_raw: Optional[str] = Field(
        default=None,
        description="Original user text for MOQ"
    )
    
    @field_validator('volume', 'moq')
    @classmethod
    def validate_positive_int(cls, v):
        """Ensure volume and MOQ are positive if provided."""
        if v is not None and v < 0:
            raise ValueError("Volume and MOQ must be non-negative")
        return v
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for easy integration."""
        result = {
            "volume": self.volume,
            "volume_raw": self.volume_raw,
            "channel": self.channel.value,
            "channel_raw": self.channel_raw,
            "target_market": self.target_market.value,
            "target_market_raw": self.target_market_raw,
        }
        
        # Add optional fields if present
        if self.price_range:
            result["price_range"] = {
                "min": self.price_range.min,
                "max": self.price_range.max,
                "currency": self.price_range.currency
            }
        if self.price_range_raw:
            result["price_range_raw"] = self.price_range_raw
        
        if self.delivery_timeline:
            result["delivery_timeline"] = self.delivery_timeline.value
        if self.delivery_timeline_raw:
            result["delivery_timeline_raw"] = self.delivery_timeline_raw
        
        if self.moq is not None:
            result["moq"] = self.moq
        if self.moq_raw:
            result["moq_raw"] = self.moq_raw
        
        return result


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def validate_extraction_result(llm_response_str: str) -> tuple[SourcingIntents, Optional[str]]:
    """
    Validate and parse LLM extraction response.
    
    Args:
        llm_response_str: JSON string from LLM
        
    Returns:
        Tuple of (SourcingIntents object, error_message)
        If validation fails, returns (None, error_message)
    """
    import json
    
    try:
        # First, try to parse as JSON
        try:
            data = json.loads(llm_response_str)
        except json.JSONDecodeError as e:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'\{[^{}]*\}', llm_response_str, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
            else:
                return None, f"Invalid JSON: {str(e)}"
        
        # Validate with Pydantic
        parsed = SourcingIntents.model_validate(data)
        return parsed, None
        
    except ValidationError as e:
        error_msg = f"Validation failed: {e.json()}"
        return None, error_msg
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"

