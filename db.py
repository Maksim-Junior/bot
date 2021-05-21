import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String
from aiogram import utils
from aiogram.types import ParseMode

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL, echo=True)
meta = MetaData()

job = Table(
    'Job',
    meta,
    Column('title', String(250), nullable=False),
    Column('url', String(250), nullable=False)
)

search_words: Table = Table(
    'SearchWords',
    meta,
    Column('word', String(250), nullable=False),
    Column('chatid', Integer(), nullable=False)
)

meta.create_all(engine)
conn = engine.connect()


def find_all_jobs():
    jobs = job.select()
    result = conn.execute(jobs)
    return result.all()


def find_id_search(chat_id):
    words = search_words.select().where(search_words.c.chatid == chat_id)
    result = conn.execute(words)
    return result.all()


def find_all_search():
    all_search = search_words.select()
    result = conn.execute(all_search)
    return result.all()


async def process_search(message):
    search_exist = True

    word = search_words.select().where(search_words.c.word == message.text, search_words.c.chatid == message.chat.id)
    result = conn.execute(word)

    list_result = []
    if result.all() == list_result:
        search_exist = False

    if search_exist:
        del_word = search_words.delete().where(search_words.c.word == message.text, search_words.c.chatid == message.chat.id)
        conn.execute(del_word)
        await message.answer(f'Строка поиска "{message.text}" удалена')
    elif not search_exist:
        insrt = search_words.insert().values(word=message.text, chatid=message.chat.id)
        conn.execute(insrt)
        await message.answer(f'Строка поиска "{message.text}" добавлена')
    else:
        await message.answer(f'Строка поиска "{message.text}" уже есть')

    return search_exist


async def process_job(title, url, chat_id, bot):
    job_exist = True

    some_job = job.select().where(job.c.title == title)
    result = conn.execute(some_job)

    list_result = []
    if result.all() == list_result:
        job_exist = False

    if not job_exist:
        rec = job.insert().values(title=title, url=url)
        conn.execute(rec)
        message_text = utils.markdown.hlink(title, url)
        await bot.send_message(chat_id=chat_id, text=message_text, parse_mode=ParseMode.HTML)

    return job_exist


