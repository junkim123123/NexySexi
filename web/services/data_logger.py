"""
NexSupply Data Logger - Business Intelligence & Trend Analysis
Tracks user searches and AI responses for market insight extraction.

Supports both PostgreSQL (production) and SQLite (local development).
"""

import json
import os
import logging
import threading
from datetime import datetime
from typing import Dict, Optional, List, Tuple, Any
from contextlib import contextmanager

import streamlit as st

# Configure logging (production-safe)
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)


# =============================================================================
# DATABASE CONNECTION MANAGEMENT
# =============================================================================

# Try to import PostgreSQL driver
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    logger.warning("psycopg2 not available, falling back to SQLite")

# Try to import SQLite (always available)
try:
    import sqlite3
    SQLITE_AVAILABLE = True
except ImportError:
    SQLITE_AVAILABLE = False
    logger.error("sqlite3 not available!")

# Database connection cache
_db_connection: Any = None
_connection_lock = None
_db_type: Optional[str] = None  # 'postgresql' or 'sqlite'


def _get_connection_lock():
    """Get thread lock for connection management."""
    global _connection_lock
    if _connection_lock is None:
        _connection_lock = threading.Lock()
    return _connection_lock


def _get_database_url() -> Optional[str]:
    """Get database URL from config."""
    from utils.config import Config
    return Config.get_database_url()


def _detect_db_type() -> str:
    """Detect which database to use based on available connection."""
    db_url = _get_database_url()
    
    if db_url and db_url.startswith('postgresql://'):
        if PSYCOPG2_AVAILABLE:
            return 'postgresql'
        else:
            logger.warning("PostgreSQL URL provided but psycopg2 not installed. Falling back to SQLite.")
    
    # Fallback to SQLite
    if SQLITE_AVAILABLE:
        return 'sqlite'
    
    raise RuntimeError("No database driver available!")


def _get_sqlite_path() -> str:
    """Get SQLite database file path."""
    if os.path.exists("/tmp"):
        # Cloud environment
        return "/tmp/nexsupply_logs.db"
    else:
        # Local development
        return os.path.join(os.path.dirname(os.path.dirname(__file__)), "nexsupply_logs.db")


