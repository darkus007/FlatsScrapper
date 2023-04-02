"""
Загружает настройки для проекта.

Использован пакет dotenv:
    pip install python-dotenv
"""

from os import getenv

from dotenv import load_dotenv


load_dotenv()

DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
DB_NAME = getenv('DB_NAME')
DB_USER = getenv('DB_USER')
DB_PASS = getenv('DB_PASS')

LOGGER_LEVEL = getenv('LOGGER_LEVEL')
