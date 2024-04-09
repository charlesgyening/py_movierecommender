from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
from imdb_info import recommend_movie, save_info_to_txt
from openai_integration import generate_gpt_response, generate_condensed_summary

load_dotenv()
print('Starting up bot...')

TOKEN: Final = os.getenv('TELEGRAM_TOKEN')

# Application setup
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', recommend_movie))

    # Messages
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        text: str = update.message.text

        # Process user input and generate OpenAI GPT-3 response
        gpt_prompt = f"User asks: '{text}'. Provide information and recommendations for this movie."
        gpt_response = generate_gpt_response(gpt_prompt)

        # Send the GPT-3 response back to the user
        await update.message.reply_text(gpt_response)

        # Get movie recommendations and additional details
        recommendation = recommend_movie(update, text)
        # Send the movie recommendation to the user
        await update.message.reply_text(recommendation)

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(recommend_movie)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=1)
