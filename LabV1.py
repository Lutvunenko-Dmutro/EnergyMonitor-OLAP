import os
import asyncio
import logging
import tempfile
from functools import partial
import aiohttp
import sys

from aiogram import Bot, Dispatcher, types, executor
from yt_dlp import YoutubeDL

# Налаштування логування
logging.basicConfig(level=logging.INFO)

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Не задано дійсний токен! Переконайтеся, що встановлена змінна оточення API_TOKEN.")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

def download_tiktok_video(url: str) -> str:
    """Завантажує відео з TikTok за допомогою yt-dlp у тимчасову папку."""
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, 'tiktok_video.%(ext)s')
    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'format': 'mp4',
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        logging.info(f"Відео завантажено: {filename}")
    return filename

async def async_download_tiktok_video(url: str) -> str:
    """Асинхронне завантаження відео."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(download_tiktok_video, url))

async def delete_file_after_delay(filepath: str, delay: float = 60):
    """Видаляє файл через delay секунд після виклику."""
    await asyncio.sleep(delay)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.info(f"Файл видалено: {filepath}")
        else:
            logging.warning(f"Файл для видалення не знайдено: {filepath}")
    except Exception as e:
        logging.error(f"Помилка видалення файлу {filepath}: {e}")

async def resolve_tiktok_redirect(url: str) -> str:
    """Розпаковує коротке TikTok-посилання (vm.tiktok.com) до повного."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True) as resp:
            return str(resp.url)

@dp.message_handler()
async def handle_message(message: types.Message):
    if not message.text:
        return

    url = message.text.strip()
    is_tiktok = "tiktok" in url.lower()
    is_tiktok_photo = ("/photo/" in url.lower()) or ("aweme_type=150" in url.lower())

    if url.startswith("https://vm.tiktok.com/"):
        url = await resolve_tiktok_redirect(url)
        is_tiktok = "tiktok" in url.lower()
        is_tiktok_photo = ("/photo/" in url.lower()) or ("aweme_type=150" in url.lower())

    if is_tiktok_photo:
        await message.reply("Це TikTok-фото, але бот не підтримує завантаження TikTok-фото напряму.")
        return

    if is_tiktok:
        await message.reply("Обробляю твоє посилання, зачекай трохи...")
        try:
            video_path = await async_download_tiktok_video(url)
            with open(video_path, 'rb') as video_file:
                await bot.send_video(chat_id=message.chat.id, video=video_file)
            asyncio.create_task(delete_file_after_delay(video_path, delay=60))
        except Exception as e:
            logging.error(f"Помилка обробки посилання {url}: {e}")
            await message.reply("Виникла помилка при завантаженні відео. Спробуй пізніше.")
        return

if __name__ == '__main__':
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as e:
        logging.error(f"Несподівана помилка головного циклу: {e}", exc_info=True)
        sys.exit(1)