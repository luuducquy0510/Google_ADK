from dotenv import load_dotenv
import os
import logging
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from agent_tool import web_search_tool, rag_tool
from google.genai import types # For creating message Content/Parts
from model import AgentResponse
import prompt as prompt


# Load environment variables from .env file
load_dotenv()
# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


AGENT_MODEL = os.getenv("AGENT_MODEL")
if not AGENT_MODEL:
    logger.error("AGENT_MODEL is not set in the environment variables.")
    raise ValueError("AGENT_MODEL is not set in the environment variables.")
API_KEY = os.environ["GOOGLE_API_KEY"]
if not API_KEY:
    logger.error("API_KEY is not set in the environment variables.")
    raise ValueError("API_KEY is not set in the environment variables.")


# Configuration for the agent
web_search_agent = Agent(
    name="web_search_agent",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="A helpful assistant that can search the web for information.",
    instruction=prompt.web_search_prompt, # The prompt for the agent
    tools=[web_search_tool], # Pass the function directly
)

logger.debug(f"Agent '{web_search_agent.name}' created using model '{AGENT_MODEL}'.")

deep_research_agent = Agent(
    name="deep_research_agent",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="A helpful assistant that can search the web for information.",
    instruction=prompt.deep_research_agent_prompt, # The prompt for the agent
    tools=[web_search_tool], # Pass the function directly
)

internal_search_agent = Agent(
    name="internal_search_agent",
    model=AGENT_MODEL, # Can be a string for Gemini or a LiteLlm object
    description="A helpful assistant that can search the web for information.",
    instruction=prompt.internal_search_agent_prompt, # The prompt for the agent
    tools=[rag_tool], # Pass the function directly
)
session_service = InMemorySessionService()


async def call_agent_async(agent_name, query: str):
    """Sends a query to the agent and prints the final response."""
    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])

    global session_service

    session = session_service.create_session(
    app_name="Multi Agent App",
    user_id="user_123",
    session_id="session_123"
    )

    runner = Runner(
    agent=agent_name, # The agent we want to run
    app_name="Multi Agent App",   # Associates runs with our app
    session_service=session_service # Uses our session manager
    )

    final_response_text = "Agent did not produce a final response." # Default
    # Print the response from the agent
    async for event in runner.run_async(user_id="user_123", session_id="session_123", new_message=content):
    # You can uncomment the line below to see *all* events during execution
    # print(f"  [Event] Author: {event.author}, Type: {type(event).__name__}, Final: {event.is_final_response()}, Content: {event.content}")

        # Key Concept: is_final_response() marks the concluding message for the turn.
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                final_response_text = event.content.parts[0].text
            elif event.actions and event.actions.escalate: # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            # Add more checks here if needed (e.g., specific error codes)
            break # Stop processing events once the final response is found
    return AgentResponse(response = final_response_text)