# app/tools.py
import random
from langchain_core.tools import tool
from pydantic import BaseModel, Field

class AnalyzerInput(BaseModel):
    account_id: str = Field(description="The unique bank account identifier to scan")
    days: int = Field(default=30, description="The lookback window context in days for history tracking")

@tool("transaction_pattern_analyzer", args_schema=AnalyzerInput)
def transaction_pattern_analyzer(account_id: str, days: int = 30) -> str:
    """Analyzes transaction history for potential fraud patterns."""
    deterministic_seed = sum(ord(char) for char in account_id)
    random.seed(deterministic_seed)
    
    risk_score = random.randint(10, 95)
    
    if risk_score > 70:
        return (
            f"Analysis complete for Account {account_id} (Lookback: {days} days). "
            f"Overall AML risk score: {risk_score}/100 (HIGH). "
            f"Flagged: High velocity rapid fund transfers and potential structuring patterns detected. "
            f"Recommend immediate SAR filing."
        )
    else:
        return (
            f"Analysis complete for Account {account_id} (Lookback: {days} days). "
            f"Overall AML risk score: {risk_score}/100 (LOW). "
            f"Account displays standard baseline transactional velocity. Monitor as normal."
        )


class ScreenerInput(BaseModel):
    name: str = Field(description="The full name of the individual or counterparty entity to screen")

@tool("sanctions_pep_screener", args_schema=ScreenerInput)
def sanctions_pep_screener(name: str) -> str:
    """Screens individuals against global sanctions and PEP (Politically Exposed Persons) lists."""
    normalized_name = name.strip().title()
    
    deterministic_seed = sum(ord(char) for char in name.lower())
    random.seed(deterministic_seed)
    match_confidence = random.randint(40, 99)
    
    if match_confidence > 75:
        return (
            f"Match found for target entity '{normalized_name}' — Global Sanctions Watchlist. "
            f"Match confidence: {match_confidence}%. "
            f"Required action: Freeze account immediately, escalate to Compliance Officer, and file a blocking report within 24 hours."
        )
    
    return f"No matches found for entity '{normalized_name}' across global PEP/Sanction watchlists. Match confidence: {match_confidence}%."


class SarInput(BaseModel):
    account_id: str = Field(description="The target banking account identifier for the report")
    findings: str = Field(description="Identified suspicious patterns, risk scores, or investigative notes to compile")

@tool("sar_draft_generator", args_schema=SarInput)
def sar_draft_generator(account_id: str, findings: str) -> str:
    """Generates a draft for a Suspicious Activity Report (SAR) based on case files."""
    return (
        f"--- CONFIDENTIAL REGULATORY SAR NARRATIVE DRAFT ---\n"
        f"SUBJECT ACCOUNT IDENTIFIER: {account_id}\n"
        f"DETECTION TIMELINE: Active Investigation Window\n"
        f"SUMMARY OF SUSPICIOUS ACTIVITY LOGGED: {findings}\n"
        f"REGULATORY COMPLIANCE REQUIREMENT: File formal report via FinCEN/FIU portal within 30-day statutory window."
    )


def get_tools():
    return [transaction_pattern_analyzer, sanctions_pep_screener, sar_draft_generator]
