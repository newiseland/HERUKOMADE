from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import heroku3

# Replace with your actual Telegram bot token and Heroku API key
TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
HEROKU_API_KEY = 'YOUR_HEROKU_API_KEY'

# Initialize Heroku client
heroku_conn = heroku3.from_key(HEROKU_API_KEY)

# Start command
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! I can help you manage your Heroku app. Use the commands to control it.')

# Add a new environment variable to the Heroku app
def add_var(update: Update, context: CallbackContext):
    app_name = context.args[0]
    key = context.args[1]
    value = context.args[2]
    app = heroku_conn.apps()[app_name]
    app.config()[key] = value
    update.message.reply_text(f"Environment variable {key} added to {app_name}.")

# Delete an environment variable from the Heroku app
def del_var(update: Update, context: CallbackContext):
    app_name = context.args[0]
    key = context.args[1]
    app = heroku_conn.apps()[app_name]
    app.config().delete(key)
    update.message.reply_text(f"Environment variable {key} deleted from {app_name}.")

# Deploy your Heroku app (trigger a manual deploy)
def deploy(update: Update, context: CallbackContext):
    app_name = context.args[0]
    app = heroku_conn.apps()[app_name]
    app.restart()
    update.message.reply_text(f"{app_name} has been redeployed.")

# Restart your Heroku app
def restart(update: Update, context: CallbackContext):
    app_name = context.args[0]
    app = heroku_conn.apps()[app_name]
    app.restart()
    update.message.reply_text(f"{app_name} has been restarted.")

# Help command
def help(update: Update, context: CallbackContext):
    help_text = (
        "/start - Welcome message\n"
        "/addvar <app_name> <key> <value> - Add environment variable\n"
        "/delvar <app_name> <key> - Delete environment variable\n"
        "/deploy <app_name> - Deploy your app\n"
        "/restart <app_name> - Restart your app"
    )
    update.message.reply_text(help_text)

def main():
    # Set up the Updater and Dispatcher
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("addvar", add_var))
    dispatcher.add_handler(CommandHandler("delvar", del_var))
    dispatcher.add_handler(CommandHandler("deploy", deploy))
    dispatcher.add_handler(CommandHandler("restart", restart))
    dispatcher.add_handler(CommandHandler("help", help))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
