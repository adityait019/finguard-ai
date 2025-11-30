from typing import Dict, Any, Optional
from datetime import datetime
import json

class SimpleMemoryBank:
    """Simple in-memory storage for user context and conversation history."""
    
    def __init__(self):
        self._sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, session_id: str, user_profile: Optional[Dict[str, Any]] = None):
        """Create a new session with optional user profile."""
        self._sessions[session_id] = {
            "created_at": datetime.now().isoformat(),
            "user_profile": user_profile or {},
            "conversation_history": [],
            "metrics": {
                "total_interactions": 0,
                "tools_used": [],
                "agents_invoked": []
            }
        }
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        return self._sessions.get(session_id)
    
    def update_session(self, session_id: str, key: str, value: Any):
        """Update specific session field."""
        if session_id in self._sessions:
            self._sessions[session_id][key] = value
    
    def add_to_history(self, session_id: str, entry: Dict[str, Any]):
        """Add entry to conversation history."""
        if session_id in self._sessions:
            self._sessions[session_id]["conversation_history"].append({
                "timestamp": datetime.now().isoformat(),
                **entry
            })
    
    def log_metric(self, session_id: str, metric_type: str, value: Any):
        """Log metrics for observability."""
        if session_id in self._sessions:
            if metric_type == "tool_used":
                self._sessions[session_id]["metrics"]["tools_used"].append(value)
            elif metric_type == "agent_invoked":
                self._sessions[session_id]["metrics"]["agents_invoked"].append(value)
            self._sessions[session_id]["metrics"]["total_interactions"] += 1
    
    def get_context_summary(self, session_id: str) -> str:
        """Generate compact context summary for prompt."""
        session = self.get_session(session_id)
        if not session:
            return "No prior context available."
        
        profile = session.get("user_profile", {})
        history = session.get("conversation_history", [])
        
        # Context compaction: only last 3 interactions + profile
        recent_history = history[-3:] if len(history) > 3 else history
        
        context = f"User Profile: {json.dumps(profile)}\n"
        context += f"Recent Interactions: {len(recent_history)}\n"
        for item in recent_history:
            context += f"- {item.get('summary', 'N/A')}\n"
        
        return context

# Global instance
memory_bank = SimpleMemoryBank()
