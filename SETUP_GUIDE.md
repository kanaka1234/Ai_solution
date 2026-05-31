# AI Agent Orchestration Platform - Complete Setup & Implementation Guide

## 📦 Project Overview

A lightweight Python-based platform for creating, configuring, and orchestrating autonomous AI agents that collaborate in real time. Features include a Streamlit web UI, FastAPI backend runtime, tool execution, persistent memory, and Telegram bot integration.

### Key Features
✅ Create agents with custom personality and tools  
✅ Real-time agent execution and monitoring  
✅ Telegram integration for conversational interaction  
✅ Web UI dashboard for visual management  
✅ Persistent agent state and memory  
✅ Extensible tool registry  
✅ Execution logging and history  

## 📂 Project Structure

All files have been created in: `c:\Users\ADMIN\Desktop\sample\ai-agent-platform\`

### Directory Layout
```
ai-agent-platform/
├── backend/                    # Agent runtime & REST API
│   ├── agents/                # Agent classes and management
│   ├── tools/                 # Tool implementations
│   ├── connectors/            # Messaging connectors (Telegram, etc.)
│   ├── database/              # Database models and utilities
│   ├── config.py              # Configuration management
│   └── runtime.py             # Main FastAPI server
├── frontend/                   # Streamlit web application
│   ├── app.py                 # Main app
│   ├── components.py          # Reusable UI components
│   └── pages/                 # Multi-page UI sections
├── data/                       # Local data storage
├── init.py                    # Platform initialization
├── setup.bat / setup.sh       # Quick setup scripts
├── README.md                  # Simple quick-start guide
├── ARCHITECTURE.md            # Design decisions & system architecture
└── requirements.txt           # Python dependencies
```

## 🚀 Quick Start (Windows)

### Option 1: Automatic Setup (Recommended)

1. **Navigate to project**:
   ```powershell
   cd c:\Users\ADMIN\Desktop\sample\ai-agent-platform
   ```

2. **Run setup script**:
   ```powershell
   .\setup.bat
   ```
   This will:
   - Create a virtual environment
   - Install all dependencies
   - Initialize the database
   - Create sample agents

### Option 2: Manual Setup

1. **Create virtual environment**:
   ```powershell
   python -m venv venv
   venv\Scripts\activate.bat
   ```

2. **Install dependencies**:
   ```powershell
   pip install -r requirements.txt
   ```

3. **Set up environment**:
   ```powershell
   copy .env.example .env
   # Edit .env and add your Telegram bot token (optional)
   ```

4. **Initialize database**:
   ```powershell
   python init.py
   ```

### Running the Platform

**Terminal 1 - Backend Runtime**:
```powershell
venv\Scripts\activate.bat
python backend/runtime.py
```
✓ Runs on `http://127.0.0.1:8000`

**Terminal 2 - Frontend UI**:
```powershell
venv\Scripts\activate.bat
streamlit run frontend/app.py
```
✓ Runs on `http://localhost:8501`

### Access the Platform
- **Web UI**: Open browser → `http://localhost:8501`
- **API Documentation**: Open browser → `http://127.0.0.1:8000/docs`
- **Telegram Bot**: Send messages to your bot (if configured)

## ⚙️ Configuration

### Environment Variables (.env)

Copy `.env.example` to `.env` and configure:

```env
# Telegram Bot Token (optional, for Telegram integration)
TELEGRAM_BOT_TOKEN=your_token_from_botfather

# OpenAI API Key (optional, for LLM capabilities)
OPENAI_API_KEY=sk-...

# Database URL (SQLite by default, change for PostgreSQL)
DATABASE_URL=sqlite:///data/agents.db

# Backend Server
BACKEND_HOST=127.0.0.1
BACKEND_PORT=8000

# Streamlit UI
STREAMLIT_PORT=8501

# Agent Limits
MAX_AGENT_MEMORY_MB=100
MAX_TOOL_EXECUTION_TIME=30
```

