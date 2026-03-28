import os
import telebot
import google.generativeai as genai

# የእርሶ ቶክኖች እዚህ ተተክተዋል
BOT_TOKEN = "8558837716:AAGqh6T7PyJGzElWWWCija1ygnYSm4cm4Gc"
GEMINI_API_KEY = "AIzaSyDUCF6xNLhlRnMnoQS4ZVdRBAT5C7QcG8o"

# Gemini ማዋቀር
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

bot = telebot.TeleBot(BOT_TOKEN)

# የቦቱ መክፈቻ መልእክት (Identity: Mask On 🎭)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = "ሰላም! እኔ 'Mask On' 🎭 የተባልኩ የ Gemini AI ቦት ነኝ። ምን ልርዳህ?"
  bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def chat(message):
  try:
    # ቦቱ እያሰበ መሆኑን ለማሳየት
    bot.send_chat_action(message.chat.id, 'typing')
    
    # ከ Gemini መልስ መጠየቅ
    response = model.generate_content(message.text)
    
    # መልሱን ለተጠቃሚው መላክ
    if response.text:
      bot.reply_to(message, response.text)
    else:
      bot.reply_to(message, "ይቅርታ፣ 'Mask On' 🎭 አሁን መልስ መስጠት አልቻለም።")
  except Exception as e:
    bot.reply_to(message, "ይቅርታ፣ ስህተት ተከስቷል። እባክህ ቆይተህ ሞክር።")
    print(f"Error: {e}")

# ቦቱን ማስነሳት
if __name__ == "__main__":
  print("Mask On 🎭 is running...")
  bot.infinity_polling()
