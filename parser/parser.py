import time

from playwright.sync_api import sync_playwright, Page, expect


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
                } for item in self.page.query_selector_all("a[class='media-card']")
            ]

    def get_manga_info(self, url: str):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)

            context = browser.new_context()
            page = context.new_page()
            page.goto(url)

            return {
                "info": [
                    {
                        item.inner_text().split(sep="\n")[0]: item.inner_text().split(sep="\n")[1]
                    } for item in page.query_selector_all("a[class='media-info-list__item']")
                ],
                "genres": [
                    item.inner_text() for item in page.query_selector_all("a[class='media-tag-item ']")
                ]
            }

    def get_chapters(self, url: str):
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=False)

            context = browser.new_context()
            page = context.new_page()
            page.goto(url)

            page.query_selector("li[data-key='chapters']").click()

            chapters = []

            for i in range(100):  # make the range as long as needed
                page.mouse.wheel(0, 500)
                time.sleep(0.3)

                chapters += page.query_selector_all("div[class='media-chapter']")

            chapters = list(set(chapters))

            ...


if __name__ == "__main__":
    print(MangalibParser().get_chapters(url='https://mangalib.me/one-piece'))
