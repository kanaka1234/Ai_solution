"""Database utilities and helpers"""
from backend.database.models import SessionLocal, AgentModel, WorkflowModel, ExecutionLogModel

def get_agent(agent_id: str):
    """Fetch agent by ID"""
    db = SessionLocal()
    agent = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    db.close()
    return agent

def save_agent(agent_data: dict):
    """Save or update agent"""
    db = SessionLocal()
    agent_id = agent_data.get("id")
    existing = db.query(AgentModel).filter(AgentModel.id == agent_id).first()
    
    if existing:
        for key, value in agent_data.items():
            setattr(existing, key, value)
    else:
        agent = AgentModel(**agent_data)
        db.add(agent)
    
    db.commit()
    db.close()

def get_all_agents():
    """Fetch all agents"""
    db = SessionLocal()
    agents = db.query(AgentModel).all()
    db.close()
    return agents

def delete_agent(agent_id: str):
    """Delete agent by ID"""
    db = SessionLocal()
    db.query(AgentModel).filter(AgentModel.id == agent_id).delete()
    db.commit()
    db.close()

def log_execution(agent_id: str, workflow_id: str, status: str, output: str, error: str = None, execution_time: int = 0):
    """Log agent/workflow execution"""
    db = SessionLocal()
    log = ExecutionLogModel(
        agent_id=agent_id,
        workflow_id=workflow_id,
        status=status,
        output=output,
        error=error,
        execution_time=execution_time
    )
    db.add(log)
    db.commit()
    db.close()

def get_execution_logs(limit: int = 100):
    """Fetch recent execution logs"""
    db = SessionLocal()
    logs = db.query(ExecutionLogModel).order_by(ExecutionLogModel.created_at.desc()).limit(limit).all()
    db.close()
    return logs
