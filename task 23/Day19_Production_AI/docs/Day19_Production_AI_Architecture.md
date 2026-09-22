# Understand Production AI Architecture

## Training code

```text
Python -> Model -> Prediction
```

Training code is usually an experiment: load data, fit or call a model, inspect a result. A notebook is stateful, often single-user, and can tolerate manual steps.

## AI application

```text
Client -> API -> Authentication -> Business Logic -> RAG / Agent -> LLM
       -> Database -> Cache -> Logging -> Monitoring
```

A production service must handle many users, malformed requests, secrets, timeouts, retries, cost, persistent conversation history, observability, and failures in dependent services. The API is the stable boundary; services own business behavior; agents and RAG own model context; databases preserve durable state; Redis handles fast temporary state; logs and metrics make incidents diagnosable.

## Request flow

```text
Client -> HTTP request -> FastAPI -> endpoint -> service -> response
```

The notebook answers one question. The application must answer questions reliably, repeatedly, securely, and with evidence about what happened.
