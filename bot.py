# بوت تليجرام متكامل - نسخة احترافية
import requests
import time
import os
import random
from datetime import datetime
from flask import Flask, request, jsonify
from threading import Thread

BOT_TOKEN = "8657067891:AAENEXG6CeTjZcZ4Ic1v-giNLFBIKjeornk"
DEVELOPER_NAME = "بكري بيس"
WATERMARK = "[BAKRI BIS AI]"
BOT_USERNAME = "BakriImageBot"

IMAGE_WIDTH = 2048
IMAGE_HEIGHT = 2048

app = Flask(__name__)
last_update_id = 0
processed_ids = set()

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": chat_id, "text": text})
    except:
        pass

def send_photo(chat_id, image_url, caption=""):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
    try:
        requests.post(url, json={"chat_id": chat_id, "photo": image_url, "caption": caption[:1024]})
    except:
        pass

def get_updates():
    global last_update_id
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"
    try:
        response = requests.get(url, params={"offset": last_update_id + 1, "timeout": 30})
        return response.json().get("result", [])
    except:
        return []

def generate_image(prompt):
    encoded = prompt.replace(" ", "%20")
    quality_words = ["8K", "HDR", "professional", "masterpiece", "ultra high quality"]
    enhancer = random.choice(quality_words)
    final_prompt = f"{prompt}, {enhancer}"
    encoded_prompt = final_prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={IMAGE_WIDTH}&height={IMAGE_HEIGHT}&nologo=true"

def get_welcome():
    return f"🌟 {WATERMARK}\nأرسل وصف الصورة وسأولدها لك!"

def handle_message(text, chat_id):
    if text in ["/start", "ابدأ"]:
        return get_welcome()
    elif len(text) > 3:
        return None, text
    else:
        return "أرسل وصفاً للصورة (أكثر من 3 أحرف)"

def run_bot():
    global last_update_id, processed_ids
    while True:
        try:
            updates = get_updates()
            for update in updates:
                update_id = update.get("update_id")
                if update_id in processed_ids:
                    continue
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg["chat"]["id"]
                    text = msg.get("text", "")
                    if text:
                        result = handle_message(text, chat_id)
                        if isinstance(result, tuple):
                            _, prompt = result
                            send_message(chat_id, f"🎨 جاري توليد الصورة...")
                            image_url = generate_image(prompt)
                            send_photo(chat_id, image_url, f"✨ {WATERMARK}\n{prompt}")
                        elif result:
                            send_message(chat_id, result)
                        processed_ids.add(update_id)
                        if update_id > last_update_id:
                            last_update_id = update_id
            time.sleep(1)
        except Exception as e:
            print(f"خطأ: {e}")
            time.sleep(5)

@app.route('/')
def home():
    return f"{WATERMARK} - بوت يعمل 24/7"

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
