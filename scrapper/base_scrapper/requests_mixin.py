import logging
from time import sleep

from requests import get
from fake_useragent import UserAgent

from logger import init_logger, LOGGER_LEVEL

SLEEP_SECONDS = 5


logger = init_logger(__name__, LOGGER_LEVEL)
logging.getLogger('urllib3').setLevel(logging.ERROR)


class RequestsMixin:
    """
    Добавляет метод requests_get для получения HTML-страницы с использованием библиотеки requests.
    """
    def __init__(self):
        self.useragent = UserAgent()

    def requests_get(self, url: str, params=None) -> str:
        """
        Возвращает ответ на GET-запрос или пустую строку.

        :param url: URL-адрес.
        :param params: Дополнительные параметры.
        :return: :class:`Response <Response>` object или пустую строку.
        """
        headers = {'User-Agent': '', 'Accept': '*/*'}
        for i in range(3):  # три попытки получить страницу
            try:
                headers['User-Agent'] = self.useragent.random
                rq = get(url, params=params, headers=headers)
                if rq.status_code == 200:
                    return rq.text
                else:
                    logger.error(f"{rq.status_code}: {url}")
                    sleep(SLEEP_SECONDS)
            except Exception as ex:
                logger.error(f"Функция RequestsMixin.requests_get вызвала исключение:\n{ex}")
        return ''
