import os
from fastapi import FastAPI
from pydantic import BaseModel

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from personal_assistant.agent import root_agent

app = FastAPI()

# Initialize ADK services
session_service = InMemorySessionService()

runner = Runner(
    agent=root_agent,
    app_name="workday_assistant",
    session_service=session_service
)

# Request model
class QueryRequest(BaseModel):
    query: str
    session_id: str = "default-session"

# Health check
@app.get("/")
def read_root():
    return {"status": "Workday Assistant API is running"}

# Main endpoint

@app.post("/query")
async def query_agent(request: QueryRequest):
    try:
        import uuid

        events = []
        user_id = "default-user"

        # ALWAYS create a fresh session
        session_id = str(uuid.uuid4())

        await session_service.create_session(
            app_name="workday_assistant",
            user_id=user_id,
            session_id=session_id
        )

        # Message
        user_message = types.Content(
            role="user",
            parts=[types.Part(text=request.query)]
        )

        async for event in runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_message
        ):
            events.append(event)

        final_response = ""

        for e in events:
            try:
                if hasattr(e, "content") and e.content:
                    if hasattr(e.content, "parts"):
                        for part in e.content.parts:
                            if hasattr(part, "text") and part.text:
                                final_response = part.text
                    else:
                        final_response = str(e.content)
            except Exception:
                continue

        return {"response": final_response or "No response generated."}

    except Exception as e:
        return {"error": str(e)}