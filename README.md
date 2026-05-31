# AI Agent Orchestration Platform

A lightweight platform to create, configure, and orchestrate autonomous AI agents that collaborate in real time.

## Quick Start

### Prerequisites
- Python 3.10+
- pip

### Installation & Setup

1. **Clone and navigate to the project:**
   ```bash
   cd ai-agent-platform
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   - Copy `.env.example` to `.env` and fill in:
     - `TELEGRAM_BOT_TOKEN` (get from BotFather on Telegram)
     - `OPENAI_API_KEY` (optional, for LLM-based agents)
     - `DATABASE_URL` (defaults to SQLite: `sqlite:///agents.db`)

5. **Run the application:**
   ```bash
   # Start the agent runtime backend (in one terminal)
   python backend/runtime.py
   
   # Start the Streamlit UI (in another terminal)
   streamlit run frontend/app.py
   ```

6. **Access the platform:**
   - Open browser to `http://localhost:8501` (Streamlit UI)
   - Backend API runs on `http://localhost:8000`
   - Telegram bot is live and ready for messages

## Architecture

- **Backend (`/backend`):** Agent runtime, tools, messaging connectors, database
- **Frontend (`/frontend`):** Streamlit web UI for agent creation and workflow management
- **Database:** SQLite (local) or PostgreSQL (configurable)
- **Messaging:** Telegram Bot API for external agent interaction
- **Tools:** Execute system commands, HTTP requests, and custom functions

## Project Structure

```
ai-agent-platform/
├── backend/
│   ├── agents/          # Agent definitions and execution logic
│   ├── tools/           # Tool implementations (HTTP, shell, etc.)
│   ├── connectors/      # Messaging connectors (Telegram, Slack, etc.)
│   ├── database/        # Database models and utilities
│   ├── runtime.py       # Main agent runtime server
│   └── config.py        # Configuration
├── frontend/
│   ├── pages/           # Streamlit pages
│   ├── app.py           # Main Streamlit app
│   └── components.py    # Reusable UI components
├── data/                # Local database and files
├── requirements.txt     # Python dependencies
├── .env.example         # Environment template
└── README.md
```

## Features

✓ Create and configure agents with custom personality, tools, and schedules  
✓ Define workflows connecting multiple agents  
✓ Real-time agent execution and monitoring  
✓ Telegram integration for conversational interaction  
✓ Web UI for visual management and logs  
✓ Persistent agent state and memory  
✓ Tool execution with basic sandboxing  

## Development Notes

- Agents run in a background thread pool managed by the runtime
- Inter-agent communication happens via an async queue system
- Database uses SQLAlchemy ORM for easy switching between SQLite and PostgreSQL
- Streamlit auto-refreshes on file changes during development

## License

MIT yes
