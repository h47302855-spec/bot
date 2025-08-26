import time
import random
import requests
from datetime import datetime, timedelta

# ===========================
# 🔑 تنظیمات
# ===========================
TOKEN = "8424586245:AAGr1yuXlO2LVEw6vSIR4mv4imngUn29RLk"
OWNER_ID = 7354277212   # آیدی عددی تو
CHANNEL_USERNAME = "HajiFree_V2rey"  # عضویت اجباری
URL = f"https://api.telegram.org/bot{TOKEN}"

# ===========================
# 📊 دیتابیس ساده
# ===========================
users = {}  # {user_id: {"coins": int, "last_daily": date}}
active_groups = {}
original_titles = {}

# 🔠 26 فونت عددی
FONTS = [
    str.maketrans("0123456789:", "𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟕𝟖𝟗:"),
    str.maketrans("0123456789:", "⓿①②③④⑤⑥⑦⑧⑨:"),
    str.maketrans("0123456789:", "⓪𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡:"),
    str.maketrans("0123456789:", "０１２３４５６７８９:"),
    str.maketrans("0123456789:", "❶❷❸❹❺❻❼❽❾⓿:"),
    str.maketrans("0123456789:", "➀➁➂➃➄➅➆➇➈0:"),
    str.maketrans("0123456789:", "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓿:"),
    str.maketrans("0123456789:", "𝟘𝟙𝟚𝟛𝟜𝟝𝟞𝟟𝟠𝟡:"),
    str.maketrans("0123456789:", "𝟎𝟏𝟐𝟑𝟒𝟓𝟔𝟕𝟖𝟗:"),
    str.maketrans("0123456789:", "🄌①②③④⑤⑥⑦⑧⑨:"),
    str.maketrans("0123456789:", "🄀🄁🄂🄃🄄🄅🄆🄇🄈🄉:"),
    str.maketrans("0123456789:", "⒈⒉⒊⒋⒌⒍⒎⒏⒐0:"),
    str.maketrans("0123456789:", "⓪➊➋➌➍➎➏➐➑➒:"),
    str.maketrans("0123456789:", "⁰¹²³⁴⁵⁶⁷⁸⁹:"),
    str.maketrans("0123456789:", "₀₁₂₃₄₅₆₇₈₉:"),
    str.maketrans("0123456789:", "⓪①②③④⑤⑥⑦⑧⑨:"),
    str.maketrans("0123456789:", "❶❷❸❹❺❻❼❽❾⓿:"),
    str.maketrans("0123456789:", "⑴⑵⑶⑷⑸⑹⑺⑻⑼⓪:"),
    str.maketrans("0123456789:", "⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴:"),
    str.maketrans("0123456789:", "➊➋➌➍➎➏➐➑➒➓:"),
    str.maketrans("0123456789:", "⓵⓶⓷⓸⓹⓺⓻⓼⓽⓿:"),
    str.maketrans("0123456789:", "🄁🄂🄃🄄🄅🄆🄇🄈🄉🄊:"),
    str.maketrans("0123456789:", "➀➁➂➃➄➅➆➇➈➉:"),
    str.maketrans("0123456789:", "❶❷❸❹❺❻❼❽❾❿:"),
    str.maketrans("0123456789:", "Ⓞ①②③④⑤⑥⑦⑧⑨:")
]

# ===========================
# 📌 توابع
# ===========================
def api(method, data=None):
    try:
        r = requests.post(f"{URL}/{method}", data=data)
        return r.json()
    except:
        return {}

def get_updates(offset=None):
    return requests.get(f"{URL}/getUpdates", params={"timeout": 30, "offset": offset}).json()

def send_message(chat_id, text, reply_markup=None):
    data = {"chat_id": chat_id, "text": text}
    if reply_markup:
        data["reply_markup"] = reply_markup
    return api("sendMessage", data)

def delete_message(chat_id, msg_id):
    api("deleteMessage", {"chat_id": chat_id, "message_id": msg_id})

def set_title(chat_id, title):
    api("setChatTitle", {"chat_id": chat_id, "title": title})

def check_join(user_id):
    r = requests.get(f"{URL}/getChatMember?chat_id=@{CHANNEL_USERNAME}&user_id={user_id}").json()
    status = r.get("result", {}).get("status", "")
    return status in ["member", "administrator", "creator"]

