"""
Database configuration and initialization module
"""
import sqlite3
from typing import List, Dict, Any
import os

class DatabaseManager:
    def __init__(self, db_name: str = "example.db"):
        self.db_name = db_name
        self.connection = None
        self.setup_database()
    
    def setup_database(self):
        """Initialize database with schema and sample data"""
        self.connection = sqlite3.connect(self.db_name)
        cursor = self.connection.cursor()
        
        # Create employees table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            department TEXT NOT NULL,
            role TEXT NOT NULL,
            salary INTEGER,
            hire_date DATE,
            email TEXT UNIQUE
        )
        ''')
        
        # Create departments table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS departments (
            dept_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dept_name TEXT NOT NULL UNIQUE,
            location TEXT,
            manager_id INTEGER,
            FOREIGN KEY (manager_id) REFERENCES employees(id)
        )
        ''')
        
        # Create projects table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            department_id INTEGER,
            start_date DATE,
            end_date DATE,
            budget REAL,
            FOREIGN KEY (department_id) REFERENCES departments(dept_id)
        )
        ''')
        
        # Insert sample data if tables are empty
        self.insert_sample_data()
        
        self.connection.commit()
    
    def insert_sample_data(self):
        """Insert sample data for testing"""
        cursor = self.connection.cursor()
        
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM employees")
        if cursor.fetchone()[0] > 0:
            return
        
        # Sample employees data
        employees_data = [
            ('John Doe', 'IT', 'Software Engineer', 75000, '2022-01-15', 'john.doe@company.com'),
            ('Jane Smith', 'HR', 'HR Manager', 65000, '2021-03-10', 'jane.smith@company.com'),
            ('Bob Johnson', 'IT', 'DevOps Engineer', 80000, '2022-06-20', 'bob.johnson@company.com'),
            ('Alice Brown', 'Marketing', 'Marketing Specialist', 55000, '2023-02-01', 'alice.brown@company.com'),
            ('Charlie Wilson', 'Finance', 'Financial Analyst', 70000, '2021-11-05', 'charlie.wilson@company.com'),
            ('Eva Davis', 'IT', 'Senior Developer', 90000, '2020-08-12', 'eva.davis@company.com'),
            ('Frank Miller', 'HR', 'Recruiter', 50000, '2023-01-20', 'frank.miller@company.com'),
            ('Grace Lee', 'IT', 'QA Engineer', 60000, '2022-09-15', 'grace.lee@company.com')
        ]
        
        cursor.executemany('''
        INSERT INTO employees (name, department, role, salary, hire_date, email)
        VALUES (?, ?, ?, ?, ?, ?)
        ''', employees_data)
        
        # Sample departments data
        departments_data = [
            ('IT', 'Building A - Floor 3', 1),
            ('HR', 'Building B - Floor 1', 2),
            ('Marketing', 'Building A - Floor 2', 4),
            ('Finance', 'Building B - Floor 2', 5)
        ]
        
        cursor.executemany('''
        INSERT INTO departments (dept_name, location, manager_id)
        VALUES (?, ?, ?)
        ''', departments_data)
        
        # Sample projects data
        projects_data = [
            ('Website Redesign', 1, '2023-01-01', '2023-06-30', 50000.0),
            ('Employee Portal', 1, '2023-03-15', '2023-12-31', 75000.0),
            ('Recruitment Campaign', 2, '2023-02-01', '2023-04-30', 25000.0),
            ('Financial Audit System', 4, '2023-01-15', '2023-09-30', 100000.0)
        ]
        
        cursor.executemany('''
        INSERT INTO projects (project_name, department_id, start_date, end_date, budget)
        VALUES (?, ?, ?, ?, ?)
        ''', projects_data)
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """Execute a SQL query and return results"""
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        return [dict(zip(columns, row)) for row in rows]
    
    def get_schema_info(self) -> str:
        """Get database schema information"""
        cursor = self.connection.cursor()
        
        # Get table names
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        schema_info = "Database Schema:\n"
        for table in tables:
            table_name = table[0]
            schema_info += f"\nTable: {table_name}\n"
            
            # Get column information
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            
            for column in columns:
                col_name, col_type = column[1], column[2]
                schema_info += f"  - {col_name}: {col_type}\n"
        
        return schema_info
    
    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()

# Test the database setup
if __name__ == "__main__":
    db = DatabaseManager()
    print(db.get_schema_info())
    
    # Test query
    results = db.execute_query("SELECT * FROM employees LIMIT 3")
    print("\nSample data:")
    for result in results:
        print(result)
    
    db.close()