def get_db_connection():
    """Get database connection (PostgreSQL or SQLite)."""
    global _db_connection, _db_type
    
    if _db_type is None:
        _db_type = _detect_db_type()
    
    if _db_type == 'postgresql':
        db_url = _get_database_url()
        if not db_url:
            raise RuntimeError("DATABASE_URL not configured for PostgreSQL")
        
        try:
            conn = psycopg2.connect(db_url)
            return conn
        except Exception as e:
            logger.error(f"PostgreSQL connection failed: {e}")
            # Fallback to SQLite if PostgreSQL fails
            logger.warning("Falling back to SQLite")
            _db_type = 'sqlite'
    
    # SQLite connection
    db_path = _get_sqlite_path()
    conn = sqlite3.connect(db_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@contextmanager
def db_session():
    """Context manager for database sessions."""
    lock = _get_connection_lock()
    conn = None
    
    with lock:
        try:
            conn = get_db_connection()
            yield conn
            conn.commit()
        except Exception as e:
            if conn:
                conn.rollback()
            logger.error(f"Database session error: {e}", exc_info=True)
            raise
        finally:
            if conn:
                conn.close()


def _get_placeholder() -> str:
    """Get SQL placeholder style based on database type."""
    global _db_type
    if _db_type == 'postgresql':
        return '%s'
    else:
        return '?'


def _adapt_timestamp_for_db(timestamp: str) -> Any:
    """Adapt timestamp format for database."""
    global _db_type
    if _db_type == 'postgresql':
        # PostgreSQL expects TIMESTAMP
        return timestamp
    else:
        # SQLite uses TEXT
        return timestamp


def _adapt_date_function(date_expr: str) -> str:
    """Adapt date functions for database type."""
    global _db_type
    if _db_type == 'postgresql':
        # PostgreSQL uses DATE() function
        return f"DATE({date_expr})"
    else:
        # SQLite uses DATE() function (same)
        return f"DATE({date_expr})"


def _adapt_datetime_function(days: int) -> str:
    """Adapt datetime subtraction for database type."""
    global _db_type
    if _db_type == 'postgresql':
        return f"NOW() - INTERVAL '{days} days'"
    else:
        return f"datetime('now', '-{days} days')"


# =============================================================================
# DATABASE INITIALIZATION
# =============================================================================

def init_database():
    """Initialize database with required tables."""
    global _db_type
    
    if _db_type is None:
        _db_type = _detect_db_type()
    
    placeholder = _get_placeholder()
    
    with db_session() as conn:
        cursor = conn.cursor()
        
        if _db_type == 'postgresql':
            # PostgreSQL table creation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_logs (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    user_query TEXT NOT NULL,
                    analysis_mode TEXT,
                    confidence_score REAL,
                    product_category TEXT,
                    estimated_landed_cost REAL,
                    supplier_count INTEGER,
                    top_risk_factors TEXT,
                    ai_result_json JSONB,
                    user_email TEXT,
                    session_id TEXT,
                    request_source TEXT DEFAULT 'web',
                    processing_time_ms INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mode_usage (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    mode_name TEXT NOT NULL,
                    template_used TEXT,
                    converted_to_analysis BOOLEAN DEFAULT FALSE,
                    session_id TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultation_requests (
                    id SERIAL PRIMARY KEY,
                    timestamp TIMESTAMP NOT NULL,
                    user_email TEXT NOT NULL,
                    user_name TEXT,
                    product_query TEXT,
                    message TEXT,
                    analysis_id INTEGER,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (analysis_id) REFERENCES analysis_logs(id)
                )
            """)
        else:
            # SQLite table creation
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analysis_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_query TEXT NOT NULL,
                    analysis_mode TEXT,
                    confidence_score REAL,
                    product_category TEXT,
                    estimated_landed_cost REAL,
                    supplier_count INTEGER,
                    top_risk_factors TEXT,
                    ai_result_json TEXT,
                    user_email TEXT,
                    session_id TEXT,
                    request_source TEXT DEFAULT 'web',
                    processing_time_ms INTEGER,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS mode_usage (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    mode_name TEXT NOT NULL,
                    template_used TEXT,
                    converted_to_analysis BOOLEAN DEFAULT 0,
                    session_id TEXT
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS consultation_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT NOT NULL,
                    user_email TEXT NOT NULL,
                    user_name TEXT,
                    product_query TEXT,
                    message TEXT,
                    analysis_id INTEGER,
                    status TEXT DEFAULT 'pending',
                    FOREIGN KEY (analysis_id) REFERENCES analysis_logs(id)
                )
            """)
        
        # Create indexes
        try:
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_timestamp ON analysis_logs(timestamp)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_mode ON analysis_logs(analysis_mode)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_logs_category ON analysis_logs(product_category)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_mode_usage_name ON mode_usage(mode_name)")
        except Exception as e:
            logger.warning(f"Index creation warning (may already exist): {e}")


# =============================================================================
# LOGGING FUNCTIONS
# =============================================================================

def log_analysis(
    query: str,
    mode: str,
    json_data: Dict,
    user_email: Optional[str] = None,
    processing_time_ms: Optional[int] = None
) -> Optional[int]:
    """
    Log an analysis request and its AI response.
    
    Args:
        query: User's search query text
        mode: Analysis mode (e.g., 'market', 'verify', 'cost', 'leadtime')
        json_data: Full AI response JSON
        user_email: Optional user email (if report requested)
        processing_time_ms: Optional API processing time
    
    Returns:
        ID of the inserted log record, or None if failed
    """
    try:
        init_database()
        
        # Extract key metrics from JSON
        confidence = json_data.get("analysis_confidence", 0)
        product_info = json_data.get("product_info", {})
        product_category = product_info.get("category", "Unknown")
        
        landed_cost = json_data.get("landed_cost", {})
        estimated_cost = landed_cost.get("cost_per_unit_usd", 0)
        
        suppliers = json_data.get("suppliers", [])
        supplier_count = len(suppliers) if suppliers else 0
        
        # Extract top risk factors
        risk_analysis = json_data.get("risk_analysis", {})
        risk_items = risk_analysis.get("key_risks", [])
        top_risks = json.dumps(risk_items[:3] if risk_items else [], ensure_ascii=False)
        
        # Session tracking
        session_id = st.session_state.get("session_id", "unknown")
        
        # Prepare JSON data
        global _db_type
        if _db_type == 'postgresql':
            # PostgreSQL can use JSONB
            json_str = json.dumps(json_data, ensure_ascii=False, default=str)
        else:
            # SQLite uses TEXT
            json_str = json.dumps(json_data, ensure_ascii=False, default=str)
        
        timestamp = datetime.now().isoformat()
        placeholder = _get_placeholder()
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO analysis_logs (
                    timestamp, user_query, analysis_mode, confidence_score,
                    product_category, estimated_landed_cost, supplier_count,
                    top_risk_factors, ai_result_json, user_email, session_id,
                    processing_time_ms
                ) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, 
                         {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, 
                         {placeholder}, {placeholder})
            """, (
                timestamp,
                query,
                mode,
                confidence,
                product_category,
                estimated_cost,
                supplier_count,
                top_risks,
                json_str,
                user_email,
                session_id,
                processing_time_ms
            ))
            
            if _db_type == 'postgresql':
                cursor.execute("SELECT LASTVAL()")
                return cursor.fetchone()[0]
            else:
                return cursor.lastrowid
            
    except Exception as e:
        logger.error(f"Error logging analysis: {e}", exc_info=True)
        import sys
        print(f"[DATA_LOGGER ERROR] Failed to log analysis: {e}", file=sys.stderr)
        return None


def log_mode_usage(
    mode_name: str,
    template_used: str,
    converted: bool = False
) -> Optional[int]:
    """Log when a user clicks a Quick Start card."""
    try:
        init_database()
        
        session_id = st.session_state.get("session_id", "unknown")
        timestamp = datetime.now().isoformat()
        placeholder = _get_placeholder()
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO mode_usage (timestamp, mode_name, template_used, converted_to_analysis, session_id)
                VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (
                timestamp,
                mode_name,
                template_used,
                converted,
                session_id
            ))
            
            if _db_type == 'postgresql':
                cursor.execute("SELECT LASTVAL()")
                return cursor.fetchone()[0]
            else:
                return cursor.lastrowid
            
    except Exception as e:
        logger.error(f"Error logging mode usage: {e}", exc_info=True)
        return None


def log_consultation_request(
    user_email: str,
    user_name: str = "",
    product_query: str = "",
    message: str = "",
    analysis_id: Optional[int] = None
) -> Optional[int]:
    """Log a consultation request."""
    try:
        init_database()
        
        timestamp = datetime.now().isoformat()
        placeholder = _get_placeholder()
        
        with db_session() as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO consultation_requests (
                    timestamp, user_email, user_name, product_query, message, analysis_id
                ) VALUES ({placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder}, {placeholder})
            """, (
                timestamp,
                user_email,
                user_name,
                product_query,
                message,
                analysis_id
            ))
            
            if _db_type == 'postgresql':
                cursor.execute("SELECT LASTVAL()")
                return cursor.fetchone()[0]
            else:
                return cursor.lastrowid
            
    except Exception as e:
        logger.error(f"Error logging consultation: {e}", exc_info=True)
        return None


