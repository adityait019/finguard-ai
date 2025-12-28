import os
from google.adk.agents.llm_agent import Agent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters
from fin_guard_ai.tools.file_reader import read_bank_statement
from fin_guard_ai.prompts.prompt_loader import load_prompt
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME=os.getenv('GEMINI_MODEL_NAME', 'gemini/gemini-2.0-flash')
llm=LiteLlm(model=MODEL_NAME, api_key=os.getenv('FIRST_GOOGLE_API_KEY'))

# Same MCP config as root agent
MCP_SERVER_PATH = r"C:\Users\adity\project\agent capstone\fin_guard_ai\mcp_server.py"

if not os.path.exists(MCP_SERVER_PATH):
    print(f"WARNING: MCP server script not found at {MCP_SERVER_PATH}")

mcp_tools_analyst = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",
            args=[MCP_SERVER_PATH],
        ),
        timeout=15.0,
    ),
    tool_filter=["read_transaction_file"],  # Analyst only needs CSV tool
)

analyst_agent = Agent(
    model=llm,
    name='statement_analyst',
    description='Specialist agent that reads bank statement files and analyzes spending patterns using both local and MCP tools.',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\analyst_prompt.txt'),
    tools=[
        read_bank_statement,      # Local CSV tool
        mcp_tools_analyst,        # MCP CSV tool
    ],
)
