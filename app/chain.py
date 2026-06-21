# app/chain.py
import os
from dotenv import load_dotenv
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI

from .tools import get_tools
from .prompts import get_agent_prompt
from .memory import get_session_history  # We will fill this in next

load_dotenv()

def create_aml_agent_executor():
    llm = ChatOpenAI(model=os.getenv("MODEL_NAME", "gpt-4o-mini"), temperature=0.0)
    
    tools_list = get_tools()
    
    prompt_template, example_selector = get_agent_prompt()
    
    base_agent = create_openai_tools_agent(llm, tools_list, prompt_template)
    
    agent_executor = AgentExecutor(
        agent=base_agent, 
        tools=tools_list, 
        verbose=True,
        handle_parsing_errors=True
    )
    
    def route_inputs(inputs: dict):
        matched_examples = example_selector.select_examples({"input": inputs["input"]})
        formatted_context = "\n\n".join(
            [f"User: {ex['input']}\nAssistant: {ex['output']}" for ex in matched_examples]
        )
        return {
            "input": inputs["input"],
            "few_shot_context": formatted_context,
            "chat_history": inputs.get("chat_history", [])
        }

    composed_chain = route_inputs | agent_executor

    return RunnableWithMessageHistory(
        composed_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history"
    )

aml_agent_chain = create_aml_agent_executor()

def chat(session_id: str, message: str) -> dict:
    try:
        output = aml_agent_chain.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )
        return {
            "response": output["output"],
            "status": "success"
        }
    except Exception as err:
        return {
            "response": "An operational system anomaly occurred while running compliance analytics. Please check transactional telemetry records manually.",
            "status": "degraded_fallback"
        }
