import os
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import heroku3  # Ensure you have this installed: `pip install heroku3`

# Get the Telegram Bot Token and Heroku API Key from environment variables
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')  # Replace with your actual token
HEROKU_API_KEY = os.getenv('HEROKU_API_KEY')  # Replace with your actual Heroku API key

if not TELEGRAM_TOKEN or not HEROKU_API_KEY:
    raise ValueError("Telegram Bot Token or Heroku API Key is missing.")

# Connect to Heroku API using the Heroku API Key
heroku_conn = heroku3.from_key(HEROKU_API_KEY)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome! I can help you manage your Heroku app. Use the commands to control it.')

# Add a new environment variable to the Heroku app
async def add_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        app_name = context.args[0]
        key = context.args[1]
        value = context.args[2]
        app = heroku_conn.apps()[app_name]
        app.config()[key] = value
        await update.message.reply_text(f"Environment variable {key} added to {app_name}.")
    except IndexError:
        await update.message.reply_text("Usage: /addvar <app_name> <key> <value>")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Delete an environment variable from the Heroku app
async def del_var(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        app_name = context.args[0]
        key = context.args[1]
        app = heroku_conn.apps()[app_name]
        app.config().delete(key)
        await update.message.reply_text(f"Environment variable {key} deleted from {app_name}.")
    except IndexError:
        await update.message.reply_text("Usage: /delvar <app_name> <key>")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Deploy your Heroku app (trigger a manual deploy)
async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        app_name = context.args[0]
        app = heroku_conn.apps()[app_name]
        app.restart()
        await update.message.reply_text(f"{app_name} has been redeployed.")
    except IndexError:
        await update.message.reply_text("Usage: /deploy <app_name>")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

# Restart your Heroku app
async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        app_name = context.args[0]
        app = heroku_conn.apps()[app_name]
        app.restart()
        await update.message.reply_text(f"{app_name} has been restarted.")
    except IndexError:
        await update.message.reply_text("Usage: /restart <app_name>")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

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

# Main function to start the bot
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
    # Start the async main function
    asyncio.run(main())
