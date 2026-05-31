"""Settings page"""
import streamlit as st
import os

st.set_page_config(page_title="Settings", page_icon="⚙️")

st.header("⚙️ Settings")

st.subheader("Backend Configuration")
col1, col2 = st.columns(2)

with col1:
    st.write("**Backend URL**")
    st.code("http://127.0.0.1:8000")

with col2:
    st.write("**Streamlit UI**")
    st.code("http://localhost:8501")

st.divider()

st.subheader("Environment Variables")

env_vars = {
    "TELEGRAM_BOT_TOKEN": os.getenv("TELEGRAM_BOT_TOKEN", "Not set"),
    "DATABASE_URL": os.getenv("DATABASE_URL", "sqlite:///data/agents.db"),
    "OPENAI_API_KEY": "***" if os.getenv("OPENAI_API_KEY") else "Not set",
}

for key, value in env_vars.items():
    st.write(f"**{key}**: {value}")

st.divider()

st.subheader("Help & Documentation")
st.markdown("""
- 📖 [README](../README.md) - Getting started guide
- 🔧 [Tools Documentation](https://example.com/tools)
- 🤖 [Agent API Reference](https://example.com/api)
- 💬 [Telegram Bot Setup](https://example.com/telegram)
""")
