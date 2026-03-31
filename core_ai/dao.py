from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid

@dataclass
class DAO:
    # Core identity
    decision_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    session_id: str = ""
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    # What the agent saw and did
    input: Dict[str, Any] = field(default_factory=dict)
    reasoning: Optional[str] = None
    output: Dict[str, Any] = field(default_factory=dict)

    # What we determined about it
    risk_level: str = "low"           # "low", "medium", "high"
    flag_reason: Optional[str] = None

    # RBI compliance
    compliance_tags: List[str] = field(default_factory=list)

    # Agent metadata
    agent_name: str = ""
    action_type: str = ""             # e.g. "approve", "reject", "flag", "query"

    def to_dict(self):
        return {
            "decision_id": self.decision_id,
            "session_id": self.session_id,
            "timestamp": self.timestamp,
            "input": self.input,
            "reasoning": self.reasoning,
            "output": self.output,
            "risk_level": self.risk_level,
            "flag_reason": self.flag_reason,
            "compliance_tags": self.compliance_tags,
            "agent_name": self.agent_name,
            "action_type": self.action_type,
        }