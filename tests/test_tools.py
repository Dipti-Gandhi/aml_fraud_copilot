# tests/test_tools.py
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import pytest
from app.tools import transaction_pattern_analyzer, sanctions_pep_screener, sar_draft_generator
from app.chain import chat
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

TEST_MATRIX = [
    {"id": 1, "category": "Tool Usage", "query": "Analyze account 55-389 for suspicious activity."},
    {"id": 2, "category": "Tool Usage", "query": "Are there any structuring patterns in recent deposits?"},
    {"id": 3, "category": "Tool Usage", "query": "Screen beneficiary ‘Al-Farooq Trading LLC’ against sanctions."},
    {"id": 4, "category": "Tool Usage", "query": "Generate a SAR for investigation case #INV-2210."},
    {"id": 5, "category": "Tool Usage", "query": "What is the AML risk score for customer ID C-7781?"},
    {"id": 6, "category": "Tool Usage", "query": "Show me all cash transactions above 9L in the last quarter."},
    {"id": 7, "category": "Tool Usage", "query": "Flag any round-trip transactions between accounts A and B."},
    {"id": 8, "category": "FAQ / Follow-up", "query": "Is this customer a Politically Exposed Person?"},
    {"id": 9, "category": "FAQ / Follow-up", "query": "Compare transaction velocity this month vs. last 6-month average."},
    {"id": 10, "category": "FAQ / Follow-up", "query": "What are the regulatory filing deadlines for this case?"},
    {"id": 11, "category": "FAQ / Follow-up", "query": "List all counterparties associated with flagged account."},
    {"id": 12, "category": "FAQ / Follow-up", "query": "Has this customer triggered any previous alerts?"},
    {"id": 13, "category": "FAQ / Follow-up", "query": "What risk typology does this pattern match?"},
    {"id": 14, "category": "FAQ / Follow-up", "query": "Draft an escalation memo for the compliance committee."},
    {"id": 15, "category": "Multi-turn", "query": "Run enhanced due diligence on customer profile."},
    {"id": 16, "category": "Multi-turn", "query": "Check if the originating bank is in a high-risk jurisdiction."},
    {"id": 17, "category": "Multi-turn", "query": "What STR fields are mandatory for RBI filing?"},
    {"id": 18, "category": "Multi-turn", "query": "Identify the ultimate beneficial owner of the receiving entity."},
    {"id": 19, "category": "Multi-turn", "query": "Summarize all open AML alerts for my review queue."},
    {"id": 20, "category": "Multi-turn", "query": "Provide an investigation timeline with key evidence points."}
]

def test_transaction_pattern_analyzer_unit():
    result = transaction_pattern_analyzer.invoke({"account_id": "55-389", "days": 30})
    assert "Analysis complete" in result or "Risk Score" in result
    assert "55-389" in result

def test_sanctions_pep_screener_unit():
    result = sanctions_pep_screener.invoke({"name": "Al-Farooq Trading LLC"})
    assert "Match" in result or "No matches" in result

def test_sar_draft_generator_unit():
    result = sar_draft_generator.invoke({"account_id": "INV-2210", "findings": "Automated system test run traces."})
    assert "SAR NARRATIVE" in result or "REGULATORY COMPLIANCE" in result

@pytest.mark.parametrize("case", TEST_MATRIX)
def test_execute_matrix_query_and_generate_report(case):
    session_id = f"matrix_verification_session_{case['id']}"
    
    outcome = chat(session_id=session_id, message=case["query"])
    
    assert "response" in outcome
    assert outcome["status"] in ["success", "degraded_fallback"]
    assert len(outcome["response"]) > 0

def test_fastapi_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "model_configuration" in data

def test_fastapi_chat_endpoint():
    payload = {
        "message": "Analyze transaction risk thresholds for account 44-102",
        "session_id": "api_integration_test_token"
    }
    response = client.post("/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "api_integration_test_token"
    assert "response" in data
    assert "status" in data

def test_fastapi_reset_endpoint():
    payload = {"session_id": "api_integration_test_token"}
    response = client.post("/reset", json=payload)
    assert response.status_code == 200
    assert "cleared successfully" in response.json()["message"]

def test_fastapi_reset_endpoint_missing_payload():
    response = client.post("/reset", json={})
    assert response.status_code == 400
    assert "Missing required" in response.json()["detail"]
