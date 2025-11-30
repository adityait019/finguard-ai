from google.adk.agents.llm_agent import Agent
from fin_guard_ai.prompts.prompt_loader import load_prompt

budget_advisor_agent = Agent(
    model='gemini-2.0-flash',
    name='budget_advisor',
    description='Specialist agent that provides personalized budget recommendations and savings strategies based on spending analysis.',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\budget_advisor_prompt.txt'),
    tools=[]  # Will use root agent's tools
)
