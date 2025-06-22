import os
import sys
import asyncio
import logging
import tempfile
from functools import partial
from dotenv import load_dotenv  # додати цей імпорт
import requests
import functools

from yt_dlp import YoutubeDL

# Налаштування логування
logging.basicConfig(level=logging.INFO)

load_dotenv()  # додати цей виклик перед отриманням API_TOKEN

API_TOKEN = os.getenv("API_TOKEN")
if not API_TOKEN:
    raise ValueError("Не задано дійсний токен! Переконайтеся, що встановлена змінна оточення API_TOKEN.")

BASE_URL = f"https://api.telegram.org/bot{API_TOKEN}"

def download_tiktok_video(url: str) -> str:
    temp_dir = tempfile.gettempdir()
    output_template = os.path.join(temp_dir, 'tiktok_video.%(ext)s')
    ydl_opts = {
        'outtmpl': output_template,
        'quiet': True,
        'format': 'mp4',
        # 'force_generic_extractor': True  # Цей параметр не допомагає для TikTok, можна прибрати
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            logging.info(f"Відео завантажено: {filename}")
        return filename
    except Exception as e:
        logging.error(f"YT-DLP TikTok error: {e}")
        raise RuntimeError(
            "Не вдалося завантажити відео з TikTok. "
            "Можливо, TikTok змінив захист або yt-dlp ще не підтримує цей формат. "
            "Оновіть yt-dlp (pip install -U yt-dlp) або спробуйте інший сервіс."
        ) from e

async def async_download_tiktok_video(url: str) -> str:
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, partial(download_tiktok_video, url))

async def delete_file_after_delay(filepath: str, delay: float = 60):
    await asyncio.sleep(delay)
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            logging.info(f"Файл видалено: {filepath}")
        else:
            logging.warning(f"Файл для видалення не знайдено: {filepath}")
    except Exception as e:
        logging.error(f"Помилка видалення файлу {filepath}: {e}")

async def run_in_executor(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))

async def send_message(chat_id, text):
    await run_in_executor(requests.post, f"{BASE_URL}/sendMessage", json={
        "chat_id": chat_id,
        "text": text
    })

async def send_video(chat_id, file_path):
    def _send_video():
        with open(file_path, 'rb') as f:
            files = {'video': (os.path.basename(file_path), f)}
            data = {'chat_id': chat_id}
            requests.post(f"{BASE_URL}/sendVideo", data=data, files=files)
    await run_in_executor(_send_video)

def resolve_tiktok_redirect(url: str) -> str:
    resp = requests.get(url, allow_redirects=True, timeout=10)
    return resp.url

async def get_last_update_id():
    def _get():
        resp = requests.get(f"{BASE_URL}/getUpdates", params={"limit": 1, "timeout": 0})
        data = resp.json()
        results = data.get("result", [])
        if results:
            return results[-1]["update_id"] + 1
        return None
    return await run_in_executor(_get)

async def poll_updates():
    offset = await get_last_update_id()
    while True:
        def _get_updates(current_offset):
            params = {"timeout": 30}
            if current_offset is not None:
                params["offset"] = current_offset
            resp = requests.get(f"{BASE_URL}/getUpdates", params=params)
            return resp.json()
        data = await run_in_executor(_get_updates, offset)
        for update in data.get("result", []):
            offset = update["update_id"] + 1
            await handle_update(update)

async def handle_update(update):
    if 'message' not in update or 'text' not in update['message']:
        return

    chat_id = update['message']['chat']['id']
    url = update['message']['text'].strip()

    if url.startswith("https://vm.tiktok.com/"):
        url = await asyncio.get_running_loop().run_in_executor(None, resolve_tiktok_redirect, url)

    if "tiktok" not in url.lower() or "/photo/" in url.lower() or "aweme_type=150" in url.lower():
        return

    await send_message(chat_id, "Обробляю твоє посилання, зачекай трохи...")

    try:
        video_path = await async_download_tiktok_video(url)
        await send_video(chat_id, video_path)
        asyncio.create_task(delete_file_after_delay(video_path, delay=60))
    except Exception as e:
        logging.error(f"Помилка: {e}")
        await send_message(chat_id, "Виникла помилка при завантаженні відео. Спробуй пізніше.")

if __name__ == '__main__':
    try:
        asyncio.run(poll_updates())
    except Exception as e:
        logging.error(f"Несподівана помилка головного циклу: {e}", exc_info=True)
        sys.exit(1)