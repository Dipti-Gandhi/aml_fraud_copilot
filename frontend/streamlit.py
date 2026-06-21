# frontend/streamlit.py
import streamlit as st
import requests
import time
import uuid

FASTAPI_URL = "http://localhost:8000"

st.set_page_config(page_title="AML Co-Pilot Dashboard", layout="wide")
st.title("AML & Fraud Detection Co-Pilot")

def response_generator(text):
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.03)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

with st.sidebar:
    st.subheader("Compliance Session Telemetry")
    st.info(f"Active Session ID:\n`{st.session_state.session_id}`")
    
    if st.button("Reset Conversational Memory", use_container_width=True):
        try:
            resp = requests.post(f"{FASTAPI_URL}/reset", json={"session_id": st.session_state.session_id}, timeout=5)
            if resp.status_code == 200:
                st.session_state.messages = []
                st.success("Context memory purged successfully.")
                st.rerun()
            else:
                st.error("Failed to clear backend memory registry.")
        except Exception:
            st.error("Unable to establish communication link with backend API node.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input := st.chat_input("Enter account ID inquiry, sanctions search string, or SAR generation request..."):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
        
    response_text = ""
    is_fallback = False
    
    with st.spinner("Invoking specialized compliance tool execution graphs..."):
        try:
            resp = requests.post(
                f"{FASTAPI_URL}/chat",
                json={
                    "message": user_input,
                    "session_id": st.session_state.session_id,
                },
                timeout=60,
            )
            if resp.status_code == 200:
                data = resp.json()
                response_text = data.get("response", "")
                
                if data.get("status") == "degraded_fallback":
                    is_fallback = True
            else:
                response_text = "Error: Backend orchestration gateway rejected the data package."
        except requests.exceptions.Timeout:
            response_text = "Error: Compliance tracking operations timed out."
        except Exception:
            response_text = "Error: Communication interface connection failure."

    with st.chat_message("assistant"):
        if is_fallback:
            st.warning("Notice: Response delivered via secondary graceful degradation safety chain.")
            
        final_response = st.write_stream(response_generator(response_text))
        
    st.session_state.messages.append({"role": "assistant", "content": final_response})
