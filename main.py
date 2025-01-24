from gtts import gTTS
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from decouple import config

import os

from functions import handle_document, split_text

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text('Привет! Я бот Бушейши, который помогает озвучивать текстовые сообщения. Просто отправь мне текст, который хочешь услышать.')

async def text_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    voice = f'files/{update.message.id}.mp3'
    text = update.message.text or update.message.caption
    tts = gTTS(text, lang='ru')
    tts.save(voice)
    await update.message.reply_audio(voice)
    os.remove(voice)

async def document(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    voice = f'files/{update.message.id}.mp3'
    file = await update.message.document.get_file()
    file_path = f"files/{update.message.document.file_name}"
    await file.download_to_drive(file_path)

    text = handle_document(file_path)
    text_list = split_text(text)
    print(text_list)
    for t in text_list:
        tts = gTTS(t, lang='ru')
        tts.save(voice)
        await update.message.reply_audio(voice)
        os.remove(voice)


def main() -> None:
    TOKEN = config('TG_TOKEN')
    application = Application.builder().token(TOKEN).build()
    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.Document.ALL, document))
    application.add_handler(MessageHandler(filters.ALL, text_message))


    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()