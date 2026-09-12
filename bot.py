import asyncio
import os
import random
import edge_tts
import google.generativeai as genai
from telethon import TelegramClient, events
from telethon.sessions import StringSession

# ক্রেডেন্সিয়ালস
API_ID = 38710926
API_HASH = "9047aad732a7b1793fcd1857c56d7d3f"

# সেশন স্ট্রিংয়ের শেষের প্যাডিং বা সমান চিহ্ন (=) ত্রুটি এড়াতে ফিক্সড ফরম্যাট
raw_session = "1BVtsOHsBu3KiEn8jeyhzUXzezWrOpBBb0MwdRHI_oLamWaFNonkk9JkQ0008nheuaVmIQb146LF6xJtJ1FDqh2A_58-y_28NIOH4a15wqkyQdegTbvHMCzwoMdIXEWZfNfnBAquwVCbSVBrJKVHJxzz60dfvowHMC8fu_Choak6CvX1aEQN6LyFVZwyiueCpHT3vijFtZ8mSxm70qmz6rwin63YJW3SzXKDZLAjZxKhGi44vVRyUDMRM-aTDs3U11QiKUffUMvaXsC-KBXZ456uPk0NPPqhnKeYc1mia4g1Ih00zpkUfMaRJw5CRqfxA84pnNM0FBD12_A-yB9gxid40oQ="
padding_fix = len(raw_session) % 4
if padding_fix > 0:
  raw_session += "=" * (4 - padding_fix)

SESSION_STRING = raw_session

# জেমিনি এআই কনফিগারেশন
GEMINI_API_KEY = "AQ.Ab8RN6JnYVG6Z7yf_OybQ79MyRrTbnonv4c50z--l21ITRfhew"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# মাইক্রোসফটের ন্যাচারাল মেয়ে মানুষের কন্ঠের ভয়েস
VOICE_NAME = "bn-BD-NabanitaNeural"

# ইউজারদের স্টেট ট্র্যাকিং ডিকশনারি
user_states = {}

# সিরিয়াল বা কিউ (Queue) ম্যানেজ করার সিস্টেম
message_queue = asyncio.Queue()

# টেলিথন ক্লাইন্ট ইনিশিয়ালাইজেশন
client = TelegramClient(
    StringSession(SESSION_STRING), API_ID, API_HASH, connection_retries=None
)


# ব্যাকগ্রাউন্ডে সিরিয়াল অনুযায়ী প্রসেস করার ফাংশন
async def process_queue():
  while True:
    event, user_text, chat_id = await message_queue.get()
    try:
      delay = random.uniform(12, 18)
      await asyncio.sleep(delay)

      text_lower = user_text.lower()

      if "পেমেন্ট" in text_lower or "বিকাশ" in text_lower or "নগদ" in text_lower:
        payment_reply = (
            "পেমেন্ট করার জন্য আমাদের বিকাশ ও নগদ নম্বর:\n"
            "💳 বিকাশ / নগদ: `01346133685`\n\n"
            "টাকা পাঠিয়ে স্ক্রিনশট দিন।"
        )
        await event.respond(payment_reply, parse_mode="md")
        message_queue.task_done()
        continue

      if chat_id not in user_states:
        if (
            "সার্ভিস" in text_lower
            or "service" in text_lower
            or "servis" in text_lower
        ):
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
          await event.respond(service_text)
          message_queue.task_done()
          continue

        elif (
            "গ্রুপ" in text_lower
            or "group" in text_lower
            or "gruf" in text_lower
        ):
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
          await event.respond(group_text)
          message_queue.task_done()
          continue
        else:
          intro_reply = (
              "স্বাগতম! আপনার কি লাগবে?\n\n১. **সার্ভিস** (কল বা চ্যাট)\n২."
              " **গ্রুপ** (লিস্ট দেখতে চান)\n\nদয়া করে লিখে জানান আপনার কোনটি লাগবে।"
          )
          await event.respond(intro_reply, parse_mode="md")
          message_queue.task_done()
          continue

      prompt = (
          "তুমি একজন রিয়েল তরুণী মেয়ে (Samiya)। টেলিগ্রামে কেউ তোমাকে মেসেজ দিলে"
          f' যেভাবে একদম শর্ট, মিষ্টি ও প্রাকৃতিকভাবে বাংলায় চ্যাট করো, ঠিক সেভাবে'
          f' উত্তর দাও। মেসেজটি হলো: "{user_text}"'
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

      audio_path = f"voice_{chat_id}.mp3"

      try:
        communicate = edge_tts.Communicate(reply_text, VOICE_NAME)
        await communicate.save(audio_path)
        await event.respond(file=audio_path, voice_note=True)
      except Exception:
        await event.respond(reply_text)
      finally:
        if os.path.exists(audio_path):
          os.remove(audio_path)

    except Exception as e:
      print(f"ত্রুটি: {e}")
    finally:
      message_queue.task_done()


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_userbot_message(event):
  chat_id = event.sender_id
  user_text = event.raw_text

  if not user_text:
    return

  await message_queue.put((event, user_text, chat_id))


async def main():
  print("Samiya Smart Userbot চালু হচ্ছে...")
  asyncio.create_task(process_queue())
  await client.start()
  print("বট সফলভাবে রান করছে!")
  await client.run_until_disconnected()


if __name__ == "__main__":
  asyncio.run(main())
