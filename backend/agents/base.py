"""Agent base class and execution logic"""
import json
import uuid
from datetime import datetime
from typing import Any, Dict, List
import asyncio
from backend.database.utils import log_execution

class Agent:
    """Base Agent class"""
    
    def __init__(self, agent_id: str = None, name: str = "", personality: str = "", tools: List[str] = None, memory: Dict = None):
        self.id = agent_id or str(uuid.uuid4())
        self.name = name
        self.personality = personality
        self.tools = tools or []
        self.memory = memory or {}
        self.enabled = True
        self.created_at = datetime.utcnow()
        
    def to_dict(self) -> Dict:
        """Convert agent to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "personality": self.personality,
            "tools": self.tools,
            "memory": self.memory,
            "enabled": self.enabled,
            "created_at": self.created_at.isoformat()
        }
    
    async def execute(self, task: str, context: Dict = None) -> Dict[str, Any]:
        """
        Execute agent task
        
        Args:
            task: Task description
            context: Additional context for execution
            
        Returns:
            Execution result with output and metadata
        """
        start_time = datetime.utcnow()
        result = {
            "status": "success",
            "output": f"Agent {self.name} processed: {task}",
            "agent_id": self.id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        try:
            # Update memory
            if context:
                self.memory.update(context)
            
            # Log execution
            execution_time = int((datetime.utcnow() - start_time).total_seconds() * 1000)
            log_execution(self.id, None, "success", result["output"], None, execution_time)
            
        except Exception as e:
            result["status"] = "failed"
            result["error"] = str(e)
            log_execution(self.id, None, "failed", "", str(e))
        
        return result
    
    def add_to_memory(self, key: str, value: Any):
        """Add information to agent memory"""
        self.memory[key] = value
    
    def get_from_memory(self, key: str) -> Any:
        """Retrieve information from agent memory"""
        return self.memory.get(key)

class AgentManager:
    """Manage agent instances and execution"""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.execution_queue = asyncio.Queue()
    
    def create_agent(self, name: str, personality: str = "", tools: List[str] = None) -> Agent:
        """Create a new agent"""
        agent = Agent(name=name, personality=personality, tools=tools or [])
        self.agents[agent.id] = agent
        return agent
    
    def get_agent(self, agent_id: str) -> Agent:
        """Get agent by ID"""
        return self.agents.get(agent_id)
    
    def list_agents(self) -> List[Agent]:
        """List all agents"""
        return list(self.agents.values())
    
    async def execute_agent(self, agent_id: str, task: str, context: Dict = None) -> Dict:
        """Execute agent task"""
        agent = self.get_agent(agent_id)
        if not agent:
            return {"status": "error", "message": f"Agent {agent_id} not found"}
        
        return await agent.execute(task, context)
    
    def delete_agent(self, agent_id: str) -> bool:
        """Delete agent"""
        if agent_id in self.agents:
            del self.agents[agent_id]
            return True
        return False

# Global agent manager
agent_manager = AgentManager()
