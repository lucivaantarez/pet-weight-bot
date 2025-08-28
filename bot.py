#!/usr/bin/env python3
"""
Telegram Bot for Pet Weight Calculator
"""

import logging
import os
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    ContextTypes, ConversationHandler, filters
)
from calculator import PetWeightCalculator

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
WEIGHT, AGE = range(2)

class PetWeightBot:
    def __init__(self, token: str):
        self.token = token
        self.calculator = PetWeightCalculator()
        self.application = Application.builder().token(token).build()
        
        # Set up conversation handler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_weight)],
                AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_age)],
            },
            fallbacks=[CommandHandler('cancel', self.cancel)],
        )
        
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("formula", self.formula_command))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Start the conversation and ask for weight."""
        welcome_text = """
🐾 *Pet Weight Calculator Bot* 🐾

I can calculate your pet's hatch weight using the formula:
`W = (Wh / 11) × (A + 10)`

Please enter your pet's current weight in kg:
        """
        await update.message.reply_text(
            welcome_text, 
            parse_mode='Markdown',
            reply_markup=ReplyKeyboardRemove()
        )
        return WEIGHT
    
    async def get_weight(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Store weight and ask for age."""
        try:
            weight = float(update.message.text)
            if weight <= 0:
                await update.message.reply_text("Please enter a positive weight:")
                return WEIGHT
            
            context.user_data['weight'] = weight
            await update.message.reply_text("Now enter your pet's age (1-100):")
            return AGE
            
        except ValueError:
            await update.message.reply_text("Please enter a valid number for weight:")
            return WEIGHT
    
    async def get_age(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Calculate and display results."""
        try:
            age = int(update.message.text)
            if age < 1 or age > 100:
                await update.message.reply_text("Age must be between 1-100. Please try again:")
                return AGE
            
            weight = context.user_data['weight']
            hatch_weight = self.calculator.calculate_hatch_weight(weight, age)
            weight_class = self.calculator.get_weight_class(weight)
            
            result_text = f"""
✅ *Calculation Results:*

• Current Weight: `{weight} kg`
• Age: `{age}`
• Hatch Weight: `{hatch_weight:.2f} kg`
• Weight Class: `{weight_class}`

Use /start to calculate again or /formula to see the formula.
            """
            
            await update.message.reply_text(result_text, parse_mode='Markdown')
            return ConversationHandler.END
            
        except ValueError:
            await update.message.reply_text("Please enter a valid number for age:")
            return AGE
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Send a help message."""
        help_text = """
🤖 *Bot Commands:*

/start - Calculate hatch weight
/formula - Show the formula used
/help - Show this help message

📊 *Weight Classes:*
• Small: < 1 kg
• Normal: 1-5 kg  
• Huge: 5-7 kg
• Titanic: 8-9 kg
• Godly: ≥ 9 kg
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def formula_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Show the formula."""
        formula_text = """
🧮 *Formula Used:*

`W = (Wh / 11) × (A + 10)`

Where:
• W = Current Weight
• Wh = Hatch Weight  
• A = Age (1-100)

To find Hatch Weight (Wh):
`Wh = (W × 11) ÷ (A + 10)`
        """
        await update.message.reply_text(formula_text, parse_mode='Markdown')
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        """Cancel the conversation."""
        await update.message.reply_text(
            "Calculation cancelled.",
            reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END
    
    def run(self):
        """Run the bot."""
        self.application.run_polling()

# Main execution
if __name__ == '__main__':
    # Get token from environment variable
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN environment variable not set!")
        print("Please set your Telegram bot token as an environment variable.")
        exit(1)
    
    bot = PetWeightBot(BOT_TOKEN)
    print("Bot is running...")
    bot.run()
