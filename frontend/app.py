"""Main Streamlit app"""
import streamlit as st
import requests
import json
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="AI Agent Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    .stTabs [data-baseweb="tab-list"] button {
        font-size: 18px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# Backend URL
BACKEND_URL = "http://127.0.0.1:8000"

# Initialize session state
if "agents" not in st.session_state:
    st.session_state.agents = []
if "selected_agent" not in st.session_state:
    st.session_state.selected_agent = None

# Header
st.title("🤖 AI Agent Orchestration Platform")
st.markdown("Create, configure, and manage autonomous AI agents that collaborate in real time.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Backend Status
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200:
            st.success("✓ Backend Connected")
        else:
            st.error("✗ Backend Offline")
    except:
        st.error("✗ Cannot reach backend")
    
    st.divider()
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["Dashboard", "Agents", "Tools", "Logs"],
        label_visibility="collapsed"
    )

# Main content
if page == "Dashboard":
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Agents", 0, help="Number of active agents")
    with col2:
        st.metric("Workflows", 0, help="Number of defined workflows")
    with col3:
        st.metric("Tool Executions", 0, help="Total tool executions")
    
    st.divider()
    
    st.subheader("📊 Recent Activity")
    st.info("No recent activity yet. Create an agent to get started!")

elif page == "Agents":
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("🤖 Agent Management")
    with col2:
        if st.button("➕ New Agent", use_container_width=True):
            st.session_state.show_create_agent = True
    
    st.divider()
    
    # Create Agent Form
    if st.session_state.get("show_create_agent", False):
        st.markdown("### Create New Agent")
        
        col1, col2 = st.columns(2)
        with col1:
            agent_name = st.text_input("Agent Name", placeholder="e.g., Data Analyst")
        with col2:
            agent_desc = st.text_input("Description", placeholder="What does this agent do?")
        
        personality = st.text_area("Personality", placeholder="Describe the agent's personality and behavior")
        
        tools = st.multiselect(
            "Tools",
            ["shell", "http", "memory"],
            help="Select tools this agent can use"
        )
        
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            if st.button("✓ Create", use_container_width=True):
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/agents/create",
                        params={
                            "name": agent_name,
                            "personality": personality,
                            "tools": tools
                        }
                    )
                    if response.status_code == 200:
                        st.success("✓ Agent created successfully!")
                        st.session_state.show_create_agent = False
                        st.rerun()
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Failed to create agent: {str(e)}")
        
        with col2:
            if st.button("✗ Cancel", use_container_width=True):
                st.session_state.show_create_agent = False
                st.rerun()
    
    st.divider()
    st.markdown("### Agents List")
    
    # Fetch and display agents
    try:
        response = requests.get(f"{BACKEND_URL}/agents")
        if response.status_code == 200:
            agents = response.json().get("agents", [])
            
            if agents:
                for agent in agents:
                    with st.expander(f"🤖 {agent['name']}", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("ID", agent['id'][:8] + "...")
                        with col2:
                            st.metric("Tools", len(agent.get('tools', [])))
                        with col3:
                            status = "Enabled" if agent.get('enabled', True) else "Disabled"
                            st.metric("Status", status)
                        
                        st.write(f"**Personality:** {agent.get('personality', 'N/A')}")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            if st.button("Execute", key=f"exec_{agent['id']}"):
                                task = st.text_input("Task", key=f"task_{agent['id']}")
                                if task:
                                    try:
                                        exec_response = requests.post(
                                            f"{BACKEND_URL}/agents/{agent['id']}/execute",
                                            params={"task": task}
                                        )
                                        result = exec_response.json()
                                        if result["status"] == "success":
                                            st.success(result["output"])
                                        else:
                                            st.error(result.get("error", "Execution failed"))
                                    except Exception as e:
                                        st.error(f"Error: {str(e)}")
                        
                        with col2:
                            if st.button("Delete", key=f"del_{agent['id']}"):
                                try:
                                    del_response = requests.delete(f"{BACKEND_URL}/agents/{agent['id']}")
                                    if del_response.status_code == 200:
                                        st.success("Agent deleted")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
            else:
                st.info("No agents yet. Create one to get started!")
        else:
            st.error("Failed to fetch agents")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

elif page == "Tools":
    st.subheader("🔧 Available Tools")
    
    try:
        response = requests.get(f"{BACKEND_URL}/tools")
        if response.status_code == 200:
            tools = response.json().get("tools", [])
            
            for tool in tools:
                with st.expander(f"📦 {tool}", expanded=False):
                    if tool == "shell":
                        st.write("Execute system shell commands safely")
                        st.code("Allowed commands: echo, ls, pwd, date, whoami, cat")
                    elif tool == "http":
                        st.write("Make HTTP requests")
                        st.code("Methods: GET, POST, PUT, DELETE")
                    elif tool == "memory":
                        st.write("Store and retrieve data from agent memory")
                        st.code("Actions: set, get, list")
        else:
            st.error("Failed to fetch tools")
    except Exception as e:
        st.error(f"Connection error: {str(e)}")

elif page == "Logs":
    st.subheader("📋 Execution Logs")
    st.info("Execution logs will appear here as agents run tasks.")
    
    # Placeholder for logs
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "agent": "No logs yet",
        "status": "pending"
    }
    st.json(log_data)

st.divider()
st.caption("AI Agent Orchestration Platform v1.0 | Built with Streamlit")
