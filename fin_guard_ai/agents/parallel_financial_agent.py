"""Parallel financial analysis agents (following ADK docs pattern)."""
import os
from google.adk.agents import LlmAgent, ParallelAgent
from google.adk.agents.llm_agent import Agent as LlmAgent
from fin_guard_ai.tools.calculators import calculate_compound_interest, calculate_emi
from fin_guard_ai.tools.file_reader import read_bank_statement
from fin_guard_ai.prompts.prompt_loader import load_prompt

# Analyst 1: Transaction Analysis (stores in state: "transaction_summary")
transaction_analyst = LlmAgent(
    name="TransactionAnalyst",
    model='gemini-2.0-flash',
    instruction="""Analyze transactions. Use read_bank_statement or MCP tools.
    Store result in state as 'transaction_summary'. Output ONLY the summary.""",
    description="Analyzes transaction CSV files.",
    tools=[read_bank_statement],
    output_key="transaction_summary"  # Stores in session state
)

# Analyst 2: Investment Analysis (stores in state: "investment_advice")  
investment_analyst = LlmAgent(
    name="InvestmentAnalyst", 
    model='gemini-2.0-flash',
    instruction="""Analyze investments. Use compound_interest tool.
    Store result in state as 'investment_advice'. Output ONLY the advice.""",
    description="Provides investment recommendations.",
    tools=[calculate_compound_interest],
    output_key="investment_advice"
)

# Analyst 3: Loan Analysis (stores in state: "loan_analysis")
loan_analyst = LlmAgent(
    name="LoanAnalyst",
    model='gemini-2.0-flash', 
    instruction="""Analyze loans. Use calculate_emi tool.
    Store result in state as 'loan_analysis'. Output ONLY the analysis.""",
    description="Analyzes loan EMIs and affordability.",
    tools=[calculate_emi],
    output_key="loan_analysis"
)

# Parallel Agent - Runs all 3 concurrently!
parallel_financial_agent = ParallelAgent(
    name="ParallelFinancialAgent",
    sub_agents=[transaction_analyst, investment_analyst, loan_analyst],
    description="Runs transaction, investment, and loan analysis in parallel."
)
