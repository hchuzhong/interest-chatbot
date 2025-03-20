import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import logging
import os
from dotenv import load_dotenv
from bu_chatgpt import HKBU_ChatGPT

load_dotenv()

def main():
    token = os.getenv('TELEGRAM_ACCESS_TOKEN')
    print('TELEGRAM_ACCESS_TOKEN:', token)
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    global chatgpt
    chatgpt = HKBU_ChatGPT()
    chatgpt_handler = MessageHandler(Filters.text & (~Filters.command), equip_chatgpt)

    echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    dispatcher.add_handler(chatgpt_handler)

    updater.start_polling()
    updater.idle()

def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def equip_chatgpt(update, context):
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: " + str(update))
    logging.info("Context: " + str(context))
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

if __name__ == '__main__':
    main()