"""Script for Mangalib scrabbing, info mining"""
import time
from dataclasses import dataclass
from typing import Any

from playwright.sync_api import sync_playwright


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

    def get_manga_list(self, keyword: str) -> list[dict[str, str]]:
        """Получение списка манги"""
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)

            self.context = browser.new_context()
            self.page = self.context.new_page()
            self.page.goto(f"https://mangalib.me/manga-list?sort=rate&dir=desc&page=1&name={keyword}&site_id=1")

            return [
                {
                    "url": item.get_attribute(name="href"),
                    "text": item.inner_text()
                } for item in self.page.query_selector_all(MangalibLocators.SEARCH_ELEMENT)
            ]

    def get_manga_info(self, url: str) -> dict[str, Any]:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)

            context = browser.new_context()
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
            browser = pw.chromium.launch(headless=False)

            context = browser.new_context()
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

    print(MangalibParser().get_chapters(url='https://mangalib.me/netoroplivyy-fermer-v-drugom-mire'))
