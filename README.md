Collaborative Multi-Agent Market Analysis System

Project Overview

This project implements a collaborative multi-agent market analysis system using CrewAI and Retrieval-Augmented Generation (RAG). The system analyzes large-scale product reviews and generates structured business insights to support data-driven decision-making.
The architecture combines embedding-based retrieval with specialized AI agents to extract trends, sentiment, competitor insights, and recommendations.

System Architecture

Phase 1: Data Engineering

Cleaned and preprocessed Amazon reviews dataset

Structured review data for analysis

Removed duplicates and irrelevant entries


Phase 2: RAG System

SentenceTransformers-based embeddings

FAISS vector database for similarity search

Metadata filtering (rating, category, etc.)

CrewAI-ready retrieval API


Phase 3: Multi-Agent Analysis

Using CrewAI, specialized agents perform:

Trend analysis

Sentiment classification

Competitor insight extraction

Structured business report generation

Tech Stack

Python

CrewAI

FAISS

SentenceTransformers

Streamlit (for UI)

Ollama (local LLM support)


Features
-Retrieval-Augmented Generation (RAG) pipeline

-Multi-agent collaborative analysis

-Structured JSON output

-Streamlit-based interactive UI

-Downloadable analysis reports

-Local LLM support via Ollama

Scalable architecture

