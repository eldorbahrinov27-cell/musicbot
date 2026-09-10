import os
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import yt_dlp

# Render uchun veb-server
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running successfully!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    server.serve_forever()

threading.Thread(target=run_server, daemon=True).start()

# Tokenni Render xotirasidan o'qiymiz
TOKEN = os.environ.get("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Salom! Menga istalgan qo'shiq nomini yuboring, men uni YouTube'dan topib yuklab beraman! 🎵")

@dp.message()
async def send_music(message: types.Message):
    query = message.text
    if not query:
        return
        
    wait_msg = await message.answer("🔍 Qidirilmoqda va yuklab olinmoqda, biroz kuting...")
    
    ydl_opts = {
        'format': 'bestaudio',
        'outtmpl': 'downloaded_song.%(ext)s',
        'quiet': True,
        'extractor_args': {'youtube': {'player_client': ['android']}},
    }
    
    try:
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(f"ytsearch1:{query}", download=True)
                filename = ydl.prepare_filename(info)
                return filename

        loop = asyncio.get_running_loop()
        file_path = await loop.run_in_executor(None, download)
        
        if os.path.exists(file_path):
            audio = FSInputFile(file_path)
            await message.answer_audio(audio)
            try:
                await bot.delete_message(chat_id=message.chat.id, message_id=wait_msg.message_id)
            except:
                pass
            os.remove(file_path)
        else:
            await message.answer("Kechirasiz, bu qo'shiqni topib bo'lmadi.")
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



