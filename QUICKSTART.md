# 🚀 Quick Start Guide

## Setup (2 minutes)

1. **Install dependencies**:

   ```bash
   uv sync
   ```

2. **Set your OpenAI API key**:

   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   export OPENAI_ENDPOINT="https://your-openapi-endpoint/
   ```

3. **Run the application**:
   ```bash
   uv run python run.py
   ```

## Test Without API Key

You can test the tools and database without an OpenAI API key:

```bash
uv run python test_tools.py
```

## Quick Demo

Try these natural language queries:

- "Show me all employees in the IT department"
- "Who are the highest paid employees?"
- "How many employees work in each department?"

## File Structure

```
nlp-to-sql-app/
├── main.py              # Command-line interface
├── web_app.py           # Streamlit web interface
├── run.py               # Launcher script
├── nlp_to_sql_agent.py  # Main LangGraph agent
├── database.py          # Database management
├── tools.py             # LangChain tools
├── test_tools.py        # Tool testing
├── sql_schema.py        # Basic schema script
├── .env.template        # Environment template
├── README.md            # Full documentation
└── QUICKSTART.md        # This file
```

## Architecture

```
User Query → LangGraph Agent → Tools → Database → Response
           ↓
    1. Get Schema
    2. Generate SQL
    3. Validate SQL
    4. Execute SQL
    5. Format Response
```

## Key Components

- **uv**: Package management
- **LangChain**: LLM framework
- **LangGraph**: Workflow orchestration
- **OpenAI GPT**: Natural language understanding
- **SQLite**: Local database
- **Streamlit**: Web interface

---

**Ready to convert natural language to SQL!** 🎯
