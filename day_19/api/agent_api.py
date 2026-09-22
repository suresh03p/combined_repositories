"""
FastAPI Integration for Multi-Agent System
Exposes agent functionality through REST API.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class MessageRequest(BaseModel):
    """Request model for chat endpoint."""
    conversation_id: Optional[str] = None
    message: str


class MessageResponse(BaseModel):
    """Response model for chat endpoint."""
    answer: str
    agents_used: List[str]
    status: str
    conversation_id: str
    timestamp: str


class ToolInfo(BaseModel):
    """Information about available tool."""
    name: str
    description: str
    category: str


class StatusResponse(BaseModel):
    """Status response."""
    conversation_id: str
    status: str
    current_step: int
    total_steps: int
    agents_used: List[str]
    created_at: str
    last_updated: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    agents_available: int
    tools_available: int
    uptime_seconds: int


class MultiAgentAPI:
    """
    FastAPI-based API for multi-agent system.
    
    Endpoints:
    - POST /agent/chat - Process user request
    - GET /agent/tools - List available tools
    - GET /agent/status/{conversation_id} - Get conversation status
    - GET /health - Health check
    """
    
    def __init__(self):
        """Initialize API."""
        self.start_time = datetime.now()
        self.conversations = {}
    
    def chat(self, request: MessageRequest) -> MessageResponse:
        """
        Process user message through multi-agent system.
        
        Request:
        {
            "conversation_id": "CONV-001",
            "message": "Find my leave allowance and calculate remaining leave."
        }
        
        Response:
        {
            "answer": "You have 11 leave days remaining.",
            "agents_used": [
                "research_agent",
                "calculator_agent",
                "writer_agent"
            ],
            "status": "success",
            "conversation_id": "CONV-001",
            "timestamp": "2026-09-01T10:30:00"
        }
        """
        from workflows.supervisor import SupervisorAgent
        
        supervisor = SupervisorAgent()
        result = supervisor.process_request(request.message)
        
        conversation_id = result['conversation_id']
        self.conversations[conversation_id] = result
        
        return MessageResponse(
            answer=result['final_answer'],
            agents_used=['research_agent', 'calculator_agent', 'writer_agent'],
            status="success",
            conversation_id=conversation_id,
            timestamp=datetime.now().isoformat()
        )
    
    def get_tools(self) -> Dict[str, Any]:
        """
        Get list of available tools.
        
        Response:
        {
            "tools": [
                {
                    "name": "Vector Search",
                    "category": "Research",
                    "description": "Search documents using vector embeddings"
                },
                {
                    "name": "Calculator",
                    "category": "Calculation",
                    "description": "Perform mathematical calculations"
                },
                {
                    "name": "Formatter",
                    "category": "Writing",
                    "description": "Format and summarize content"
                }
            ],
            "total": 3
        }
        """
        tools = [
            {
                "name": "Vector Search",
                "category": "Research",
                "description": "Search documents using vector embeddings"
            },
            {
                "name": "RAG Search",
                "category": "Research",
                "description": "Retrieval-Augmented Generation search"
            },
            {
                "name": "Calculator",
                "category": "Calculation",
                "description": "Perform mathematical calculations"
            },
            {
                "name": "Formula Evaluator",
                "category": "Calculation",
                "description": "Evaluate complex formulas"
            },
            {
                "name": "Text Formatter",
                "category": "Writing",
                "description": "Format and summarize content"
            },
            {
                "name": "Report Generator",
                "category": "Writing",
                "description": "Generate professional reports"
            },
            {
                "name": "Document Search",
                "category": "Research",
                "description": "Full-text search on documents"
            },
            {
                "name": "Date Calculator",
                "category": "Calculation",
                "description": "Calculate date differences"
            }
        ]
        
        return {
            "tools": tools,
            "total": len(tools),
            "categories": list(set(t["category"] for t in tools))
        }
    
    def get_status(self, conversation_id: str) -> StatusResponse:
        """
        Get conversation status.
        
        Response:
        {
            "conversation_id": "CONV-001",
            "status": "completed",
            "current_step": 3,
            "total_steps": 3,
            "agents_used": ["research_agent", "calculator_agent", "writer_agent"],
            "created_at": "2026-09-01T10:30:00",
            "last_updated": "2026-09-01T10:30:15"
        }
        """
        if conversation_id not in self.conversations:
            return {
                "status": "error",
                "message": f"Conversation {conversation_id} not found"
            }
        
        conv = self.conversations[conversation_id]
        state = conv.get('state', {})
        
        return StatusResponse(
            conversation_id=conversation_id,
            status=state.get('status', 'unknown'),
            current_step=state.get('current_step', 0),
            total_steps=state.get('total_steps', 0),
            agents_used=list(state.get('agent_results', {}).keys()),
            created_at=state.get('created_at', ''),
            last_updated=state.get('updated_at', '')
        )
    
    def health(self) -> HealthResponse:
        """
        Health check endpoint.
        
        Response:
        {
            "status": "healthy",
            "version": "1.0.0",
            "agents_available": 3,
            "tools_available": 8,
            "uptime_seconds": 3600
        }
        """
        uptime = (datetime.now() - self.start_time).total_seconds()
        
        return HealthResponse(
            status="healthy",
            version="1.0.0",
            agents_available=3,
            tools_available=8,
            uptime_seconds=int(uptime)
        )


# FastAPI Application Example

def create_fastapi_app():
    """Create FastAPI application with all endpoints."""
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import JSONResponse
        
        app = FastAPI(
            title="Multi-Agent AI Assistant API",
            description="API for multi-agent system",
            version="1.0.0"
        )
        
        api = MultiAgentAPI()
        
        @app.post("/agent/chat")
        def chat(request: MessageRequest) -> MessageResponse:
            """Process chat message through agent system."""
            try:
                return api.chat(request)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/agent/tools")
        def get_tools():
            """Get available tools."""
            return api.get_tools()
        
        @app.get("/agent/status/{conversation_id}")
        def get_status(conversation_id: str):
            """Get conversation status."""
            try:
                return api.get_status(conversation_id)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/health")
        def health_check() -> HealthResponse:
            """Health check endpoint."""
            return api.health()
        
        return app
    
    except ImportError:
        print("FastAPI not installed. Install with: pip install fastapi uvicorn")
        return None


# API Documentation Example

API_DOCUMENTATION = """
# Multi-Agent AI Assistant API Documentation

