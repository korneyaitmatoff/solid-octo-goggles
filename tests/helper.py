"""модуль вспомогательных классов и функций"""

from dataclasses import dataclass
from requests import session


@dataclass(frozen=True)
class MangaModel:
    url: str
    title: str


@dataclass(frozen=True)
class ChapterModel:
    link: str
    name: str


def check_model(obj, model):
    try:
        model(**obj)
    except Exception as e:
        raise e


class ParserApi:
    def __init__(self, url: str = "http://127.0.0.1", port: str = 8000):
        self.url = f"{url}:{port}"

    def ping(self):
        return session().get(f"{self.url}/ping")

    def check_database(self): ...

    def get_manga_list(self, title: str):
        return session().get(f"{self.url}/get_manga_list/{title}")

    def get_manga_chapters(self, url: str):
        return session().get(f"{self.url}/get_manga_chapters/{url}")
