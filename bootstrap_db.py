"""Bootstrap module for build db tables"""
from database.handler import DatabaseHandler
from utilities.config import get_db_config
from database.tables import meta


def bootstrap():
    """Function for build tables"""

    with DatabaseHandler(**get_db_config()) as db:
        meta.create_all(db.engine)


if __name__ == '__main__':
    bootstrap()
