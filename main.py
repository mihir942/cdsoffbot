# 1. Importing python's in-built libraries
import os
import logging
import datetime
import math

# 2. Importing external libraries
import gspread
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler

# 3. Setting up logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.ERROR)
logger = logging.getLogger(__name__)

# 4. Initialising the default webhook variables
DEFAULT_WEBHOOK_ADDR = "0.0.0.0"
DEFAULT_WEBHOOK_PORT = 8080

# 5. Google Cloud Console API Key (JSON Format)
googledict={
  "type": "service_account",
  "project_id": "cdsoffbot",
  "private_key_id": "b38ea4b9cfdba21e3b760fd5faf266cf491e7b8b",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCvuz7keoXK7rJ0\nCFeJSwL6nt+n8yzI1Cdc3f9dulqsTxz+2bQf1l6dFSAqVmlB9Ma1YF0ss1rFnL3L\nRF/Ns0koFmFldI4N8kq7KVrOYNCFX/axYSoEbTQwjm+XXLQqpD/DmRXsbSxOc8Fb\ng8uBLTxHZpLTebMFSdPgc0BX9TTtd85PdNPojpY3Wr3gC/wnbEAG6MiwrTq53S8D\njOsTZxeAZ64isEFUHlMBeM271GfxHuuFwl2UTq7hPP+tjpmK+LqQiPfm2cF33Vk2\nMFcjZNs1olSnkH3vLxUxDD4x5Qu8OlhEnpmq6VEYSxc66UKvxNwmPChQPgr/QnoL\nvFQJqnuNAgMBAAECggEAFOUWQtOAshL0vBA73FLDfWpDnLQw6IY1UfkBgrMEUgWs\nJG9dWAXExTe8Vdxlcpa4w9s76PNAgUu0U4WDQLGnKrGSjh4wP99F3IA70Fs5oAo7\ninbLqLAVawqcoSpAL+vMuySqMyz9/iwMWyXOHkNzLeg34BZR33iaTU9W4L6CtxN7\nhWmiNRIrSMH3pUiIMocIXY29e+S+j3BdPFLeY+J9FxMhrqrihJg637V9Oy9hyPIo\n9+O9e065cpS5V3iLevcslr01fu37vd6/ccxcqn+zX194XauBi2hfw/MNP+GsvZq/\nQKIbz+Zom2bZPlzrep7Ymf4OBwh8tL8+VhcmYhWMjwKBgQDsEKV+Haa1OH1FUnE1\n9hD/AvfzTUblcTAOrb43uvouOKwaCUwkFAtLaTFp3NcOku45QhFD/9iGPqwDQBIf\nFc3qHObC/yYaTY4nrdH/YQCh+SaA+2POae/bsr0L6g2v0fJuwCJh6UI307qkIFpD\nRDlygklfc4A/bZpnFQUzeclX0wKBgQC+kkgxrnGIsQe9AjlFEM8T23rcRDL8oGCf\n3GHz/XINraH2PCmuQpiGdIpP01cA4u5STULm2s68bTV6o5juDCaCRDwUA/z08osS\nkWz2kitDI4Vx1ZryWDFnkwMe7tS6E5fDj5POsfVmxayqMJSe4gPXVsHZy22HlxyU\n0S6pEj0jHwKBgAvlvuF/TxKdGTswL4J/t1WS6bo6b9NKhBiJSyf15XwE4S+ivlKn\nK/aOA66JMdGLODRsjwA1Wc1SRUsYpJEqgSlGcZ7sSxhSRlLboNTVJ7oCG52ujdYu\nYqdY98ws7Kmq1CQezNzQa8Tyh9qTwtjXDGooBNipspH/zSNa3Ns+TRZ/AoGAGQEq\nldI0tWG9CTC8gPJmqU1X/oS4R+tnIjKRa6kqiN7qbFuSgHned23dJAIv3T7pVEUs\n7QtyqsiNhszmaP2RI/B+DYZEb4NPeh04tdWR9Zo4jSogzYGC4fspIqrloJCnjhJN\nq4YwE88GC8KaDYrMRDnu73vAoFTUfDZCMA7jlLMCgYAaWGNhdWkUpVv+y5Yfm2Mc\nsIVoqYaNAVZXHrheKXcpXbyXUAyPT1qF0UQLsf1F29xJ4fWkzzM0cgzIsJV8R2Kv\nfR3J8KMiraNATaVDj+HKsdH0FGrGGlTMckQWc2roBYWokLlmhb2Rzv+mD8hafoh7\n1PkSNZWp3Rzk7he638HTkg==\n-----END PRIVATE KEY-----\n",
  "client_email": "cdsoffbotsvcaccount@cdsoffbot.iam.gserviceaccount.com",
  "client_id": "102899209451764634282",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/cdsoffbotsvcaccount%40cdsoffbot.iam.gserviceaccount.com"
}

