"""
NexSupply Analytics Dashboard
Internal page for business intelligence and trend analysis.

Access: Add ?admin=1 to URL or navigate directly to this page.
"""

import streamlit as st
from services.data_logger import render_analytics_dashboard

# Page config
st.set_page_config(
    page_title="NexSupply Analytics",
    page_icon="📊",
    layout="wide"
)

# Simple admin check (in production, add proper authentication)
admin_mode = st.query_params.get("admin", "0") == "1"

if not admin_mode:
    st.warning("⚠️ This page is for internal use only.")
    st.markdown("Add `?admin=1` to the URL to access analytics.")
    st.stop()

# Render the analytics dashboard
render_analytics_dashboard()

