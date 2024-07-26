from fastapi import FastAPI

from database.handler import DatabaseHandler
from models.response import Response
from parsers.mangalib import MangalibParser
from utilities.config import get_db_config

app = FastAPI()


@app.get('/ping')
def ping():
    return Response(
        status_code=200,
        data={
            "response": "pong"
        }
    )


@app.get("/ping_db")
def check_database():
    with DatabaseHandler(**get_db_config()) as db:
        return Response(
            status_code=200,
            data={
                "response": str(db.test_connect())
            }
        )


@app.get("/get_manga_list/{manga_title}")
def get_manga_list(title: str):
    return Response(
        status_code=200,
        data={
            "data": MangalibParser().get_manga_list(keyword=title)
        }
    )


@app.get("/get_manga_chapters/{url}")
def get_manga_chapters(url: str):
    try:
        return Response(
            status_code=200,
            data={
                "data": MangalibParser().get_chapters(path=url)
            }
        )
    except Exception as e:
        return Response(
            status_code=500,
            data=e
        )


@app.get("/get_translators/{url}")
def get_manga_translators(url: str):
    return Response(
        status_code=200,
        data={
            "data": MangalibParser().get_translators(path=url)
        }
    )