### Getting a Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow prompts to create bot
4. Copy bot token and paste in `.env`

## 🏗️ Architecture Overview

```
User (Browser)
    ↓ HTTP
Streamlit UI (Port 8501)
    ↓ HTTP/JSON
FastAPI Runtime (Port 8000)
    ├─ AgentManager (spawn, execute agents)
    ├─ ToolRegistry (shell, http, memory tools)
    ├─ Connectors (Telegram bot, etc.)
    └─ Database (SQLite/PostgreSQL)
    
External Channels
    ↓ Telegram API
    Telegram Bot ←→ Agent via Runtime API
```

### Key Components

**Backend (FastAPI)**:
- Agent lifecycle management
- Tool execution engine
- REST API for frontend
- Database persistence
- Async task execution

**Frontend (Streamlit)**:
- Agent dashboard
- Create/edit agents
- Execute tasks
- View logs
- Multi-page navigation

**Database (SQLAlchemy ORM)**:
- Agents table
- Workflows table
- Execution logs table
- Supports SQLite (default) & PostgreSQL

**Tools**:
- **Shell**: Execute whitelisted commands
- **HTTP**: Make HTTP requests
- **Memory**: Store/retrieve agent data

## 📖 Usage Examples

### 1. Create an Agent (via Web UI)

1. Open `http://localhost:8501`
2. Click "Agents" in sidebar
3. Click "➕ New Agent"
4. Fill in:
   - **Name**: "Email Assistant"
   - **Personality**: "You are helpful and professional"
   - **Tools**: Select "http" and "memory"
5. Click "Create"

### 2. Execute a Task

1. In Agents page, find your agent
2. Click "Execute"
3. Enter task: "Send an email notification"
4. View result

### 3. Use Telegram Bot

1. Configure `TELEGRAM_BOT_TOKEN` in `.env`
2. Restart backend
3. Open Telegram, find your bot
4. Send: `/start`
5. Send task message, bot will process via connected agent

### 4. Use API (Programmatic)

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# Create agent
response = requests.post(
    f"{BASE_URL}/agents/create",
    params={
        "name": "My Agent",
        "personality": "Helpful assistant",
        "tools": ["http", "memory"]
    }
)
agent = response.json()["agent"]
agent_id = agent["id"]

# Execute task
response = requests.post(
    f"{BASE_URL}/agents/{agent_id}/execute",
    params={"task": "Hello, process this task"}
)
result = response.json()
print(result)

# View agent memory
response = requests.get(f"{BASE_URL}/agents/{agent_id}/memory")
memory = response.json()["memory"]
print(memory)
```

## 🔧 Extending the Platform

### Adding a New Tool

Edit `backend/tools/registry.py`:

```python
class FileReaderTool(Tool):
    def __init__(self):
        super().__init__("file_reader", "Read file contents")
    
    async def execute(self, filepath: str, **kwargs):
        try:
            with open(filepath, 'r') as f:
                content = f.read()
            return {"status": "success", "content": content}
        except Exception as e:
            return {"status": "error", "message": str(e)}

# Register in ToolRegistry.__init__()
self.tools["file_reader"] = FileReaderTool()
```

### Adding a New Connector

Create `backend/connectors/slack.py`:

```python
from slack_sdk import WebClient
from slack_bolt.app import App

class SlackConnector:
    def __init__(self, token):
        self.app = App(token=token)
        self.agent_id = None
    
    @self.app.message(...)
    async def handle_message(body, say):
        user_message = body["text"]
        # Execute agent with message
        result = await agent_manager.execute_agent(
            self.agent_id, 
            user_message
        )
        say(result["output"])
```

### Adding a Frontend Page

Create `frontend/pages/05_MyPage.py`:

```python
import streamlit as st
import requests

st.set_page_config(page_title="My Page", page_icon="📊")

st.header("📊 My Custom Page")

