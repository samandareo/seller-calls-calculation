import asyncio
import logging
import sys
from os import getenv
import get_data as gd
import pytz

from aiogram import Bot, Dispatcher, Router, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = "7149543830:AAFl1ZLv4DYr9Z0reu-7j0sdeg8_oqS_ENY"

dp = Dispatcher()
scheduler = AsyncIOScheduler()
SUPER_ADMIN = 895775406
ADMIN = [180519876, 895775406]

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(message.from_user.id)
    if message.from_user.id in ADMIN:
        await message.reply(f"Salom, {hbold(message.from_user.full_name)}!\nBugungi qo'ng'iroqlar haqida umumiy ma'lumot olishingiz mumkin! \n\nMa'lumot olish uchun: /calls")
    else:
        await message.reply("Afsuski siz botdan foydalana olmaysiz😔!")



@dp.message()
async def command_handler(message: types.Message) -> None:
    if message.from_user.id in ADMIN:
        if message.text == "/calls":
            sent_msg =await message.reply("Biroz kuting...")
            gd.main()
            str = f"☎️<b>Qo'ng'iroqlar</b>\n\n{gd.result()}"
            await sent_msg.edit_text(str, parse_mode=ParseMode.HTML)
    else:
        await message.reply("Afsuski siz botdan foydalana olmaysiz😔!")



async def scheduled_message():
    gd.main()
    text = f'Bugungi qo\'ng\'iroqlar bo\'yicha ma\'lumot🧾\n\n{gd.result(gd.seller_azizxon,gd.seller_asal,gd.sel)}'
    for user_id in ADMIN:
        await Bot(token=TOKEN).send_message(chat_id=user_id, text=text, parse_mode=ParseMode.HTML)


scheduler.configure(timezone=pytz.timezone('Asia/Tashkent'))
scheduler.add_job(scheduled_message, 'cron', hour=20)
scheduler.start()

async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())