import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import FSInputFile
import yt_dlp

TOKEN = "8422789528:AAF2TIqP_TzL5AcLGwUwj_hltNIyqc8catw"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Salom! Musiqa qidirish uchun qo'shiq nomi yoki ijrochini yozing.")

@dp.message()
async def search_and_send_music(message: types.Message):
    status_msg = await message.answer(f"🔍 <b>'{message.text}'</b> bo'yicha musiqa qidirilmoqda...", parse_mode="HTML")
    query = message.text
    filename = f"song_{message.from_user.id}"

    ydl_opts = {
        'format': 'm4a/bestaudio/best',
        'outtmpl': f'{filename}.%(ext)s',
        'quiet': True,
        'default_search': 'ytsearch1',
    }

    try:
        loop = asyncio.get_event_loop()
        
        def download():
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(query, download=True)
                if 'entries' in info and info['entries']:
                    return info['entries'][0]
                return info

        info = await loop.run_in_executor(None, download)
        
        downloaded_file = None
        for ext in ['m4a', 'mp3', 'webm', 'opus']:
            if os.path.exists(f"{filename}.{ext}"):
                downloaded_file = f"{filename}.{ext}"
                break

        if downloaded_file:
            title = info.get('title', 'Musiqa')
            audio = FSInputFile(downloaded_file)
            await message.answer_audio(audio, caption=f"🎵 <b>{title}</b>", parse_mode="HTML")
            os.remove(downloaded_file)
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Musiqa topilmadi.")

    except Exception as e:
        await status_msg.edit_text("❌ Musiqa yuklab olishda xatolik yuz berdi.")
        logging.error(f"Xato: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
