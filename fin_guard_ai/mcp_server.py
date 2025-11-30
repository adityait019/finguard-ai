# """Pure MCP stdio server for FinGuard tools (ADK compatible)."""
# import asyncio
# import csv
# import json
# import sys
# from pathlib import Path
# from typing import Any

# from mcp.server import Server
# from mcp.server.models import InitializationOptions
# from mcp.server.stdio import stdio_server
# from mcp.types import Tool, TextContent, ServerCapabilities
# # Initialize pure MCP server

# import logging
# import sys

# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - FinGuard MCP - [%(levelname)s] - %(message)s",
#     handlers=[logging.StreamHandler(sys.stderr)],  
# )
# logger = logging.getLogger("finguard_mcp")


# server = Server("finguard-mcp-server")


# @server.list_tools()
# async def handle_list_tools() -> list[Tool]:
#     return [
#         Tool(
#             name="read_transaction_file",
#             description="Read transaction CSV file from resources folder. Args: file_name (str)",
#             inputSchema={
#                 "type": "object",
#                 "properties": {"file_name": {"type": "string"}},
#                 "required": ["file_name"],
#             },
#         ),
#         Tool(
#             name="calculate_loan_emi",
#             description="Calculate EMI for loans. Args: principal (float), annual_rate (float), tenure_years (int)",
#             inputSchema={
#                 "type": "object",
#                 "properties": {
#                     "principal": {"type": "number"},
#                     "annual_rate": {"type": "number"},
#                     "tenure_years": {"type": "integer"},
#                 },
#                 "required": ["principal", "annual_rate", "tenure_years"],
#             },
#         ),
#         Tool(
#             name="search_financial_info",
#             description="Get information about Indian financial instruments. Args: query (str)",
#             inputSchema={
#                 "type": "object",
#                 "properties": {"query": {"type": "string"}},
#                 "required": ["query"],
#             },
#         ),
#     ]

# logger.info("MCP server starting on stdio...")
# server = Server("finguard-mcp-server")

# @server.call_tool()
# async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
#     project_root = Path(__file__).parent.parent
#     logger.info(f"Tool called: %s with arguments: %s", name, json.dumps(arguments))
#     if name == "read_transaction_file":
#         file_name = arguments["file_name"]
#         file_path = project_root / "fin_guard_ai" / "resources" / file_name
        
#         if not file_path.exists():
#             logger.error("File not found: %s", file_path)
#             return [TextContent(type="text", text=f"Error: File {file_name} not found")]
        
#         try:
#             logger.info("Reading transaction file: %s", file_path)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 reader = csv.DictReader(f)
#                 transactions = list(reader)
            
#             total_credit = sum(float(t.get('Amount', 0)) for t in transactions if t.get('Type') == 'Credit')
#             total_debit = sum(abs(float(t.get('Amount', 0))) for t in transactions if t.get('Type') == 'Debit')
#             categories = {}
#             for t in transactions:
#                 if t.get('Type') == 'Debit':
#                     cat = t.get('Category', 'Unknown')
#                     amt = abs(float(t.get('Amount', 0)))
#                     categories[cat] = categories.get(cat, 0) + amt
            
#             result = f"""Transaction data from {file_name}:
# Total Income: ₹{total_credit:,.2f}
# Total Expenses: ₹{total_debit:,.2f}
# Net Savings: ₹{(total_credit - total_debit):,.2f}

# Spending by Category:
# """ + "\n".join(f"  {cat}: ₹{amt:,.2f}" for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True))
#             return [TextContent(type="text", text=result)]
#         except Exception as e:
#             return [TextContent(type="text", text=f"Error reading file: {str(e)}")]
    
#     elif name == "calculate_loan_emi":
#         principal = float(arguments["principal"])
#         annual_rate = float(arguments["annual_rate"])
#         tenure_years = int(arguments["tenure_years"])
        
#         tenure_months = tenure_years * 12
#         monthly_rate = (annual_rate / 100) / 12
        
#         if monthly_rate == 0:
#             emi = principal / tenure_months
#         else:
#             emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
        
