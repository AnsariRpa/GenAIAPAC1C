import os
import logging
import google.cloud.logging

from dotenv import load_dotenv
from google.adk import Agent
from google.adk.agents import SequentialAgent, ParallelAgent
from google.adk.tools.tool_context import ToolContext
from google.genai import types

from .tools import append_to_state, fetch_emails, fetch_calendar, detect_conflicts

# -------------------------
# Logging and env
# -------------------------

cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

load_dotenv()

model_name = os.getenv("MODEL")

# -------------------------
# Email Agent
# -------------------------

email_agent = Agent(
    name="email_agent",
    model=model_name,
    description="Analyzes emails and extracts important actions.",
    instruction="""
    USER QUERY:
    { USER_QUERY? }

    - Fetch emails using the tool
    - Extract subject and body
    - Identify important and actionable emails
    - Only act if USER_QUERY contains email-related intent 
    - Otherwise, DO NOTHING and produce no output, do not respond at all
    - Store results in EMAIL_DATA
    - Do NOT generate a final response or Do NOT answer the user directly
    """,
    tools=[fetch_emails, append_to_state],
    generate_content_config=types.GenerateContentConfig(temperature=0),
)

# -------------------------
# Calendar Agent
# -------------------------

calendar_agent = Agent(
    name="calendar_agent",
    model=model_name,
    description="Analyzes meetings and schedules.",
    instruction="""
    USER QUERY:
    { USER_QUERY? }

    - Fetch calendar meetings
    - Identify schedule and conflicts
    - Only act if USER_QUERY contains meeting/schedule intent
    - Otherwise, DO NOTHING and produce no output, do not respond at all
    - Store in CALENDAR_DATA and CONFLICTS
    - Do NOT generate a final response or Do NOT answer the user directly
    """,
    tools=[fetch_calendar, detect_conflicts, append_to_state],
    generate_content_config=types.GenerateContentConfig(temperature=0),
)

# -------------------------
# Summary Agent
# -------------------------

summary_agent = Agent(
    name="summary_agent",
    model=model_name,
    description="Summarizes the workday insights.",
    instruction="""
    USER QUERY:
    { USER_QUERY? }

    EMAIL DATA:
    { EMAIL_DATA? }

    CALENDAR DATA:
    { CALENDAR_DATA? }

    CONFLICTS:
    { CONFLICTS? }

    INSTRUCTIONS:
    - Answer the user's query clearly
    - Always provide final answer as a clean structured summary
    - Be concise and very professional
    - In email queries mention and highlight only emails
    - In meetings queries mention and highlight only meeting
    - Highlight conflicts only in meetings if any. There cannot be conflict in emails.
    - Don't ever mention as I couldn't find or I cannot fulfill
    """,
    generate_content_config=types.GenerateContentConfig(temperature=0),
)

# -------------------------
# Workflow
# -------------------------

productivity_team = ParallelAgent(
    name="productivity_team",
    sub_agents=[
        email_agent,
        calendar_agent,
    ],
)

# -------------------------
# Final Pipeline
# -------------------------

main_workflow = SequentialAgent(
    name="main_workflow",
    sub_agents=[
        productivity_team,
        summary_agent,
    ],
)

# -------------------------
# Root Agent
# -------------------------

root_agent = Agent(
    name="workday_assistant",
    model=model_name,
    description="Helps users manage emails, meetings, and tasks.",
    instruction="""
    - Ask user what they want to know about their workday
    - Use the append_to_state tool to store user input in USER_QUERY
    - Then continue the workflow based on the query
    - If the query is about emails, use email_agent
    - If the query is about meetings, calendar, or schedule, use calendar_agent
    """,
    tools=[append_to_state],
    sub_agents=[main_workflow],
    generate_content_config=types.GenerateContentConfig(temperature=0),
)