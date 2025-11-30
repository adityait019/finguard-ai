from google.adk.agents import SequentialAgent
from .parallel_financial_agent import parallel_financial_agent
from .merger_agent import merger_agent

root_agent = SequentialAgent(
    name="FinancialAnalysisPipeline",
    sub_agents=[parallel_financial_agent, merger_agent],
    description="Parallel financial analysis + synthesis pipeline."
)
