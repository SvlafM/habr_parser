import asyncio
import logging

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

from parser.parser import get_task

bot = Bot('вставить_токен_бота')
dp = Dispatcher()

task = ''
cur_users = list()


def update_task(new_value):
    global task
    task = new_value
    return task


async def on_shutdown():
    for user in cur_users:
        try:
            await bot.send_message(user, 'Бот упал, пиздец')
        except Exception as ex_:
            logging.error(f'Error: {ex_}\nMessage can\'t be received to user {user}')
            continue
    await dp.stop_polling()


@dp.message(Command('start'))
async def start_cmd(message: types.Message):
    await message.answer('''==РАБОТАЕМ==''')
    cur_users.append(message.chat.id)
    await message.answer(task, disable_web_page_preview=True)


async def start_monitoring():
    while True:
        await asyncio.sleep(0.1)
        new_task = await get_task()
        if new_task:
            update_task(new_task)
            for user in cur_users:
                try:
                    await bot.send_message(user, task, disable_web_page_preview=True)
                except Exception as ex_:
                    logging.error(f'Error: {ex_}\nMessage can\'t be received to user {user}')
                    continue
        else:
            pass


async def main():
    try:
        await asyncio.gather(dp.start_polling(bot),
                             start_monitoring())
    except Exception as ex_:
        logging.error(f'Бот упал с такой ошибкой: {repr(ex_)}')
        await on_shutdown()


if __name__ == '__main__':
    asyncio.run(main())

