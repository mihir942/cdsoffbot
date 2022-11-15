# 1. Importing python's in-built libraries
import os
import logging
import datetime
import math

# 2. Importing external libraries
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 3. Setting up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR)
logger = logging.getLogger(__name__)

# 4. Initialising the default webhook variables
DEFAULT_WEBHOOK_ADDR = "0.0.0.0"
DEFAULT_WEBHOOK_PORT = 8080

# 5. Help message
# help_msg = "/start - Will reply 'Hi, <your name>'\n" +
# "/register - register yourself with the bot\n" +
# "/help - shows this message\n\n"+
# "/newoff - apply for new off\n"+
# "/newleave - apply for new leave\n"+
# "/newmc - indicate here if applying for MC\n"+
# "/newma - indicate here if going for MA\n\n"+
# "/editoffs - edit any of your offs/leaves/etc.\n"+
# "/editmydetails - to edit your rank,name"

def start_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Hello {update.effective_user.first_name}. This bot works in development.")

def error_handler(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

def main() -> None:
    # Load environment variables
    load_dotenv()

    # Get TOKEN variable from .env
    TOKEN = os.environ.get("TOKEN")

    # Get env variable from .env (defaults to development)
    env = os.environ.get("ENV","development").lower()

    # Get webhook server settings from .env
    webhook_addr = os.environ.get("WEBHOOK_ADDR", DEFAULT_WEBHOOK_ADDR)
    webhook_port = os.environ.get("WEBHOOK_PORT", DEFAULT_WEBHOOK_PORT)
    webhook_url = os.environ.get("WEBHOOK_URL")

    # Create updater instance
    updater = Updater(TOKEN, use_context=True)

    # Registering all our handlers
    updater.dispatcher.add_handler(CommandHandler("start",start_handler))
    updater.dispatcher.add_error_handler(error_handler)

    # If production, set webhook. If development, set polling
    if env == "production":
        updater.start_webhook(
            listen=webhook_addr,
            port=webhook_port,
            url_path=TOKEN,
            webhook_url=f"{webhook_url}/{TOKEN}"
        )
        logger.info(f"Start webhook HTTP server - {webhook_addr}:{webhook_port}")
    else:
        updater.start_polling()
        logger.info(f"Start polling updates")

    # Bot runs until the process receives SIGINT, SIGTERM or SIGABRT.
    updater.idle()

if __name__ == "__main__":
    main()
