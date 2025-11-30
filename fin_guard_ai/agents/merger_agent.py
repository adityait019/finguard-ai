from google.adk.agents.llm_agent import Agent
from fin_guard_ai.prompts.prompt_loader import load_prompt

merger_agent = Agent(
    name="FinancialMerger",
    model='gemini-2.0-flash',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\merger_prompt.txt'),  # Create this
    description="Combines parallel analysis into final report.",
    # No tools needed
)
