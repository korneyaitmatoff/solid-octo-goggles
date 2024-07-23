from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import declarative_base

meta = declarative_base()


class Manga(meta):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR)
    url = Column(VARCHAR)


class Chapter(meta):
    __tablename__ = "chapters"
    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer, ForeignKey("manga.id"), nullable=False)
    url = Column(VARCHAR)


class Tasks(meta):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    name = Column(Text)
