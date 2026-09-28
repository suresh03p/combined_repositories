# Agent Roles

## Supervisor Agent
Owns the workflow and shared state. Interprets the request, selects the next bounded task, delegates to one agent at a time, records its returned result, and decides what happens next. Aggregates completion and handles failures; it does not silently treat a missing result as success.

## Research Agent
Finds candidate source material for the request and returns source-attributed evidence. It does not write the final answer or control workflow progression. In this starter it searches a bundled offline source file.

## RAG Agent
Retrieves relevant passages from the local knowledge base to ground the answer. It returns documents and source metadata to the supervisor. The starter uses transparent keyword overlap, not embeddings or a vector database.

## Analysis Agent
Examines research and retrieved evidence, reports counts, and extracts simple themes. It makes its work available as structured shared-state data; it does not make unsupported claims.

## Validation Agent
Checks that a request exists and that available evidence has source metadata. It records failed checks and notes in shared state. This is a lightweight structural check, not a guarantee of factual accuracy.

## Writer Agent
Produces the final response from the available evidence, includes source names, and discloses when evidence is missing or validation found a gap.

## Ownership and Communication
The supervisor owns task routing and status. Each specialist owns only its assigned result. Communication follows `supervisor -> agent -> result -> supervisor`; the supervisor stores each result before dispatching the next stage. The shared `AgentState` is the common, serializable record, not an invitation for agents to overwrite one another's fields.
