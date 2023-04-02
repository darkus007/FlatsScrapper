"""
Модуль для работы с базой данных PostageSQL.

"""

from typing import Dict

import psycopg2
from config import DB_USER, DB_PASS, DB_NAME, DB_PORT, DB_HOST

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

connect = psycopg2.connect(DATABASE_URL)


def create_db() -> None:
    """
    Создает базу данных и таблицы в ней,
    если база и таблицы уже существуют,
    то ничего не делает.
    """
    with connect.cursor() as cursor:
        with open('database/createdb.sql', 'r') as file:
            sql = file.read()
        cursor.execute(sql)
        connect.commit()


def drop(*table_names: str) -> None:
    """ Очищает таблицы в базе данных. """
    for table in table_names:
        with connect.cursor() as cursor:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            connect.commit()


def insert(table: str, data: Dict) -> None:
    """
    Добавляет запись в базу данных.

    :param table: Название таблицы.
    :param data: Словарь для записи,
                где ключ - поле таблицы,
                а значение - данные для записи.
    :return: None.
    """
    columns = ', '.join(data.keys())
    values = tuple(data.values())
    query = str(f"INSERT INTO {table} ({columns}) VALUES {values} ON CONFLICT ({tuple(data.keys())[0]}) DO NOTHING;")
    query = query.replace('None', 'NULL')
    cursor = connect.cursor()
    try:
        cursor.execute(query)
        connect.commit()
    except Exception as ex:
        # в случае, если такая запись уже есть, пропускаем
        print(f"Ошибка при записи в БД: {ex}")
        connect.rollback()
    finally:
        cursor.close()


def insert_price(table: str, data: Dict) -> None:
    """
    Добавляет запись в базу данных.

    :param table: Название таблицы.
    :param data: Словарь для записи,
                где ключ - поле таблицы,
                а значение - данные для записи.
    :return: None.
    """
    cursor = connect.cursor()
    query_get = f"SELECT prices.flat_id, prices.price, prices.booking_status " \
                f"FROM prices " \
                f"INNER JOIN (" \
                f"SELECT flat_id, max(data_created) AS max_data " \
                f"FROM prices " \
                f"GROUP BY flat_id) AS last_price ON last_price.flat_id = prices.flat_id " \
                f"WHERE prices.data_created = last_price.max_data AND prices.flat_id = {data['flat_id']};"
    cursor.execute(query_get)
    last_exist = cursor.fetchone()

    if not (last_exist[1] == data['price'] and last_exist[2] == data['booking_status']):
        columns = ', '.join(data.keys())
        values = tuple(data.values())
        query = str(f"INSERT INTO {table} ({columns}) VALUES {values};")
        query = query.replace('None', 'NULL')
        try:
            cursor.execute(query)
            connect.commit()
        except Exception as ex:
            # в случае, чего-то непредвиденного
            print(f"Ошибка при записи в БД: {ex}")
            connect.rollback()
        finally:
            cursor.close()


def fetch(table: str, columns: list[str]) -> list[tuple | None]:
    """
    Возвращает результаты из одной таблицы базы данных.

    :param table: Название таблицы.
    :param columns: Список с полями таблицы.
    :return: Список кортежей.
    """
    columns_joined = ", ".join(columns)
    with connect.cursor() as cursor:
        cursor.execute(f"SELECT {columns_joined} FROM {table}")
        return cursor.fetchall()


def execute_sql_fetch(sql: str) -> list[tuple | None]:
    """
    Выполняет sql запрос и возвращает результат.

    :param sql: SQL запрос.
    :return: Список кортежей или пустой список.
    """
    with connect.cursor() as cursor:
        cursor.execute(sql)
        return cursor.fetchall()


def execute_sql(sql: str) -> None:
    """
    Выполняет sql команду.

    :param sql: SQL запрос.
    :return: None.
    """
    with connect.cursor() as cursor:
        cursor.execute(sql)
        connect.commit()
