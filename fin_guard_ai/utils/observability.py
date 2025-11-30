"""
Observability utilities: logging, tracing, and metrics for agent operations.
"""
import logging
import time
from typing import Dict, Any, Callable, Optional
from functools import wraps
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - [%(levelname)s] - %(message)s'
)

logger = logging.getLogger("FinGuard")

# Global metrics store
METRICS = {
    "agent_calls": {},
    "tool_calls": {},
    "total_latency_ms": 0,
    "error_count": 0
}

def log_agent_call(agent_name: str, input_summary: str, session_id: Optional[str] = None):
    """Log agent invocation."""
    logger.info(f"Agent Called | agent={agent_name} | session={session_id} | input={input_summary[:100]}")
    
    if agent_name not in METRICS["agent_calls"]:
        METRICS["agent_calls"][agent_name] = 0
    METRICS["agent_calls"][agent_name] += 1

def log_tool_call(tool_name: str, args: Dict[str, Any], session_id: Optional[str] = None):
    """Log tool invocation."""
    logger.info(f"Tool Called | tool={tool_name} | session={session_id} | args={args}")
    
    if tool_name not in METRICS["tool_calls"]:
        METRICS["tool_calls"][tool_name] = 0
    METRICS["tool_calls"][tool_name] += 1

def trace_execution(func: Callable):
    """Decorator to trace function execution time."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        trace_id = f"{func.__name__}_{int(start_time * 1000)}"
        
        logger.info(f"Trace Start | trace_id={trace_id} | function={func.__name__}")
        
        try:
            result = func(*args, **kwargs)
            duration_ms = (time.time() - start_time) * 1000
            METRICS["total_latency_ms"] += duration_ms
            
            logger.info(f"Trace End | trace_id={trace_id} | duration_ms={duration_ms:.2f} | status=success")
            return result
        
        except Exception as e:
            duration_ms = (time.time() - start_time) * 1000
            METRICS["error_count"] += 1
            
            logger.error(f"Trace Error | trace_id={trace_id} | duration_ms={duration_ms:.2f} | error={str(e)}")
            raise
    
    return wrapper

def get_metrics_summary() -> Dict[str, Any]:
    """Get current metrics summary."""
    return {
        "timestamp": datetime.now().isoformat(),
        "metrics": METRICS,
        "summary": {
            "total_agent_calls": sum(METRICS["agent_calls"].values()),
            "total_tool_calls": sum(METRICS["tool_calls"].values()),
            "avg_latency_ms": METRICS["total_latency_ms"] / max(sum(METRICS["agent_calls"].values()), 1),
            "error_rate": METRICS["error_count"] / max(sum(METRICS["agent_calls"].values()), 1)
        }
    }

def log_metrics():
    """Log current metrics."""
    summary = get_metrics_summary()
    logger.info(f"Metrics Summary | {summary}")
