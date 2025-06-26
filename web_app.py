"""
Web interface for NLP to SQL application using Streamlit
"""
import streamlit as st
import os
from nlp_to_sql_agent import NLPToSQLAgent
from database import DatabaseManager
import pandas as pd

def main():
    st.set_page_config(
        page_title="NLP to SQL Query Converter",
        page_icon="🔍",
        layout="wide"
    )
    
    st.title("🔍 NLP to SQL Query Converter")
    st.markdown("Convert natural language questions into SQL queries and execute them!")
    
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # API Key input
    api_key = st.sidebar.text_input(
        "OpenAI API Key", 
        type="password",
        help="Enter your OpenAI API key to use the service"
    )
    
    if not api_key:
        st.warning("Please enter your OpenAI API key in the sidebar to continue.")
        st.stop()
    
    # Initialize the agent
    try:
        if "agent" not in st.session_state:
            st.session_state.agent = NLPToSQLAgent(api_key=api_key)
            st.success("✅ Agent initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing agent: {e}")
        st.stop()
    
    # Database schema display
    with st.expander("📊 Database Schema", expanded=False):
        db_manager = DatabaseManager()
        schema_info = db_manager.get_schema_info()
        st.text(schema_info)
        db_manager.close()
    
    # Main interface
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Enter your question")
        
        # Predefined example queries
        example_queries = [
            "Show me all employees in the IT department",
            "Who are the highest paid employees?", 
            "How many employees work in each department?",
            "Find all employees hired after 2022",
            "What projects are currently running?",
            "Show me employees with salary greater than 70000",
            "List all departments and their locations"
        ]
        
        selected_example = st.selectbox(
            "Choose an example query:",
            [""] + example_queries
        )
        
        # Text input for custom query
        user_query = st.text_area(
            "Or enter your custom question:",
            value=selected_example if selected_example else "",
            height=100,
            placeholder="e.g., Show me all employees in the IT department"
        )
        
        # Submit button
        if st.button("🚀 Generate SQL & Execute", type="primary"):
            if user_query.strip():
                with st.spinner("Processing your query..."):
                    try:
                        result = st.session_state.agent.query(user_query)
                        
                        # Store results in session state
                        st.session_state.last_result = result
                        
                        st.success("✅ Query processed successfully!")
                        
                    except Exception as e:
                        st.error(f"Error processing query: {e}")
            else:
                st.warning("Please enter a question first!")
    
    with col2:
        st.header("Quick Stats")
        
        # Quick database stats
        try:
            db_manager = DatabaseManager()
            
            # Employee count
            emp_count = db_manager.execute_query("SELECT COUNT(*) as count FROM employees")[0]['count']
            st.metric("Total Employees", emp_count)
            
            # Department count
            dept_count = db_manager.execute_query("SELECT COUNT(DISTINCT department) as count FROM employees")[0]['count']
            st.metric("Departments", dept_count)
            
            # Project count
            proj_count = db_manager.execute_query("SELECT COUNT(*) as count FROM projects")[0]['count']
            st.metric("Projects", proj_count)
            
            db_manager.close()
            
        except Exception as e:
            st.error(f"Error loading stats: {e}")
    
    # Display results if available
    if hasattr(st.session_state, 'last_result') and st.session_state.last_result:
        result = st.session_state.last_result
        
        st.header("📋 Results")
        
        # Tabs for different views
        tab1, tab2, tab3 = st.tabs(["🤖 AI Response", "📝 Generated SQL", "📊 Raw Data"])
        
        with tab1:
            st.markdown("### Natural Language Response")
            st.write(result['final_response'])
            
            # Validation results
            if 'validation_result' in result:
                if "warning" in result['validation_result'].lower():
                    st.warning(f"⚠️ {result['validation_result']}")
                elif "error" in result['validation_result'].lower():
                    st.error(f"❌ {result['validation_result']}")
                else:
                    st.success(f"✅ {result['validation_result']}")
        
        with tab2:
            st.markdown("### Generated SQL Query")
            st.code(result['generated_sql'], language='sql')
            
            # Copy button
            if st.button("📋 Copy SQL"):
                st.write("SQL copied to clipboard!")
        
        with tab3:
            st.markdown("### Query Results")
            
            # Try to parse and display as DataFrame
            try:
                if "Query Results:" in result['sql_results']:
                    # Extract tabular data from formatted results
                    lines = result['sql_results'].split('\n')
                    if len(lines) > 3:  # Has header and data
                        st.text(result['sql_results'])
                    else:
                        st.info("No tabular data to display")
                else:
                    st.info(result['sql_results'])
                    
            except Exception as e:
                st.text(result['sql_results'])
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p>Built with ❤️ using LangChain, LangGraph, and Streamlit</p>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
