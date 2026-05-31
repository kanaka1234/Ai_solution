"""Tool definitions and execution"""
import subprocess
import requests
import json
from typing import Any, Dict, List
import time

class Tool:
    """Base Tool class"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    async def execute(self, **kwargs) -> Dict[str, Any]:
        """Execute tool - override in subclasses"""
        raise NotImplementedError

class ShellTool(Tool):
    """Execute shell commands safely"""
    
    def __init__(self):
        super().__init__("shell", "Execute system shell commands")
        self.allowed_commands = ["echo", "ls", "pwd", "date", "whoami", "cat"]
    
    async def execute(self, command: str, timeout: int = 30) -> Dict[str, Any]:
        """Execute shell command with safety checks"""
        # Safety check - only allow whitelisted commands
        cmd_name = command.split()[0] if command else ""
        
        if cmd_name not in self.allowed_commands:
            return {
                "status": "error",
                "message": f"Command '{cmd_name}' is not allowed. Allowed: {self.allowed_commands}"
            }
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                "status": "success",
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None,
                "return_code": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {"status": "error", "message": f"Command timed out after {timeout}s"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

class HTTPTool(Tool):
    """Make HTTP requests"""
    
    def __init__(self):
        super().__init__("http", "Make HTTP requests")
    
    async def execute(self, method: str, url: str, headers: Dict = None, data: Dict = None, timeout: int = 10) -> Dict[str, Any]:
        """Make HTTP request"""
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers,
                json=data,
                timeout=timeout
            )
            return {
                "status": "success",
                "status_code": response.status_code,
                "response": response.text
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}

class MemoryTool(Tool):
    """Store and retrieve data from memory"""
    
    def __init__(self):
        super().__init__("memory", "Store and retrieve data from agent memory")
        self.storage = {}
    
    async def execute(self, action: str, key: str = None, value: Any = None) -> Dict[str, Any]:
        """Manage memory storage"""
        if action == "set":
            self.storage[key] = value
            return {"status": "success", "message": f"Stored {key}"}
        elif action == "get":
            return {"status": "success", "value": self.storage.get(key)}
        elif action == "list":
            return {"status": "success", "keys": list(self.storage.keys())}
        else:
            return {"status": "error", "message": f"Unknown action: {action}"}

class ToolRegistry:
    """Registry for available tools"""
    
    def __init__(self):
        self.tools: Dict[str, Tool] = {
            "shell": ShellTool(),
            "http": HTTPTool(),
            "memory": MemoryTool()
        }
    
    def get_tool(self, tool_name: str) -> Tool:
        """Get tool by name"""
        return self.tools.get(tool_name)
    
    def register_tool(self, name: str, tool: Tool):
        """Register a new tool"""
        self.tools[name] = tool
    
    def list_tools(self) -> List[str]:
        """List available tools"""
        return list(self.tools.keys())

# Global tool registry
tool_registry = ToolRegistry()