# =============================================================================
# ANALYTICS FUNCTIONS
# =============================================================================

def _fetch_rows_as_dict(cursor) -> List[Dict]:
    """Fetch rows and convert to dictionary list."""
    global _db_type
    if _db_type == 'postgresql':
        # Use RealDictCursor for PostgreSQL
        return [dict(row) for row in cursor.fetchall()]
    else:
        # SQLite Row factory already returns dict-like objects
        return [dict(row) for row in cursor.fetchall()]


def get_consultation_requests(days: int = 30, limit: int = 100) -> List[Dict]:
    """Get recent consultation requests from database."""
    try:
        placeholder = _get_placeholder()
        date_expr = _adapt_datetime_function(days)
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT 
                    id, timestamp, user_email, user_name, 
                    product_query, message, status
                FROM consultation_requests
                WHERE timestamp >= {date_expr}
                ORDER BY timestamp DESC
                LIMIT {placeholder}
            """, (limit,))
            
            return _fetch_rows_as_dict(cursor)
            
    except Exception as e:
        logger.error(f"Error getting consultation requests: {e}", exc_info=True)
        return []


def get_top_queries(limit: int = 20, days: int = 30) -> List[Dict]:
    """Get most frequent search queries."""
    try:
        placeholder = _get_placeholder()
        date_expr = _adapt_datetime_function(days)
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT user_query, COUNT(*) as count, analysis_mode
                FROM analysis_logs
                WHERE timestamp >= {date_expr}
                GROUP BY user_query, analysis_mode
                ORDER BY count DESC
                LIMIT {placeholder}
            """, (limit,))
            
            return _fetch_rows_as_dict(cursor)
            
    except Exception as e:
        logger.error(f"Error getting top queries: {e}", exc_info=True)
        return []


