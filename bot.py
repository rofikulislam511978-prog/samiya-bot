import os
import logging
import threading
from flask import Flask
from telethon import TelegramClient, events
import google.generativeai as genai
import edge_tts

# লগিং সেটআপ
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# কনফিগারেশন (আপনার সঠিক তথ্য দিয়ে সেট করা)
API_ID = 38710926
API_HASH = "9047aad732a7b1793fcd1857c56d7d3f"
GEMINI_API_KEY = "AQ.Ab8RN6KZUV1Wez0x7Rouv49MQJCrBOqQqQaFvJgOkpwd8CsXgA"

# জেমিনি কনফিগার করুন
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {"temperature": 0.7, "max_output_tokens": 150}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", generation_config=generation_config
)

VOICE_NAME = "bn-BD-NabanitaNeural"

# টেলিথন ক্লায়েন্ট ইনিশিয়ালাইজ (ইউজারবট)
client = TelegramClient("samiya_session", API_ID, API_HASH)

# ফ্লাস্ক সার্ভার (রেন্ডার সচল রাখার জন্য)
app = Flask(__name__)


@app.route("/")
def home():
  return "Samiya Userbot is running successfully!"


def run_flask():
  port = int(os.environ.get("PORT", 10000))
  app.run(host="0.0.0.0", port=port)


# ইনকামিং মেসেজ হ্যান্ডলার (শুধু ইনবক্স বা প্রাইভেট চ্যাটের জন্য)
@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_message(event):
  sender = await event.get_sender()
  if sender.bot:
    return  # বট মেসেজ ইগ্নোর করবে

  user_text = event.raw_text
  if not user_text:
    return

  # পেমেন্ট সম্পর্কিত নির্দেশনা
  if "পেমেন্ট" in user_text.lower():
    payment_reply = (
        "পেমেন্ট করার জন্য আমাদের বিকাশ ও নগদ নম্বর:\n"
        "💳 বিকাশ / নগদ : `01346133685`\n"
        "টাকা পাঠিয়ে স্ক্রিনশট দিন!"
    )
    await event.respond(payment_reply, parse_mode="markdown")
    return

  # সার্ভিস বা প্রাইস লিস্ট
  if "সার্ভিস" in user_text.lower() or "service" in user_text.lower():
    service_text = (
        "⭐ **সার্ভিস ও রেট লিস্ট:**\n"
        "⏱️ ০৫ মিনিট - ৮০ টাকা\n"
        "⏱️ ১০ মিনিট - ১২০ টাকা\n"
        "⏱️ ১৫ মিনিট - ১৬০ টাকা\n"
        "⏱️ ২০ মিনিট - ১৮০ টাকা\n"
        "⏱️ ৩০ মিনিট - ২২০ টাকা\n"
        "⏱️ ৬০ মিনিট - ৪০০ টাকা\n"
        "⚠️ কোনো পিক হবে না!\n"
        "📩 মেসেজ দিয়ে জিজ্ঞেস করবেন না যে রিয়েল হবে কি না"
    )
    await event.respond(service_text)
    return

  # জেমিনি দিয়ে এআই চ্যাট এবং ভয়েস রিপ্লাই তৈরি
  prompt = f"তুমি একজন রিয়েল তরুণী মেয়ে (Sumaiya) টেলিগ্রামে কেউ তোমাকে মেসেজ দিলে যেভাবে চ্যাট করো, মিষ্টি এবং প্রাকৃতিকভাবে বাংলায় চ্যাট করো, ঠিক সেভাবে উত্তর দাও। মেসেজটি হলো: \"{user_text}\""

  try:
    ai_response = model.generate_content(prompt)
    reply_text = (
        ai_response.text.strip() if ai_response.text else "আহা, বিষয়টি বুঝতে পেরেছি।"
    )
  except Exception:
    reply_text = "উহ, এই মুহূর্তে একটু ব্যস্ত আছি।"

  audio_path = "voice_reply.mp3"
  try:
    communicate = edge_tts.Communicate(reply_text, VOICE_NAME)
    await communicate.save(audio_path)

    # ভয়েস মেসেজ হিসেবে পাঠানো
    await client.send_file(event.chat_id, audio_path, voice_note=True)
  except Exception:
    # ভয়েস ফেইল করলে টেক্সট রিপ্লাই পাঠাবে
    await event.respond(reply_text)
  finally:
    if os.path.exists(audio_path):
      os.remove(audio_path)


if __name__ == "__main__":
  # ব্যাকগ্রাউন্ডে ফ্লাস্ক সার্ভার চালু করা
  server_thread = threading.Thread(target=run_flask, daemon=True)
  server_thread.start()

  logger.info("Samiya Userbot is starting...")
  client.start()
  client.run_until_disconnected()
