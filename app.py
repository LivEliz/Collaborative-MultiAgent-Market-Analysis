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
# Page Configuration
# ==============================

st.set_page_config(
    page_title="Market Analysis System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================
# Helper Data Load
# ==============================

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/cleaned_reviews.csv")

        # Standardize column names
        df.columns = df.columns.str.strip().str.lower()

        # Ensure review_date exists
        if "review_date" in df.columns:
            df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")

        return df

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
# Sidebar
# ==============================

with st.sidebar:

    st.header("Control Panel")

    # ---------- Category Filter ----------

    if not df.empty and "category" in df.columns:
        categories = ["All"] + sorted(df["category"].dropna().unique())
    else:
        categories = ["All"]

    selected_category = st.selectbox("Product Category", categories)

    # ---------- Date Range ----------

    if not df.empty and "review_date" in df.columns:
        df["review_date"] = pd.to_datetime(df["review_date"], errors="coerce")
        min_date = df["review_date"].min().date()
        max_date = df["review_date"].max().date()
    else:
        min_date = date(2010,1,1)
        max_date = date.today()

    selected_dates = st.slider(
        "Time Range",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
    )

    st.divider()

    # ---------- System Mode ----------

    st.subheader("System Settings")

    demo_mode = st.toggle(
        "Simulation Mode",
        value=True,
        help="Run simulation using pre-computed data."
    )

    # ---------- Export ----------

    if st.session_state.result:

        st.divider()

        st.download_button(
            "Download JSON Report",
            data=json.dumps(st.session_state.result, indent=4),
            file_name=f"market_analysis_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
            mime="application/json"
        )


# ==============================
# Header
# ==============================

st.title("Multi-Agent Market Intelligence")

st.caption("Collaborative Analysis • RAG • Real-time Trend Extraction")

query = st.text_area(
    "What would you like to analyze?",
    placeholder="Example: Analyze tablet battery life and display quality"
)


# ==============================
# Execute Button
# ==============================

col1, col2, col3 = st.columns([1,2,1])

if col2.button("Execute Collaborative Analysis"):

    if not query.strip():
        st.warning("Please enter a query.")

    else:

        with st.spinner("Running multi-agent analysis..."):

            start_time = time.time()

            if demo_mode:

                time.sleep(2)
                st.session_state.result = MOCK_AGENT_OUTPUT

            else:

                try:

                    from agents.crew_setup import create_crew

                    crew = create_crew(query)

                    result_obj = crew.kickoff()

                    if hasattr(result_obj, "tasks_output") and result_obj.tasks_output:

                        raw_output = result_obj.tasks_output[-1].raw

                    else:

                        raw_output = str(result_obj)

                    cleaned = re.sub(r"```json|```", "", raw_output).strip()

                    st.session_state.result = json.loads(cleaned)

                except Exception as e:

                    st.error(
                        f"Execution failed. Ensure Ollama is running (`ollama run llama3.2:3b`).\n\nError: {e}"
                    )

                    st.stop()

            st.session_state.insights = generate_insights(st.session_state.result)

            st.session_state.execution_time = round(time.time() - start_time, 2)

            st.rerun()


# ==============================
# Results Dashboard
# ==============================

if st.session_state.result and st.session_state.insights:

    data = st.session_state.result
    ins = st.session_state.insights

    st.divider()

    tabs = st.tabs([
        "Overview",
        "Trends",
        "Sentiment",
        "Competitors",
        "SWOT",
        "Data Explorer"
    ])


# ==============================
# TAB 1 — Overview
# ==============================

    with tabs[0]:

        col1, col2, col3, col4 = st.columns(4)

        trend_score = ins.get("trend_score", 0)

        sentiment = data.get("sentiment_summary", {})

        total_s = (
            int(sentiment.get("positive",0)) +
            int(sentiment.get("negative",0)) +
            int(sentiment.get("neutral",0))
        )

        col1.metric("Trend Score", trend_score)

        col2.metric("Execution Time", f"{st.session_state.execution_time}s")

        col3.metric("Insight Volume", total_s)

        col4.metric("Mode", "Simulation" if demo_mode else "Live")

        st.subheader("Recommendations")

        for rec in data.get("recommendations", []):
            st.success(rec)


# ==============================
# TAB 2 — Trends
# ==============================

    with tabs[1]:

        trends = data.get("trends", [])

        if trends:

            for t in trends:
                st.write("•", t)

        else:

            st.info("No trends detected")

        if ins["charts"].get("keywords"):
            st.plotly_chart(ins["charts"]["keywords"], use_container_width=True)


# ==============================
# TAB 3 — Sentiment
# ==============================

    with tabs[2]:

        st.plotly_chart(
            ins["charts"]["sentiment"],
            use_container_width=True
        )


# ==============================
# TAB 4 — Competitors
# ==============================

    with tabs[3]:

        comps = data.get("competitor_insights", [])

        if not comps:

            st.info("No competitors detected")

        else:

            for c in comps:

                st.subheader(c.get("brand","Unknown"))

                st.write(c.get("insight",""))


# ==============================
# TAB 5 — SWOT
# ==============================

    with tabs[4]:

        swot = ins.get("swot_analysis", {})

        col1, col2 = st.columns(2)

        with col1:

            st.subheader("Strengths")
            for i in swot.get("Strengths", []):
                st.write("•", i)

            st.subheader("Opportunities")
            for i in swot.get("Opportunities", []):
                st.write("•", i)

        with col2:

            st.subheader("Weaknesses")
            for i in swot.get("Weaknesses", []):
                st.write("•", i)

            st.subheader("Threats")
            for i in swot.get("Threats", []):
                st.write("•", i)


# ==============================
# TAB 6 — Data Explorer
# ==============================

    with tabs[5]:

        if df.empty:

            st.warning("Dataset not found. Ensure data/cleaned_reviews.csv exists.")

        else:

            view_df = df.copy()

            if selected_category != "All" and "category" in view_df.columns:
                view_df = view_df[view_df["category"] == selected_category]

            if "review_date" in view_df.columns:

                view_df = view_df[
                    (view_df["review_date"].dt.date >= selected_dates[0]) &
                    (view_df["review_date"].dt.date <= selected_dates[1])
                ]

            columns = [
                c for c in [
                    "product_name",
                    "rating",
                    "category",
                    "review_text",
                    "review_date"
                ] if c in view_df.columns
            ]

            st.dataframe(
                view_df[columns].head(50),
                use_container_width=True
            )