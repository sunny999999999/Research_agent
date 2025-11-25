## This project is an AI-powered autonomous research agent that generates detailed research reports using:

### Google Sheets (via API)
### Firecrawl Web Search + Extraction
### OpenAI / Gemini LLMs
### Autogen Framework
### Streamlit Frontend

The agent performs web search, content extraction, reasoning, and structured report generation automatically.
A Streamlit UI allows users to input:
### Prospect Name and Company Name

## The agent then produces a personalized research report saved as report.txt.
```
- pip install uv
- uv init
- uv venv
- uv pip install -r requirements.txt
- pass the google sheet id in .env (if required)
- pass gemini api key in .env
-pass the fire crawl api key in .env
-streamlit run app.py
```


