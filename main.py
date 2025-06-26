#!/usr/bin/env python3
"""
Main entry point for the NLP to SQL Application
"""
import sys
import os
from dotenv import load_dotenv
from nlp_to_sql_agent import NLPToSQLAgent
from database import DatabaseManager

def main():
    """Main function to run the NLP to SQL application"""
    
    # Load environment variables
    load_dotenv()
    
    print("🔍 NLP to SQL Query Converter")
    print("=" * 50)
    print("Welcome! This application converts natural language queries to SQL.")
    print()
    
    # Check for OpenAI API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ Error: OpenAI API key not found!")
        print("Please set your OPENAI_API_KEY environment variable:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        print()
        print("Or create a .env file with:")
        print("OPENAI_API_KEY=your-api-key-here")
        return 1
    
    # Initialize the agent
    try:
        print("🚀 Initializing NLP to SQL Agent...")
        agent = NLPToSQLAgent(api_key=api_key)
        print("✅ Agent initialized successfully!")
        print()
        
        # Show database schema
        print("📊 Database Schema:")
        print(agent.db_manager.get_schema_info())
        print()
        
        # Interactive loop
        print("💬 Interactive Mode - Enter your questions (type 'quit' to exit)")
        print("-" * 50)
        
        while True:
            try:
                user_input = input("\n🤔 Your question: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                
                if not user_input:
                    continue
                
                print("🔄 Processing your query...")
                result = agent.query(user_input)
                
                print(f"\n📝 Generated SQL:")
                print(f"   {result['generated_sql']}")
                
                print(f"\n🤖 Response:")
                print(f"   {result['final_response']}")
                
                if "warning" in result['validation_result'].lower():
                    print(f"\n⚠️  Validation: {result['validation_result']}")
                elif "error" in result['validation_result'].lower():
                    print(f"\n❌ Validation: {result['validation_result']}")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
        
        agent.close()
        
    except Exception as e:
        print(f"❌ Error initializing agent: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
