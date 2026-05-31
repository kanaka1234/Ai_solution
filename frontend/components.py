"""Reusable Streamlit components"""
import streamlit as st
import requests

def agent_card(agent):
    """Display agent card"""
    with st.container():
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.subheader(f"🤖 {agent['name']}")
            st.caption(agent.get('personality', 'No personality set'))
        
        with col2:
            tools = agent.get('tools', [])
            st.metric("Tools", len(tools))
        
        with col3:
            status = "✓ Active" if agent.get('enabled', True) else "✗ Inactive"
            st.write(status)

def workflow_card(workflow):
    """Display workflow card"""
    with st.container():
        st.subheader(f"🔗 {workflow['name']}")
        st.caption(workflow.get('description', 'No description'))
        
        agents_count = len(workflow.get('agents', []))
        st.metric("Agents", agents_count)

def execution_log_table(logs):
    """Display execution logs table"""
    data = []
    for log in logs:
        data.append({
            "Agent ID": log.get('agent_id', 'N/A'),
            "Status": log.get('status', 'unknown'),
            "Time (ms)": log.get('execution_time', 0),
            "Timestamp": log.get('created_at', 'N/A')
        })
    
    if data:
        st.dataframe(data, use_container_width=True)
    else:
        st.info("No execution logs yet")

def agent_form():
    """Agent creation form"""
    with st.form("create_agent_form"):
        name = st.text_input("Agent Name")
        personality = st.text_area("Personality")
        tools = st.multiselect("Tools", ["shell", "http", "memory"])
        
        submitted = st.form_submit_button("Create Agent")
        
        if submitted:
            if not name:
                st.error("Agent name is required")
            else:
                return {
                    "name": name,
                    "personality": personality,
                    "tools": tools
                }
    
    return None

def workflow_form():
    """Workflow creation form"""
    with st.form("create_workflow_form"):
        name = st.text_input("Workflow Name")
        description = st.text_area("Description")
        
        submitted = st.form_submit_button("Create Workflow")
        
        if submitted:
            if not name:
                st.error("Workflow name is required")
            else:
                return {
                    "name": name,
                    "description": description
                }
    
    return None