# 6. Google Cloud Console Variables, to access spreadsheet
SPREADSHEET_NAME = "RAW"
BIODATA_SHEET_NAME = "biodata"
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_dict(googledict, scope)
client = gspread.authorize(creds)
mysheet = client.open(SPREADSHEET_NAME).worksheet(BIODATA_SHEET_NAME)

# ----------------------------------------------------#
#              >> CODE STARTS HERE <<                 #
# ----------------------------------------------------#

# -------------------- 1. Constants -------------------- #
HEADER_ROW_LIST = mysheet.row_values(1)

RANK_STR = "Rank"
RANK_INDX = HEADER_ROW_LIST.index(RANK_STR)

NAME_STR = "Name"
NAME_INDX = HEADER_ROW_LIST.index(NAME_STR)

USERID_STR = "userid"
USERID_INDX = HEADER_ROW_LIST.index(USERID_STR)

SECTION_STR = "Section"
SECTION_INDX = HEADER_ROW_LIST.index(SECTION_STR)

SECTION, NAME = range(2)

# -------------------- 2. Handlers -------------------- #
# COMMAND HANDLER
def start_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(f"Hello {update.effective_user.first_name}. This bot works.")

    userid = str(update.message.from_user.id)
    all_userid = mysheet.col_values(USERID_INDX + 1)

    if userid not in all_userid:
        context.bot.send_message(update.effective_user.id,"Please type /register to register yourself.")

# COMMAND HANDLER
def register_handler(update: Update, context: CallbackContext) -> int:
    userid = str(update.message.from_user.id)
    all_userid = mysheet.col_values(USERID_INDX + 1)

    all_section_types = mysheet.col_values(SECTION_INDX + 1)[1:]
    all_section_types = list(set(all_section_types))
    all_section_types.sort()
    keyboard = [[InlineKeyboardButton(sect,callback_data=sect) for sect in all_section_types]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if userid not in all_userid:
        update.message.reply_text("Not registered. Key in your section number",reply_markup=reply_markup)
        return SECTION
    else:
        update.message.reply_text("You've already been registered :)")
        return ConversationHandler.END

# CALLBACKQUERY HANDLER
def section(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    context.bot.send_message(update.effective_user.id,f"You've chosen section {query.data}...")

    all_values = mysheet.get_all_values()
    all_names = [row[RANK_INDX] + " " + row[NAME_INDX] for row in all_values]
    keyboard = [[InlineKeyboardButton(all_names[i],callback_data=str(i))] for i in range(len(all_values)) if all_values[i][SECTION_INDX] == query.data]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Choose who you are",reply_markup=reply_markup)

    return NAME

# CALLBACKQUERY HANDLER
def name(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()

    all_values = mysheet.get_all_values()
    index = int(query.data)
    row = all_values[index]
    name = row[RANK_INDX] + " " + row[NAME_INDX]

    context.bot.send_message(update.effective_user.id,f"Hi, {name}.")
    userid = update.effective_user.id
    mysheet.update_cell(index+1,USERID_INDX + 1,userid)
    context.bot.send_message(update.effective_user.id,f"You're now registered.")

    return ConversationHandler.END

# COMMAND HANDLER
def cancel_handler(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Cancelled. Back to normal.")
    return ConversationHandler.END

# ERROR HANDLER
def error_handler(update: Update, context: CallbackContext) -> None:
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# -------------------- 3. Main -------------------- #
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

    # Initialising the Conversation Handlers
    registerConvoHandler = ConversationHandler(
        entry_points=[CommandHandler('register',register_handler)],
        states={
            SECTION: [CallbackQueryHandler(section)],
            NAME: [CallbackQueryHandler(name)]
        },
        fallbacks=[CommandHandler('cancel',cancel_handler)]
    )

    # Registering all our handlers
    updater.dispatcher.add_handler(CommandHandler("start",start_handler))
    updater.dispatcher.add_handler(registerConvoHandler)

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