#         total_payment = emi * tenure_months
#         total_interest = total_payment - principal
        
#         result = f"""EMI Calculation Results:
# ━━━━━━━━━━━━━━━━━━━━━━
# Loan Amount: ₹{principal:,.2f}
# Interest Rate: {annual_rate}% per annum
# Tenure: {tenure_years} years ({tenure_months} months)

# Monthly EMI: ₹{emi:,.2f}
# Total Payment: ₹{total_payment:,.2f}
# Total Interest: ₹{total_interest:,.2f}

# Affordability Check:
# - Recommended monthly income: ₹{(emi / 0.4):,.2f} or more"""
#         return [TextContent(type="text", text=result)]
    
#     elif name == "search_financial_info":
#         query = arguments["query"].lower()
#         info_db = {
#             "fd": "Fixed Deposit rates: SBI 6.5-7.0%, HDFC 6.75-7.25%, ICICI 6.7-7.2%",
#             "ppf": "PPF Rate: 7.1% | Lock-in: 15 years | Max: ₹1.5L/year",
#             "nps": "NPS: 9-12% expected | Extra ₹50k tax deduction",
#             "mutual fund": "Equity: 12-15%, Debt: 6-8%, Hybrid: 8-10%",
#             "tax": "80C: PPF, ELSS, NPS, Insurance",
#         }
#         for key, info in info_db.items():
#             if key in query:
#                 return [TextContent(type="text", text=info)]
#         return [TextContent(type="text", text=f"No info for '{query}'. Try: FD, PPF, NPS")]
    
#     return [TextContent(type="text", text=f"Unknown tool: {name}")]


# async def main():
#     logger.info("Starting FinGuard MCP server (stdio)… waiting for client connections")
#     async with stdio_server() as (read_stream, write_stream):
#         logger.info("FinGuard MCP server initialized, ready for tool calls")
#         await server.run(
#             read_stream,
#             write_stream,
#             InitializationOptions(
#                 server_name="finguard-mcp-server",
#                 server_version="1.0.0",
#                 capabilities=ServerCapabilities(tools=None),
#             ),
#         )


# if __name__ == "__main__":
#     asyncio.run(main())

"""Pure MCP stdio server for FinGuard tools (ADK compatible)."""
import asyncio
import csv
import json
import sys
import logging
from pathlib import Path
from typing import Any

from mcp import ServerCapabilities
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Setup logging to stderr only (not stdout - that breaks JSON-RPC)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - FinGuard MCP - [%(levelname)s] - %(message)s",
    handlers=[logging.StreamHandler(sys.stderr)],
)
logger = logging.getLogger("finguard_mcp")

# Initialize pure MCP server
server = Server("finguard-mcp-server")

