# Banking AML & Fraud Detection Co-Pilot

## Initialize Your Virtual Environment
```bash
# Create environment
python -m venv .venv

# Activate
source .venv/bin/activate
```

## Install Project Dependencies
```bash
pip install -r requirements.txt
```

## Setup Your Local Environment Configuration
```env
OPENAI_API_KEY=your_actual_openai_api_key
MODEL_NAME=gpt-4o-mini
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_actual_langsmith_api_key
LANGCHAIN_PROJECT=aml-fraud-copilot
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
```

## Running the Application Suite

### 1. Launch the FastAPI Backend Core
```bash
uvicorn app.main:app --reload
```

### 2. Launch the Interactive Dashboard Portal
```bash
streamlit run frontend/streamlit.py
```

## Run the Tests & Generate Test Report
```bash
pytest --cov=app tests/
```
