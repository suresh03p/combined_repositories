"""Day21 RAG Module"""
from typing import *

import pdfplumber, json

def extract_pdfs(pdf_paths):
    records=[]
    for pdf_path in pdf_paths:
        with pdfplumber.open(pdf_path) as pdf:
            for page_no,page in enumerate(pdf.pages,start=1):
                records.append({"document":pdf_path,"page":page_no,"text":page.extract_text() or ""})
    return records
