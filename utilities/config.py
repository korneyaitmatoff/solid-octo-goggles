from os import environ
from typing import Any


def get_db_config() -> dict[str, Any]:
    return {
        "host": environ['POSTGRES_HOST'],
        "port": environ['POSTGRES_PORT'],
        "user": environ['POSTGRES_USER'],
        "password": environ['POSTGRES_PASSWORD'],
        "db": environ['POSTGRES_DB'],
    }
