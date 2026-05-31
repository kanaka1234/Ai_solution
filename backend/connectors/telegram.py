"""Telegram bot connector for agent interaction"""
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
from backend.config import config
from backend.agents.base import agent_manager

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TelegramConnector:
    """Telegram Bot Connector"""
    
    def __init__(self, token: str = None):
        self.token = token or config.TELEGRAM_BOT_TOKEN
        self.app = None
        self.agent_id = None  # Agent connected to this bot
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "Welcome to AI Agent Platform! 🤖\n\n"
            "Send any message and I'll process it.\n"
            "Use /help for available commands."
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
Available Commands:
/start - Start the bot
/help - Show this help
/status - Check agent status
/agents - List available agents
/use <agent_id> - Select an agent to interact with
/memory - View agent memory
/history - View conversation history
        """
        await update.message.reply_text(help_text)
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle incoming messages"""
        user_message = update.message.text
        
        if not self.agent_id:
            await update.message.reply_text(
                "No agent selected. Use /use <agent_id> to select an agent."
            )
            return
        
        try:
            # Execute agent with message as task
            result = await agent_manager.execute_agent(
                self.agent_id,
                user_message,
                {"telegram_user_id": update.effective_user.id}
            )
            
            if result["status"] == "success":
                await update.message.reply_text(f"✓ {result['output']}")
            else:
                await update.message.reply_text(f"✗ Error: {result.get('error', 'Unknown error')}")
        
        except Exception as e:
            logger.error(f"Error handling message: {e}")
            await update.message.reply_text(f"Error: {str(e)}")
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check agent status"""
        if self.agent_id:
            agent = agent_manager.get_agent(self.agent_id)
            if agent:
                await update.message.reply_text(
                    f"Agent: {agent.name}\n"
                    f"Status: {'Enabled' if agent.enabled else 'Disabled'}\n"
                    f"Tools: {', '.join(agent.tools) or 'None'}"
                )
            else:
                await update.message.reply_text("Agent not found")
        else:
            await update.message.reply_text("No agent selected")
    
    async def setup(self):
        """Setup Telegram bot"""
        if not self.token:
            logger.error("TELEGRAM_BOT_TOKEN not set")
            return False
        
        self.app = Application.builder().token(self.token).build()
        
        # Add handlers
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help_command))
        self.app.add_handler(CommandHandler("status", self.status_command))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        return True
    
    async def run(self, agent_id: str = None):
        """Run bot"""
        self.agent_id = agent_id or (agent_manager.list_agents()[0].id if agent_manager.list_agents() else None)
        
        if not self.agent_id:
            logger.error("No agent available")
            return
        
        if await self.setup():
            logger.info(f"Starting Telegram bot for agent: {self.agent_id}")
            await self.app.run_polling()

# Global connector instance
telegram_connector = TelegramConnector()
