"""Database handler module"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import create_session


class DatabaseHandler:
    def __init__(
            self,
            host: str = "localhost",
            port: str = "5432",
            user: str = "postgres",
            password: str = "postgres",
            db: str = "storage"
    ):
        self.engine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(user, password, host, port, db))

        self.session = None

    def __enter__(self):
        self.session = create_session(self.engine)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

    def test_connect(self) -> list:
        """Function for check connection with database"""
        return self.session.execute(text("SELECT 1;")).all()

    def execute_sql(self, sql: text):
        """Function for execute sql script"""
        return self.session.execute(sql)

    def select(self, table):
        """Function for execute select query"""
        return self.session.query(table).all()

    def delete(self, table, filters):
        """Function for delete rows by filters"""
        self.session.query(table).filter(*filters).delete()
        self.session.commit()

    def insert(self, table, data):
        """Function for insert data into table"""
        new_record = table(**data)

        self.session.add(new_record)
        self.session.commit()
        self.session.refresh(new_record)
