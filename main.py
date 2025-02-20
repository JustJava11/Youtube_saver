import logging
import os
import sys
import asyncio
import pytubefix
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

router = Router()

@router.message(Command('start'))
async def hello_handler(message: Message):
    username = message.from_user.username
    await message.answer_sticker('CAACAgIAAxkBAAEx70dntwZ5iIHXyUmoSRiS6_zCWcidCAACRRMAAmmvyUuppUmQogXywzYE')
    await message.answer(
f"""
Hello @{username}👋
I'm Youtube saver bot!
Send me link and i will send you video"""
    )

@router.message()
async def send_video_handler(message: Message):
    youtube_url = message.text.strip()

    # if 'youtube.com' not in youtube_url or "youtube.be" not in youtube_url:
    if "youtube.com" not in youtube_url and "youtu.be" not in youtube_url:
        await message.reply("This is not youtube link please send only youtube link!")
        return

    await message.answer('Video is downloading....')

    try:
        yt = pytubefix.YouTube(youtube_url)
        video_stream = yt.streams.get_highest_resolution()

        if not video_stream:
            await message.answer('unable to find video stream')
            return

        filename = f"{yt.title}.mp4"
        temp_file = video_stream.download(output_path='downloads', filename=filename)

        video_file = FSInputFile(temp_file)
        await message.answer('Video is downloaded! Sending file...')

        await message.answer_video(video_file)
        os.remove(temp_file)

    except Exception as e:
        await message.reply(f'Error with downloading{e}')

async def main():
    bot = Bot('TOKEN')
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())