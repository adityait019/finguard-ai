"""Test agent for MCPToolset integration."""
import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from fin_guard_ai.prompts.prompt_loader import load_prompt
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME=os.getenv('GEMINI_MODEL_NAME', 'gemini/gemini-2.0-flash')
llm=LiteLlm(model=MODEL_NAME, api_key=os.getenv('FIRST_GOOGLE_API_KEY'))

# Path to your MCP server (adjust if needed)
MCP_SERVER_PATH = r"C:\Users\adity\project\agent capstone\fin_guard_ai\mcp_server.py"

mcp_test_tools = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[MCP_SERVER_PATH],
        ),
        timeout=10.0,  # Increased timeout for Windows
    ),
    tool_filter=["read_transaction_file", "calculate_loan_emi", "search_financial_info"],
)

mcp_test_agent = Agent(
    model=llm,
    name='mcp_test',
    description='Test agent for MCP tool integration',
    instruction="""You are a test agent that demonstrates MCP tool integration. 
    When asked about transactions, ALWAYS use the MCP tool 'read_transaction_file'. 
    When asked about loans, use 'calculate_loan_emi'. 
    When asked about financial products, use 'search_financial_info'.
    
    Your job is to test these MCP tools work correctly.""",
    tools=[mcp_test_tools],
)
