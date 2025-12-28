from google.adk.agents.llm_agent import Agent
from fin_guard_ai.prompts.prompt_loader import load_prompt
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME=os.getenv('GEMINI_MODEL_NAME', 'gemini/gemini-2.0-flash')
llm=LiteLlm(model=MODEL_NAME, api_key=os.getenv('FIRST_GOOGLE_API_KEY'))

budget_advisor_agent = Agent(
    model=llm,
    name='budget_advisor',
    description='Specialist agent that provides personalized budget recommendations and savings strategies based on spending analysis.',
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\budget_advisor_prompt.txt'),
    tools=[]  # Will use root agent's tools
)
