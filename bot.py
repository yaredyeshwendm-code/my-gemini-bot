import telebot
import requests
import os
from flask import Flask
from threading import Thread

# Configuration
BOT_TOKEN = "8558837716:AAGqh6T7PyJGzElWWWCija1ygnYSm4cm4Gc"
GEMINI_API_KEY = "AIzaSyDUCF6xNLhlRnMnoQS4ZVdRBAT5C7QcG8o"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask('')

@app.route('/')
def home():
  return "Bot is Online!"

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  t = Thread(target=run)
  t.start()

def get_gemini_response(text):
  url = f"https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
  headers = {"Content-Type": "application/json"}
  payload = {"contents": [{"parts": [{"text": text}]}]}
  try:
    response = requests.post(url, headers=headers, json=payload)
    result = response.json()
    return result['candidates'][0]['content']['parts'][0]['text']
  except:
    return "ይቅርታ፣ አሁን ላይ መልስ ለመስጠት አልቻልኩም። እባክህ ትንሽ ቆይተህ ሞክር።"

@bot.message_handler(commands=['start'])
def welcome(message):
  welcome_text = (
    "ሰላም! 👋 እኔ የጌሚኒ (Gemini) አርቴፊሻል ኢንተለጀንስ ቦት ነኝ Mask On እባላለሁ።\n\n"
    "የፈለከውን ጥያቄ መጠየቅ ትችላለህ፤ \n"
    "ምን ልርዳህ?"
  )
  bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
  try:
  (typing...)
    bot.send_chat_action(message.chat.id, 'typing')
    response = get_gemini_response(message.text)
    bot.reply_to(message, response)
  except Exception as e:
    print(f"Error: {e}")

if __name__ == "__main__":
  keep_alive() 
  print("ቦቱ ስራ ጀምሯል...")
  bot.infinity_polling()