# ===========================
# 🚀 ربات
# ===========================
def main():
    last_update_id = None
    last_minute = -1  

    while True:
        updates = get_updates(last_update_id)
        if "result" in updates and updates["result"]:
            for update in updates["result"]:
                last_update_id = update["update_id"] + 1

                if "message" not in update: 
                    continue

                msg = update["message"]
                chat_id = msg["chat"]["id"]
                user_id = msg["from"]["id"]
                text = msg.get("text", "")
                msg_id = msg.get("message_id")

                if "new_chat_title" in msg:  
                    delete_message(chat_id, msg_id)
                    continue

                if user_id not in users:
                    users[user_id] = {"coins": 0, "last_daily": None}

                # ⛔️ عضویت اجباری
                if not check_join(user_id) and user_id != OWNER_ID:
                    send_message(chat_id, f"⛔️ اول باید عضو بشی:\n👉 https://t.me/{CHANNEL_USERNAME}")
                    continue

                # دستورات مالک
                if user_id == OWNER_ID:
                    if text.startswith("/addcoin"):
                        _, uid, amount = text.split()
                        uid, amount = int(uid), int(amount)
                        users.setdefault(uid, {"coins": 0, "last_daily": None})
                        users[uid]["coins"] += amount
                        send_message(chat_id, f"✅ {amount} سکه به {uid} اضافه شد.")
                    elif text.startswith("/removecoin"):
                        _, uid, amount = text.split()
                        uid, amount = int(uid), int(amount)
                        users.setdefault(uid, {"coins": 0, "last_daily": None})
                        users[uid]["coins"] -= amount
                        send_message(chat_id, f"❌ {amount} سکه از {uid} کم شد.")
                    elif text.startswith("/broadcast"):
                        msg_b = text.replace("/broadcast ", "")
                        for uid in users:
                            send_message(uid, f"📢 پیام مدیریت:\n{msg_b}")
                        send_message(chat_id, "✅ پیام برای همه ارسال شد.")

                # دستورات عمومی
                if text == "/start":
                    send_message(chat_id, "🎉 خوش اومدی! پنل زیر رو بزن:", reply_markup='''{
                        "keyboard": [["🎮 بازی", "💰 سکه‌ها"],["⏰ تایم گروه", "🧹 پاکسازی"]], 
                        "resize_keyboard": true
                    }''')

                elif text == "💰 سکه‌ها":
                    coins = users[user_id]["coins"]
                    send_message(chat_id, f"💰 سکه‌های شما: {coins}")

                elif text == "🎮 بازی":
                    game = random.choice([
                        "https://t.me/gamebot",
                        "https://t.me/inlinegamesbot"
                    ])
                    send_message(chat_id, f"🎲 برای بازی اینو بزن:\n{game}")

                elif text == "⏰ تایم گروه":
                    active_groups[chat_id] = True
                    if chat_id not in original_titles:
                        original_titles[chat_id] = msg["chat"].get("title", "")
                    send_message(chat_id, "✅ تایمر روشن شد")

                elif text == "🧹 پاکسازی":
                    send_message(chat_id, "❓ چندتا پیام پاک کنم؟ (مثلا بنویس 50 یا all)")

                elif text.isdigit() and msg.get("reply_to_message"):
                    count = int(text)
                    for i in range(count):
                        try:
                            delete_message(chat_id, msg_id - i)
                        except:
                            pass
                    send_message(chat_id, f"🧹 {count} پیام پاک شد.")

                elif text.lower() == "all":
                    for i in range(msg_id, 0, -1):
                        try:
                            delete_message(chat_id, i)
                        except:
                            pass
                    send_message(chat_id, "🧹 همه پیام‌ها پاک شد.")

        # آپدیت تایم روی اسم گروه
        now = datetime.now()
        if now.minute != last_minute:
            last_minute = now.minute
            for chat_id, active in list(active_groups.items()):
                if active:
                    current_time = now.strftime("%H:%M")
                    font = random.choice(FONTS)
                    styled = current_time.translate(font)
                    new_title = f"{original_titles.get(chat_id, '')} | {styled}"
                    set_title(chat_id, new_title)

        time.sleep(3)

if __name__ == "__main__":
    print("🚀 ربات استارت شد ...")
    main()