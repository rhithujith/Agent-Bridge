from fastapi import APIRouter, HTTPException
from database import supabase

router = APIRouter()

@router.get("/report")
async def get_report(api_key: str):
    if not api_key:
        raise HTTPException(status_code=400, detail="api_key required")

    logs = supabase.table("logs")\
        .select("*")\
        .eq("api_key", api_key)\
        .order("created_at", desc=True)\
        .execute().data

    if not logs:
        return {"message": "No data yet for this api_key"}

    total = len(logs)
    flagged = [l for l in logs if l['flagged']]
    success = [l for l in logs if l['status'] == 'success']
    avg_latency = round(sum(l['latency_ms'] or 0 for l in logs) / total)
    score = round((total - len(flagged)) / total * 100)

    actions_breakdown = {}
    for l in logs:
        actions_breakdown[l['action']] = actions_breakdown.get(l['action'], 0) + 1

    return {
        "api_key": api_key,
        "total_actions": total,
        "success_rate": round(len(success) / total * 100),
        "average_latency_ms": avg_latency,
        "incidents": len(flagged),
        "compliance_score": score,
        "actions_breakdown": actions_breakdown,
        "incident_list": flagged,
        "timeline": logs[:20]
    }
