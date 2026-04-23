import requests
import time

BOT_TOKEN = "8657067891:AAENEXG6CeTjZcZ4Ic1v-giNLFBIKjeornk"
DEVELOPER_NAME = "بكري بيس"
WATERMARK = "[BAKRI BIS AI]"

last_id = 0

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except:
        pass

def send_photo(chat_id, image_url, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        requests.post(url, json={"chat_id": chat_id, "photo": image_url, "caption": caption})
    except:
        pass

def get_updates():
    global last_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        data = requests.get(url, params={"offset": last_id + 1, "timeout": 30}).json()
        return data.get("result", [])
    except:
        return []

def generate_image(prompt):
    encoded = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{encoded}?width=1024&height=1024"

def handle_message(text, chat_id):
    if text.startswith("/start"):
        return f"🌟 مرحبا بك في {WATERMARK}\nأرسل /image وصف الصورة"
    elif text.startswith("/image"):
        prompt = text[6:].strip()
        if len(prompt) < 3:
            return "✏️ اكتب وصفاً للصورة"
        send_message(chat_id, f"🎨 جاري توليد الصورة...")
        image_url = generate_image(prompt)
        send_photo(chat_id, image_url, f"✨ {WATERMARK}\n{prompt}")
        return None
    else:
        return f"🎨 أرسل /image وصف الصورة"

print(f"{WATERMARK} يعمل...")
while True:
    try:
        updates = get_updates()
        for update in updates:
            if "message" in update:
                msg = update["message"]
                chat_id = msg["chat"]["id"]
                text = msg.get("text", "")
                if text:
                    response = handle_message(text, chat_id)
                    if response:
                        send_message(chat_id, response)
                    last_id = update["update_id"]
        time.sleep(1)
    except Exception as e:
        print(f"خطأ: {e}")
        time.sleep(5)
