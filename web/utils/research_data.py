"""
Research Data Injection Module
Allows users to provide market research data that will be used to enhance AI analysis.
"""

import json
import re
from typing import Dict, Any, Optional


def parse_research_data_from_text(text: str) -> Optional[Dict[str, Any]]:
    """
    Parse research data from user's context input text.
    
    Supports multiple formats:
    1. JSON format: {"demand_level": "High", "competition_level": "Medium"}
    2. Key-value format:
       - 수요: High
       - 경쟁: Medium
       - 시장 규모: $250M
    3. Natural language format:
       - Demand is high
       - Competition is medium
       - Market size is $250M
    
    Args:
        text: User input text that may contain research data
        
    Returns:
        Dict with parsed research data or None if no data found
    """
    if not text or not text.strip():
        return None
    
    research_data = {}
    text_lower = text.lower()
    
    # Try to parse as JSON first
    try:
        # Look for JSON object in text
        json_match = re.search(r'\{[^{}]*\}', text)
        if json_match:
            parsed = json.loads(json_match.group(0))
            if isinstance(parsed, dict):
                research_data.update(parsed)
    except (json.JSONDecodeError, AttributeError):
        pass
    
    # Parse Korean key-value format
    korean_patterns = [
        (r'수요[:\s]+(high|medium|low|높음|중간|낮음)', 'demand_level'),
        (r'경쟁[:\s]+(high|medium|low|높음|중간|낮음)', 'competition_level'),
        (r'시장\s*규모[:\s]+(\$?[\d.]+[MBK]?)', 'market_size_usd'),
        (r'주요\s*경쟁자[:\s]+(\d+)', 'competitor_count'),
        (r'마진[:\s]+(\d+)[-~](\d+)%', 'margin_range'),
    ]
    
    for pattern, key in korean_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            if key == 'demand_level':
                val = match.group(1).lower()
                research_data[key] = _normalize_level(val)
            elif key == 'competition_level':
                val = match.group(1).lower()
                research_data[key] = _normalize_level(val)
            elif key == 'market_size_usd':
                research_data[key] = match.group(1)
            elif key == 'competitor_count':
                research_data[key] = int(match.group(1))
            elif key == 'margin_range':
                research_data['margin_range_percent'] = [int(match.group(1)), int(match.group(2))]
    
    # Parse English key-value format
    english_patterns = [
        (r'demand[:\s]+(high|medium|low|medium-high)', 'demand_level'),
        (r'competition[:\s]+(high|medium|low)', 'competition_level'),
        (r'market\s*size[:\s]+(\$?[\d.]+[MBK]?)', 'market_size_usd'),
        (r'competitor[s]?[:\s]+(\d+)', 'competitor_count'),
        (r'margin[:\s]+(\d+)[-~](\d+)%', 'margin_range'),
    ]
    
    for pattern, key in english_patterns:
        match = re.search(pattern, text_lower, re.IGNORECASE)
        if match:
            if key == 'demand_level':
                val = match.group(1).lower()
                research_data[key] = _normalize_level(val)
            elif key == 'competition_level':
                val = match.group(1).lower()
                research_data[key] = _normalize_level(val)
            elif key == 'market_size_usd':
                research_data[key] = match.group(1)
            elif key == 'competitor_count':
                research_data[key] = int(match.group(1))
            elif key == 'margin_range':
                research_data['margin_range_percent'] = [int(match.group(1)), int(match.group(2))]
    
    return research_data if research_data else None


def _normalize_level(level: str) -> str:
    """Normalize level strings to standard format."""
    level_lower = level.lower()
    if level_lower in ['high', '높음', 'h']:
        return 'High'
    elif level_lower in ['medium', '중간', 'm', 'medium-high']:
        return 'Medium-High' if 'medium-high' in level_lower else 'Medium'
    elif level_lower in ['low', '낮음', 'l']:
        return 'Low'
    return level.capitalize()


def inject_research_data(ai_insights: Dict[str, Any], research_data: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Inject user-provided research data into AI insights.
    
    Research data takes precedence over AI-generated values for specified fields.
    
    Args:
        ai_insights: AI-generated insights dictionary
        research_data: User-provided research data (optional)
        
    Returns:
        Updated ai_insights with research data injected
    """
    if not research_data or not isinstance(research_data, dict):
        return ai_insights
    
    # Create a copy to avoid mutating original
    updated_insights = ai_insights.copy() if ai_insights else {}
    
    # Inject demand data
    if 'demand_level' in research_data:
        updated_insights['demand_level'] = research_data['demand_level']
        # Update demand_score based on level
        level_scores = {'High': 0.8, 'Medium-High': 0.65, 'Medium': 0.5, 'Low': 0.3}
        updated_insights['demand_score'] = level_scores.get(research_data['demand_level'], 0.5)
    
    # Inject competition data
    if 'competition_level' in research_data:
        updated_insights['competition_level'] = research_data['competition_level']
        # Update competition_score based on level
        level_scores = {'High': 0.8, 'Medium': 0.5, 'Low': 0.3}
        updated_insights['competition_score'] = level_scores.get(research_data['competition_level'], 0.5)
    
    # Inject market size
    if 'market_size_usd' in research_data:
        updated_insights['market_size_usd'] = research_data['market_size_usd']
    
    # Inject competitor count
    if 'competitor_count' in research_data:
        updated_insights['active_listings'] = research_data['competitor_count']
    
    # Inject margin range
    if 'margin_range_percent' in research_data:
        updated_insights['margin_range_percent'] = research_data['margin_range_percent']
    
    # Add note about research data usage
    if research_data:
        notes = updated_insights.get('data_coverage_notes', '')
        if notes:
            notes += ' | '
        notes += 'Analysis enhanced with user-provided market research data.'
        updated_insights['data_coverage_notes'] = notes
    
    return updated_insights


def format_research_data_for_prompt(research_data: Optional[Dict[str, Any]]) -> str:
    """
    Format research data as a readable string for AI prompt.
    
    Args:
        research_data: Research data dictionary
        
    Returns:
        Formatted string for prompt inclusion
    """
    if not research_data or not isinstance(research_data, dict):
        return "No additional research data provided."
    
    lines = ["[6] User-provided market research data:"]
    lines.append("")
    
    if 'demand_level' in research_data:
        lines.append(f"* Demand level: {research_data['demand_level']}")
    if 'competition_level' in research_data:
        lines.append(f"* Competition level: {research_data['competition_level']}")
    if 'market_size_usd' in research_data:
        lines.append(f"* Market size: {research_data['market_size_usd']}")
    if 'competitor_count' in research_data:
        lines.append(f"* Number of competitors: {research_data['competitor_count']}")
    if 'margin_range_percent' in research_data:
        margin = research_data['margin_range_percent']
        lines.append(f"* Expected margin range: {margin[0]}–{margin[1]}%")
    
    lines.append("")
    lines.append("Use this research data to inform your analysis. If provided, these values should take precedence over general estimates.")
    
    return "\n".join(lines)

