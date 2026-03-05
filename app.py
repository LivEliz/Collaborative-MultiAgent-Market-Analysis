import streamlit as st
import json
import re
import time
import pandas as pd
from datetime import datetime, date

# Import modules
from insight_engine.insight_engine import generate_insights
from mock_data import MOCK_AGENT_OUTPUT

# ==============================
# Page Configuration & CSS
# ==============================
st.set_page_config(
    page_title="Market Analysis System",
    page_icon="bar-chart",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Pastel Glassmorphism Aesthetic CSS
st.markdown("""
<style>
    /* Premium Typography */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Outfit', sans-serif !important;
        background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
        color: #475569; /* Soft Slate for text */
    }

    /* Soft Animated Pastel Hero Title */
    .hero-title {
        background: linear-gradient(to right, #ffb6c1, #c8a2c8, #add8e6);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradient 5s ease infinite;
        font-weight: 900;
        font-size: 3.5rem;
        letter-spacing: -1px;
        margin-bottom: 0;
        text-shadow: 0px 4px 15px rgba(200, 162, 200, 0.2);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .hero-subtitle {
        color: #64748b;
        font-size: 1.2rem;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 2rem;
        opacity: 0.9;
    }

    /* Light Frosted Glass Cards */
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.8);
        border-radius: 24px;
        padding: 28px;
        margin-bottom: 24px;
        box-shadow: 0 10px 40px -10px rgba(0, 0, 0, 0.05), inset 0 1px 0 rgba(255,255,255,1);
        transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 50px -15px rgba(200, 162, 200, 0.3);
        border: 1px solid rgba(200, 162, 200, 0.5);
    }

    /* Pastel Metric Aesthetics */
    .metric-value {
        font-size: 4rem;
        font-weight: 800;
        color: #334155;
        line-height: 1.1;
    }
    
    .metric-value-text {
        font-size: 2.5rem;
        font-weight: 800;
        color: #334155;
        line-height: 1.1;
    }
    
    .metric-label {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        color: #94a3b8;
        font-weight: 600;
        margin-bottom: 5px;
    }

    /* Elegant Pastel Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 15px;
        background-color: transparent;
        border-bottom: 2px solid rgba(0,0,0,0.05);
        padding-bottom: 5px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border: none;
        padding: 10px 20px;
        color: #94a3b8;
        font-size: 1.1rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #64748b;
    }
    .stTabs [aria-selected="true"] {
        color: #475569 !important;
        background-color: transparent;
        border-bottom: 3px solid #c8a2c8;
    }
    
    .stTabs [aria-selected="true"] span {
        background: linear-gradient(to right, #ffb6c1, #add8e6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }

    /* Soft Pill Button */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #ffc3a0 0%, #ffafbd 100%);
        color: white !important;
        font-weight: 700;
        font-size: 1.1rem;
        border: none;
        padding: 16px;
        border-radius: 30px; /* Fully rounded elegant pill */
        transition: all 0.4s ease;
        box-shadow: 0 8px 25px rgba(255, 175, 189, 0.4);
    }
    .stButton>button:hover {
        box-shadow: 0 12px 35px rgba(255, 175, 189, 0.6);
        transform: scale(1.02) translateY(-2px);
    }
    
    /* Elegant Text Area */
    .stTextArea textarea {
        background-color: rgba(255, 255, 255, 0.7) !important;
        border: 2px solid rgba(255, 255, 255, 0.9) !important;
        border-radius: 16px !important;
        color: #475569 !important;
        font-size: 1.1rem !important;
        padding: 18px !important;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.02), 0 4px 15px rgba(0,0,0,0.02) !important;
        transition: all 0.3s ease;
    }
    .stTextArea textarea:focus {
        border-color: #ffb6c1 !important;
        box-shadow: 0 0 0 4px rgba(255, 182, 193, 0.2) !important;
        background-color: rgba(255, 255, 255, 0.9) !important;
    }

    /* Sidebar Clean Pastel Style */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #fdfbfb 0%, #f5f7fa 100%) !important;
        border-right: 1px solid rgba(0, 0, 0, 0.04) !important;
    }
    [data-testid="stSidebar"] * {
        color: #64748b !important;
    }
    
    /* Make top banner invisible to hide streamlit defaults */
    header {visibility: hidden;}
    
    /* Custom spacing */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
    }
</style>
""", unsafe_allow_html=True)

# ==============================
# Helper Data Load
# ==============================
@st.cache_data
def load_data():
    try:
        return pd.read_csv("data/cleaned_reviews.csv")
    except Exception:
        return pd.DataFrame()

df = load_data()

# ==============================
# Session State Initialization
# ==============================
if "result" not in st.session_state:
    st.session_state.result = None
if "insights" not in st.session_state:
    st.session_state.insights = None
if "execution_time" not in st.session_state:
    st.session_state.execution_time = 0

# ==============================
# 🎛️ Sidebar Configuration
# ==============================
with st.sidebar:
    st.markdown("### Control Panel")
    
    st.markdown("#### Filter Data Context")
    
    # Category Filter
    categories = ["All"] + list(df['category'].dropna().unique()) if not df.empty else ["All"]
    selected_category = st.selectbox("Product Category", options=categories)
    
    # Time Range Filter
    min_date = pd.to_datetime(df['date']).min().date() if not df.empty else date(2010, 1, 1)
    max_date = pd.to_datetime(df['date']).max().date() if not df.empty else date.today()
    selected_dates = st.slider("Time Range", min_value=min_date, max_value=max_date, value=(min_date, max_date))
    
    st.markdown("---")
    
    # System Mode
    st.markdown("#### System Settings")
    demo_mode = st.toggle("Simulation Mode", value=True, help="Run simulation using pre-computed data.")
    
    if st.session_state.result:
        st.markdown("---")
        st.markdown("#### Export")
        st.download_button(
            label="Download JSON Report",
            data=json.dumps(st.session_state.result, indent=4),
            file_name=f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )
    
    st.markdown("---")

# ==============================
# Main UI Header
# ==============================
st.markdown("<h1 class='hero-title'>Multi-Agent Market Intelligence</h1>", unsafe_allow_html=True)
st.markdown("<p class='hero-subtitle'>Collaborative Analysis • RAG • Real-time Trend Extraction</p>", unsafe_allow_html=True)

# Input area
query = st.text_area("What would you like to analyze?", height=100, placeholder="e.g. 'Analyze the reviews for tablet battery life and display quality.'")

# ==============================
# 🚀 Execution Flow
# ==============================
col1, col2, col3 = st.columns([1, 2, 1])

if col2.button("Execute Collaborative Analysis"):
    if not query.strip():
        st.warning("Please enter a query first.")
    else:
        with st.spinner("Processing analysis..."):
            start_time = time.time()
            
            if demo_mode:
                # Simulate processing time
                time.sleep(2)
                st.session_state.result = MOCK_AGENT_OUTPUT
            else:
                try:
                    from agents.crew_setup import create_crew
                    crew = create_crew(query)
                    result_obj = crew.kickoff()
                    
                    # Clean output extraction
                    if hasattr(result_obj, "tasks_output") and result_obj.tasks_output:
                        raw_output = result_obj.tasks_output[-1].raw
                    else:
                        raw_output = str(result_obj)
                        
                    cleaned = re.sub(r"```json|```", "", raw_output).strip()
                    st.session_state.result = json.loads(cleaned)
                    
                except Exception as e:
                    st.error(f"Execution failed. Ensure Ollama is running (`ollama run llama3.2:3b`). Error: {e}")
                    st.stop()
            
            # Generate charts/insight struct
            st.session_state.insights = generate_insights(st.session_state.result)
            st.session_state.execution_time = round(time.time() - start_time, 2)
            st.rerun()

# ==============================
# 📊 Results Dashboard
# ==============================
if st.session_state.result and st.session_state.insights:
    st.markdown("---")
    data = st.session_state.result
    ins = st.session_state.insights
    
    # 🚨 Risk Alert (if applicable)
    if ins['risk_alert']:
        st.error(f"**ALERT:** {ins['risk_alert']}")
        
    # Create Tabs
    tabs = st.tabs(["Overview", "Trends", "Sentiment", "Competitors", "SWOT Grid", "Data Explorer"])

    # --- TAB 1: OVERVIEW ---
    with tabs[0]:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <div class='metric-label'>Trend Score</div>
                <div class='metric-value' style='color: {"#10b981" if ins["trend_score"] > 0 else "#ef4444"};'>{ins['trend_score']}</div>
                <div style='color: #94a3b8; font-size: 0.8rem; margin-top: 8px;'>Range: -100 to 100</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <div class='metric-label'>Response Time</div>
                <div class='metric-value'>{st.session_state.execution_time}<span style='font-size: 1.5rem;'>s</span></div>
                <div style='color: #94a3b8; font-size: 0.8rem; margin-top: 8px;'>End-to-End Latency</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            total_s = int(data['sentiment_summary']['positive']) + int(data['sentiment_summary']['negative']) + int(data['sentiment_summary']['neutral'])
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <div class='metric-label'>Insight Volume</div>
                <div class='metric-value'>{total_s}</div>
                <div style='color: #94a3b8; font-size: 0.8rem; margin-top: 8px;'>Classified Signals</div>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown(f"""
            <div class='glass-card' style='text-align: center;'>
                <div class='metric-label'>Mode</div>
                <div class='metric-value-text'>{"Simulated" if demo_mode else "Live"}</div>
                <div style='color: #94a3b8; font-size: 0.8rem; margin-top: 8px;'>Processing Pipeline</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### System Recommendations")
        recs = data.get("recommendations", [])
        for i, rec in enumerate(recs, 1):
            st.markdown(f"""
            <div style='background: rgba(30, 41, 59, 0.4); border-left: 4px solid #8b5cf6; padding: 12px 20px; border-radius: 4px; margin-bottom: 12px;'>
                <strong style='color: #8b5cf6;'>Priority {i}</strong>: {rec}
            </div>
            """, unsafe_allow_html=True)


    # --- TAB 2: TRENDS ---
    with tabs[1]:
        st.markdown("<br>", unsafe_allow_html=True)
        t_col1, t_col2 = st.columns([1, 1])
        
        with t_col1:
            st.markdown("### Extracted Micro-Trends")
            trends = data.get("trends", [])
            for trend in trends:
                st.markdown(f"""
                <div class='glass-card' style='padding: 16px; margin-bottom: 12px;'>
                    <span style='color: #2dd4bf; margin-right: 10px;'>✦</span> {trend}
                </div>
                """, unsafe_allow_html=True)
                
        with t_col2:
            st.markdown("### Theme Frequency Indicator")
            if ins['charts']['keywords']:
                st.plotly_chart(ins['charts']['keywords'], use_container_width=True, config={'displayModeBar': False})
            else:
                st.info("Insufficient text data to map frequencies.")


    # --- TAB 3: SENTIMENT ---
    with tabs[2]:
        st.markdown("<br>", unsafe_allow_html=True)
        s_col1, s_col2 = st.columns([1, 1])
        
        with s_col1:
            st.markdown("### Emotional Distribution")
            st.plotly_chart(ins['charts']['sentiment'], use_container_width=True, config={'displayModeBar': False})
            
        with s_col2:
            st.markdown("### Breakdown Metrics")
            st.markdown(f"""
            <div class='glass-card' style='border-left: 4px solid #10b981;'>
                <h2 style='margin:0;'>{data['sentiment_summary']['positive']}</h2>
                <div class='metric-label'>Positive Mentions</div>
            </div>
            
            <div class='glass-card' style='border-left: 4px solid #ef4444;'>
                <h2 style='margin:0;'>{data['sentiment_summary']['negative']}</h2>
                <div class='metric-label'>Negative Critical Alerts</div>
            </div>
            
            <div class='glass-card' style='border-left: 4px solid #6b7280;'>
                <h2 style='margin:0;'>{data['sentiment_summary']['neutral']}</h2>
                <div class='metric-label'>Neutral Observations</div>
            </div>
            """, unsafe_allow_html=True)


    # --- TAB 4: COMPETITORS ---
    with tabs[3]:
        st.markdown("<br>", unsafe_allow_html=True)
        comps = data.get("competitor_insights", [])
        if not comps:
            st.info("No explicit competitor mentions identified in the dataset context.")
        else:
            grid_cols = st.columns(3)
            for i, comp in enumerate(comps):
                with grid_cols[i % 3]:
                    st.markdown(f"""
                    <div class='glass-card' style='text-align: center;'>
                        <div style='font-size: 3rem; margin-bottom: 10px;'></div>
                        <h3 style='color: #2dd4bf; margin-bottom: 16px;'>{comp.get('brand', 'Unknown')}</h3>
                        <p style='color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;'>{comp.get('insight', '')}</p>
                    </div>
                    """, unsafe_allow_html=True)


    # --- TAB 5: SWOT ---
    with tabs[4]:
        st.markdown("<br>", unsafe_allow_html=True)
        swot = ins['swot_analysis']
        
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        def render_swot(title, items, color, col_context):
            html = f"""
            <div class='glass-card' style='border-top: 4px solid {color}; height: 100%;'>
                <h3 style='color: {color};'>{title}</h3>
                <ul style='color: #475569; line-height: 1.6; padding-left: 20px;'>
            """
            for item in items:
                html += f"<li>{item}</li>"
            html += "</ul></div>"
            col_context.markdown(html, unsafe_allow_html=True)
            
        render_swot("Strengths", swot["Strengths"], "#10b981", row1_col1)
        render_swot("Weaknesses", swot["Weaknesses"], "#ef4444", row1_col2)
        
        st.markdown("<br>", unsafe_allow_html=True) # Spacer
        
        render_swot("Opportunities", swot["Opportunities"], "#3b82f6", row2_col1)
        render_swot("Threats", swot["Threats"], "#f59e0b", row2_col2)


    # --- TAB 6: DATA EXPLORER ---
    with tabs[5]:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("### Database Evaluation Sample")
        st.markdown(f"*Showing subset of dataset context used for evaluation. Category: **{selected_category}***")
        
        # Apply filters to view
        view_df = df.copy()
        if not view_df.empty:
            if selected_category != "All":
                view_df = view_df[view_df['category'] == selected_category]
            
            view_df['date'] = pd.to_datetime(view_df['date']).dt.date
            view_df = view_df[(view_df['date'] >= selected_dates[0]) & (view_df['date'] <= selected_dates[1])]
            
            st.dataframe(
                view_df[['product_name', 'rating', 'category', 'review_text', 'date']].head(50),
                use_container_width=True,
                height=400
            )
        else:
            st.warning("Dataset not found. Please ensure data/cleaned_reviews.csv exists.")