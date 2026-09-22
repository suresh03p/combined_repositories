"""Day21 RAG Module"""
from typing import *

class VectorStore:
    def __init__(self): self.docs={}
    def add_documents(self,docs):
        for d in docs: self.docs[d['chunk_id']]=d
    def search(self,q,k=5): return list(self.docs.values())[:k]
    def delete_document(self,id): self.docs.pop(id,None)
    def get_document(self,id): return self.docs.get(id)
