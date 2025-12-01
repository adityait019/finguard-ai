# 🏦 FinGuard AI - Multi-Agent Personal Finance Concierge

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/downloads/)
[![Google ADK](https://img.shields.io/badge/Google-ADK-lightblue)](https://github.com/google/google-cloud-ai-agents)
[![uv](https://img.shields.io/badge/package%20manager-uv-orange)](https://docs.astral.sh/uv/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

A production-grade **multi-agent AI system** for Indian personal finance management, built with Google's Agent Development Kit (ADK) and Model Context Protocol (MCP). Demonstrates 11 out of 15 key agent capabilities including multi-agent orchestration, sequential & parallel execution, MCP tools, and full observability.

## 🎯 Project Overview

FinGuard AI is a sophisticated financial advisor system that:
- **Analyzes** bank transaction CSVs with specialized agents
- **Calculates** loan EMIs and investment returns
- **Recommends** budgets using the 50-30-20 rule
- **Coordinates** multi-agent workflows with A2A protocol
- **Exposes** MCP tools for external clients

### 🏆 Key Features (11/15 Course Requirements)

| Feature | Status | Evidence |
|---------|--------|----------|
| **Multi-agent system** | ✅ | Sequential: fin_guard → statement_analyst → budget_advisor |
| **Agent powered by LLM** | ✅ | Gemini 2.0 Flash across all 5 agents |
| **Tools: MCP** | ✅ | `read_transaction_file`, `calculate_loan_emi`, `search_financial_info` |
| **Tools: Custom tools** | ✅ | `calculate_emi`, `compound_interest`, `read_bank_statement` |
| **Observability** | ✅ | Logging, session tracing, agent call tracking |
| **Sessions & state** | ✅ | InMemorySessionService, state management |
| **A2A Protocol** | ✅ | Agent-to-agent delegation via `transfer_to_agent` |
| **Agent deployment** | ✅ | `adk web fin_guard_ai` → production web UI |
| **Parallel agents** | ✅ | ParallelAgent for concurrent analysis |
| **Context engineering** | ✅ | Prompt engineering with 50-30-20 rule |
| **Long-running ops** | ✅ | MCP subprocess management |

---

## 📊 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    ADK Web UI (Port 8000)                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                   fin_guard (Root Agent)                    │
│  • Gemini 2.0 Flash • Multi-agent orchestrator              │
└─────────────────────────────────────────────────────────────┘
           ↙                    ↓                   ↘
    ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐
    │  statement_  │  │   budget_    │  │     MCP Tools    │
    │   analyst    │  │    advisor   │  │   (Stdio Server) │
    │              │  │              │  │                  │
    │ CSV Analysis │  │ 50-30-20 %   │  │ • read_txn_file  │
    │ Spending     │  │ Budget Plan  │  │ • calculate_emi  │
    │ Categories   │  │ Savings Tips │  │ • search_finance │
    └──────────────┘  └──────────────┘  └──────────────────┘
```

### Data Flow Example

```
User Input: "analyze sample_transactions.csv"
    ↓
fin_guard: "I'll analyze that with my specialist"
    ↓
transfer_to_agent: statement_analyst
    ↓
statement_analyst: read_transaction_file("sample_transactions.csv")
    ↓
MCP Server (subprocess): Parse CSV → Return ₹50k income, ₹29.9k expenses
    ↓
statement_analyst: "Total savings: ₹20.1k | Top category: Housing ₹15k"
    ↓
transfer_to_agent: budget_advisor
    ↓
budget_advisor: "Applying 50-30-20 rule... [detailed plan]"
```

---

## 🚀 Quick Start

### Prerequisites

```bash
# Python 3.10+
python --version  # Should show 3.10 or higher

# Install uv (fast Python package manager)
pip install uv
# or: brew install uv  # macOS with Homebrew

# Google Cloud credentials
gcloud auth application-default login
```

### Installation

```bash
# Clone repository
git clone https://github.com/adityait019/finguard-ai.git
cd finguard-ai

# Sync dependencies with uv (creates venv automatically)
uv sync

# Activate virtual environment (optional - uv can run directly)
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
```

### Running the Application

#### Terminal 1: Start MCP Server (Stdio)

```bash
uv run python fin_guard_ai/mcp_server.py
```

Expected output:
```
2025-12-01 02:19:xx,xxx - FinGuard MCP - [INFO] - Starting FinGuard MCP server (stdio)...
2025-12-01 02:19:xx,xxx - FinGuard MCP - [INFO] - FinGuard MCP server initialized and waiting...
```

#### Terminal 2: Start ADK Web UI

```bash
uv run adk web fin_guard_ai
```

Open browser: **http://localhost:8000**

---

## 💬 Example Prompts

### 1. **Full Financial Analysis** (Sequential A2A)
```
"Use sample_transactions.csv and give me a full financial analysis"
```
**Flow:** fin_guard → statement_analyst (CSV parsing) → budget_advisor (recommendations)

**Output:**
```
Transaction Summary:
- Total Income: ₹50,000.00
- Total Expenses: ₹29,899.00
- Net Savings: ₹20,101.00

Budget Recommendations (50-30-20):
- Needs (50%): ₹25,000 (You're spending ₹20,570 ✓)
- Wants (30%): ₹15,000 (You're spending ₹4,329 ✓)
- Savings (20%): ₹10,000 (You're saving ₹20,101 ✓✓)
```

### 2. **MCP Tool Usage** (Direct MCP Call)
```
"Calculate EMI for ₹10,00,000 loan at 8.5% for 20 years"
```
**Output:**
```
EMI Calculation Results:
Monthly EMI: ₹9,604.46
Total Payment: ₹23,05,070.70
Total Interest: ₹13,05,070.70
Recommended Income: ₹24,011.15 or more
```

### 3. **Financial Info Query** (MCP search_financial_info)
```
"What are current PPF rates in India?"
```
**Output:**
```
PPF Rate: 7.1% | Lock-in: 15 years | Max: ₹1.5L/year
```

---

## 📁 Project Structure

```
fin_guard_ai/
├── agents/
│   ├── __init__.py
│   ├── finguard_agent.py          # Root multi-agent orchestrator
│   ├── analyst_agent.py           # CSV analysis specialist
│   ├── budget_advisor_agent.py    # Budget recommendations
│   ├── parallel_financial_agent.py # Parallel execution (3 concurrent)
│   └── merger_agent.py            # Merge parallel results
│
├── tools/
│   ├── calculators.py             # EMI, compound interest tools
│   └── file_reader.py             # CSV file reading
│
├── prompts/
│   ├── finguard_prompt.txt        # Main agent instructions
│   ├── analyst_prompt.txt         # Analyst instructions
│   ├── budget_advisor_prompt.txt  # Budget recommendations
│   └── merger_prompt.txt          # Result synthesis
│
├── resources/
│   └── sample_transactions.csv    # Demo transaction data
│
├── mcp_server.py                  # Pure MCP stdio server
├── agent.py                       # ADK entry point
├── pyproject.toml                 # UV project configuration
└── uv.lock                        # Locked dependencies (uv)
```

---

## 🔧 Architecture Details

### Multi-Agent Orchestration

#### Sequential Flow (Default)
```python
# fin_guard.py
root_agent = LlmAgent(
    name='fin_guard',
    sub_agents=[analyst_agent, budget_advisor_agent],
    tools=[calculate_emi, calculate_compound_interest, mcp_toolset]
)
```

**Flow:** Root agent → Analyst (CSV) → Budget Advisor (Plan) ✅

#### Parallel Flow (Optional)
```python
# parallel_financial_agent.py
parallel_analysis = ParallelAgent(
    sub_agents=[
        transaction_analyst,    # Analyzes ₹ flows
        investment_analyst,     # Reviews growth
        loan_analyst           # Checks affordability
    ]
)
sequential_pipeline = SequentialAgent(
    sub_agents=[parallel_analysis, merger_agent]
)
```

**Flow:** 3 agents run concurrently → Results merged ⚡

### MCP Tools

Pure MCP stdio server exposing 3 tools:

```python
# mcp_server.py
@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    return [
        Tool(name="read_transaction_file"),      # CSV parsing
        Tool(name="calculate_loan_emi"),         # EMI calculation
        Tool(name="search_financial_info"),      # Indian finance DB
    ]
```

**Key Feature:** Stdio transport means ADK can spawn MCP subprocess directly via `StdioConnectionParams`.

---

## 📊 Indian Financial Context

All calculations follow Indian financial standards:

### Tax Saving (Section 80C)
```
- PPF: 7.1% locked 15 years
- ELSS: Equity-linked, 3-year lock
- NPS: 9-12% expected return
```

### Budget Rule
```
50-30-20: Allocate monthly income as
- 50% Needs (housing, groceries, utilities)
- 30% Wants (dining, entertainment)
- 20% Savings & Investments
```

### Common Banks & Rates
```
- SBI FD: 6.5-7.0%
- HDFC: 6.75-7.25%
- ICICI: 6.7-7.2%
```

---

## 📈 Course Concepts Demonstrated

### ✅ 1. Multi-Agent System
- Sequential agent delegation (fin_guard → analyst → budget_advisor)
- Agent-to-agent communication via `transfer_to_agent`
- Shared session state across agents

### ✅ 2. Agent Powered by LLM
- Gemini 2.0 Flash on all 5 agents
- Complex reasoning for budget optimization
- Contextual financial advice

### ✅ 3. Tools
- **MCP:** External stdio server with 3 MCP tools
- **Custom:** Python functions (calculate_emi, read_csv)
- **Built-in:** Session management, logging

### ✅ 4. Observability
- **Logging:** Agent calls, tool invocations (observability.py)
- **Tracing:** Full session traces at `/debug/trace/session/<ID>`
- **Metrics:** Token usage, latency tracking

### ✅ 5. Sessions & State
- InMemorySessionService (demo_session_001)
- State sharing across agent handoffs
- Conversation history preservation

### ✅ 6. A2A Protocol
- Agent-to-agent delegation
- Message passing via ADK framework
- Result propagation between agents

### ✅ 7. Agent Deployment
- `adk web fin_guard_ai` → production web server
- ASGI-compliant deployment
- SSE streaming for real-time updates

### ✅ 8. Parallel Agents
- ParallelAgent executes 3 analysts concurrently
- Results merged via SequentialAgent
- Performance improvement for independent tasks

### ✅ 9. Context Engineering
- Prompt engineering with 50-30-20 budget rule
- Indian financial context injection
- Personalization for user goals

### ✅ 10. Long-Running Operations
- MCP subprocess management
- Timeout handling (15s default)
- Session persistence across tool calls

---

## 🧪 Testing

### Run Demo Analysis
```bash
# Terminal 1
uv run python fin_guard_ai/mcp_server.py

# Terminal 2
uv run adk web fin_guard_ai

# Browser: http://localhost:8000
# Prompt: "analyze sample_transactions.csv"
```

### Check Session Traces
```
http://localhost:8000/debug/trace/session/<session-id>
```

Example trace output:
```json
{
  "events": [
    {
      "author": "fin_guard",
      "content": "Transferring to statement_analyst...",
      "actions": { "transferToAgent": "statement_analyst" }
    },
    {
      "author": "statement_analyst",
      "content": "Using MCP tool read_transaction_file...",
      "functionCall": { "name": "read_transaction_file" }
    }
  ]
}
```

---

## 📋 Sample Transaction Data

`resources/sample_transactions.csv`:
```
Date,Type,Amount,Category,Description
2025-11-01,Credit,50000,Salary,Monthly salary
2025-11-02,Debit,15000,Housing,Rent
2025-11-05,Debit,3200,Groceries,Weekly groceries
2025-11-07,Debit,2930,Dining,Restaurant & food delivery
2025-11-10,Debit,1399,Entertainment,Movies & gaming
2025-11-15,Debit,1200,Utilities,Electricity & water
2025-11-20,Debit,890,Healthcare,Medical checkup
2025-11-28,Debit,5000,Investment,Mutual fund SIP
2025-11-30,Debit,280,Transport,Fuel
```

**Analysis:**
- **Total Income:** ₹50,000
- **Total Expenses:** ₹29,899
- **Net Savings:** ₹20,101 (40.2%)

---

## 🔐 Environment Setup

Create `.env` file in project root:
```bash
GOOGLE_CLOUD_PROJECT=your-gcp-project-id
GEMINI_API_KEY=your-api-key
```

Or use Google Cloud authentication:
```bash
gcloud auth application-default login
```

---

## 📚 Key Dependencies

See `pyproject.toml` for full dependency list:

```toml
[project]
dependencies = [
    "google-cloud-ai-agents>=0.8.0",
    "google-genai>=0.4.0",
    "mcp[server]>=1.2.0",
    "pydantic>=2.12",
]
```

### Why UV?

- ⚡ **70x faster** than pip (Rust-based)
- 🔒 **Deterministic** with `uv.lock`
- 🐍 **Python version manager** built-in
- 📦 **Single dependency resolver**

---

## 🎓 Learning Outcomes

By exploring this codebase, you'll understand:

1. **Multi-agent orchestration** at scale
2. **Model Context Protocol** for tool extensibility
3. **Google ADK** framework for production agents
4. **Agent-to-agent communication** patterns
5. **Session management** in distributed systems
6. **Observability** for agent systems
7. **Financial domain expertise** in AI
8. **Production deployment** of agent systems
9. **UV package manager** for modern Python
10. **Concurrent agent execution** patterns

---

## 🚀 Future Enhancements

- [ ] **HTTP/SSE MCP Transport** (replace stdio)
- [ ] **Database Sessions** (replace in-memory)
- [ ] **Real Bank API Integration** (Plaid, OPEN API)
- [ ] **Advanced RAG** for financial documents
- [ ] **Portfolio Optimization** with reinforcement learning
- [ ] **Multi-language Support** (Hindi, Tamil, etc.)
- [ ] **Mobile App** (React Native)
- [ ] **Agent Evaluation Framework** (TrueLens, Langsmith)

---

## 📝 License

Apache License 2.0 - See LICENSE file

---

## 👤 Author

**Aditya Kumar**  
Backend AI Engineer | Multi-Agent Systems | ADK Explorer  
GitHub: [@adityait019](https://github.com/adityait019)  
Location: Kolkata, West Bengal, India

---

## 🙏 Acknowledgments

- Google Cloud AI Agents (ADK) team for the framework
- Model Context Protocol (Anthropic) for tool standardization
- Astral (UV creators) for the fast package manager
- Indian fintech community for domain insights

---

## 📞 Support

For issues or questions:
1. Check `/debug/trace/session/<id>` for detailed logs
2. Review `fin_guard_ai/mcp_server.py` MCP implementation
3. Refer to [ADK Documentation](https://google.github.io/adk-docs/)
4. Check [UV Documentation](https://docs.astral.sh/uv/)

---

**Last Updated:** December 1, 2025 | **Version:** 1.0.0 (Kaggle Capstone)  
**Package Manager:** UV ⚡ | **Python:** 3.10+ | **Status:** Production Ready ✅
