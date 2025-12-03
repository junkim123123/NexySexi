"""
Supplier Card Component - Ultra Simple Version
"""

import streamlit as st
from typing import Dict
import re


def format_price_range(price_range: str) -> str:
    """Format price range consistently: $0.18-$0.24 format."""
    if not price_range or price_range.lower() == "contact":
        return "Contact for price"
    
    # If already has $ signs, return as is
    if "$" in price_range:
        return price_range
    
    # Match patterns like "0.18-0.24" or "0.18 - 0.24"
    match = re.match(r'(\d+\.?\d*)\s*[-–]\s*(\d+\.?\d*)', price_range)
    if match:
        low, high = match.groups()
        return f"${low}–${high}"
    
    # Single number
    match = re.match(r'(\d+\.?\d*)', price_range)
    if match:
        return f"${match.group(1)}"
    
    return price_range


def render_supplier_card(supplier: Dict, index: int = 0, show_actions: bool = True, compact: bool = False, show_selection: bool = True) -> bool:
    """Render a simple supplier card using only basic Streamlit components.
    
    Returns:
        bool: Whether this supplier is selected
    """
    
    # Extract data
    name = supplier.get("name", "Unknown Supplier")
    location = supplier.get("location", "Unknown")
    rating = supplier.get("rating", 4.5)
    min_order = supplier.get("min_order", "MOQ varies")
    price_range = format_price_range(supplier.get("price_range", "Contact"))
    verified = supplier.get("verified", False)
    response_time = supplier.get("response_time", "< 48h")
    certifications = supplier.get("certifications", [])
    # Convert years_in_business to int safely
    years_raw = supplier.get("years_in_business", 0)
    try:
        years_in_business = int(years_raw) if years_raw else 0
    except (ValueError, TypeError):
        years_in_business = 0
    
    factory_grade = supplier.get("factory_grade", "Unknown")
    trade_assurance = supplier.get("trade_assurance", False)
    quality_tier = supplier.get("quality_tier", "Medium")
    risk_notes = supplier.get("risk_notes", "No specific risks identified")
    
    # Quality stars
    quality_map = {"high": "★★★", "medium": "★★☆", "low": "★☆☆"}
    stars = quality_map.get(quality_tier.lower(), "★★☆")
    
    # Years label
    years_label = f"{years_in_business}+ yrs" if years_in_business > 0 else "New"
    
    # Risk emoji
    risk_lower = risk_notes.lower() if risk_notes else ""
    if any(kw in risk_lower for kw in ["high risk", "no buyer", "shutdown"]):
        risk_emoji = "🔴"
    elif any(kw in risk_lower for kw in ["delay", "deposit", "requires", "verify"]):
        risk_emoji = "🟡"
    else:
        risk_emoji = "🟢"
    
    # Initialize selection state
    selection_key = f"supplier_selected_{index}"
    if selection_key not in st.session_state:
        st.session_state[selection_key] = False
    
    is_selected = st.session_state[selection_key]
    
    # Card
    with st.container(border=True):
        # Header with selection checkbox
        col_check, col_name = st.columns([1, 8])
        with col_check:
            if show_selection:
                is_selected = st.checkbox("Select supplier", value=is_selected, key=f"check_{index}", label_visibility="collapsed")
                st.session_state[selection_key] = is_selected
        with col_name:
            st.subheader(name)
        st.caption(f"📍 {location} · {factory_grade}")
        
        # Trust badges as simple text
        badges = []
        if verified:
            badges.append("✅ Verified")
        badges.append(f"📅 {years_label}")
        if trade_assurance:
            badges.append("🛡️ Protected")
        else:
            badges.append("⚠️ No Protection")
        badges.append(f"{stars}")
        st.write(" · ".join(badges))
        
        # Key metrics - simple write
        st.write(f"⭐ **{rating}** · 💰 **{price_range}** · 📦 **{min_order}** · ⚡ **{response_time}**")
        
        st.divider()
        
        # Risk Assessment Box (Enhanced Visualization)
        risk_color = "#FEF2F2" if risk_emoji == "🔴" else "#FFFBEB" if risk_emoji == "🟡" else "#F0FDF4"
        risk_border = "#FCA5A5" if risk_emoji == "🔴" else "#FDE68A" if risk_emoji == "🟡" else "#86EFAC"
        risk_text_color = "#991B1B" if risk_emoji == "🔴" else "#92400E" if risk_emoji == "🟡" else "#166534"
        
        st.markdown(f"""
            <div style="background: {risk_color}; border: 1px solid {risk_border}; border-radius: 8px; 
                        padding: 12px; margin: 8px 0;">
                <div style="font-weight: 600; color: {risk_text_color}; margin-bottom: 4px;">
                    {risk_emoji} Risk Assessment
                </div>
                <div style="font-size: 0.85rem; color: #4B5563;">
                    {risk_notes}
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Quick Risk Indicators (NEW - Grid format)
        col_r1, col_r2, col_r3, col_r4 = st.columns(4)
        
        # Financial stability indicator based on trade assurance + years
        fin_grade = "A+" if trade_assurance and years_in_business >= 8 else "A" if trade_assurance else "B" if years_in_business >= 3 else "C"
        fin_color = "green" if fin_grade in ["A+", "A"] else "orange" if fin_grade == "B" else "red"
        
        # Quality indicator
        qual_grade = "A" if quality_tier.lower() == "high" else "B" if quality_tier.lower() == "medium" else "C"
        qual_color = "green" if qual_grade == "A" else "orange" if qual_grade == "B" else "red"
        
        # Response speed
        resp_fast = "< 12" in response_time or "< 24" in response_time
        resp_grade = "A" if resp_fast else "B"
        resp_color = "green" if resp_fast else "orange"
        
        # Verification
        verif_grade = "A" if verified and trade_assurance else "B" if verified else "C"
        verif_color = "green" if verif_grade == "A" else "orange" if verif_grade == "B" else "red"
        
        # Grade definitions for tooltips
        fin_tooltip = "A+: Strong balance sheet, low debt, trade assurance. A: Trade assurance or 8+ years. B: 3+ years stable. C: New or unverified."
        qual_tooltip = "A: High quality tier, ISO certified. B: Medium quality, some certifications. C: Basic quality, limited certifications."
        resp_tooltip = "A: < 12-24h response time. B: 24-48h response time."
        verif_tooltip = "A: Verified + trade assurance. B: Verified only. C: Unverified."
        
        with col_r1:
            st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:#64748B;'>Financial <span title='{fin_tooltip}' style='cursor:help;'>ⓘ</span></div><div style='text-align:center;font-weight:700;color:{fin_color};'>{fin_grade}</div>", unsafe_allow_html=True)
        with col_r2:
            st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:#64748B;'>Quality <span title='{qual_tooltip}' style='cursor:help;'>ⓘ</span></div><div style='text-align:center;font-weight:700;color:{qual_color};'>{qual_grade}</div>", unsafe_allow_html=True)
        with col_r3:
            st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:#64748B;'>Response <span title='{resp_tooltip}' style='cursor:help;'>ⓘ</span></div><div style='text-align:center;font-weight:700;color:{resp_color};'>{resp_grade}</div>", unsafe_allow_html=True)
        with col_r4:
            st.markdown(f"<div style='text-align:center;font-size:0.75rem;color:#64748B;'>Verified <span title='{verif_tooltip}' style='cursor:help;'>ⓘ</span></div><div style='text-align:center;font-weight:700;color:{verif_color};'>{verif_grade}</div>", unsafe_allow_html=True)
        
        # Rating criteria explanation (only on first card)
        if index == 0:
            st.markdown("""
                <div style="background: #F8FAFC; border-radius: 6px; padding: 8px 12px; margin-top: 8px; 
                            font-size: 0.75rem; color: #64748B; display: flex; align-items: center; gap: 6px;">
                    <span style="font-size: 0.9rem;">ⓘ</span>
                    <span><strong>Ratings:</strong> A = low risk / B = moderate / C = higher attention required. Hover over ⓘ for details.</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Certifications
        if certifications:
            st.caption(f"📜 {' · '.join(certifications[:4])}")
        
        # Contact button
        if show_actions:
            if st.button(f"📩 Request Quote", key=f"quote_{index}"):
                from utils.config import Config
                contact_email = Config.get_consultation_email()
                st.info(f"📧 Email **{contact_email}** with subject: 'Quote: {name}'")
    
    return is_selected


def render_supplier_list(suppliers: list, max_display: int = 3, show_actions: bool = True, compact: bool = False, show_selection: bool = True) -> list:
    """Render a list of supplier cards.
    
    Returns:
        list: List of selected supplier indices
    """
    if not suppliers:
        st.info("No suppliers found.")
        return []
    
    selected_indices = []
    for idx, supplier in enumerate(suppliers[:max_display]):
        is_selected = render_supplier_card(supplier, index=idx, show_actions=show_actions, compact=compact, show_selection=show_selection)
        if is_selected:
            selected_indices.append(idx)
    
    remaining = len(suppliers) - max_display
    if remaining > 0:
        st.caption(f"+ {remaining} more available")
    
    # Show selection summary
    if show_selection and selected_indices:
        st.success(f"✅ {len(selected_indices)} supplier(s) selected for contact")
    
    return selected_indices
