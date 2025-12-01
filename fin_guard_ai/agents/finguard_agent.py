import os

from google.adk.agents.llm_agent import Agent as LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from mcp import StdioServerParameters

from fin_guard_ai.tools.calculators import calculate_compound_interest, calculate_emi
from fin_guard_ai.prompts.prompt_loader import load_prompt
from fin_guard_ai.agents.analyst_agent import analyst_agent
from fin_guard_ai.agents.budget_advisor_agent import budget_advisor_agent
from fin_guard_ai.agents.parallel_financial_agent import parallel_financial_agent



MCP_SERVER_PATH = r"C:\Users\adity\project\agent capstone\fin_guard_ai\mcp_server.py"

# Safety check for local dev (you can comment this out after you verify)
if not os.path.exists(MCP_SERVER_PATH):
    print(f"WARNING: MCP server script not found at {MCP_SERVER_PATH}. Please adjust the path if needed.")

# Define MCPToolset that connects to your MCP server via stdio
finguard_mcp_toolset = MCPToolset(
    connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(
            command="python",           # or "python3" depending on your environment
            args=[MCP_SERVER_PATH],
            env=None     # Path to your MCP server script
        ),
        timeout=15,  # optional
    ),
    # Optional: filter only the tools you want the LLM to see
    # tool_filter=['read_transaction_file', 'calculate_loan_emi', 'search_financial_info'],
)

root_agent = LlmAgent(
    model='gemini-2.0-flash',
    name='fin_guard',
    description='A proactive personal finance and investment concierge with multi-agent and MCP-enabled capabilities.',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\finguard_prompt.txt'),
    tools=[
        calculate_compound_interest,
        calculate_emi,
        finguard_mcp_toolset,  # MCP tools from your MCP server
    ],
    sub_agents=[analyst_agent, budget_advisor_agent,parallel_financial_agent],
)

