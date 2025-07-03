"""
NLP to SQL Agent using LangGraph
"""
import os
from typing import Dict, Any, List, Optional
# from langchain_openai import ChatOpenAI
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.schema import BaseMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict, Annotated
from database import DatabaseManager
from tools import create_tools
import pandas as pd


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    generated_sql: str
    sql_results: pd.DataFrame
    schema_info: str
    validation_result: str
    final_response: str

class NLPToSQLAgent:
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        # Initialize OpenAI client
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # self.llm = ChatOpenAI(
        #     api_key=self.api_key,
        #     model=model,
        #     temperature=0
        # )
        self.llm = AzureChatOpenAI(
            azure_endpoint=os.environ.get("OPENAI_ENDPOINT"),
            api_key=os.environ.get("OPENAI_API_KEY"),
            azure_deployment=os.environ.get("DEPLOYMENT"),
            openai_api_type=os.environ.get("OPENAI_API_TYPE"),
            # api_version=os.environ.get("OPENAI_API_VERSION"),
            temperature=0
        )
        
        # Initialize database and tools
        self.db_manager = DatabaseManager()
        self.tools = create_tools(self.db_manager)
        
        # Create the workflow graph
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(AgentState)
        
        # Add nodes
        workflow.add_node("get_schema", self._get_schema_node)
        workflow.add_node("generate_sql", self._generate_sql_node)
        workflow.add_node("validate_sql", self._validate_sql_node)
        workflow.add_node("execute_sql", self._execute_sql_node)
        workflow.add_node("format_response", self._format_response_node)
        
        # Define the flow
        workflow.set_entry_point("get_schema")
        workflow.add_edge("get_schema", "generate_sql")
        workflow.add_edge("generate_sql", "validate_sql")
        workflow.add_edge("validate_sql", "execute_sql")
        workflow.add_edge("execute_sql", "format_response")
        workflow.add_edge("format_response", END)
        
        return workflow.compile()
    
    def _get_schema_node(self, state: AgentState) -> AgentState:
        """Get database schema information"""
        schema_tool = next(tool for tool in self.tools if tool.name == "schema_info")
        schema_info = schema_tool._run()
        
        state["schema_info"] = schema_info
        return state
    
    def _generate_sql_node(self, state: AgentState) -> AgentState:
        """Generate SQL query from natural language"""
        prompt = ChatPromptTemplate.from_template("""
You are an expert SQL query generator. Given a natural language query and database schema,
generate a precise SQL query.

Database Schema:
{schema_info}

User Query: {user_query}

Guidelines:
1. Only generate SELECT queries for safety
2. Use proper SQL syntax for SQLite
3. Include appropriate WHERE clauses, JOINs, and ORDER BY as needed
4. Return only the SQL query without explanations
5. End the query with a semicolon

SQL Query:
""")
        
        formatted_prompt = prompt.format(
            schema_info=state["schema_info"],
            user_query=state["user_query"]
        )
        
        response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
        sql_query = response.content.strip()
        
        # Clean up the response to extract just the SQL
        if "```sql" in sql_query:
            sql_query = sql_query.split("```sql")[1].split("```")[0].strip()
        elif "```" in sql_query:
            sql_query = sql_query.split("```")[1].strip()
        
        state["generated_sql"] = sql_query
        state["messages"].append(AIMessage(content=f"Generated SQL: {sql_query}"))
        
        return state
    
    def _validate_sql_node(self, state: AgentState) -> AgentState:
        """Validate the generated SQL query"""
        validator_tool = next(tool for tool in self.tools if tool.name == "sql_validator")
        validation_result = validator_tool._run(state["generated_sql"])
        
        state["validation_result"] = validation_result
        return state
    
    def _execute_sql_node(self, state: AgentState) -> AgentState:
        """Execute the SQL query"""
        executor_tool = next(tool for tool in self.tools if tool.name == "sql_query_executor")
        sql_results = executor_tool._run(state["generated_sql"])
        
        state["sql_results"] = sql_results
        return state
    
    def _format_response_node(self, state: AgentState) -> AgentState:
        """Format the final response"""
        prompt = ChatPromptTemplate.from_template("""
Based on the user's natural language query and the SQL execution results, 
provide a clear, human-readable response.

User Query: {user_query}
Generated SQL: {generated_sql}
SQL Results: {sql_results}
Validation: {validation_result}

Provide a natural language response that:
1. Answers the user's question directly
2. Mentions any important insights from the data
3. If there were validation warnings, briefly mention them
4. Keep the response conversational and helpful

Response:
""")
        
        formatted_prompt = prompt.format(
            user_query=state["user_query"],
            generated_sql=state["generated_sql"],
            sql_results=state["sql_results"],
            validation_result=state["validation_result"]
        )
        
        response = self.llm.invoke([HumanMessage(content=formatted_prompt)])
        final_response = response.content.strip()
        
        state["final_response"] = final_response
        state["messages"].append(AIMessage(content=final_response))
        
        return state
    
    def query(self, user_input: str) -> Dict[str, Any]:
        """Process a natural language query and return SQL + results"""
        initial_state = AgentState(
            messages=[HumanMessage(content=user_input)],
            user_query=user_input,
            generated_sql="",
            sql_results="",
            schema_info="",
            validation_result="",
            final_response=""
        )
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return {
            "user_query": final_state["user_query"],
            "generated_sql": final_state["generated_sql"],
            "validation_result": final_state["validation_result"],
            "sql_results": final_state["sql_results"],
            "final_response": final_state["final_response"]
        }
    
    def close(self):
        """Close database connection"""
        self.db_manager.close()

# Example usage and testing
if __name__ == "__main__":
    # Note: You need to set your OpenAI API key
    # export OPENAI_API_KEY="your-api-key-here"
    
    try:
        agent = NLPToSQLAgent()
        
        # Test queries
        test_queries = [
            "Show me all employees in the IT department",
            "Who are the highest paid employees?",
            "How many employees work in each department?",
            "What projects are currently running?",
            "Find all employees hired after 2022"
        ]
        
        print("NLP to SQL Agent Test")
        print("=" * 50)
        
        for query in test_queries:
            print(f"\nQuery: {query}")
            print("-" * 30)
            
            try:
                result = agent.query(query)
                print(f"SQL: {result['generated_sql']}")
                print(f"Response: {result['final_response']}")
            except Exception as e:
                print(f"Error: {e}")
    
    except ValueError as e:
        print(f"Setup Error: {e}")
        print("Please set your OpenAI API key using: export OPENAI_API_KEY='your-key-here'")
    
    finally:
        if 'agent' in locals():
            agent.close()
