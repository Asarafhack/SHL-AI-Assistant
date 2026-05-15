# SHL AI Assistant

Conversational SHL assessment recommender built using FastAPI, FAISS, and SentenceTransformers.

## Features

- Conversational assessment recommendation
- Clarification handling
- Multi-turn refinement
- Assessment comparison
- Prompt injection protection
- Semantic retrieval using embeddings
- SHL catalog grounding

## Tech Stack

- FastAPI
- SentenceTransformers
- FAISS
- Python

## Run Locally

```bash
pip install -r requirements.txt
python embeddings/build_embeddings.py
python -m uvicorn app.main:app --reload