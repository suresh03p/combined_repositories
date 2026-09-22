"""Day21 RAG Module"""
from typing import *

import re

def clean_text(text:str)->str:
    text=re.sub(r'\s+',' ',text)
    return text.strip()

# Aggressive cleaning can remove meaningful terms, punctuation, headings, and structure used during retrieval.
