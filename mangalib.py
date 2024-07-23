"""Script for Mangalib scrabbing, info mining"""
import time
from dataclasses import dataclass
from typing import Any

from playwright.sync_api import sync_playwright

from database.handler import DatabaseHandler
from database import tables
from utilities.config import get_db_config


@dataclass(frozen=True)
class MangalibLocators:
    DOWNLOAD_BUTTON = "div[class='media-chapter__icon media-chapter__icon_download tooltip']"
    SEARCH_ELEMENT = "a[class='media-card']"
    INFO_BLOCK = "a[class='media-info-list__item']"
    GENRE_TAG_BLOCK = "a[class='media-tag-item ']"
    CHAPTER_BLOCK = "div[class='media-chapter__body']"
    SHOW_CHAPTERS_BUTTON = "li[data-key='chapters']"
    CHAPTER_LINK = "a[class='link-default']"


class MangalibParser:
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)" \
         " Chrome/116.0.0.0 Safari/537.36 Edg/116.0.1938.81"

    def get_manga_list(self, keyword: str) -> list[dict[str, str]]:
        """Получение списка манги"""
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)

            self.context = browser.new_context(user_agent=self.UA)
            self.page = self.context.new_page()
            self.page.goto(f"https://mangalib.me/manga-list?sort=rate&dir=desc&page=1&name={keyword}&site_id=1")

            return [
                {
                    "url": item.get_attribute(name="href"),
                    "title": item.inner_text()
                } for item in self.page.query_selector_all(MangalibLocators.SEARCH_ELEMENT)
            ]

    def get_manga_info(self, url: str) -> dict[str, Any]:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)

            context = browser.new_context(user_agent=self.UA)
            page = context.new_page()
            page.goto(url)

            return {
                "info": [
                    {
                        item.inner_text().split(sep="\n")[0]: item.inner_text().split(sep="\n")[1]
                    } for item in page.query_selector_all(MangalibLocators.INFO_BLOCK)
                ],
                "genres": [
                    item.inner_text() for item in page.query_selector_all(MangalibLocators.GENRE_TAG_BLOCK)
                ]
            }

    def get_chapters(self, url: str):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)

            context = browser.new_context(user_agent=self.UA)
            page = context.new_page()
            page.goto(url)

            page.query_selector(MangalibLocators.SHOW_CHAPTERS_BUTTON).click()

            chapters = {}

            for i in range(100):
                for chapter in page.query_selector_all(MangalibLocators.CHAPTER_BLOCK):
                    chapters[chapter.inner_text()] = chapter. \
                        query_selector(MangalibLocators.CHAPTER_LINK).get_attribute("href")

                time.sleep(0.2)
                page.mouse.wheel(0, 500)

            return chapters


if __name__ == "__main__":
    def get_tasks() -> list[Any]:
        """Function for get tasks from db"""

        with DatabaseHandler(**get_db_config()) as db:
            return [data for data in db.select(tables.Tasks)]


    def delete_task(id: int):
        """Delete task from DB"""
        with DatabaseHandler(**get_db_config()) as db:
            return db.delete(table=tables.Tasks, filters=(tables.Tasks.id == id,))


    def add_manga(data: dict[Any, Any]):
        """Add manga to DB"""
        with DatabaseHandler(**get_db_config()) as db:
            db.insert(table=tables.Manga, data=data)


    for task in get_tasks():
        for data in MangalibParser().get_manga_list(keyword=task.name):
            add_manga(data)

        delete_task(id=task.id)
