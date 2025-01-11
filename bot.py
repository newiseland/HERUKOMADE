from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes


# Load environment variables from .env file

import os
import heroku3  # Make sure to install the `heroku3` package using `pip install heroku3`

# Read the Heroku API key from the environment variable
HEROKU_API_KEY = os.getenv('HRKU-3fbe925b-3597-45f6-addf-8962a039b268')

# Authenticate with Heroku API
heroku_conn = heroku3.from_key(HEROKU_API_KEY)

# Now you can use `heroku_conn` to interact with your Heroku app, for example:
app_name = "your-app-name"
app = heroku_conn.apps()[app_name]

# Example: List environment variables for your app
print(app.config())
# Replace with your actual Telegram bot token and Heroku API key
TELEGRAM_TOKEN = '7907726222:AAGx_WNkbmTGhHfOMAXqdk6rZXNB6Kjo4FQ'
HEROKU_API_KEY = 'HRKU-3fbe925b-3597-45f6-addf-8962a039b268'

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os

# Replace with your actual Telegram bot token
TELEGRAM_TOKEN = os.getenv('7907726222:AAGx_WNkbmTGhHfOMAXqdk6rZXNB6Kjo4FQ')

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome! I can help you manage your Heroku app. Use the commands to control it.')

# Add a new environment variable to the Heroku app
async def add_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app_name = context.args[0]
    key = context.args[1]
    value = context.args[2]
    app = heroku_conn.apps()[app_name]
    app.config()[key] = value
    await update.message.reply_text(f"Environment variable {key} added to {app_name}.")

# Delete an environment variable from the Heroku app
async def del_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app_name = context.args[0]
    key = context.args[1]
    app = heroku_conn.apps()[app_name]
    app.config().delete(key)
    await update.message.reply_text(f"Environment variable {key} deleted from {app_name}.")

# Deploy your Heroku app (trigger a manual deploy)
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app_name = context.args[0]
    app = heroku_conn.apps()[app_name]
    app.restart()
    await update.message.reply_text(f"{app_name} has been redeployed.")

# Restart your Heroku app
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    app_name = context.args[0]
    app = heroku_conn.apps()[app_name]
    app.restart()
    await update.message.reply_text(f"{app_name} has been restarted.")

# Help command
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "/start - Welcome message\n"
        "/addvar <app_name> <key> <value> - Add environment variable\n"
        "/delvar <app_name> <key> - Delete environment variable\n"
        "/deploy <app_name> - Deploy your app\n"
        "/restart <app_name> - Restart your app"
    )
    await update.message.reply_text(help_text)

async def main():
    # Initialize the Application with the bot token
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("addvar", add_var))
    application.add_handler(CommandHandler("delvar", del_var))
    application.add_handler(CommandHandler("deploy", deploy))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("help", help))

    # Initialize the application and start the bot
    await application.initialize()  # Await initialization
    await application.run_polling()  # Await the bot's polling to start

    # Graceful shutdown when the app stops
    await application.shutdown()  # Await shutdown to clean up properly when the app stops

if __name__ == '__main__':
    asyncio.run(main())  # Start the async main function
