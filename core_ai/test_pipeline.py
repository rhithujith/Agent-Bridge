"""
Quick smoke-test for the full AgentBridge pipeline.

Usage (from any directory):
    python core_ai/test_pipeline.py                         # rule engine only
    python core_ai/test_pipeline.py --api-key sk-ant-...    # + AI analysis
"""

import sys
import os

# core_ai/ first — resolves bare imports (from dao, from parser, etc.)
# Agent-Bridge/ second — resolves package imports (from core_ai.dao, etc.)
CORE_AI_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(CORE_AI_DIR)
for p in (ROOT, CORE_AI_DIR):
    if p not in sys.path:
        sys.path.insert(0, p)
# Keep core_ai first so bare 'compliance' resolves to core_ai/compliance.py,
# not the top-level compliance/ package.
sys.path = [CORE_AI_DIR] + [p for p in sys.path if p != CORE_AI_DIR]

from pipeline import process
from report_generator import generate_report

# ─────────────────────────────────────────────────────────────────────────────
# API key — pass via --api-key flag or set ANTHROPIC_API_KEY env var
# ─────────────────────────────────────────────────────────────────────────────

API_KEY = None
for i, arg in enumerate(sys.argv):
    if arg == "--api-key" and i + 1 < len(sys.argv):
        API_KEY = sys.argv[i + 1]
        break
if not API_KEY:
    API_KEY = os.environ.get("ANTHROPIC_API_KEY")

if not API_KEY:
    print("⚠  No API key provided — AI analysis will be skipped.")
    print("   Pass --api-key sk-ant-... or set ANTHROPIC_API_KEY to include it.\n")

# ─────────────────────────────────────────────────────────────────────────────
# SAMPLE LOG
# ─────────────────────────────────────────────────────────────────────────────

raw_log = {
    "id": "dec_001",
    "session_id": "sess_abc",
    "ts": "2025-08-30T10:15:00",
    "input_data": {"user_id": "U123", "amount": 75000},
    "thought": None,
    "result": {"action": "approve", "confidence": 0.62},
    "agent": "fraud_detection_agent",
}

# ─────────────────────────────────────────────────────────────────────────────
# RUN PIPELINE
# ─────────────────────────────────────────────────────────────────────────────

dao = process(raw_log, api_key=API_KEY)

# ─────────────────────────────────────────────────────────────────────────────
# PRINT RESULTS
# ─────────────────────────────────────────────────────────────────────────────

print("=" * 50)
print("RULE ENGINE")
print("=" * 50)
print("Risk Level   :", dao.risk_level)
print("Flag Reason  :", dao.flag_reason)
print("Compliance   :", dao.compliance_tags)
print("Violations   :", dao.compliance_violations)

print()
print("=" * 50)
print("AI ANALYSIS")
print("=" * 50)
if dao.ai_explanation:
    print("Status       :", dao.ai_compliance_status)
    print("Category     :", dao.ai_category)
    print("Risk Level   :", dao.ai_risk_level)
    print("Issue        :", dao.ai_issue_detected)
    print("Escalate     :", dao.ai_escalate_to_human)
    print("Confidence   :", dao.ai_confidence_score)
    print("Explanation  :", dao.ai_explanation)
    print("Recommended  :", dao.ai_recommended_action)
    print("Refs         :", dao.ai_regulatory_refs)
else:
    print("(skipped — no API key)")

print()
print("=" * 50)
print("REPORT")
print("=" * 50)
report = generate_report("sess_abc", [dao])
print("Verdict      :", report["verdict"])
print("Risk breakdown:", report["session_summary"]["risk_breakdown"])
print()
print("RBI Response Block:")
rbi = report["rbi_response_block"]
print("  High-risk decisions    :", rbi["high_risk_decisions"])
print("  Compliance verdict     :", rbi["compliance_verdict"])
print("  Categories detected    :", rbi["risk_categories_detected"])
print("  AI recommendations     :", rbi["ai_recommended_actions"])
print("  Note                   :", rbi["note"])