## Base URL
```
http://localhost:8000
```

## Endpoints

### 1. Chat - Process Request
**Endpoint:** `POST /agent/chat`

**Description:** Send a request to the multi-agent system.

**Request Body:**
```json
{
    "conversation_id": "CONV-001",  # Optional
    "message": "Find my leave allowance and calculate remaining leave."
}
```

**Response (200):**
```json
{
    "answer": "You have 11 leave days remaining...",
    "agents_used": [
        "research_agent",
        "calculator_agent",
        "writer_agent"
    ],
    "status": "success",
    "conversation_id": "CONV-001",
    "timestamp": "2026-09-01T10:30:00"
}
```

**Response (500):**
```json
{
    "detail": "Error message"
}
```

---

### 2. Get Available Tools
**Endpoint:** `GET /agent/tools`

**Description:** Retrieve list of available tools.

**Response (200):**
```json
{
    "tools": [
        {
            "name": "Vector Search",
            "category": "Research",
            "description": "Search documents using vector embeddings"
        }
    ],
    "total": 8,
    "categories": ["Research", "Calculation", "Writing"]
}
```

---

### 3. Get Conversation Status
**Endpoint:** `GET /agent/status/{conversation_id}`

**Description:** Get status of a specific conversation.

**Path Parameters:**
- `conversation_id` (string): The conversation ID

**Response (200):**
```json
{
    "conversation_id": "CONV-001",
    "status": "completed",
    "current_step": 3,
    "total_steps": 3,
    "agents_used": ["research_agent", "calculator_agent"],
    "created_at": "2026-09-01T10:30:00",
    "last_updated": "2026-09-01T10:30:15"
}
```

**Response (404):**
```json
{
    "detail": "Conversation CONV-001 not found"
}
```

---

### 4. Health Check
**Endpoint:** `GET /health`

**Description:** Check API health status.

**Response (200):**
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "agents_available": 3,
    "tools_available": 8,
    "uptime_seconds": 3600
}
```

---

## Usage Examples

### Example 1: Simple Request

```bash
curl -X POST "http://localhost:8000/agent/chat" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "What is the leave policy?"
  }'
```

### Example 2: Complex Request

```bash
curl -X POST "http://localhost:8000/agent/chat" \\
  -H "Content-Type: application/json" \\
  -d '{
    "conversation_id": "CONV-001",
    "message": "Find the leave policy and calculate my remaining days if I used 7."
  }'
```

### Example 3: Check Status

```bash
curl -X GET "http://localhost:8000/agent/status/CONV-001"
```

### Example 4: Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Error Handling

All errors return appropriate HTTP status codes:

- `200` - Success
- `400` - Bad request
- `404` - Not found
- `500` - Server error

Error response format:
```json
{
    "detail": "Error description"
}
```

---

## Running the API

### Option 1: Using Uvicorn

```bash
pip install fastapi uvicorn
uvicorn api:app --reload
```

### Option 2: Using Python

```python
from api import create_fastapi_app
import uvicorn

app = create_fastapi_app()
uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## API Version History

- v1.0.0 - Initial release with 3 core agents
- Future: Token-based authentication, Rate limiting, Webhooks
"""


if __name__ == "__main__":
    # Create API instance
    api = MultiAgentAPI()
    
    # Test endpoints
    print("=== Testing Multi-Agent API ===\n")
    
    # Test health
    health = api.health()
    print(f"Health: {health}\n")
    
    # Test tools
    tools = api.get_tools()
    print(f"Available tools: {tools['total']}\n")
    
    print(API_DOCUMENTATION)
