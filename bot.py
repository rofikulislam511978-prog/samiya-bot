import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

# টেলিগ্রাম বটের নতুন টোকেন
TOKEN = "8928921868:AAGLjBuVxwE0yR7Akpi1ghjTa7jfAVy1UdY"

# লগিং সেটআপ
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Render-এর পোর্ট স্ক্যানার শান্ত রাখতে একটি মিনি ডামি সার্ভার (ফেক ওয়েব সার্ভার)
class DummyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_dummy_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), DummyHandler)
    logger.info(f"Dummy web server running on port {port}")
    server.serve_forever()

# মেসেজ হ্যান্ডলার (কেউ মেসেজ দিলে এটি কাজ করবে)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    chat_id = update.message.chat_id
    
    # ইউজারকে রিপ্লাই দেওয়ার কোড এখানে লিখতে পারেন
    logger.info(f"Received message: {user_message} from chat ID: {chat_id}")
    await context.bot.send_message(chat_id=chat_id, id=update.message.message_id, text="আপনার মেসেজটি পেয়েছি!")

def main():
    # ব্যাকগ্রাউন্ডে ডামি সার্ভার চালু করার জন্য থ্রেড শুরু করা হলো
    server_thread = threading.Thread(target=run_dummy_server, daemon=True)
    server_thread.start()

    # টেলিগ্রাম বট অ্যাপ্লিকেশন তৈরি
    application = ApplicationBuilder().token(TOKEN).build()

    # সমস্ত টেক্সট মেসেজ হ্যান্ডেল করার জন্য হ্যান্ডলার যোগ করা হলো
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # বট চালু করা হচ্ছে
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
