import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import yt_dlp

# 1. Render uchun veb-server (Bot o'chib qolmasligi uchun)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

# Veb-serverni fonda ishga tushiramiz
threading.Thread(target=run_server, daemon=True).start()

# 2. Bot sozlamalari
TOKEN = "8422789528:AAF2TIqP_TzL5AcLGwUwj_hltNIyqc8catw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Start komandasi
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Salom! Musiqa botiga xush kelibsiz.")

# Botni ishga tushirish
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

