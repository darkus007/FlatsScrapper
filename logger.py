"""
Модуль инициализации логера (logging.Logger).
"""
import logging
import logging.handlers
from sys import stdout

LOGGER_LEVEL = "DEBUG"


def init_logger(name: str, level: str | int) -> logging.Logger:
    """
    Возвращает сконфигурированный логер.

    :param name: Имя логера.
    :param level: Уровень логирования.
    :return: Экземпляр класса Logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    log_format = logging.Formatter('%(asctime)s %(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S ')

    # file_handler = logging.FileHandler(f'logs/{name}.log', mode='a')
    file_handler = logging.handlers.RotatingFileHandler(filename=f'logs/{name}.log',
                                                        mode='a',
                                                        maxBytes=1048576,   # 1 Мегабайт = 1048576 Байт
                                                        backupCount=10)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(log_format)

    stream_handler = logging.StreamHandler(stdout)
    stream_handler.setLevel(logging.DEBUG)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
