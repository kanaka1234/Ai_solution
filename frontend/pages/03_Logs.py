"""Logs page"""
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Logs", page_icon="📋")

st.header("📋 Execution Logs")

# Placeholder for logs
st.info("Execution logs will be displayed here as agents run tasks.")

try:
    # Fetch logs from backend
    response = requests.get(f"{BACKEND_URL}/logs")
    if response.status_code == 200:
        logs = response.json()["logs"]
        if logs:
            st.json(logs)
        else:
            st.info("No logs yet")
except:
    st.info("Backend not available")
