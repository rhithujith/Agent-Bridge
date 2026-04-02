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

    # Anomaly engine results (from anomaly.py)
    risk_level: str = "low"
    flag_reason: Optional[str] = None

    # Compliance mapping results (from compliance.py)
    compliance_tags: List[str] = field(default_factory=list)
    compliance_violations: List[str] = field(default_factory=list)

    # Agent metadata
    agent_name: str = ""
    action_type: str = ""

    # ── NEW: AI Analysis fields ──
    ai_action_summary: Optional[str] = None
    ai_compliance_status: Optional[str] = None
    ai_risk_level: Optional[str] = None
    ai_category: Optional[str] = None
    ai_issue_detected: Optional[bool] = None
    ai_explanation: Optional[str] = None
    ai_recommended_action: Optional[str] = None
    ai_confidence_score: Optional[float] = None
    ai_regulatory_refs: List[str] = field(default_factory=list)
    ai_escalate_to_human: bool = False
    ai_raw_response: Optional[Dict] = None
    

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
            "compliance_violations": self.compliance_violations,
            "agent_name": self.agent_name,
            "action_type": self.action_type,
            "ai_action_summary": self.ai_action_summary,
            "ai_compliance_status": self.ai_compliance_status,
            "ai_risk_level": self.ai_risk_level,
            "ai_category": self.ai_category,
            "ai_issue_detected": self.ai_issue_detected,
            "ai_explanation": self.ai_explanation,
            "ai_recommended_action": self.ai_recommended_action,
            "ai_confidence_score": self.ai_confidence_score,
            "ai_regulatory_refs": self.ai_regulatory_refs,
            "ai_escalate_to_human": self.ai_escalate_to_human,
            "ai_raw_response": self.ai_raw_response,
        }