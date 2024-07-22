from fastapi import FastAPI

from database.handler import DatabaseHandler
from models.response import Response
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


@app.get("/check_config")
def check_config():
    return Response(
        status_code=200,
        data={
            "response": get_db_config()
        }
    )
