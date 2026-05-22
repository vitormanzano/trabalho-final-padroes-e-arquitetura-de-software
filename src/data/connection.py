import oracledb

from src.config.settings import settings


class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
        return cls._instance

    def get_connection(self):
        if self._connection is None:
            self._connection = oracledb.connect(
                user="",
                password="",
                dsn=""
            )
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None