def get_mode_distribution(days: int = 30) -> Dict[str, int]:
    """Get distribution of analysis modes used."""
    try:
        date_expr = _adapt_datetime_function(days)
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT analysis_mode, COUNT(*) as count
                FROM analysis_logs
                WHERE timestamp >= {date_expr}
                GROUP BY analysis_mode
                ORDER BY count DESC
            """)
            
            rows = _fetch_rows_as_dict(cursor)
            return {row['analysis_mode']: row['count'] for row in rows}
            
    except Exception as e:
        logger.error(f"Error getting mode distribution: {e}", exc_info=True)
        return {}


def get_category_trends(days: int = 30) -> List[Dict]:
    """Get trending product categories."""
    try:
        date_expr = _adapt_datetime_function(days)
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT 
                    product_category,
                    COUNT(*) as search_count,
                    AVG(estimated_landed_cost) as avg_cost,
                    AVG(confidence_score) as avg_confidence
                FROM analysis_logs
                WHERE timestamp >= {date_expr}
                    AND product_category IS NOT NULL
                    AND product_category != 'Unknown'
                GROUP BY product_category
                ORDER BY search_count DESC
                LIMIT 15
            """)
            
            return _fetch_rows_as_dict(cursor)
            
    except Exception as e:
        logger.error(f"Error getting category trends: {e}", exc_info=True)
        return []


