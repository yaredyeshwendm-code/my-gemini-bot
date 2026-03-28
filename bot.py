import telebot
import google.generativeai as genai
import os
from flask import Flask
from threading import Thread

# 1. ቦቱን ለሬንደር (Render) ማዘጋጀት
app = Flask(__name__)

@app.route('/')
def home():
  return "Mask On Bot is running!"

# 2. ያቀረብካቸውን ቶክኖች እዚህ ተክቻቸዋለሁ
BOT_TOKEN = "8558837716:AAGqh6T7PyJGzElWWWCija1ygnYSm4cm4Gc"
GEMINI_API_KEY = "AIzaSyDUCF6xNLhlRnMnoQS4ZVdRBAT5C7QcG8o"

# 3. ጌሚኒን ማዘጋጀት
genai.configure(api_key=GEMINI_API_KEY)
bot = telebot.TeleBot(BOT_TOKEN)

# 4. ቦቱ ማንነቱን እንዲያውቅ የተሰጠ መመሪያ (System Prompt)
SYSTEM_PROMPT = "Your name is Mask On. You are a helpful, smart, and friendly AI assistant. Always introduce yourself as Mask On if asked."

@bot.message_handler(func=lambda message: True)
def chat(message):
  try:
    model = genai.GenerativeModel("gemini-pro")
    # ለጌሚኒ ቦቱ ማን እንደሆነ እንነግረዋለን
    full_prompt = f"{SYSTEM_PROMPT}\n\nUser: {message.text}\nMask On:"
    
    response = model.generate_content(full_prompt)
    bot.reply_to(message, response.text)
  except Exception as e:
    print(f"Error: {e}")
    bot.reply_to(message, "I'm sorry, I'm having a little trouble thinking. Try again in a moment!")

def run_bot():
  bot.polling(none_stop=True)

if __name__ == "__main__":
  # ቦቱን በጀርባ ማስነሳት
  Thread(target=run_bot).start()
  
  # ሬንደር የሚፈልገውን ፖርት (Port) መክፈት
  port = int(os.environ.get("PORT", 10000))
  app.run(host='0.0.0.0', port=port)
