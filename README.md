GenAI APAC Hackathon – Personal Workday Assistant
________________________________________
Overview
This project is a Personal Workday AI Assistant which helps automate daily productivity tasks like checking emails, tracking meetings, and summarizing content.
Instead of switching between tools, user can just ask one query and get the required information.
Built using Google ADK + Vertex AI (Gemini) and deployed on Cloud Run.
________________________________________
What it does
•	Fetches and filters important emails
•	Retrieves meeting details
•	Summarizes email content
•	Routes user query to the correct agent automatically
________________________________________
Architecture (Simple View)
User Query → Orchestrator → Specialized Agents → Tools → Response
Components:
•	Agents: Email Agent, Calendar Agent, Summarizer Agent
•	Tools: Email API, Calendar API
•	Orchestrator: Routes queries intelligently
•	LLM: Gemini (Vertex AI)
________________________________________
Example Queries
•	"Show my important emails"
•	"Summarize the latest email"
•	"What meetings do I have today?"
________________________________________
Tech Stack
•	Python
•	FastAPI
•	Google ADK
•	Vertex AI (Gemini)
•	Docker
•	Google Cloud Run
________________________________________
Deployment
The application is containerized and deployed on Google Cloud Run, making it scalable and serverless.
________________________________________
Configuration
Environment variables are used for configuration.
Refer:
.env.example
________________________________________
Run Locally
pip install -r requirements.txt
uvicorn main:app --reload
________________________________________
API
POST /query
Example:
{
  "query": "Summarize my latest email"
}
________________________________________
Highlights
•	Multi-agent architecture
•	Clean separation of agents and tools
•	Cloud-native deployment
•	No secrets exposed
________________________________________
Author
Mohammed Ansari
________________________________________
Hackathon Submission
GenAI APAC Hackathon Cohort 1 – Personal Workday Assistant

