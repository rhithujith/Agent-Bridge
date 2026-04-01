from core_ai.dao import DAO
from core_ai.parser import parse_to_dao
from core_ai.anomaly import check_anomalies
from core_ai.compliance import map_compliance
from typing import Any, Dict


def process(raw_log: Dict[str, Any]) -> DAO:
    """
    Full processing pipeline for a single raw agent log.
    Returns an enriched, compliance-mapped, anomaly-checked DAO.
    
    Called by the backend on every incoming /log request.
    """

    # Step 1: Parse raw log into structured DAO
    dao = parse_to_dao(raw_log)

    # Step 2: Check for anomalies, assign risk level
    dao = check_anomalies(dao)

    # Step 3: Map to RBI compliance clauses
    dao = map_compliance(dao)

    return dao