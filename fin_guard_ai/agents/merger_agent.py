from google.adk.agents.llm_agent import Agent
from fin_guard_ai.prompts.prompt_loader import load_prompt
from google.adk.models.lite_llm import LiteLlm
import os
from dotenv import load_dotenv
load_dotenv(override=True)

MODEL_NAME=os.getenv('GEMINI_MODEL_NAME', 'gemini/gemini-2.0-flash')
llm=LiteLlm(model=MODEL_NAME, api_key=os.getenv('FIRST_GOOGLE_API_KEY'))

merger_agent = Agent(
    name="FinancialMerger",
    model=llm,
    instruction=load_prompt(r'C:\Users\adity\project\agent capstone\fin_guard_ai\prompts\merger_prompt.txt'),  # Create this
    description="Combines parallel analysis into final report.",
    # No tools needed
)
