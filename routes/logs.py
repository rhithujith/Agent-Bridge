from fastapi import APIRouter, HTTPException
from compliance.rules import check_rules
from database import supabase
import datetime

router = APIRouter()

@router.post("/log")
async def receive_log(data: dict):
    if not data.get("api_key"):
        raise HTTPException(status_code=400, detail="api_key required")
    if not data.get("action"):
        raise HTTPException(status_code=400, detail="action required")

    flagged, reason = check_rules(data)

    entry = {
        "api_key": data["api_key"],
        "agent_name": data.get("agent_name", "unknown"),
        "action": data["action"],
        "inputs": str(data.get("inputs", ""))[:500],
        "output": str(data.get("output", ""))[:500],
        "latency_ms": data.get("latency_ms", 0),
        "status": data.get("status", "success"),
        "flagged": flagged,
        "flag_reason": reason,
        "domain": data.get("domain", "fintech")
    }

    supabase.table("logs").insert(entry).execute()
    return {"ok": True, "flagged": flagged, "flag_reason": reason}

@router.get("/logs")
async def get_logs(api_key: str, limit: int = 50):
    if not api_key:
        raise HTTPException(status_code=400, detail="api_key required")

    result = supabase.table("logs")\
        .select("*")\
        .eq("api_key", api_key)\
        .order("created_at", desc=True)\
        .limit(limit)\
        .execute()

    return result.data