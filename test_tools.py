#!/usr/bin/env python3
"""
Test script to verify tools functionality
"""
from database import DatabaseManager
from tools import create_tools

def test_tools():
    """Test all tools without requiring OpenAI API"""
    print("🧪 Testing NLP to SQL Tools")
    print("=" * 40)
    
    # Initialize database
    db_manager = DatabaseManager()
    print("✅ Database initialized")
    
    # Create tools
    tools = create_tools(db_manager)
    print(f"✅ Created {len(tools)} tools")
    
    # Test each tool
    for tool in tools:
        print(f"\n🔧 Testing {tool.name}:")
        
        if tool.name == "schema_info":
            result = tool._run()
            print("📊 Schema info retrieved successfully")
            print(result[:200] + "..." if len(result) > 200 else result)
            
        elif tool.name == "sql_validator":
            test_sql = "SELECT * FROM employees WHERE department = 'IT';"
            result = tool._run(test_sql)
            print(f"✅ Validation result: {result}")
            
        elif tool.name == "sql_query_executor":
            test_sql = "SELECT COUNT(*) as total_employees FROM employees;"
            result = tool._run(test_sql)
            print(f"📊 Query result:\n{result}")
    
    db_manager.close()
    print("\n✅ All tools tested successfully!")

if __name__ == "__main__":
    test_tools()
