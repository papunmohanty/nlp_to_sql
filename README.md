# 🔍 NLP to SQL Query Converter

A powerful application that converts natural language questions into SQL queries using LangChain, LangGraph, Agents, and Tools. Built with uv for fast Python package management and featuring both command-line and web interfaces.

## 🌟 Features

- **Natural Language Processing**: Convert plain English questions to SQL queries
- **LangGraph Workflow**: Sophisticated agent-based processing pipeline
- **Multiple Interfaces**: Command-line and web-based (Streamlit) interfaces
- **SQLite Database**: Pre-configured with sample employee, department, and project data
- **Query Validation**: Built-in SQL query validation and safety checks
- **Tool Integration**: Modular tools for schema inspection, query execution, and validation
- **Real-time Execution**: Execute queries and get formatted results

## 🏗️ Architecture

The application is built using:

- **uv**: Fast Python package manager and project management
- **LangChain**: Framework for developing applications with LLMs
- **LangGraph**: Library for building stateful, multi-actor applications
- **OpenAI GPT**: Large language model for natural language understanding
- **SQLite**: Lightweight database for data storage
- **Streamlit**: Web framework for the user interface
- **Pydantic**: Data validation and settings management

## 📋 Prerequisites

- Python 3.12+
- uv package manager
- OpenAI API key

## 🚀 Installation

1. **Clone and navigate to the project**:
   ```bash
   cd nlp-to-sql-app
   ```

2. **Install dependencies using uv**:
   ```bash
   uv sync
   ```

3. **Set up environment variables**:
   ```bash
   cp .env.template .env
   # Edit .env and add your OpenAI API key
   ```

   Or export directly:
   ```bash
   export OPENAI_API_KEY="your-openai-api-key-here"
   export OPENAI_ENDPOINT="https://your-openapi-endpoint/
   ```

## 🎯 Usage

### Command Line Interface

Run the interactive command-line interface:

```bash
uv run python main.py
```

Example session:
```
🔍 NLP to SQL Query Converter
==================================================
Welcome! This application converts natural language queries to SQL.

🚀 Initializing NLP to SQL Agent...
✅ Agent initialized successfully!

📊 Database Schema:
...

💬 Interactive Mode - Enter your questions (type 'quit' to exit)
--------------------------------------------------

🤔 Your question: Show me all employees in the IT department

🔄 Processing your query...

📝 Generated SQL:
   SELECT * FROM employees WHERE department = 'IT';

🤖 Response:
   I found 4 employees in the IT department: John Doe (Software Engineer), Bob Johnson (DevOps Engineer), Eva Davis (Senior Developer), and Grace Lee (QA Engineer).
```

### Web Interface

Launch the Streamlit web application:

```bash
uv run streamlit run web_app.py
```

Then open your browser to `http://localhost:8501`

## 📊 Database Schema

The application comes with a pre-configured SQLite database containing:

### Tables

1. **employees**
   - id (INTEGER PRIMARY KEY)
   - name (TEXT)
   - department (TEXT)
   - role (TEXT)
   - salary (INTEGER)
   - hire_date (DATE)
   - email (TEXT UNIQUE)

2. **departments**
   - dept_id (INTEGER PRIMARY KEY)
   - dept_name (TEXT UNIQUE)
   - location (TEXT)
   - manager_id (INTEGER)

3. **projects**
   - project_id (INTEGER PRIMARY KEY)
   - project_name (TEXT)
   - department_id (INTEGER)
   - start_date (DATE)
   - end_date (DATE)
   - budget (REAL)

### Sample Data
- 8 employees across IT, HR, Marketing, and Finance departments
- 4 departments with locations and managers
- 4 active projects with budgets and timelines

## 🔧 Components

### Core Files

- **`main.py`**: Command-line interface entry point
- **`web_app.py`**: Streamlit web interface
- **`nlp_to_sql_agent.py`**: Main agent using LangGraph workflow
- **`database.py`**: Database management and schema definition
- **`tools.py`**: LangChain tools for SQL operations
- **`sql_schema.py`**: Simple schema creation script

### LangGraph Workflow

The agent follows this workflow:
1. **Get Schema**: Retrieve database schema information
2. **Generate SQL**: Convert natural language to SQL using LLM
3. **Validate SQL**: Check query syntax and safety
4. **Execute SQL**: Run the query against the database
5. **Format Response**: Create human-readable response

### Tools

1. **QueryExecutorTool**: Execute SQL queries safely
2. **SchemaInfoTool**: Retrieve database schema information
3. **QueryValidatorTool**: Validate SQL syntax and structure

## 🎭 Example Queries

Try these natural language questions:

- "Show me all employees in the IT department"
- "Who are the highest paid employees?"
- "How many employees work in each department?"
- "Find all employees hired after 2022"
- "What projects are currently running?"
- "Show me employees with salary greater than 70000"
- "List all departments and their locations"

## 🛡️ Safety Features

- **Read-only queries**: Only SELECT statements are allowed
- **Query validation**: Syntax checking before execution
- **Error handling**: Comprehensive error catching and reporting
- **Safe execution**: Protection against dangerous SQL operations

## 🔮 Future Enhancements

- Support for multiple database types (PostgreSQL, MySQL)
- Query history and favorites
- Export results to CSV/Excel
- Advanced analytics and visualization
- Multi-table join optimization
- Custom schema upload

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

1. **OpenAI API Key Error**:
   - Ensure your API key is correctly set in environment variables
   - Check that your OpenAI account has sufficient credits

2. **Database Connection Error**:
   - The SQLite database is created automatically
   - Check file permissions in the project directory

3. **Dependency Issues**:
   - Run `uv sync` to ensure all dependencies are installed
   - Check Python version compatibility (3.12+)

4. **Import Errors**:
   - Ensure you're running commands from the project root directory
   - Verify the virtual environment is activated when using uv

### Getting Help

If you encounter issues:
1. Check the error messages carefully
2. Ensure all prerequisites are met
3. Verify your OpenAI API key is valid
4. Check the GitHub issues for similar problems

---

**Built with ❤️ using LangChain, LangGraph, and modern Python tools**
