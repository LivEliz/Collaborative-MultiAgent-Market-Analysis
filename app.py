import streamlit as st
import json
import re
from agents.crew_setup import create_crew

# ==============================
# Page Configuration
# ==============================
st.set_page_config(
    page_title="AI Market Analysis System",
    layout="wide"
)

st.title("🤖 Collaborative Multi-Agent Market Analysis System")
st.write("Using CrewAI + RAG")

# ==============================
# Session State Initialization
# ==============================
if "result" not in st.session_state:
    st.session_state.result = None

# ==============================
# User Input
# ==============================
query = st.text_area("Enter Market Analysis Query:", height=100)

run_button = st.button("🚀 Run Analysis")

# ==============================
# Run Crew Only When Clicked
# ==============================
if run_button:

    if not query.strip():
        st.warning("Please enter a query.")
    else:
        with st.spinner("Running agents... Please wait."):

            try:
                crew = create_crew(query)
                st.session_state.result = crew.kickoff()
            except Exception as e:
                st.error(f"Crew execution failed: {e}")
                st.stop()

# ==============================
# Display Results
# ==============================
if st.session_state.result:

    st.success("Analysis Complete!")

    result = st.session_state.result

    # -----------------------------------
    # Extract Final Output Properly
    # -----------------------------------
    try:
        # If CrewOutput object
        if hasattr(result, "tasks_output") and result.tasks_output:
            final_output = result.tasks_output[-1].raw
        else:
            final_output = result

        # Clean markdown JSON if present
        if isinstance(final_output, str):
            cleaned = re.sub(r"```json|```", "", final_output).strip()
            data = json.loads(cleaned)
        else:
            data = final_output

    except Exception:
        st.error("Model did not return valid JSON.")
        st.code(str(result))
        st.stop()

    # ==========================
    # 📈 Trends Section
    # ==========================
    st.subheader("📈 Trends")

    trends = data.get("trends", [])
    if trends:
        for trend in trends:
            st.write("•", trend)
    else:
        st.info("No trends detected.")

    # ==========================
    # 😊 Sentiment Summary
    # ==========================
    st.subheader("😊 Sentiment Summary")

    sentiment = data.get("sentiment_summary", {})

    col1, col2, col3 = st.columns(3)
    col1.metric("Positive", sentiment.get("positive", "N/A"))
    col2.metric("Negative", sentiment.get("negative", "N/A"))
    col3.metric("Neutral", sentiment.get("neutral", "N/A"))

    # ==========================
    # 🏆 Competitor Insights
    # ==========================
    st.subheader("🏆 Competitor Insights")

    competitor_data = data.get("competitor_insights", [])

    if competitor_data:
        for item in competitor_data:
            brand = item.get("brand", "Competitor")
            with st.expander(brand):
                for key, value in item.items():
                    if key != "brand":
                        st.write(f"**{key.replace('_',' ').title()}**:", value)
    else:
        st.info("No competitor insights found.")

    # ==========================
    # 💡 Recommendations
    # ==========================
    st.subheader("💡 Recommendations")

    recommendations = data.get("recommendations", [])

    if recommendations:
        for rec in recommendations:
            st.write("•", rec)
    else:
        st.info("No recommendations generated.")

    # ==========================
    # 📥 Download Button
    # ==========================
    st.download_button(
        label="⬇ Download Full JSON Report",
        data=json.dumps(data, indent=4),
        file_name="market_analysis_report.json",
        mime="application/json"
    )