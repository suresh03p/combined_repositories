"""Streamlit dashboard for changing retrieval configuration."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1]))
import streamlit as st
from rag.advanced_rag import AdvancedRAG

st.set_page_config(page_title="RAG Retrieval Lab", layout="wide")
st.title("RAG Retrieval Lab")
st.caption("Change the configuration, then inspect the grounded result and its sources.")
chunk_size = st.sidebar.slider("Chunk size", 128, 1024, 500, step=64)
overlap = st.sidebar.slider("Chunk overlap", 0, min(300, chunk_size - 1), 50, step=10)
top_k = st.sidebar.slider("Top-K", 1, 20, 5)
semantic_weight = st.sidebar.slider("Semantic weight", 0.0, 1.0, 0.7, step=0.1)
keyword_weight = 1.0 - semantic_weight
query = st.text_input("Query", "How many annual leave days do employees receive?")
if st.button("Search", type="primary"):
    pipeline = AdvancedRAG(chunk_size=chunk_size, overlap=overlap)
    result = pipeline.ask(query, k=top_k)
    st.subheader("Answer")
    st.write(result["answer"])
    st.subheader("Sources")
    st.dataframe(result["sources"], use_container_width=True)
    st.info(f"Semantic weight: {semantic_weight:.1f} | Keyword weight: {keyword_weight:.1f} | Indexed chunks: {len(pipeline.documents)}")
