"""
Input parser for extracting structured data from user queries.
Parses volume, channel, target market, and other parameters from natural language input.
"""

import re
from typing import Dict, Optional, Tuple
from utils.config import AppSettings


def parse_volume(text: str) -> Optional[int]:
    """
    Parse volume/quantity from text.
    
    Supports:
    - Korean: 만, 천, 백
    - English: million, thousand, k, m
    - Numbers: 2000000, 2,000,000
    
    Examples:
    - "200만개" -> 2000000
    - "5천개" -> 5000
    - "2 million units" -> 2000000
    - "5000" -> 5000
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Korean number patterns
    korean_patterns = [
        (r'(\d+(?:\.\d+)?)\s*만\s*개?', 10000),  # 만 (10,000)
        (r'(\d+(?:\.\d+)?)\s*천\s*개?', 1000),   # 천 (1,000)
        (r'(\d+(?:\.\d+)?)\s*백\s*개?', 100),    # 백 (100)
    ]
    
    for pattern, multiplier in korean_patterns:
        match = re.search(pattern, text_lower)
        if match:
            number = float(match.group(1))
            return int(number * multiplier)
    
    # English patterns
    english_patterns = [
        (r'(\d+(?:\.\d+)?)\s*million', 1000000),
        (r'(\d+(?:\.\d+)?)\s*m', 1000000),
        (r'(\d+(?:\.\d+)?)\s*thousand', 1000),
        (r'(\d+(?:\.\d+)?)\s*k', 1000),
    ]
    
    for pattern, multiplier in english_patterns:
        match = re.search(pattern, text_lower)
        if match:
            number = float(match.group(1))
            return int(number * multiplier)
    
    # Plain numbers (remove commas)
    number_match = re.search(r'(\d{1,3}(?:,\d{3})*(?:\.\d+)?)', text)
    if number_match:
        number_str = number_match.group(1).replace(',', '')
        try:
            return int(float(number_str))
        except ValueError:
            pass
    
    return None


def parse_target_market(text: str) -> Optional[str]:
    """
    Parse target market/country from text.
    
    Examples:
    - "미국" -> "USA"
    - "미국 시장" -> "USA"
    - "US market" -> "USA"
    - "United States" -> "USA"
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Market mappings
    market_map = {
        # Korean
        '미국': 'USA',
        '미국시장': 'USA',
        '미국 시장': 'USA',
        'us': 'USA',
        'usa': 'USA',
        'united states': 'USA',
        'u.s.': 'USA',
        'u.s.a.': 'USA',
        
        # Other markets (add as needed)
        'eu': 'EU',
        '유럽': 'EU',
        'europe': 'EU',
        'uk': 'UK',
        '영국': 'UK',
        'united kingdom': 'UK',
        'canada': 'Canada',
        '캐나다': 'Canada',
        'australia': 'Australia',
        '호주': 'Australia',
    }
    
    for key, value in market_map.items():
        if key in text_lower:
            return value
    
    return None


def parse_channel(text: str) -> Optional[str]:
    """
    Parse sales channel from text.
    
    Examples:
    - "편의점 시장" -> "Convenience Store"
    - "편의점" -> "Convenience Store"
    - "Amazon FBA" -> "Amazon FBA"
    - "retail" -> "Retail"
    """
    if not text:
        return None
    
    text_lower = text.lower()
    
    # Channel mappings
    channel_map = {
        # Korean
        '편의점': 'Convenience Store',
        '편의점 시장': 'Convenience Store',
        '편의점시장': 'Convenience Store',
        '온라인': 'Online',
        '오프라인': 'Offline',
        '소매': 'Retail',
        '도매': 'Wholesale',
        
        # English
        'amazon fba': 'Amazon FBA',
        'amazon': 'Amazon FBA',
        'fba': 'Amazon FBA',
        'convenience store': 'Convenience Store',
        'retail': 'Retail',
        'wholesale': 'Wholesale',
        'online': 'Online',
        'offline': 'Offline',
        'e-commerce': 'E-commerce',
        'ecommerce': 'E-commerce',
    }
    
    for key, value in channel_map.items():
        if key in text_lower:
            return value
    
    return None


def parse_input_parameters(query: str) -> Dict[str, any]:
    """
    Parse structured parameters from user query.
    
    Args:
        query: User's natural language input
        
    Returns:
        Dictionary with parsed parameters:
        - volume_units: Optional[int]
        - target_market: Optional[str]
        - channel: Optional[str]
        - route: Optional[str] (inferred from target_market)
    """
    if not query:
        return {}
    
    # Combine query parts if it's a list
    if isinstance(query, list):
        query = ' '.join(str(q) for q in query)
    
    query_str = str(query)
    
    # Parse each component
    volume = parse_volume(query_str)
    target_market = parse_target_market(query_str)
    channel = parse_channel(query_str)
    
    # Infer route from target_market
    route = None
    if target_market == "USA":
        route = "cn_to_us_west_coast"
    elif target_market == "EU":
        route = "cn_to_eu"
    elif target_market == "UK":
        route = "cn_to_uk"
    
    result = {}
    if volume:
        result['volume_units'] = volume
    if target_market:
        result['target_market'] = target_market
    if channel:
        result['channel'] = channel
    if route:
        result['route'] = route
    
    return result

