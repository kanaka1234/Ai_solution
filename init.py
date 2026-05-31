"""
Quick start script for the AI Agent Platform

Run this to initialize the platform with sample data.
"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.database.models import init_db
from backend.agents.base import agent_manager

def main():
    print("🚀 Initializing AI Agent Platform...\n")
    
    # Initialize database
    print("📦 Setting up database...")
    init_db()
    print("✓ Database initialized\n")
    
    # Create sample agents
    print("🤖 Creating sample agents...")
    
    agent1 = agent_manager.create_agent(
        name="Data Analyst",
        personality="You are a careful data analyst who provides detailed insights",
        tools=["http", "memory"]
    )
    print(f"✓ Created agent: {agent1.name} ({agent1.id[:8]}...)")
    
    agent2 = agent_manager.create_agent(
        name="Task Executor",
        personality="You execute tasks efficiently and reliably",
        tools=["shell", "memory"]
    )
    print(f"✓ Created agent: {agent2.name} ({agent2.id[:8]}...)\n")
    
    print("✅ Platform initialized successfully!")
    print("\nNext steps:")
    print("1. Run: python backend/runtime.py")
    print("2. Run: streamlit run frontend/app.py")
    print("3. Open: http://localhost:8501")

if __name__ == "__main__":
    main()
