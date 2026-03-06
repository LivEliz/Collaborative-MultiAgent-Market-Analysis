# Collaborative Multi-Agent Market Analysis System

A professional browser-based market intelligence platform powered by a Collaborative Multi-Agent System (CrewAI) and Retrieval-Augmented Generation (RAG). This system transforms large-scale raw product reviews into actionable business insights using local, open-source intelligence.

## 🔄 Project Architecture

The system follows a 5-step engineering pipeline:

1.  **Data Collection & Preprocessing**: Automated ingestion and cleaning of reviews (Pandas, NLP).
2.  **RAG Pipeline**: Vectorization of knowledge using SentenceTransformers and retrieval via FAISS.
3.  **Multi-Agent Collaborative System**: Four specialized CrewAI agents (Trend, Sentiment, Competitor, and Report) collaborating on a shared context.
4.  **Business Intelligence Layer**: Analysis of agent outputs into SWOT grids, trend scores, and risk alerts.
5.  **Interactive Dashboard**: A custom-built Streamlit interface with a pastel glassmorphism aesthetic.

---

## 👥 Responsibility Breakdown

| Member | Role | Key Technologies |
| :--- | :--- | :--- |
| **Member 1** | Data Engineer | Python, Pandas, NLTK/spaCy |
| **Member 2** | RAG Engineer | FAISS, SentenceTransformers |
| **Member 3** | Multi-Agent Architect | CrewAI, LangChain |
| **Member 4** | Insight Engineer | Data Analytics, Plotly |
| **Member 5** | Frontend & Deployment | Streamlit, CSS |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.9+
- (Optional) Ollama (for live local LLM execution)

### Installation
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the System
Run the dashboard locally using:
```bash
python -m streamlit run app.py
```

---

## 🛠 Features

### Simulation Mode (Presentation Ready)
The system includes a **Simulation Mode** that allows for instant demonstrations without requiring a running LLM instance. It uses pre-computed analysis to show the full capability of the multi-agent collaboration and visualization engine.

### Advanced Visualization
- **Dynamic Sentiment Tracking**: Responsive donut charts visualizing emotional distribution.
- **Micro-Trend Extraction**: Real-time keyword frequency analysis using local embeddings.
- **SWOT Analysis**: Automatically generated grid classifying Strengths, Weaknesses, Opportunities, and Threats.

### Privacy-First Intelligence
The entire system operates **locally**. No data is sent to external APIs (like OpenAI or Gemini). It utilizes high-performance local models for embeddings and agentic logic, ensuring data privacy and cost-efficiency.

---

## 🎨 Design Aesthetic
The dashboard features a **Premium Pastel UI** with:
- Glassmorphism components for an airy, modern feel.
- Custom Outfit typography for high-end readability.
- Animated pastel gradients to enhance user engagement.
- A fully unbranded, professional finish suitable for corporate presentations.

