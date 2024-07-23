"""Bootstrap module for build db tables"""
from sqlalchemy import text

from database.handler import DatabaseHandler
from utilities.config import get_db_config


def bootstrap():
    """Function for build tables"""

    def read_sql(sql_name: str) -> text:
        """Function for read file.sql"""
        with open(f"sql/{sql_name}") as f:
            res = text(f.read())

            f.close()

            return res

    with DatabaseHandler(**get_db_config()) as db:
        db.execute_sql(sql=read_sql("create_table_manga.sql"))
        db.execute_sql(sql=read_sql("create_table_chapters.sql"))
        db.execute_sql(sql=read_sql("create_table_tasks.sql"))


if __name__ == '__main__':
    print(bootstrap())
