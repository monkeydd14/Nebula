import os
import telebot
import requests

# Railway Environment Variable (BOT_TOKEN) ထဲကနေ လှမ်းဖတ်ပါမယ်
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 မင်္ဂလာပါ! MLBB ID စစ်ပေးမယ့် Bot ဖြစ်ပါတယ်။\n\n"
        "🔍 **အသုံးပြုပုံ:**\n"
        "`/ml [ID] [Server]` ပုံစံအတိုင်း ရိုက်ပို့ပေးပါ။\n\n"
        "📝 **ဥပမာ:** `/ml 1114917746 13486`"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")

@bot.message_handler(commands=['ml'])
def check_ml_id(message):
    args = message.text.split()
    if len(args) < 3:
        bot.reply_to(message, "⚠️ ကျေးဇူးပြု၍ ID နှင့် Server ကို မှန်ကန်အောင် ရိုက်ပါ။\nဥပမာ- `/ml 1114917746 13486`", parse_mode="Markdown")
        return

    player_id = args[1]
    server_id = args[2]
    status_msg = bot.reply_to(message, "⏳ API မှ အချက်အလက်များကို စစ်ဆေးနေပါသည်...")

    api_url = f"https://api.isan.eu.org/ml?id={player_id}&server={server_id}"

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("success") or "name" in data:
                nickname = data.get("name", "မသိပါ")
                result_text = (
                    "✅ **MLBB User Found!**\n\n"
                    "👤 **Nickname:** `" + nickname + "`\n"
                    "🆔 **Player ID:** `" + player_id + "`\n"
                    "🌐 **Server:** `" + server_id + "`"
                )
            else:
                result_text = "❌ အချက်အလက် ရှာမတွေ့ပါ။ ID သို့မဟုတ် Server မှားနေနိုင်ပါသည်။"
        else:
            result_text = "⚠️ API Error! ခေတ္တစောင့်ပြီးမှ ပြန်လည်ကြိုးစားပေးပါ။"
    except requests.exceptions.RequestException:
        result_text = "🌐 API Server နဲ့ ချက်ဆက်မှု မအောင်မြင်ပါ။"

    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")

# Bot ကို စတင်ပတ်မောင်းခြင်း
bot.infinity_polling()
