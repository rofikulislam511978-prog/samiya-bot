import asyncio
import os
import random
from telethon import TelegramClient, events
from telethon.errors import FloodWaitError
import google.generativeai as genai
import edge_tts

# রেলওয়ে বা এনভায়রনমেন্ট থেকে ভ্যারিয়েবলগুলো রিড করা
API_ID = int(os.getenv("API_ID", "38710926"))
API_HASH = os.getenv("API_HASH", "9047aad732a7b1793fcd1857c56d7d3f")
SESSION_STRING = os.getenv("SESSION") or os.getenv("STRING_SESSION")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# জেমিনি এআই কনফিগারেশন
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 800,
}
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "You are Samiya, a friendly human girl chatting on Telegram. "
        "Reply naturally in Bengali, keeping it concise, sweet, and conversational."
    ),
)

# মাইক্রোসফটের ন্যাচারাল মেয়েদের বাংলা ভয়েস
VOICE_NAME = "bn-BD-NabanitaNeural"

# টেলিগ্রাম ক্লায়েন্ট ইনিশিয়ালাইজেশন
client = TelegramClient(
    session=SESSION_STRING, api_id=API_ID, api_hash=API_HASH
)

# ইউজারদের স্টেট ট্র্যাক করার জন্য ডিকশনারি
user_states = {}

# সিরিয়াল অনুযায়ী কাজ করার জন্য কিউ (Queue) এবং লক
message_queue = asyncio.Queue()
is_processing = False


async def text_to_speech(text, filename="response.mp3"):
  communicate = edge_tts.Communicate(text, VOICE_NAME)
  await communicate.save(filename)
  return filename


async def process_queue():
  global is_processing
  while not message_queue.empty():
    is_processing = True
    sender_id, event, user_text, chat_id = await message_queue.get()

    try:
      # ১. মানুষের মতো ১৫-১৬ সেকেন্ড বা র্যান্ডম বিরতি
      delay = random.uniform(15, 18)
      await asyncio.sleep(delay)

      text_lower = user_text.lower()

      # পেমেন্ট সংক্রান্ত কথা বললে বিকাশ/নগদ নম্বর দিয়ে দেওয়া
      if "পেমেন্ট" in text_lower or "বিকাশ" in text_lower or "নগদ" in text_lower:
        payment_reply = (
            "পেমেন্ট করার জন্য আমাদের বিকাশ ও নগদ নম্বর:\n"
            "💳 বিকাশ / নগদ: `01346133685`\n\n"
            "টাকা পাঠিয়ে স্ক্রিনশট দিন।"
        )
        async with event.client.action(chat_id, "record-audio"):
          audio_file = await text_to_speech(payment_reply)
          await asyncio.sleep(2)
        await event.respond(file=audio_file, voice_note=True)
        if os.path.exists(audio_file):
          os.remove(audio_file)
        continue

      # ইউজার সার্ভিস বা গ্রুপ দেখতে চাইলে
      if chat_id not in user_states:
        if "সার্বিস" in text_lower or "service" in text_lower or "servis" in text_lower:
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
          async with event.client.action(chat_id, "record-audio"):
            audio_file = await text_to_speech(service_text)
            await asyncio.sleep(2)
          await event.respond(file=audio_file, voice_note=True)
          if os.path.exists(audio_file):
            os.remove(audio_file)
          continue

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
          async with event.client.action(chat_id, "record-audio"):
            audio_file = await text_to_speech(group_text)
            await asyncio.sleep(2)
          await event.respond(file=audio_file, voice_note=True)
          if os.path.exists(audio_file):
            os.remove(audio_file)
          continue
        else:
          intro_reply = (
              "স্বাগতম! আপনার কি লাগবে?\n\n১. সার্ভিস (কল বা চ্যাট)\n২. গ্রুপ (লিস্ট দেখতে চান)\n\nদয়া করে লিখে জানান আপনার কোনটি লাগবে।"
          )
          async with event.client.action(chat_id, "record-audio"):
            audio_file = await text_to_speech(intro_reply)
            await asyncio.sleep(2)
          await event.respond(file=audio_file, voice_note=True)
          if os.path.exists(audio_file):
            os.remove(audio_file)
          continue

      # সাধারণ কথার জন্য জেমিনি দিয়ে উত্তর তৈরি করা
      prompt = (
          "তুমি একজন রিয়েল তরুণী মেয়ে (Samiya)। টেলিগ্রামে কেউ তোমাকে মেসেজ দিলে যেভাবে"
          f' একদম শর্ট, মিষ্টি ও প্রাকৃতিকভাবে বাংলায় চ্যাট করো, ঠিক সেভাবে উত্তর দাও। মেসেজটি হলো: "{user_text}"'
      )

      try:
        ai_response = await asyncio.to_thread(model.generate_content, prompt)
        reply_text = (
            ai_response.text.strip()
            if ai_response.text
            else "আচ্ছা, বিষয়টি বুঝতে পেরেছি।"
        )
      except Exception:
        reply_text = "উহু, এই মুহূর্তে একটু ব্যস্ত আছি।"

      # ভয়েস নোট তৈরি ও পাঠানো
      async with event.client.action(chat_id, "record-audio"):
        audio_file = await text_to_speech(reply_text)
        await asyncio.sleep(2)

      await event.respond(file=audio_file, voice_note=True)

      if os.path.exists(audio_file):
        os.remove(audio_file)

    except FloodWaitError as e:
      await asyncio.sleep(e.seconds)
    except Exception as e:
      print(print(f"Error: {e}"))
    finally:
      message_queue.task_done()

  is_processing = False


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_incoming_message(event):
  sender_id = event.sender_id
  chat_id = event.chat_id
  user_text = event.raw_text

  if not user_text:
    return

  # কিউ-তে মেসেজ যোগ করা (সিরিয়ালি উত্তর দেওয়ার জন্য)
  await message_queue.put((sender_id, event, user_text, chat_id))

  global is_processing
  if not is_processing:
    asyncio.create_task(process_queue())


def main():
  print("Samiya Userbot is starting with all features...")
  client.start()
  print("Samiya Userbot is Online and running!")
  client.run_until_disconnected()


if __name__ == "__main__":
  main()