def get_risk_trends(days: int = 30) -> Dict[str, int]:
    """Get frequency of different risk factors mentioned."""
    try:
        risk_counts = {}
        date_expr = _adapt_datetime_function(days)
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT top_risk_factors
                FROM analysis_logs
                WHERE timestamp >= {date_expr}
                    AND top_risk_factors IS NOT NULL
            """)
            
            for row in _fetch_rows_as_dict(cursor):
                try:
                    risks = json.loads(row['top_risk_factors'])
                    for risk in risks:
                        risk_name = risk.get('type', str(risk)) if isinstance(risk, dict) else str(risk)
                        risk_counts[risk_name] = risk_counts.get(risk_name, 0) + 1
                except (json.JSONDecodeError, KeyError, TypeError):
                    continue
        
        return dict(sorted(risk_counts.items(), key=lambda x: x[1], reverse=True))
        
    except Exception as e:
        logger.error(f"Error getting risk trends: {e}", exc_info=True)
        return {}


def get_daily_stats(days: int = 30) -> List[Dict]:
    """Get daily analysis counts."""
    try:
        date_expr = _adapt_datetime_function(days)
        date_func = _adapt_date_function('timestamp')
        
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            cursor.execute(f"""
                SELECT 
                    {date_func} as date,
                    COUNT(*) as count,
                    COUNT(DISTINCT session_id) as unique_sessions
                FROM analysis_logs
                WHERE timestamp >= {date_expr}
                GROUP BY {date_func}
                ORDER BY date DESC
            """)
            
            return _fetch_rows_as_dict(cursor)
            
    except Exception as e:
        logger.error(f"Error getting daily stats: {e}", exc_info=True)
        return []


def get_conversion_funnel() -> Dict:
    """Get conversion funnel metrics."""
    try:
        with db_session() as conn:
            cursor = conn.cursor()
            if _db_type == 'postgresql':
                cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Mode card clicks
            cursor.execute("SELECT COUNT(*) as count FROM mode_usage")
            mode_clicks = _fetch_rows_as_dict(cursor)[0]['count']
            
            # Converted to analysis
            cursor.execute("SELECT COUNT(*) as count FROM mode_usage WHERE converted_to_analysis = TRUE")
            mode_conversions = _fetch_rows_as_dict(cursor)[0]['count']
            
            # Total analyses
            cursor.execute("SELECT COUNT(*) as count FROM analysis_logs")
            total_analyses = _fetch_rows_as_dict(cursor)[0]['count']
            
            # Consultation requests
            cursor.execute("SELECT COUNT(*) as count FROM consultation_requests")
            consultations = _fetch_rows_as_dict(cursor)[0]['count']
            
            return {
                "mode_card_clicks": mode_clicks,
                "mode_to_analysis": mode_conversions,
                "total_analyses": total_analyses,
                "consultation_requests": consultations,
                "conversion_rate": round(consultations / total_analyses * 100, 1) if total_analyses > 0 else 0
            }
            
    except Exception as e:
        logger.error(f"Error getting conversion funnel: {e}", exc_info=True)
        return {}


# =============================================================================
# STREAMLIT ANALYTICS DASHBOARD
# =============================================================================

def render_analytics_dashboard():
    """Render internal analytics dashboard for NexSupply team."""
    
    st.title("📊 NexSupply Analytics Dashboard")
    
    # Show database type
    global _db_type
    if _db_type is None:
        _db_type = _detect_db_type()
    
    db_badge = "🐘 PostgreSQL" if _db_type == 'postgresql' else "💾 SQLite"
    st.markdown(f"*Internal business intelligence and trend analysis | {db_badge}*")
    
    # Time range selector
    days = st.selectbox("Time Range", [7, 14, 30, 90], index=2, format_func=lambda x: f"Last {x} days")
    
    st.markdown("---")
    
    # Key Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    funnel = get_conversion_funnel()
    
    with col1:
        st.metric("Total Analyses", funnel.get("total_analyses", 0))
    with col2:
        st.metric("Mode Card Clicks", funnel.get("mode_card_clicks", 0))
    with col3:
        st.metric("Consultation Requests", funnel.get("consultation_requests", 0))
    with col4:
        st.metric("Conversion Rate", f"{funnel.get('conversion_rate', 0)}%")
    
    st.markdown("---")
    
    # Consultation Requests Section
    st.subheader("💬 Consultation Requests")
    consultation_requests = get_consultation_requests(days=days, limit=50)
    
    if consultation_requests:
        st.info(f"📊 **{len(consultation_requests)} requests** saved to database")
        
        for req in consultation_requests[:20]:
            with st.expander(f"📧 {req.get('user_email', 'No email')} - {str(req.get('timestamp', ''))[:10]}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Email:** {req.get('user_email', 'N/A')}")
                    st.write(f"**Name:** {req.get('user_name', 'N/A')}")
                    st.write(f"**Status:** {req.get('status', 'pending')}")
                with col2:
                    st.write(f"**Product/Query:** {req.get('product_query', 'N/A')[:100]}")
                    if req.get('message'):
                        st.write(f"**Message:** {req.get('message', '')[:200]}")
    else:
        st.info("No consultation requests yet")
    
    st.markdown("---")
    
    # Two column layout
    left_col, right_col = st.columns(2)
    
    with left_col:
        # Top Queries
        st.subheader("🔍 Top Search Queries")
        top_queries = get_top_queries(limit=10, days=days)
        if top_queries:
            for q in top_queries:
                st.markdown(f"**{q['count']}x** · {q['user_query'][:50]}...")
        else:
            st.info("No data yet")
        
        st.markdown("---")
        
        # Mode Distribution
        st.subheader("📊 Analysis Mode Distribution")
        mode_dist = get_mode_distribution(days=days)
        if mode_dist:
            import plotly.express as px
            fig = px.pie(
                values=list(mode_dist.values()),
                names=list(mode_dist.keys()),
                hole=0.4
            )
            fig.update_layout(height=300, margin=dict(t=20, b=20, l=20, r=20))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data yet")
    
    with right_col:
        # Category Trends
        st.subheader("📦 Trending Categories")
        categories = get_category_trends(days=days)
        if categories:
            for cat in categories[:8]:
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{cat['product_category']}**")
                with col_b:
                    st.markdown(f"`{cat['search_count']} searches`")
        else:
            st.info("No data yet")
        
        st.markdown("---")
        
        # Risk Trends
        st.subheader("⚠️ Common Risk Factors")
        risks = get_risk_trends(days=days)
        if risks:
            for risk, count in list(risks.items())[:6]:
                st.markdown(f"• **{risk}**: {count} mentions")
        else:
            st.info("No data yet")
    
    # Daily Activity Chart
    st.markdown("---")
    st.subheader("📈 Daily Activity")
    
    daily = get_daily_stats(days=days)
    if daily:
        import plotly.express as px
        import pandas as pd
        df = pd.DataFrame(daily)
        fig = px.line(df, x='date', y='count', markers=True)
        fig.update_layout(height=250, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No activity data yet")


# =============================================================================
# INITIALIZATION
# =============================================================================

# Initialize database on module import
try:
    init_database()
except Exception as e:
    logger.warning(f"Database initialization warning: {e}")
