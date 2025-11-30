from fin_guard_ai.agents.finguard_agent import root_agent
from fin_guard_ai.services.session_service import memory_bank
from fin_guard_ai.utils.observability import log_agent_call, get_metrics_summary
import uuid

# Initialize default session for demo
default_session_id = "demo_session_001"
memory_bank.create_session(
    session_id=default_session_id,
    user_profile={
        "monthly_income": 50000,
        "risk_profile": "moderate",
        "savings_goal": 10000,
        "location": "Kolkata"
    }
)

# Log startup
log_agent_call("fin_guard", "Agent initialized", default_session_id)

# Export agent (ADK will use this)
agent = root_agent

# Helper to get metrics (for demonstration)
def show_metrics():
    """Display current observability metrics."""
    return get_metrics_summary()
