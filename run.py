#!/usr/bin/env python3
"""
Launcher script for the NLP to SQL application
"""
import sys
import os
import subprocess

def print_banner():
    """Print application banner"""
    print("🔍 NLP to SQL Query Converter")
    print("=" * 50)
    print("Choose how you'd like to run the application:")
    print()

def main():
    """Main launcher function"""
    print_banner()
    
    print("1. 💬 Command Line Interface (Interactive)")
    print("2. 🌐 Web Interface (Streamlit)")
    print("3. 🧪 Test Tools (No API key required)")
    print("4. 🔧 Initialize Database Only")
    print("5. ❌ Exit")
    print()
    
    while True:
        try:
            choice = input("Enter your choice (1-5): ").strip()
            
            if choice == "1":
                print("\n🚀 Starting Command Line Interface...")
                os.system("uv run python main.py")
                break
                
            elif choice == "2":
                print("\n🚀 Starting Web Interface...")
                print("🌐 Opening browser at http://localhost:8501")
                os.system("uv run streamlit run web_app.py")
                break
                
            elif choice == "3":
                print("\n🧪 Running Tool Tests...")
                os.system("uv run python test_tools.py")
                break
                
            elif choice == "4":
                print("\n🔧 Initializing Database...")
                os.system("uv run python database.py")
                break
                
            elif choice == "5":
                print("\n👋 Goodbye!")
                break
                
            else:
                print("❌ Invalid choice. Please enter 1-5.")
                
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
