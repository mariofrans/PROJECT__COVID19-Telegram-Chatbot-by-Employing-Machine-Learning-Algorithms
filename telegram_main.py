import smvbot as ts
import predict as p
from output import handler

import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

SVM = True
NB = False
NN = False

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def echo(update, context):
    """Echo the user message."""

    userResponse = update.message.text.lower()
    if SVM:
        update.message.reply_text(handler(ts.tags[ts.svm(userResponse)]))
    elif NB:
        update.message.reply_text(handler(ts.tags[ts.MultiNB(userResponse)]))
    elif NN:
        update.message.reply_text(handler(p(userResponse)))
    
def help(update, context):
    text = (
        "Welcome to your chatbot assistant"
        "\nYou can ask anything about COVID-19, I will try my best to answer :)"
        "\n\n"
        "\n=================================================="
        "\nThis bot could use different algorithms"
        "\nUse slash + Algorithm name, (SVM, NN, and NB)"
        "\nExample: \SVM"

    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

# NGL this is so ugh 
def SVM(update, context):
    SVM = True
    NB = False
    NN = False
    text = (
        "You are using SVM algorithm now"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

def NB(update, context):
    SVM = False
    NB = True
    NN = False
    text = (
        "You are using NB algorithm now"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

def NN(update, context):
    SVM = False
    NB = False
    NN = True
    text = (
        "You are using NN algorithm now"
    )
    update.message.reply_text(text=text, parse_mode=ParseMode.HTML)

def main():
    # The 1882~ is telegram token
    updater = Updater("1867275326:AAF7IEBKLM62L4RYmp2Vd3UnrGRmCoq1WDQ", use_context=True)

    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("help", help))

    dp.add_handler(CommandHandler("SVM", SVM))
    dp.add_handler(CommandHandler("NB", NB))
    dp.add_handler(CommandHandler("NN", NN))

    # This is to call echo function
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()