import psycopg2
from psycopg2 import OperationalError


def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Создает и возвращает соединение с базой данных PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Соединение с PostgreSQL установлено.")
    except OperationalError as e:
        print(f"Ошибка при подключении: {e}")
    return conn


def execute_query(connection, query, params=None):
    """Выполняет SQL-запрос."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        connection.commit()
        print("Запрос выполнен успешно.")
        return cursor
    except OperationalError as e:
        print(f"Ошибка при выполнении запроса: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()


def fetch_data(connection, query, params=None):
    """Выполняет запрос и возвращает результат."""
    cursor = connection.cursor()
    try:
        cursor.execute(query, params or ())
        return cursor
    except OperationalError as e:
        print(f"Ошибка при получении данных: {e}")
        return None
