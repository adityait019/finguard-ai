# agent.py
from google.adk.agents.llm_agent import Agent
from fin_guard_ai.tools.calculators import calculate_compound_interest
from fin_guard_ai.prompts.prompt_loader import load_prompt
from fin_guard_ai.agents.analyst_agent import analyst_agent




root_agent = Agent(
    model='gemini-2.0-flash',
    name='fin_guard',
    description='A proactive personal finance and investment concierge.',
    # Load the instruction from the file
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\finguard_prompt.txt'),
    tools=[calculate_compound_interest,],
    sub_agents=[analyst_agent],
)