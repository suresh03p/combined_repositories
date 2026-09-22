"""Day21 RAG Module"""
from typing import *

def fixed_chunk(text,size=512,overlap=50):
    chunks=[];start=0
    while start<len(text):
        chunks.append(text[start:start+size])
        start+=max(1,size-overlap)
    return chunks
