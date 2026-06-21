# app/logger.py
import json
import logging
from datetime import datetime

class ComplianceJsonFormatter(logging.Formatter):
    def format(self, record):
        log_payload = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "session_id": getattr(record, "session_id", "SYSTEM_LOG")
        }
        return json.dumps(log_payload)

def setup_compliance_logger():
    logger = logging.getLogger("aml_co_pilot")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(ComplianceJsonFormatter())
        logger.addHandler(stream_handler)
        
    return logger

logger = setup_compliance_logger()