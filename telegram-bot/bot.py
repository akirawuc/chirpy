import os
from dotenv import load_dotenv
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo, ReplyKeyboardRemove
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from summarize import *
from datetime import datetime, timedelta, date, timezone
import time
from pathlib import Path

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Constants for pagination steps
FIRST_PAGE = 0
ITEMS_PER_PAGE = 1
df = pd.DataFrame()
post_data = {}
def get_pagination_keyboard(current_page):
    
    keyboard = []
    # Add a 'Previous' button if it's not the first page
    if current_page > FIRST_PAGE:
        keyboard.append(InlineKeyboardButton('Previous', callback_data=f'page_{current_page - 1}'))
    # Add a 'Next' button if there are more pages left
    if (current_page + 1) * ITEMS_PER_PAGE < 25:
        keyboard.append(InlineKeyboardButton('Next', callback_data=f'page_{current_page + 1}'))
    return keyboard

  
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    message = " Welcome anon! Chirpy are your little birds that live on lens. 🦜\n\n"
    message += "And don't forget, Chirpy have highly dense artificial neurons so they are well versed in human language... They can summarize the long conversations and can give you time back and less FOMO. \n\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode='HTML')
    

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

import json

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global post_data
    # await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message)
    text = update.message.text
    post_data = {'command': 'post', 'text': text}
    if update.message['photo']:
        text = update.message["caption"]
        file = update.message.photo[-1].file_id
        obj = await context.bot.get_file(file)
        path = await obj.download_to_drive(f'images_tmp/{file}.jpg')
        post_data['text'] = text
        post_data['path'] = f'images_tmp/{file}.jpg'
    text = f'"{text}" \n Shared by {update.message.forward_from["first_name"]} - @{update.message.forward_from["username"]} on TG.'
    confirm = [InlineKeyboardButton("Send post", callback_data='confirm')]
    reply_markup = InlineKeyboardMarkup([confirm])
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Send this post? \n {text}", reply_markup=reply_markup)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global post_data
    try:
        similar_callback = update.message.reply_to_message['reply_markup']['inline_keyboard'][1][1]['callback_data']
        if similar_callback:
            post_id = similar_callback.split('_')[1]
            text = update.message.text
            post_data = {'command': 'reply', 'post_id': post_id, 'text': text}
            if update.message['photo']:
                text = update.message["caption"]
                file = update.message.photo[-1].file_id
                obj = await context.bot.get_file(file)
                path = await obj.download_to_drive(f'images_tmp/{file}.jpg')
                post_data['text'] = text
                post_data['path'] = f'images_tmp/{file}.jpg'
            
            confirm = [InlineKeyboardButton("Send reply", callback_data='confirm')]
            reply_markup = InlineKeyboardMarkup([confirm])
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Send this reply? \n "{text}"', reply_markup=reply_markup)
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="You can only reply to post directly served by Skitties bot.")
    except Exception as e:
        print(e)
        
async def connect(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message with a button that opens a the web app."""
    await update.message.reply_text(
        "Please press the button below to connect your Lens profile",
        reply_markup=ReplyKeyboardMarkup.from_button(
            KeyboardButton(
                text="Click to connect your Lens profile!",
                # web_app=WebAppInfo(url="https://react-app.walletconnect.com/"),
                # web_app=WebAppInfo(url="https://python-telegram-bot.org/static/webappbot"),
                # web_app=WebAppInfo(url="https://chirpy-chi.vercel.app"),
                web_app=WebAppInfo(url="https://www.akirun.com/"),
            )
        ),
    )

# Handle incoming WebAppData
async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Print the received data and remove the button."""
    # Here we use `json.loads`, since the WebApp sends the data JSON serialized string
    # (see webappbot.html)
    data = json.loads(update.effective_message.web_app_data.data)
    print(data)
    await update.message.reply_html(
        text=(
            f"You selected the color with the HEX value <code>{data['hex']}</code>. The "
            f"corresponding RGB value is <code>{tuple(data['rgb'].values())}</code>."
        ),
        reply_markup=ReplyKeyboardRemove(),
    )

if __name__ == '__main__':
    
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    

    application.add_handler(CommandHandler("connect", connect))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, web_app_data))

    # Quote handler
    quote_handler = MessageHandler(filters.FORWARDED, quote)
    application.add_handler(quote_handler)

    # Reply handler
    reply_handler = MessageHandler(filters.REPLY, reply)
    application.add_handler(reply_handler)

    # Other handlers
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    application.add_handler(unknown_handler)
    
    application.run_polling()
