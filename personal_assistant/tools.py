import logging
from google.adk.tools.tool_context import ToolContext

# -------------------------
# State Management Tool
# -------------------------

def append_to_state(tool_context: ToolContext, field: str, value: str) -> dict:
    existing = tool_context.state.get(field, [])
    tool_context.state[field] = existing + [value]

    logging.info(f"[STATE UPDATE] {field}: {value}")
    return {"status": "success"}


# -------------------------
# Sample MCP TOOLS
# -------------------------

def fetch_emails(tool_context: ToolContext) -> dict:
    # Placeholder → Real MCP call can be addedd here
    emails = [
    {
        "subject": "Client escalation",
        "body": "Client is unhappy with delivery. Needs response by EOD. High priority."
    },
    {
        "subject": "QBR deck update",
        "body": "Please update QBR deck with latest metrics and send before tomorrow meeting."
    }
    ]

    tool_context.state["EMAIL_DATA"] = emails
    return {"status": "success", "data": emails}


def fetch_calendar(tool_context: ToolContext) -> dict:
    # Placeholder → Real MCP call can be addedd here
    meetings = [
        {"title": "Standup", "time": "10:00-10:30"},
        {"title": "Client Call", "time": "10:15-11:00"},
        {"title": "Internal Review", "time": "11:30-12:00"}
    ]

    tool_context.state["CALENDAR_DATA"] = meetings
    return {"status": "success", "data": meetings}


def detect_conflicts(tool_context: ToolContext) -> dict:
    meetings = tool_context.state.get("CALENDAR_DATA", [])

    conflicts = []
    # Simple overlap logic (placeholder)
    if len(meetings) > 1:
        conflicts.append("Potential overlap between meetings")

    tool_context.state["CONFLICTS"] = conflicts
    return {"status": "success", "data": conflicts}