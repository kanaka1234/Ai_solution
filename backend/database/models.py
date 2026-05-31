from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime
from backend.config import config

# Database setup
engine = create_engine(config.DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class AgentModel(Base):
    """Agent database model"""
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text)
    personality = Column(Text)  # JSON string
    tools = Column(JSON)  # List of tool names
    memory = Column(JSON)  # Agent memory storage
    schedule = Column(String)  # Cron-like schedule
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class WorkflowModel(Base):
    """Workflow database model"""
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True)
    name = Column(String, index=True)
    description = Column(Text)
    agents = Column(JSON)  # List of agent IDs
    triggers = Column(JSON)  # Workflow triggers
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ExecutionLogModel(Base):
    """Execution log for agents and workflows"""
    __tablename__ = "execution_logs"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String)
    workflow_id = Column(String)
    status = Column(String)  # "running", "success", "failed"
    output = Column(Text)
    error = Column(Text)
    execution_time = Column(Integer)  # milliseconds
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    """Initialize database"""
    Base.metadata.create_all(engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
