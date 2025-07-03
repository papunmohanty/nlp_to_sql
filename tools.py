"""
Tools for SQL query execution and validation
"""
from typing import Dict, Any, List
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from database import DatabaseManager
import pandas as pd


class QueryExecutorInput(BaseModel):
    sql_query: str = Field(description="SQL query to execute")

class QueryExecutorTool(BaseTool):
    name: str = "sql_query_executor"
    description: str = "Execute SQL queries against the database and return results"
    args_schema: type[BaseModel] = QueryExecutorInput
    db_manager: DatabaseManager = Field(exclude=True)
    
    def __init__(self, db_manager: DatabaseManager, **data):
        super().__init__(db_manager=db_manager, **data)
    
    def _run(self, sql_query: str) -> str:
        """Execute the SQL query and return formatted results"""
        try:
            # Basic validation
            if not self._is_safe_query(sql_query):
                return "Error: Query contains potentially dangerous operations"
            
            results = self.db_manager.execute_query(sql_query)
            
            if not results:
                return "Query executed successfully but returned no results"
            
            # Format results for display
            return self._format_results(results)
            
        except Exception as e:
            return f"Error executing query: {str(e)}"
    
    def _is_safe_query(self, query: str) -> bool:
        """Basic safety check for SQL queries"""
        dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
        query_upper = query.upper()
        
        for keyword in dangerous_keywords:
            if keyword in query_upper:
                return False
        return True
    
    def _format_results(self, results: List[Dict[str, Any]]) -> str:
        # print(f"SQL Query Result Type:\n{type(results)}")
        # print(f"SQL Query Result:\n{results}")
        # """Format query results for display"""
        # if not results:
        #     return "No results found"
        
        # # Get column headers
        # headers = list(results[0].keys())
        
        # # Create formatted table
        # formatted = "Query Results:\n"
        # formatted += "-" * 50 + "\n"
        
        # # Add headers
        # formatted += " | ".join(f"{header:15}" for header in headers) + "\n"
        # formatted += "-" * 50 + "\n"
        
        # # Add data rows (limit to first 10 for readability)
        # for i, row in enumerate(results[:10]):
        #     formatted += " | ".join(f"{str(row[header]):15}" for header in headers) + "\n"
        
        # if len(results) > 10:
        #     formatted += f"\n... and {len(results) - 10} more rows"
        # print(f"formatted:\n{formatted}")
        # return formatted
        return pd.DataFrame(results)


class SchemaInfoInput(BaseModel):
    table_name: str = Field(description="Optional table name to get specific info", default="")

class SchemaInfoTool(BaseTool):
    name: str = "schema_info"
    description: str = "Get database schema information including table names and column details"
    args_schema: type[BaseModel] = SchemaInfoInput
    db_manager: DatabaseManager = Field(exclude=True)
    
    def __init__(self, db_manager: DatabaseManager, **data):
        super().__init__(db_manager=db_manager, **data)
    
    def _run(self, table_name: str = "") -> str:
        """Get schema information"""
        try:
            schema_info = self.db_manager.get_schema_info()
            
            if table_name:
                # Filter for specific table
                lines = schema_info.split('\n')
                filtered_lines = []
                capture = False
                
                for line in lines:
                    if f"Table: {table_name}" in line:
                        capture = True
                    elif line.startswith("Table:") and capture:
                        break
                    
                    if capture:
                        filtered_lines.append(line)
                
                return '\n'.join(filtered_lines) if filtered_lines else f"Table '{table_name}' not found"
            
            return schema_info
            
        except Exception as e:
            return f"Error getting schema info: {str(e)}"

class QueryValidatorInput(BaseModel):
    sql_query: str = Field(description="SQL query to validate")

class QueryValidatorTool(BaseTool):
    name: str = "sql_validator"
    description: str = "Validate SQL query syntax and structure"
    args_schema: type[BaseModel] = QueryValidatorInput
    db_manager: DatabaseManager = Field(exclude=True)
    
    def __init__(self, db_manager: DatabaseManager, **data):
        super().__init__(db_manager=db_manager, **data)
    
    def _run(self, sql_query: str) -> str:
        """Validate SQL query"""
        try:
            # Basic syntax validation
            validation_errors = []
            
            # Check for basic SQL structure
            query_clean = sql_query.strip().upper()
            
            if not query_clean:
                return "Error: Empty query"
            
            # Check if it starts with SELECT (for read-only queries)
            if not query_clean.startswith('SELECT'):
                validation_errors.append("Warning: Only SELECT queries are recommended")
            
            # Check for balanced parentheses
            if query_clean.count('(') != query_clean.count(')'):
                validation_errors.append("Error: Unbalanced parentheses")
            
            # Check for semicolon at end (optional but good practice)
            if not query_clean.endswith(';'):
                validation_errors.append("Warning: Query should end with semicolon")
            
            # Try to parse with database (this will catch syntax errors)
            try:
                # Use EXPLAIN to validate without executing
                explain_query = f"EXPLAIN QUERY PLAN {sql_query}"
                self.db_manager.connection.cursor().execute(explain_query)
                
            except Exception as parse_error:
                validation_errors.append(f"Syntax Error: {str(parse_error)}")
            
            if validation_errors:
                return "Validation Issues:\n" + "\n".join(validation_errors)
            else:
                return "Query validation passed successfully"
                
        except Exception as e:
            return f"Error during validation: {str(e)}"

def create_tools(db_manager: DatabaseManager) -> List[BaseTool]:
    """Create and return all tools"""
    return [
        QueryExecutorTool(db_manager=db_manager),
        SchemaInfoTool(db_manager=db_manager),
        QueryValidatorTool(db_manager=db_manager)
    ]
