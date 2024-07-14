"""Database handler module"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import create_session


class DatabaseHandler:
    def __init__(self, host: str, port: int, user: str, password: str, db: str):
        self.engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))

        self.session = None

    def __enter__(self):
        self.session = create_session(self.engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def test_connect(self) -> list:
        return self.session.execute(text("SELECT 1;")).all()
