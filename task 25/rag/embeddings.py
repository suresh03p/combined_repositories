"""Day21 RAG Module"""
from typing import *

def generate_embeddings(chunks,model=None):
    return [{"chunk_id":i,"text":c,"embedding":[0.0]*384,"metadata":{}} for i,c in enumerate(chunks)]
