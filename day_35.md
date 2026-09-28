# Day 35: Multi-Agent AI

This project demonstrates a supervisor coordinating specialized agents through shared workflow state. The sequence is:

`Supervisor -> Research -> RAG -> Analysis -> Validation -> Writer`

The supervisor routes work between agents, while research, retrieval, analysis, validation, and writing remain separate stages. The workflow uses bundled JSON data and deterministic keyword matching; it runs offline and does not use live web search, embeddings, or an LLM.

Project files and full documentation: [Day35_39_Multi_Agent_AI](day_35/Day35_39_Multi_Agent_AI/README.md).

From the project directory, run with Python 3.10 or newer:

```powershell
python -m src.api.main
python -m unittest discover -s tests -v
```
