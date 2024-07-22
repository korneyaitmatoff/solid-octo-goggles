from sqlalchemy import VARCHAR, Column, ForeignKey, Integer, MetaData, Text

meta = MetaData()


class Manga(meta):
    __tablename__ = "manga"

    id = Column(Integer, primary_key=True)
    title = Column(VARCHAR)
    description = Text


class Chapter(meta):
    id = Column(Integer, primary_key=True)
    manga_id = Column(Integer, ForeignKey("manga.id"), nullable=False)
    name = Column(Text)
