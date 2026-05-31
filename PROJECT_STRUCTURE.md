# Project Structure

```
ai-agent-platform/
│
├── README.md                          # Quick start guide (minimal, just how to run)
├── ARCHITECTURE.md                    # Design decisions & architecture overview
├── requirements.txt                   # Python dependencies
├── .env.example                       # Environment variables template
├── .gitignore                         # Git ignore file
├── init.py                           # Initialize platform with sample agents
├── setup.bat                         # Windows quick setup script
├── setup.sh                          # macOS/Linux quick setup script
│
├── backend/                          # Agent runtime & API
│   ├── __init__.py
│   ├── config.py                     # Configuration from environment
│   ├── runtime.py                    # FastAPI main server (run this first)
│   │
│   ├── agents/                       # Agent implementation
│   │   ├── __init__.py
│   │   └── base.py                   # Agent class, AgentManager
│   │
│   ├── tools/                        # Tool implementations
│   │   ├── __init__.py
│   │   └── registry.py               # Tool base class, registry, implementations
│   │
│   ├── connectors/                   # External messaging connectors
│   │   ├── __init__.py
│   │   └── telegram.py               # Telegram bot connector
│   │
│   └── database/                     # Database models & utilities
│       ├── __init__.py
│       ├── models.py                 # SQLAlchemy ORM models
│       └── utils.py                  # Database helper functions
│
├── frontend/                         # Streamlit web UI
│   ├── __init__.py
│   ├── app.py                        # Main Streamlit app (run this second)
│   ├── components.py                 # Reusable UI components
│   │
│   └── pages/                        # Multi-page Streamlit apps
│       ├── 01_Agents.py              # Agent management page
│       ├── 02_Workflows.py           # Workflow builder page
│       ├── 03_Logs.py                # Execution logs viewer
│       └── 04_Settings.py            # Configuration & help
│
└── data/                             # Local data directory
    └── .gitkeep                      # Placeholder for data files
```

## File Descriptions

### Root Level

| File | Purpose |
|------|---------|
| `README.md` | Quick start guide with setup and run instructions |
| `ARCHITECTURE.md` | Detailed architecture, design decisions, and tech stack rationale |
| `requirements.txt` | All Python package dependencies |
| `.env.example` | Template for environment variables (copy to `.env`) |
| `.gitignore` | Prevents committing venv, databases, logs, etc. |
| `init.py` | Initialize database and create sample agents |
| `setup.bat` / `setup.sh` | Automated setup scripts |

### Backend Structure

#### `backend/config.py`
- Loads environment variables
- Provides centralized configuration access

#### `backend/runtime.py`
- FastAPI application
- REST API endpoints for agent management
- CORS middleware for frontend access
- Database initialization on startup

#### `backend/agents/base.py`
- `Agent` class: Individual agent with ID, name, personality, tools, memory
- `AgentManager` class: Manages agent lifecycle (create, execute, list, delete)
- `agent_manager` global instance

#### `backend/tools/registry.py`
- `Tool` base class with `execute()` interface
- `ShellTool`: Execute whitelisted shell commands
- `HTTPTool`: Make HTTP requests
- `MemoryTool`: Store/retrieve persistent data
- `ToolRegistry`: Central tool registration system

#### `backend/connectors/telegram.py`
- `TelegramConnector` class
- Commands: `/start`, `/help`, `/status`, `/use <agent_id>`
- Message handling: passes user input to connected agent
- Async bot framework

#### `backend/database/models.py`
- `AgentModel`: SQLAlchemy model for agents
- `WorkflowModel`: SQLAlchemy model for workflows
- `ExecutionLogModel`: SQLAlchemy model for execution logs
- `init_db()`: Create tables
- `get_db()`: Database session manager

#### `backend/database/utils.py`
- `get_agent()`, `save_agent()`, `get_all_agents()`, `delete_agent()`
- `log_execution()`: Log task executions
- `get_execution_logs()`: Retrieve logs

### Frontend Structure

#### `frontend/app.py`
- Main Streamlit application
- Dashboard with metrics
- Agent management (create, list, delete, execute)
- Tools viewer
- Logs viewer
- Navigation between pages

#### `frontend/components.py`
- Reusable UI components:
  - `agent_card()`: Display agent information
  - `workflow_card()`: Display workflow information
  - `execution_log_table()`: Tabular log display
  - `agent_form()`: Agent creation form
  - `workflow_form()`: Workflow creation form

#### `frontend/pages/01_Agents.py`
- Dedicated agents page
- Create new agents form
- List and manage all agents

#### `frontend/pages/02_Workflows.py`
- Workflow management (placeholder for future)
- Define agent pipelines and connections

#### `frontend/pages/03_Logs.py`
- View execution history
- Filter by agent or time range (future)

#### `frontend/pages/04_Settings.py`
- View environment configuration
- Backend status
- Links to documentation

### Data Directory

- `data/.gitkeep`: Placeholder to keep directory in git
- Runtime creates `data/agents.db` (SQLite database)

## Development Workflow

### Adding a New Tool

1. Create tool class in `backend/tools/registry.py`
2. Inherit from `Tool` base class
3. Implement `async execute(**kwargs)` method
4. Register in `ToolRegistry.__init__()`

Example:
```python
class CustomTool(Tool):
    def __init__(self):
        super().__init__("custom", "My custom tool")
    
    async def execute(self, **kwargs):
        return {"status": "success", "result": "..."}

tool_registry.register_tool("custom", CustomTool())
```

### Adding a New Connector

1. Create connector class in `backend/connectors/new_connector.py`
2. Implement interface similar to `TelegramConnector`
3. Add route to handle messages → agent execution

### Adding a New Frontend Page

1. Create `frontend/pages/XX_PageName.py`
2. Streamlit will auto-add it to navigation
3. Use components from `frontend/components.py`

## Running the Platform

1. **Terminal 1 - Backend (Agent Runtime)**:
   ```bash
   python backend/runtime.py
   ```
   Runs on `http://127.0.0.1:8000`

2. **Terminal 2 - Frontend (Web UI)**:
   ```bash
   streamlit run frontend/app.py
   ```
   Runs on `http://localhost:8501`

3. **Terminal 3 (Optional) - Telegram Bot**:
   Set `TELEGRAM_BOT_TOKEN` in `.env`, then bot will connect when runtime starts

## Key Design Patterns

- **Registry Pattern**: Tools, agents registered in central registry
- **Factory Pattern**: `AgentManager.create_agent()` creates Agent instances
- **Async/Await**: FastAPI and telegram bot use asyncio for concurrency
- **Dependency Injection**: Database sessions passed to functions
- **ORM Abstraction**: SQLAlchemy allows easy database switching

## Testing Strategy (Future)

- Unit tests for each tool
- Integration tests for agent execution
- API tests for FastAPI endpoints
- UI tests for Streamlit components
