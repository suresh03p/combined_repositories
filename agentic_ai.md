# Understand Agentic AI

## 1. LLM

An **LLM**, or Large Language Model, is the core AI model that understands and generates human language.

It can:

- Answer questions
- Summarize text
- Translate languages
- Write and explain code
- Generate emails, reports, and stories
- Analyze information provided in the prompt

An LLM usually does not automatically know current events or private company information. Its answer depends on its training data and the context supplied to it.

**Example:**

> "Explain how neural networks work."

The LLM generates an explanation based on its learned knowledge.

## 2. RAG

**RAG**, or Retrieval-Augmented Generation, connects an LLM to external information.

The process is:

1. The user asks a question.
2. The system searches a knowledge source.
3. Relevant documents or passages are retrieved.
4. The retrieved information is given to the LLM.
5. The LLM generates an answer using that information.

RAG helps reduce hallucinations and allows an application to use:

- Company documents
- Product manuals
- Internal databases
- Websites
- Legal documents
- Frequently asked questions
- Current information

**Example:**

> "What is our company's refund policy?"

The system searches company policy documents and uses the matching content to create the answer.

### Important limitation

RAG retrieves information, but it does not necessarily decide what to do next. The retrieval process may be fixed and simple.

## 3. Workflow

A **workflow** is a predefined sequence of steps.

The developer decides:

- Which step happens first
- Which tool is used
- What happens when a condition is met
- When the process ends
- When a human must approve the result

**Example customer-support workflow:**

1. Receive a customer question.
2. Classify the question.
3. Search the FAQ.
4. Generate a response.
5. Send the response to a human for approval.
6. Email the customer.

The workflow may use an LLM and RAG, but the overall process is predetermined.

### Workflow characteristics

- Predictable
- Easier to test
- Easier to monitor
- Usually reliable for repetitive tasks
- Less flexible when unexpected situations occur

## 4. Agent

An **agent** is an AI system that receives a goal and decides which actions to take.

Instead of following one fixed sequence, the agent can:

1. Understand the goal.
2. Plan possible steps.
3. Select a tool.
4. Observe the result.
5. Decide what to do next.
6. Repeat until the goal is completed or it needs assistance.

An agent might use:

- Search tools
- Databases
- Calculators
- APIs
- Code interpreters
- Email systems
- Calendar systems
- File systems

**Example:**

> "Find a suitable meeting time for everyone next week."

The agent may:

1. Check the participants' calendars.
2. Compare available times.
3. Consider time zones.
4. Find conflicts.
5. Propose the best available slot.

The developer controls the agent's tools and permissions, but the agent chooses how to use them.

### Important limitation

An agent should have boundaries, such as:

- Approved tools only
- Restricted file access
- Maximum number of actions
- Human approval for important operations
- Spending or security limits

## 5. Agentic RAG

**Agentic RAG** combines retrieval with agent-style decision-making.

A basic RAG system may perform one search and then generate an answer. An agentic RAG system can decide:

- What information it needs
- Which source to search
- Which search query to use
- Whether the results are relevant
- Whether more searches are required
- Whether sources disagree
- When it has enough evidence to answer

**Example question:**

> "Which software plan is best for a team of 12 that needs audit logs and advanced security?"

An agentic RAG system may:

1. Search the plan comparison documents.
2. Find information about team size.
3. Search security documentation.
4. Check whether audit logs are included.
5. Compare pricing information.
6. Notice conflicting information.
7. Search for the latest official documentation.
8. Combine the evidence.
9. Explain its recommendation and cite the sources.

This makes the system more flexible than simple RAG.

## Main Difference

The most useful distinction is:

> **RAG describes how the system obtains information. Agent describes how the system decides what to do.**

A system can therefore be:

- An LLM without retrieval
- An LLM with RAG
- A workflow using an LLM
- An agent using tools
- An agent using RAG
- An agentic RAG application

## Comparison Table

| Concept | Main purpose | Decision-making | Example |
|---|---|---|---|
| LLM | Generate or understand language | Responds to the prompt | Explain a technical topic |
| RAG | Use external information | Usually follows a fixed retrieval process | Search documents and answer |
| Workflow | Execute predefined steps | Developer defines the sequence | Classify, search, draft, approve |
| Agent | Achieve a goal using tools | Model chooses the next action | Check calendars and schedule a meeting |
| Agentic RAG | Search intelligently while solving a goal | Model decides what and when to retrieve | Search, evaluate, refine, and cite evidence |

## Simple Analogy

Imagine a student answering a question:

- **LLM:** The student answers from memory.
- **RAG:** The student looks up a paragraph in a textbook before answering.
- **Workflow:** The student follows a fixed study procedure.
- **Agent:** The student chooses whether to use a textbook, calculator, or ask someone for help.
- **Agentic RAG:** The student searches multiple sources, checks whether the information is reliable, resolves conflicts, and then gives an evidence-based answer.

## How They Work Together

A modern AI application may use all five:

1. An **LLM** interprets the user's request.
2. A **workflow** controls the overall process.
3. **RAG** retrieves relevant company information.
4. An **agent** decides whether more tools or searches are needed.
5. **Agentic RAG** lets the system refine its research before responding.

## Practical Examples

### Chatbot using an LLM

A user asks a general question, and the LLM generates a response from its learned patterns and the conversation context.

### Company knowledge assistant using RAG

A user asks about an internal policy. The system retrieves relevant documents and produces an answer grounded in those documents.

### Automated support workflow

A support request is classified, matched to a known category, answered from an FAQ, and routed to a human when confidence is low.

### Travel-planning agent

The user gives a goal such as planning a trip. The agent may search flights, compare hotels, check dates, calculate costs, and ask for confirmation before booking.

### Research assistant using Agentic RAG

The assistant searches several trusted sources, identifies missing evidence, performs additional searches, compares conflicting claims, and produces a cited summary.

## Advantages and Challenges

### LLM advantages

- Flexible language understanding
- Useful for many text-based tasks
- Easy to interact with using natural language

### LLM challenges

- May produce incorrect information
- May lack current or private data
- Can misunderstand ambiguous requests

### RAG advantages

- Uses current or private information
- Can provide source-grounded answers
- Reduces reliance on model memory

### RAG challenges

- Poor retrieval leads to poor answers
- Documents may be outdated or incomplete
- The system may retrieve irrelevant passages

### Workflow advantages

- Predictable behavior
- Easier testing and auditing
- Good for repeatable business processes

### Workflow challenges

- Can be rigid
- Requires developers to anticipate many cases
- May fail when a situation does not match the predefined path

### Agent advantages

- Handles changing situations
- Can select different tools for different tasks
- Can pursue complex goals with fewer fixed instructions

### Agent challenges

- Less predictable
- More difficult to test
- May use tools unnecessarily
- Requires strong permissions and safety controls

### Agentic RAG advantages

- Can perform multi-step research
- Can refine weak searches
- Can compare multiple sources
- Better suited to complex questions

### Agentic RAG challenges

- Higher cost and latency
- More complicated to monitor
- Can still make poor decisions
- Needs source-quality checks and action limits

## Final Summary

- **LLM:** The language and reasoning engine.
- **RAG:** External information supplied to the language model.
- **Workflow:** A predefined sequence of operations.
- **Agent:** A system that chooses actions to achieve a goal.
- **Agentic RAG:** An agent that intelligently searches, evaluates, and uses external information.

The progression can be summarized as:

> **LLM -> adds external knowledge with RAG -> organizes steps with workflows -> adds decision-making with agents -> combines intelligent decision-making and retrieval with Agentic RAG.**
