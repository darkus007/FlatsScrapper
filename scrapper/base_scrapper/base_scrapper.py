from abc import ABC, abstractmethod


class BaseScrapper(ABC):
    """ Базовый класс парсера. """

    @abstractmethod
    def run(self):
        """ Запускает сбор информации. """
        ...

    @abstractmethod
    def get_projects(self):
        """ Возвращает результат сбора информации по проектам. """
        ...

    @abstractmethod
    def get_flats(self):
        """ Возвращает результат сбора информации по квартирам. """
        ...

    @abstractmethod
    def get_prices(self):
        """ Возвращает результат сбора информации по ценам. """
        ...
