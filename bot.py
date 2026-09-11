import os
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    filters,
)
import google.generativeai as genai
import edge_tts

# আপনার দেওয়া টোকেন ও এপিআই কি
TELEGRAM_BOT_TOKEN = "8928921868:AAGnXVYa5CbkzhsxQ3Oq0BduM3TDthrA1CM"
GEMINI_API_KEY = "AQ.Ab8RN6JnYVG6Z7yf_OybQ79MyRrTbnonv4c50z--l21ITRfhew"

# জেমিনি এআই কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# মাইক্রোসফটের ন্যাচারাল মেয়েদের বাংলা ভয়েস
VOICE_NAME = "bn-BD-NabanitaNeural"

# ইউজারদের স্টেট ট্র্যাক করার জন্য ডিকশনারি
user_states = {}


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_text = update.message.text
  chat_id = update.message.chat_id

  if not user_text:
    return

  text_lower = user_text.lower()

  # পেমেন্ট সংক্রান্ত কথা বললে বিকাশ/নগদ নম্বর দিয়ে দেওয়া
  if "পেমেন্ট" in text_lower or "বিকাশ" in text_lower or "নগদ" in text_lower:
    payment_reply = (
        "পেমেন্ট করার জন্য আমাদের বিকাশ ও নগদ নম্বর:\n"
        "💳 বিকাশ / নগদ: `01346133685`\n\n"
        "টাকা পাঠিয়ে স্ক্রিনশট দিন।"
    )
    await update.message.reply_text(payment_reply, parse_mode="Markdown")
    return

  # ইউজার যদি আগে কোনো অপশন সিলেক্ট না করে থাকে, তবে অপশন জানতে চাওয়া
  if chat_id not in user_states:
    if "সার्वিস" in text_lower or "service" in text_lower or "servis" in text_lower:
      user_states[chat_id] = "service"
      service_text = (
          "বয়স 20 বছর, সাইজঃ 34\" গায়ের রঙ ফর্সা।\n\n"
          "✅ভিডিও কল রেট..\n"
          "🕒 ০৫ মিনিট – ৮০ টাকা\n"
          "🕡 ১০ মিনিট – ১২০ টাকা\n"
          "🕒 ১৫ মিনিট - ১৪০ টাকা\n"
          "🕒 ২০ মিনিট - ১৮০ টাকা\n"
          "🕒 ৩০ মিনিট - ২২০ টাকা\n"
          "🕒 ৬০ মিনিট - ৫০০ টাকা\n\n"
          "✅ডেমো কল:- ১মিনিট :- ৫০৳ \n\n"
          "✅অডিও কল রেট..\n"
          "🕒 ০৫ মিনিট – ৫০ টাকা\n"
          "🕡 ১০ মিনিট –১০০ টাকা\n\n"
          "গুরুত্বপূর্ণ:-\n"
          "✊ডেমো ১ মিনিট ৫০ টাকা\n"
          "⚠️কোন পিক হবে না।\n"
          "✊রিয়েল বা সরাসরি সেক্স করি না\n"
          "✊মেসেজ দিয়ে জিজ্ঞেস করবেন না যে রিয়েল হবে \n"
          "✊প্রেম ভালোবাসা বিয়ের কথা বললে ব্লক খাবেন। \n"
          "🔞 সার্ভিস নিয়ে ভাল লাগলে আবার আসবেন।💕"
      )
      await update.message.reply_text(service_text)
      return

    elif "গ্রুপ" in text_lower or "group" in text_lower or "gruf" in text_lower:
      user_states[chat_id] = "group"
      group_text = (
          "আপনারা কেউ গ্রুপ কিনলে আমাদের কাছ থেকে কিনতে পারেন\n\n"
          "🍀আজকের সেরা অফার 🍀\n"
          "━━━━━━━━━━━━━━━━━━\n"
          "🍀বাংলা গ্রুপ 20 টি 300 টাকা\n"
          "🍀ইন্ডিয়ান গ্রুপ 15 টি 300 টাকা\n"
          "🍀রেপ গ্রুপ 3 টি 300 টাকা\n"
          "🍀ট্যাঙ্গো গ্রুপ 5 টি 300 টাকা\n"
          "🍀বাচ্চাদের গ্রুপ 5 টি 350 টাকা\n"
          "🍀সিসিটিভি গ্রুপ 4 টি 300 টাকা\n"
          "🍀ওয়েব সিরিজ 3 টি 350 টাকা\n"
          "🍀জাপানি গ্রুপ 5 টি 300 টাকা\n"
          "🍀যাত্রা ডান্স গ্রুপ 1 টি 350 টাকা\n"
          "🍀হিজড়াদের গ্রুপ 2 টি 300টাকা\n"
          "🍀লেসবিয়ান গ্রুপ 4 টি 300টাকা\n"
          "🍀তামিল গ্রুপ 10 টি 350 টাকা\n"
          "🍀চায়না গ্রুপ 10 টি 350 টাকা\n"
          "🍀ভাবি বৌদি গ্রূপ 5 টি 300টাকা\n"
          "🍀ভাইরাল গ্রুপ 2 টি 400 টাকা\n"
          "🍀Chamet গ্রুপ 2 টি 300 টাকা\n"
          "🍀ছেলে ছেলে গ্রুপ 2 টি 300টাকা\n"
          "🍀গোসলের গুপ 2 টি 350টাকা\n"
          "🍀কোরিয়ান গ্রুপ 4 টি 300 টাকা\n"
          "🍀হিজাবি গ্রুপ 3 টি 300 টাকা\n"
          "🍀হিডেন গ্রুপ 5 টি 300 টাকা\n"
          "🍀পারিবারিক গ্রুপ 5 টি 300টাকা\n"
          "🍀মা ছেলের গুরুপ 5 টি 300টাকা\n"
          "🍀ভাই বোনের গ্রুপ 4 টি 300 টাকা\n"
          "🍀ফিঙ্গারিং ভিডিওগ্রুপ 4 টি400টাকা\n"
          "🍀বড় দুধের ভিডিওগ্রুপ 1 টি 300 টাকা\n"
          "━━━━━━━━━━━━━━━━━━\n"
          "বিশেষ করে যারা কিনতে পারবেন তাড়াই মেসেজ করবেন আমাদের কাছে পেমেন্ট কারার জন্য\n"
          "🍀 ❈ নগদ ❈    ❈ বিকাশ ❈\n"
          "🍀 অল গ্রুপ ২০০০ টাকা 🍀\n"
          "━━━━━━━━━━━━━━━━━━\n"
          "টাকা দেওয়ার আগে কোন গ্রুপ দেওয়া হয় না যারা কিনবেন শুধুমাত্র তারাই ইনবক্সে মেসেজ করেন গ্রুপ কেনার জন্য এই আইডিতে মেসেজ করেন: @SamiyaSamiya9"
      )
      await update.message.reply_text(group_text)
      return
    else:
      # প্রথম মেসেজ পেলে জানতে চাওয়া সে কি চাচ্ছে
      intro_reply = (
          "স্বাগতম! আপনার কি লাগবে?\n\n১. **সার্ভিস** (কল বা চ্যাট)\n২. **গ্রুপ** (লিস্ট দেখতে চান)"
          "\n\nদয়া করে লিখে জানান আপনার কোনটি লাগবে।"
      )
      await update.message.reply_text(intro_reply, parse_mode="Markdown")
      return

  # অপশন সিলেক্ট করার পর সাধারণ কথার উত্তর জেমিনি দিয়ে ভয়েস নোটে দেওয়া
  prompt = (
      "তুমি একজন রিয়েল তরুণী মেয়ে (Samiya)। টেলিগ্রামে কেউ তোমাকে মেসেজ দিলে যেভাবে"
      f' একদম শর্ট, মিষ্টি ও প্রাকৃতিকভাবে বাংলায় চ্যাট করো, ঠিক সেভাবে উত্তর দাও। মেসেজটি হলো: "{user_text}"'
  )

  try:
    ai_response = model.generate_content(prompt)
    reply_text = (
        ai_response.text.strip()
        if ai_response.text
        else "আচ্ছা, বিষয়টি বুঝতে পেরেছি।"
    )
  except Exception:
    reply_text = "উহু, এই মুহূর্তে একটু ব্যস্ত আছি।"

  audio_path = "voice_reply.mp3"

  try:
    communicate = edge_tts.Communicate(reply_text, VOICE_NAME)
    await communicate.save(audio_path)

    with open(audio_path, "rb") as voice_file:
      await context.bot.send_voice(chat_id=chat_id, voice=voice_file)
  except Exception:
    await update.message.reply_text(reply_text)
  finally:
    if os.path.exists(audio_path):
      os.remove(audio_path)


def main():
  app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
  app.add_handler(
      MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
  )
  print("SamiyaVoice_bot is running 24/7...")
  app.run_polling()


if __name__ == "__main__":
  main()