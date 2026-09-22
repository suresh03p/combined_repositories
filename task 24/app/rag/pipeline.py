from .access_control import filter_documents
from .retriever import retrieve

def secure_retrieve(user, query, documents):
    return retrieve(query, filter_documents(user, documents))
