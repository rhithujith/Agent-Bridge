from dao import DAO
from parser import parse_to_dao
from anomaly import check_anomalies
from compliance import map_compliance
from ai_analyser import analyze
from typing import Any, Dict


def process(raw_log: Dict[str, Any], api_key: str = None) -> DAO:
    """
    Full processing pipeline for a single raw agent log.
    
    api_key is optional — if not provided, AI analysis is skipped.
    This lets the system work without an API key during development.
    """

    # Step 1: Parse
    dao = parse_to_dao(raw_log)

    # Step 2: Rule-based anomaly detection
    dao = check_anomalies(dao)

    # Step 3: RBI clause mapping
    dao = map_compliance(dao)

    # Step 4: AI compliance analysis (skipped if no api_key)
    if api_key:
        dao = analyze(dao, api_key)

    return dao