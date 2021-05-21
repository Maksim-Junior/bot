import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, executor, types, utils
from aiogram.types import ParseMode
from dotenv import load_dotenv
from db import process_search, find_id_search, find_all_jobs
from parser import ParseJob

logging.basicConfig(level=logging.INFO)

load_dotenv()
TOKEN = os.getenv("TOKEN")
URL = os.getenv("URL")
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def send_search(message: types.Message):
    text = 'Телеграм бот для поиска вакансий "python developer" на jobs.tut.by. \r\n\n' \
           '/search - выводит список ключевых слов поиска. \r\n ' \
           '/list - выводит список вакансий по ключевым словам поиска.\r\n\n' \
           'При отправке любого сообщения боту(python, developer),' \
           ' это сообщение сохранится как ключевое слово поиска. \r\n' \
           'При повторной отправке такого же сообщения, ключевое слово удаляется из списка.\r\n\n' \
           'При добавлении новой вакансии на сайте, подходящей по ключевым словам поиска, бот пришлет эту вакансию.'
    await message.answer(text=text)


@dp.message_handler(commands='list')
async def send_list(message: types.Message):
    search_words = find_id_search(message.chat.id)
    jobs = find_all_jobs()
    for job in jobs:
        job_title = job.title
        for word in search_words:
            search_word = word.word.lower()
            j_t = job_title.lower()
            if j_t.find(search_word) >= 0:
                message_text = f'Строка поиска {search_word} \r\n Найдено {utils.markdown.hlink(job_title, job.url)}'

                await message.answer(text=message_text, parse_mode=ParseMode.HTML)


@dp.message_handler(commands='search')
async def send_search(message: types.Message):
    search_words = find_id_search(message.chat.id)
    await message.answer(text="Строки для поиска:")
    for word in search_words:
        await message.answer(text=word.word)


@dp.message_handler()
async def echo(message: types.Message):
    await process_search(message)


async def scheduled(wait_for, parser):
    while True:
        await asyncio.sleep(wait_for)
        await parser.parse()
        pass


if __name__ == "__main__":
    parser = ParseJob(url=URL, bot=bot)
    loop = asyncio.get_event_loop()
    loop.create_task(scheduled(300, parser))
    executor.start_polling(dp, skip_updates=True)