st.write("Custom content here")
```

Streamlit auto-discovers pages in `/frontend/pages/` directory.

## 📊 Database Schema

### Agents Table
```sql
CREATE TABLE agents (
    id STRING PRIMARY KEY,
    name STRING,
    description TEXT,
    personality TEXT,
    tools JSON,
    memory JSON,
    schedule STRING,
    enabled BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Workflows Table
```sql
CREATE TABLE workflows (
    id STRING PRIMARY KEY,
    name STRING,
    description TEXT,
    agents JSON,
    triggers JSON,
    enabled BOOLEAN,
    created_at DATETIME,
    updated_at DATETIME
);
```

### Execution Logs Table
```sql
CREATE TABLE execution_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    agent_id STRING,
    workflow_id STRING,
    status STRING,
    output TEXT,
    error TEXT,
    execution_time INTEGER,
    created_at DATETIME
);
```

## 🔐 Security Considerations

### Current Measures
- ✓ Shell tool whitelists allowed commands
- ✓ HTTP requests isolated per session
- ✓ Agent memory scoped per-agent
- ✓ CORS enabled only for local development

### Future Improvements
- Authentication (API keys, JWT)
- Role-based access control
- Audit logging
- Resource quotas (CPU, memory, network)
- Input validation and sanitization

## 🚨 Troubleshooting

### Backend won't start
```
Error: Address already in use
→ Kill process on port 8000:
  netstat -ano | findstr :8000
  taskkill /PID <PID> /F
```

### Frontend connection error
```
Error: Cannot reach backend
→ Ensure backend is running on port 8000
→ Check firewall settings
→ Verify BACKEND_URL in frontend/app.py
```

### Telegram bot not responding
```
Error: Bot receives messages but doesn't respond
→ Check TELEGRAM_BOT_TOKEN in .env
→ Restart backend after changing token
→ Check logs: tail -f logs/runtime.log
```

### Database locked
```
Error: SQLite database is locked
→ Restart both backend and frontend
→ Remove .db-wal files: rm data/*.db-*
→ For multiple processes, use PostgreSQL instead
```

## 📈 Performance Tips

### Optimize for Multiple Agents
- Use PostgreSQL instead of SQLite for concurrent access
- Increase `MAX_AGENT_MEMORY_MB` for complex agents
- Use async tools for I/O-bound operations

### Monitor Execution
- Check Logs page in UI for slow tasks
- Set reasonable timeouts: `MAX_TOOL_EXECUTION_TIME`
- Profile agent memory usage

## 🎯 Next Steps

1. **Run the platform** locally as described above
2. **Create some agents** via the web UI
3. **Configure Telegram** bot for external interaction
4. **Add custom tools** as needed
5. **Deploy to production** (set DATABASE_URL to PostgreSQL)

## 📚 Additional Resources

- `README.md` - Simple quick-start
- `ARCHITECTURE.md` - Deep dive into design decisions
- `PROJECT_STRUCTURE.md` - File-by-file documentation
- FastAPI Docs: `http://127.0.0.1:8000/docs` (when running)
- Streamlit Docs: https://docs.streamlit.io/

## 💡 Tips & Tricks

### Debugging Agents
```python
# View agent memory in frontend
import requests
response = requests.get("http://127.0.0.1:8000/agents/{id}/memory")
print(response.json()["memory"])
```

### Testing Tools Locally
```bash
# Test shell tool
curl http://127.0.0.1:8000/tools/shell/execute -X POST -d "command=echo hello"

# Test HTTP tool
curl http://127.0.0.1:8000/tools/http/execute -X POST -d "method=GET&url=https://example.com"
```

### Clearing All Data
```bash
# Remove database
rm data/agents.db

# Reinitialize
python init.py
```

## 📞 Support

For issues or questions:
1. Check logs: `backend/runtime.py` output
2. Review `ARCHITECTURE.md` for design details
3. Inspect browser console for frontend errors
4. Check FastAPI docs at `http://127.0.0.1:8000/docs`

---

**Platform Version**: 1.0.0  
**Python**: 3.10+  
**Last Updated**: May 31, 2026
