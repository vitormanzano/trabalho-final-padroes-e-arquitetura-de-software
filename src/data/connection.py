import psycopg2

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
            self._connection = psycopg2.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                dbname=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
        return self._connection

    def close(self):
        if self._connection is not None:
            self._connection.close()
            self._connection = None


def conectar_banco():
    """Retorna a conexão única com o banco (Singleton DatabaseConnection)."""
    return DatabaseConnection().get_connection()
