"""Agents page"""
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Agents", page_icon="🤖")

st.header("🤖 Agent Management")

col1, col2 = st.columns([3, 1])
with col2:
    if st.button("➕ New Agent"):
        st.session_state.show_create_form = True

st.divider()

if st.session_state.get("show_create_form", False):
    st.subheader("Create New Agent")
    
    with st.form("agent_form"):
        name = st.text_input("Name")
        personality = st.text_area("Personality")
        tools = st.multiselect("Tools", ["shell", "http", "memory"])
        
        if st.form_submit_button("Create"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/agents/create",
                    params={"name": name, "personality": personality, "tools": tools}
                )
                st.success("Agent created!")
                st.session_state.show_create_form = False
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

st.subheader("All Agents")

try:
    response = requests.get(f"{BACKEND_URL}/agents")
    agents = response.json()["agents"]
    
    for agent in agents:
        with st.expander(f"🤖 {agent['name']}"):
            st.json(agent)
except Exception as e:
    st.error(f"Error: {str(e)}")
