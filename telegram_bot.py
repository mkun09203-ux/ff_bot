import telebot
import requests
from datetime import datetime

# YAHAN APNA BOTFATHER WALA TOKEN DAALIYE (Double quotes ke andar)
TOKEN = "8656141332:AAFmUg-JBP_xjM3jdd12C1TByrk7BAql4t4"

bot = telebot.TeleBot(TOKEN)

# API Links
api_url = "http://raw.thug4ff.xyz/info"
image_api_url = "http://profile.thug4ff.xyz/api/profile"

def convert_unix_timestamp(timestamp):
    try:
        return datetime.utcfromtimestamp(int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return "Not found"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "🔥 Welcome to FF Info Bot! 🔥\n\nApni profile dekhne ke liye type karein:\n`/info <UID>`\nExample: `/info 16207002`", parse_mode='Markdown')

@bot.message_handler(commands=['info'])
def send_info(message):
    try:
        parts = message.text.split()
        if len(parts) < 2:
            bot.reply_to(message, "❌ Bhai, UID daalna bhool gaye! Aise likho: `/info 16207002`", parse_mode='Markdown')
            return
        
        uid = parts[1]
        wait_msg = bot.reply_to(message, "⏳ Data fetch kar raha hoon, thoda wait karo...")

        # 1. Text Data Mangwana
        response = requests.get(f"{api_url}?uid={uid}&key=great")
        
        if response.status_code == 404:
            bot.edit_message_text(f"❌ UID `{uid}` nahi mili. (Yaad rahe IND server abhi down hai).", chat_id=message.chat.id, message_id=wait_msg.message_id)
            return
        elif response.status_code != 200:
            bot.edit_message_text("⚠️ API Error. Thodi der baad try karein.", chat_id=message.chat.id, message_id=wait_msg.message_id)
            return

        data = response.json()
        
        basic_info = data.get('basicInfo', {})
        captain_info = data.get('captainBasicInfo', {})
        clan_info = data.get('clanBasicInfo', {})
        credit_score_info = data.get('creditScoreInfo', {})
        pet_info = data.get('petInfo', {})
        profile_info = data.get('profileInfo', {})
        social_info = data.get('socialInfo', {})

        # --- Message Design Start ---
        msg = f"**Player Information**\n\n"
        
        # ACCOUNT BASIC INFO
        msg += f"**┌ ACCOUNT BASIC INFO**\n"
        msg += f"├─ Name: {basic_info.get('nickname', 'Not found')}\n"
        msg += f"├─ UID: `{uid}`\n"
        msg += f"├─ Level: {basic_info.get('level', 'Not found')} (Exp: {basic_info.get('exp', '?')})\n"
        msg += f"├─ Region: {basic_info.get('region', 'Not found')}\n"
        msg += f"├─ Likes: {basic_info.get('liked', 'Not found')}\n"
        msg += f"├─ Honor Score: {credit_score_info.get('creditScore', 'Not found')}\n"
        msg += f"└─ Signature: {social_info.get('signature', 'None') or 'None'}\n\n"

        # ACCOUNT ACTIVITY
        msg += f"**┌ ACCOUNT ACTIVITY**\n"
        msg += f"├─ Most Recent OB: {basic_info.get('releaseVersion', '?')}\n"
        msg += f"├─ Current BP Badges: {basic_info.get('badgeCnt', 'Not found')}\n"
        msg += f"├─ BR Rank: {basic_info.get('rankingPoints', '?')}\n"
        msg += f"├─ CS Rank: {basic_info.get('csRankingPoints', '?')}\n"
        msg += f"├─ Created At: {convert_unix_timestamp(basic_info.get('createAt', 0))}\n"
        msg += f"└─ Last Login: {convert_unix_timestamp(basic_info.get('lastLoginAt', 0))}\n\n"

        # ACCOUNT OVERVIEW
        skills = profile_info.get('equipedSkills', [])
        skills_text = f"[{', '.join(map(str, skills))}]" if skills else "Not found"
        msg += f"**┌ ACCOUNT OVERVIEW**\n"
        msg += f"├─ Avatar ID: {profile_info.get('avatarId', 'Not found')}\n"
        msg += f"├─ Banner ID: {basic_info.get('bannerId', 'Not found')}\n"
        msg += f"├─ Pin ID: {captain_info.get('pinId', 'Not found') if captain_info else 'Default'}\n"
        msg += f"└─ Equipped Skills: {skills_text}\n\n"

        # PET DETAILS
        msg += f"**┌ PET DETAILS**\n"
        msg += f"├─ Equipped?: {'Yes' if pet_info.get('isSelected') else 'Not Found'}\n"
        msg += f"├─ Pet Name: {pet_info.get('name', 'Not Found')}\n"
        msg += f"├─ Pet Exp: {pet_info.get('exp', 'Not Found')}\n"
        msg += f"└─ Pet Level: {pet_info.get('level', 'Not Found')}\n\n"

        # GUILD INFO
        if clan_info:
            msg += f"**┌ GUILD INFO**\n"
            msg += f"├─ Guild Name: {clan_info.get('clanName', 'Not found')}\n"
            msg += f"├─ Guild ID: `{clan_info.get('clanId', 'Not found')}`\n"
            msg += f"├─ Guild Level: {clan_info.get('clanLevel', 'Not found')}\n"
            msg += f"├─ Live Members: {clan_info.get('memberNum', 'Not found')}/{clan_info.get('capacity', '?')}\n"
            
            if captain_info:
                msg += f"└─ Leader Info:\n"
                msg += f"   ├─ Leader Name: {captain_info.get('nickname', 'Not found')}\n"
                msg += f"   ├─ Leader UID: `{captain_info.get('accountId', 'Not found')}`\n"
                msg += f"   ├─ Leader Level: {captain_info.get('level', 'Not found')} (Exp: {captain_info.get('exp', '?')})\n"
                msg += f"   ├─ Last Login: {convert_unix_timestamp(captain_info.get('lastLoginAt', 0))}\n"
                msg += f"   ├─ Title: {captain_info.get('title', 'Not found')}\n"
                msg += f"   ├─ BP Badges: {captain_info.get('badgeCnt', '?')}\n"
                msg += f"   ├─ BR Rank: {captain_info.get('rankingPoints', 'Not found')}\n"
                msg += f"   └─ CS Rank: {captain_info.get('csRankingPoints', 'Not found')}"

        # Pehle Lamba Text Bhejna
        bot.edit_message_text(msg, chat_id=message.chat.id, message_id=wait_msg.message_id, parse_mode='Markdown')

        # 2. Outfit Image Mangwana aur Bhejna
        bot.send_chat_action(message.chat.id, 'upload_photo') # "uploading photo..." status dikhayega
        try:
            img_url = f"{image_api_url}?uid={uid}"
            img_response = requests.get(img_url)
            if img_response.status_code == 200:
                bot.send_photo(message.chat.id, img_response.content)
            else:
                bot.send_message(message.chat.id, "⚠️ Outfit photo load nahi ho payi.")
        except Exception as e:
            print(f"Image Error: {e}")

    except Exception as e:
        bot.send_message(message.chat.id, "⚠️ Kuch gadbad ho gayi data laane mein.")
        print(f"Error: {e}")

print("🚀 Telegram Bot Ekdum VIP Style Mein Start Ho Gaya Hai (With Image)...")
bot.polling()