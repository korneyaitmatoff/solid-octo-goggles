from tests.helper import ParserApi, check_model, MangaModel, ChapterModel

from pytest import mark


class TestApi:

    def test_ping(self):
        response = ParserApi().ping()

        assert response.status_code == 200
        assert response.json()["data"]["response"] == "pong"

    @mark.parametrize(
        "manga",
        [
            "Берсерк",
            "Поднятие уровня в одиночку",
            "Ванпис",
            "Паразит",
            "Союз серокрылых",
        ]
    )
    def test_get_mangalist(self, manga: str):
        response = ParserApi().get_manga_list(title=manga)

        for item in response.json()['data']['data']:
            check_model(obj=item, model=MangaModel)

        assert response.status_code == 200

    @mark.parametrize(
        "manga_url",
        [
            "jujutsu-kaisen",
        ]
    )
    def test_get_manga_chapters(self, manga_url: str):
        response = ParserApi().get_manga_chapters(url=manga_url)
        data = response.json()["data"]["data"]

        assert response.status_code == 200

        for key in data:
            check_model(
                obj=data[key],
                model=ChapterModel
            )
