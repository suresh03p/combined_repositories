"""Day21 RAG Module"""
from typing import *

def recursive_chunk(text,max_size=512):
    paras=text.split("

")
    out=[]
    for p in paras:
        if len(p)<=max_size: out.append(p)
        else: out.extend([p[i:i+max_size] for i in range(0,len(p),max_size)])
    return out
