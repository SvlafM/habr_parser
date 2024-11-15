import asyncio
import logging

import aiohttp
from utils.utils import URL
from bs4 import BeautifulSoup

last_task = ''


async def task_scheme(raw_task):
    title = raw_task.find('div', class_='task__title').get('title')
    try:
        price = raw_task.find('span', class_='count').text
    except AttributeError:
        price = raw_task.find('span', class_='negotiated_price').text
    link = raw_task.find('a').get('href').replace('/tasks', '')
    return '''
{}
Цена: {}
Ссылка: {}'''.format(title, price, f'{URL}{link}')


async def get_html():
    try:
        for i in range(3):
            async with aiohttp.ClientSession() as session:
                response = await session.get(URL)
                return await response.text(encoding='utf-8')
    except Exception as ex_:
        logging.error(f'Ошибка с получением макета страницы: {repr(ex_)}\n Повторный запрос.')
        await asyncio.sleep(5)
        pass
    else:
        raise AssertionError('Не удалось получить макет страницы')


async def get_task():
    global last_task
    await asyncio.sleep(10)
    soup = BeautifulSoup(await get_html(), 'html.parser')
    raw_task = soup.find('article', class_='task task_list')
    newest_task = await task_scheme(raw_task)
    if last_task != newest_task:
        last_task = newest_task
        return newest_task
    else:
        return None

