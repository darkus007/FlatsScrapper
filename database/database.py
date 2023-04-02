"""
Модуль для работы с выбранной базой данных.

В текущей реализации PostgreSQL.
"""

import dataclasses

from logger import init_logger
from .db_postgresql import *
from scrapper.data_classes import Project, Flat, Price

from config import LOGGER_LEVEL


logger = init_logger(__name__, LOGGER_LEVEL)


def save_to_database(table_name: str, data_to_save: list[Project | Flat | Price]) -> None:
    """
    Сохраняет в базу данных.
    Уникальность записей обеспечивается primary key.

    :param table_name: Название таблицы в базе данных.
    :param data_to_save: Данные для сохранения в виде списка датаклассов.
    :return: None.
    """
    for data in data_to_save:
        insert(table_name, dataclasses.asdict(data))


def save_prices_to_database(table_name: str, data_to_save: list[Project | Flat | Price]) -> None:
    """
    Сохраняет цены в базу данных.
    Уникальность записей обеспечивается проверкой уже записанных данных.

    :param table_name: Название таблицы в базе данных.
    :param data_to_save: Данные для сохранения в виде списка датаклассов.
    :return: None.
    """
    for data in data_to_save:
        insert_price(table_name, dataclasses.asdict(data))


def create_database_if_not_exist() -> None:
    """
    Создает таблицы в базе данных.
    Если таблицы уже созданы, то ничего не делает.
    """
    create_db()
