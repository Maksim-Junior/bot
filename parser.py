import os
from dotenv import load_dotenv
from selenium import webdriver
from db import find_all_search, process_job

load_dotenv()
DRIVER_PATH = os.getenv('DRIVER_PATH')


class ParseJob:
    def __init__(self, url, bot=None):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        self.driver.minimize_window()
        self.url = url
        self.bot = bot

    def __del__(self):
        self.driver.close()

    async def parse(self):
        search_words = find_all_search()

        for page in range(9):
            print(self.url.format(page))
            self.driver.get(self.url.format(page))
            items = len(self.driver.find_elements_by_class_name("vacancy-serp"))
            for item in range(items):
                jobs = self.driver.find_elements_by_class_name("vacancy-serp-item")
                for job in jobs:
                    job_item = job.find_element_by_class_name("bloko-link")
                    job_title = job_item.text
                    job_href = job_item.get_attribute('href')
                    for search_word in search_words:
                        s_w = search_word.word.lower()
                        j_t = job_title.lower()
                        if j_t.find(s_w) >= 0:
                            await process_job(job_title, job_href, search_word.chatid, self.bot)

