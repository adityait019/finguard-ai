import os
from google.adk.agents.llm_agent import Agent
from fin_guard_ai.tools.file_reader import read_bank_statement
from fin_guard_ai.prompts.prompt_loader import load_prompt
analyst_agent = Agent(
    model='gemini-2.0-flash',
    name='statement_analyst',
    description='Specialist agent that reads bank statement files and analyzes spending patterns.',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\analyst_prompt.txt'),
    tools=[read_bank_statement]
)
