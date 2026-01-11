import os
import litellm
from google.adk.agents.llm_agent import Agent as LlmAgent
from google.adk.models.lite_llm import LiteLlm
from dotenv import load_dotenv
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
import asyncio
load_dotenv(override=True)

# 1. API Base: Must be the root URL, WITHOUT "/ui/..."
proxy_base_url = 'http://localhost:4000' 

# 2. API Key: Must be a "Virtual Key" starting with "sk-..." 
# Generate this in the UI under the "Virtual Keys" or "API Keys" tab.
# Do NOT use your Groq or Google key here.
proxy_key = os.getenv('LITELLM_PROXY_API_KEY') 

# 3. Configure Global Settings (ADK uses these implicitly)
os.environ["LITELLM_PROXY_API_BASE"] = proxy_base_url
os.environ["LITELLM_PROXY_API_KEY"] = str(proxy_key)
litellm.use_litellm_proxy = True

# 4. Model Name: Use the "LiteLLM Model Name" from your screenshot
# In your image, this is explicitly "groq/openai/gpt-oss-120b"
MODEL_NAME = 'groq/openai/gpt-oss-120b'

# Initialize the model wrapper
llm = LiteLlm(model=MODEL_NAME)

# Create the Agent
testing_agent = LlmAgent(
    model=llm,
    name='testing_agent',
    description='A Personal Assistant.',
    instruction='You are a Knowledgeable Assistant who helps users with their queries.',
)


async def call_agent_async(query: str, runner, user_id, session_id):
    """Sends a query to the agent and prints the final response."""
    print(f"\n>>> User Query: {query}")

    # Prepare the user's message in ADK format
    content = types.Content(role='user', parts=[types.Part(text=query)])
    
    final_response_text = "Agent did not produce a final response."
    
    # Execute the agent and find the final response
    async for event in runner.run_async(
        user_id=user_id, 
        session_id=session_id, 
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response_text = event.content.parts[0].text
            break
            
    print(f"<<< Agent Response: {final_response_text}")


# Set up session and runner
session_service_proxy_env = InMemorySessionService()

# Test the proxy-enabled agent (environment variables method)
async def test_proxy_env_agent():
    print("\n--- Testing Proxy-enabled Agent (Environment Variables) ---")

    # Create the session (async) and construct the runner inside the async context
    session_proxy_env = await session_service_proxy_env.create_session(
        app_name="agents",
        user_id="user_1",
        session_id="session_proxy_env"
    )

    runner_proxy_env = Runner(
        agent=testing_agent,
        app_name="agents",
        session_service=session_service_proxy_env
    )

    await call_agent_async(
        "What's the weather in London?",
        runner=runner_proxy_env,
        user_id="user_1",
        session_id="session_proxy_env"
    )

# Execute the conversation
if __name__ == "__main__":
    asyncio.run(test_proxy_env_agent())