@server.list_tools()
async def handle_list_tools() -> list[Tool]:
    """List all available MCP tools."""
    logger.info("list_tools called")
    return [
        Tool(
            name="read_transaction_file",
            description="Read transaction CSV file from resources folder.",
            inputSchema={
                "type": "object",
                "properties": {"file_name": {"type": "string"}},
                "required": ["file_name"],
            },
        ),
        Tool(
            name="calculate_loan_emi",
            description="Calculate EMI for loans.",
            inputSchema={
                "type": "object",
                "properties": {
                    "principal": {"type": "number"},
                    "annual_rate": {"type": "number"},
                    "tenure_years": {"type": "integer"},
                },
                "required": ["principal", "annual_rate", "tenure_years"],
            },
        ),
        Tool(
            name="search_financial_info",
            description="Get information about Indian financial instruments.",
            inputSchema={
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        ),
    ]


@server.call_tool()
async def handle_call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Execute MCP tools."""
    project_root = Path(__file__).parent.parent
    logger.info(f"Tool called: {name} with args: {json.dumps(arguments)}")
    
    if name == "read_transaction_file":
        file_name = arguments["file_name"]
        file_path = project_root / "fin_guard_ai" / "resources" / file_name
        
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return [TextContent(type="text", text=f"Error: File {file_name} not found")]
        
        try:
            logger.info(f"Reading transaction file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                transactions = list(reader)
            
            total_credit = sum(float(t.get('Amount', 0)) for t in transactions if t.get('Type') == 'Credit')
            total_debit = sum(abs(float(t.get('Amount', 0))) for t in transactions if t.get('Type') == 'Debit')
            
            categories = {}
            for t in transactions:
                if t.get('Type') == 'Debit':
                    cat = t.get('Category', 'Unknown')
                    amt = abs(float(t.get('Amount', 0)))
                    categories[cat] = categories.get(cat, 0) + amt
            
            result = f"""Transaction data from {file_name}:
Total Income: ₹{total_credit:,.2f}
Total Expenses: ₹{total_debit:,.2f}
Net Savings: ₹{(total_credit - total_debit):,.2f}

Spending by Category:
""" + "\n".join(f"  {cat}: ₹{amt:,.2f}" for cat, amt in sorted(categories.items(), key=lambda x: x[1], reverse=True))
            
            logger.info(f"Successfully read {len(transactions)} transactions")
            return [TextContent(type="text", text=result)]
        except Exception as e:
            logger.error(f"Error reading file: {str(e)}")
            return [TextContent(type="text", text=f"Error reading file: {str(e)}")]
    
    elif name == "calculate_loan_emi":
        principal = float(arguments["principal"])
        annual_rate = float(arguments["annual_rate"])
        tenure_years = int(arguments["tenure_years"])
        
        tenure_months = tenure_years * 12
        monthly_rate = (annual_rate / 100) / 12
        
        if monthly_rate == 0:
            emi = principal / tenure_months
        else:
            emi = principal * monthly_rate * ((1 + monthly_rate) ** tenure_months) / (((1 + monthly_rate) ** tenure_months) - 1)
        
        total_payment = emi * tenure_months
        total_interest = total_payment - principal
        
        result = f"""EMI Calculation Results:
━━━━━━━━━━━━━━━━━━━━━━
Loan Amount: ₹{principal:,.2f}
Interest Rate: {annual_rate}% per annum
Tenure: {tenure_years} years ({tenure_months} months)

Monthly EMI: ₹{emi:,.2f}
Total Payment: ₹{total_payment:,.2f}
Total Interest: ₹{total_interest:,.2f}

Affordability Check:
- Recommended monthly income: ₹{(emi / 0.4):,.2f} or more"""
        
        logger.info(f"EMI calculated: ₹{emi:,.2f}/month")
        return [TextContent(type="text", text=result)]
    
    elif name == "search_financial_info":
        query = arguments["query"].lower()
        info_db = {
            "fd": "Fixed Deposit rates: SBI 6.5-7.0%, HDFC 6.75-7.25%, ICICI 6.7-7.2%",
            "ppf": "PPF Rate: 7.1% | Lock-in: 15 years | Max: ₹1.5L/year",
            "nps": "NPS: 9-12% expected | Extra ₹50k tax deduction",
            "mutual fund": "Equity: 12-15%, Debt: 6-8%, Hybrid: 8-10%",
            "tax": "80C: PPF, ELSS, NPS, Insurance",
        }
        
        for key, info in info_db.items():
            if key in query:
                logger.info(f"Financial info retrieved for: {key}")
                return [TextContent(type="text", text=info)]
        
        logger.info(f"No info found for query: {query}")
        return [TextContent(type="text", text=f"No info for '{query}'. Try: FD, PPF, NPS")]
    
    logger.error(f"Unknown tool: {name}")
    return [TextContent(type="text", text=f"Unknown tool: {name}")]


async def main():
    logger.info("Starting FinGuard MCP server (stdio)...")
    async with stdio_server() as (read_stream, write_stream):
        logger.info("FinGuard MCP server initialized and waiting for client connections")
        await server.run(
            read_stream,
            write_stream,
 InitializationOptions(
                server_name="finguard-mcp-server",
                server_version="1.0.0",
                capabilities=ServerCapabilities(tools=None),
            ),
        )
    

if __name__ == "__main__":
    asyncio.run(main())
