# app/prompts.py
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate, FewShotPromptTemplate
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

FEW_SHOT_EXAMPLES = [
    {
        "input": "Analyze transactions for account 90-221 in the last 30 days.",
        "output": "Analysis complete. 14 transactions flagged: 8 cash deposits just below ₹10L threshold (structuring pattern), 4 rapid fund transfers to 3 different beneficiaries within 48 hrs, and 2 round-trip flows. Overall AML risk score: 87/100 (HIGH). Recommend immediate SAR filing."
    },
    {
        "input": "Screen the name ‘Viktor Petrov’ against sanctions lists.",
        "output": "Match found: Viktor A. Petrov — OFAC SDN List (added 2023-06-15), match confidence 94%. Required action: freeze account, escalate to Compliance Officer, and file a blocking report within 24 hours."
    },
    {
        "input": "Draft a SAR for the flagged account.",
        "output": "SAR narrative generated for Account 90-221. Summary: Suspected structuring of cash deposits totaling ₹78L over 30 days across 3 branches, followed by immediate wire transfers to shell entities. Filing deadline: 30 days from detection."
    }
]

SYSTEM_PROMPT = """You are an expert Banking AML Compliance and Fraud Detection Assistant Co-Pilot. 
Your core operational scope covers identifying transactional fraud patterns, executing sanctions screening, and drafting regulatory Suspicious Activity Report (SAR) briefs.

Operational Directives:
1. Always maintain a highly professional, objective, and regulatory-focused tone.
2. Rely entirely on your custom toolkits to execute transaction analysis, name screenings, and report generation.
3. If an evaluation indicates a suspicious pattern, recommend clear, timeline-driven tracking actions following statutory compliance guidelines.
"""

def get_agent_prompt():
    example_template = PromptTemplate(
        input_variables=["input", "output"],
        template="User: {input}\nAssistant: {output}"
    )
    
    example_selector = SemanticSimilarityExampleSelector.from_examples(
        FEW_SHOT_EXAMPLES,
        OpenAIEmbeddings(),
        Chroma,
        k=1  
    )
    
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_template,
        prefix="Review this contextually relevant baseline historical resolution profile for formatting guidance:",
        suffix="Current Compliance Inquiry: {input}",
        input_variables=["input"]
    )

    return ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("system", "Reference Historical Context Trace:\n{few_shot_context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]), example_selector
