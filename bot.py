import os
import asyncio
import logging
import time
import threading
from flask import Flask
from telethon import TelegramClient, events
import google.generativeai as genai
import edge_tts

# ১. ফ্লাস্ক ডামি সার্ভার (রেন্ডারে ২৪ ঘণ্টা সচল রাখার জন্য)
app = Flask('')

@app.route('/')
def home():
    return "Samiya Personal Userbot is running 24/7!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = threading.Thread(target=run_web)
    t.start()

# ২. টেলিগ্রাম API এবং জেমিনি ক্রিয়েডেনশিয়ালস
API_ID = 38710926
API_HASH = "9047aad732a7b1793fcd1857c56d7d3f"
GEMINI_API_KEY = "AQ.Ab8RN6JnYVG6Z7yf_Oyq9TjRbTbnovn4c50z--121ITRfhew"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

VOICE_NAME = "bn-BD-NabanitaNeural"  # মিষ্টি মেয়ে কণ্ঠে ভয়েস

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# টেলিগ্রাম ক্লায়েন্ট ইনিশিয়ালাইজ
client = TelegramClient('samiya_personal_session', API_ID, API_HASH)

# সিকোয়েন্সিয়াল চ্যাট লক এবং টাইম ট্র্যাকিং ডিকশনারি
user_locks = {}
last_message_times = {}

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_incoming_message(event):
    sender = await event.get_sender()
    if sender.bot or sender.verified:
        return

    chat_id = event.chat_id
    user_text = event.raw_text
    if not user_text:
        return

    # প্রতি চ্যাটের জন্য আলাদা লক তৈরি, যেন একে একে উত্তর দেয়
    if chat_id not in user_locks:
        user_locks[chat_id] = asyncio.Lock()

    async with user_locks[chat_id]:
        current_time = time.time()
        if chat_id in last_message_times:
            time_diff = current_time - last_message_times[chat_id]
            if time_diff > 15:
                logger.info(f"Chat {chat_id} delayed by over 15 seconds. Processing sequentially.")

        last_message_times[chat_id] = current_time
        text_lower = user_text.lower()
        logger.info(f"Processing message from {sender.first_name}: {user_text}")

        # মানুষের মতো ধীর গতিতে টাইপিং স্ট্যাটাস দেখানো
        async with event.client.action(chat_id, 'typing'):
            await asyncio.sleep(2.5)

            if "পেমেন্ট" in text_lower or "বিকাশ" in text_lower or "নগদ" in text_lower:
                reply_text = "পেমেন্ট করার জন্য আমাদের বিকাশ ও নগদ নম্বর: 01346133685। টাকা পাঠিয়ে স্ক্রিনশট দাও।"
            elif "সার্ভিস" in text_lower or "call" in text_lower or "কল" in text_lower:
                reply_text = "ভিডিও কল বা অডিও কলের জন্য রেট লিস্ট ইনবক্সে দেখে নিতে পারো। বলো কি লাগবে?"
            else:
                prompt = (
                    "তুমি রিয়েল একজন তরুণী মেয়ে (Samiya)। টেলিগ্রামে কেউ তোমাকে ইনবক্সে মেসেজ দিলে যেভাবে "
                    f"খুব মিষ্টি ও স্বাভাবিক ভাষায় চ্যাট করো, ঠিক সেভাবে ছোট ও প্রাকৃতিকভাবে উত্তর দাও। মেসেজটি হলো: \"{user_text}\""
                )
                try:
                    ai_response = model.generate_content(prompt)
                    reply_text = ai_response.text.strip() if ai_response.text else "আচ্ছা, বলো।"
                except Exception:
                    reply_text = "বলো, শুনছি তো।"

        # ভয়েস মেসেজ তৈরি ও পাঠানো (মেয়ে কণ্ঠে)
        audio_path = "voice_reply.mp3"
        try:
            communicate = edge_tts.Communicate(reply_text, VOICE_NAME)
            await communicate.save(audio_path)

            async with event.client.action(chat_id, 'record-audio'):
                await asyncio.sleep(3)
                await client.send_file(chat_id, audio_path, voice_note=True)
        except Exception:
            await event.respond(reply_text)
        finally:
            if os.path.exists(audio_path):
                os.remove(audio_path)

def main():
    # ফ্লাস্ক সার্ভার ব্যাকগ্রাউন্ডে চালু করা
    keep_alive()
    print("Samiya 24/7 Safe Userbot is starting...")
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    main()
