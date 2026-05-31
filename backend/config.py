import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///data/agents.db")
    
    # Backend Server
    BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
    BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    
    # OpenAI (optional)
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    
    # Agent Limits
    MAX_AGENT_MEMORY_MB = int(os.getenv("MAX_AGENT_MEMORY_MB", 100))
    MAX_TOOL_EXECUTION_TIME = int(os.getenv("MAX_TOOL_EXECUTION_TIME", 30))
    
    # Debug
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"

config = Config()
