"""Main agent runtime server"""
import asyncio
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import logging
from backend.config import config
from backend.database.models import init_db
from backend.agents.base import agent_manager
from backend.tools.registry import tool_registry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="AI Agent Platform Runtime", version="1.0.0")

# Add CORS middleware for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Routes

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    init_db()
    logger.info("Database initialized")
    logger.info("Agent Runtime started")

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "ok", "service": "agent-runtime"}

@app.post("/agents/create")
async def create_agent(name: str, personality: str = "", tools: list = None):
    """Create a new agent"""
    try:
        agent = agent_manager.create_agent(name, personality, tools or [])
        logger.info(f"Created agent: {agent.id}")
        return {"status": "success", "agent": agent.to_dict()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/agents")
async def list_agents():
    """List all agents"""
    agents = agent_manager.list_agents()
    return {"agents": [a.to_dict() for a in agents]}

@app.get("/agents/{agent_id}")
async def get_agent(agent_id: str):
    """Get agent details"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"agent": agent.to_dict()}

@app.post("/agents/{agent_id}/execute")
async def execute_agent(agent_id: str, task: str, context: dict = None):
    """Execute agent task"""
    try:
        result = await agent_manager.execute_agent(agent_id, task, context)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/agents/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete agent"""
    if agent_manager.delete_agent(agent_id):
        logger.info(f"Deleted agent: {agent_id}")
        return {"status": "success"}
    raise HTTPException(status_code=404, detail="Agent not found")

@app.get("/tools")
async def list_tools():
    """List available tools"""
    tools = tool_registry.list_tools()
    return {"tools": tools}

@app.post("/tools/{tool_name}/execute")
async def execute_tool(tool_name: str, **kwargs):
    """Execute a tool"""
    tool = tool_registry.get_tool(tool_name)
    if not tool:
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    
    try:
        result = await tool.execute(**kwargs)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/agents/{agent_id}/memory")
async def update_memory(agent_id: str, key: str, value: any):
    """Update agent memory"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    agent.add_to_memory(key, value)
    return {"status": "success", "memory": agent.memory}

@app.get("/agents/{agent_id}/memory")
async def get_memory(agent_id: str):
    """Get agent memory"""
    agent = agent_manager.get_agent(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {"memory": agent.memory}

if __name__ == "__main__":
    logger.info(f"Starting runtime on {config.BACKEND_HOST}:{config.BACKEND_PORT}")
    uvicorn.run(
        app,
        host=config.BACKEND_HOST,
        port=config.BACKEND_PORT,
        log_level="info"
    )
