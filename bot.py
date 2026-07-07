import os
import telebot
import requests

# Railway Environment Variable ကနေ Token ဖတ်ခြင်း
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
    status_msg = bot.reply_to(message, "⏳ API အသစ်မှ အချက်အလက်များကို စစ်ဆေးနေပါသည်...")

    # API အသစ် Endpoint
    api_url = f"https://yanjiestore.com/submitt.php?ID={player_id}&server={server_id}"

    try:
        # User-Agent အတုထည့်ပေးခြင်းဖြင့် API Block ဖြစ်ခြင်းကို ကာကွယ်ရန်
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # API က နာမည်ပြန်ပေးတဲ့ Key ကို စစ်ဆေးခြင်း (ဥပမာ- "username" သို့မဟုတ် "name")
            nickname = data.get("username") or data.get("name") or data.get("Nickname")
            
            if nickname:
                result_text = (
                    "✅ **MLBB User Found!**\n\n"
                    "👤 **Nickname:** `" + str(nickname) + "`\n"
                    "🆔 **Player ID:** `" + player_id + "`\n"
                    "🌐 **Server:** `" + server_id + "`"
                )
            else:
                result_text = "❌ အချက်အလက် ရှာမတွေ့ပါ။ ID သို့မဟုတ် Server မှားနေနိုင်ပါသည်။"
        else:
            result_text = "⚠️ API Error! ခေတ္တစောင့်ပြီးမှ ပြန်လည်ကြိုးစားပေးပါ။"
            
    except requests.exceptions.RequestException:
        result_text = "🌐 API Server နဲ့ ချိတ်ဆက်မှု မအောင်မြင်ပါ။"
    except ValueError:
        result_text = "⚠️ API မှ မှန်ကန်သော အချက်အလက်များ မပေးပို့ပါ။"

    bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode="Markdown")

# Bot ပတ်မောင်းခြင်း
bot.infinity_polling()


