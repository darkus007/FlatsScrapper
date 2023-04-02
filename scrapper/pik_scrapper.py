"""
Модуль собирает информация по квартирам с сайта pik.ru в Москве и Области.

На первом этапе получаем информацию по ЖК с главной страницы.
Затем проходим по каждому ЖК и собираем информацию по квартирам и ценам.

Информацию о проектах (Жилых Комплексах) получаем на главной странице "https://www.pik.ru/projects".
Важно получить id ЖК. Квартиры получаем через api.

Запрос к api сайта для получения информации о квартирах в одном конкретном ЖК выглядит так
https://api.pik.ru/v2/filter?customSort=1&type=1,2&location=2,3&block=1124&flatPage=1&flatLimit=50&onlyFlats=1
где:
    &location=2,3 - локация, в данном случае 2,3 это Москва и Область;
    &block=1124 - код жилого комплекса (его id), получаем на главной странице "https://www.pik.ru/projects";
    &flatPage=1 - api отдает информацию постранично
    &flatLimit=50 - в количестве 50 квартир на страницу.

"""

__version__ = "v. 3.0 dated 27/03/2023"

import re
import json
from datetime import datetime
from random import randint
from sys import getsizeof
from time import sleep

from bs4 import BeautifulSoup

from logger import init_logger, LOGGER_LEVEL
from utilites import get_value_from_json
from .base_scrapper import BaseScrapper, RequestsMixin
from .data_classes import Project, Flat, Price

logger = init_logger(__name__, LOGGER_LEVEL)

HOST = "https://www.pik.ru/projects"  # страница с проектами
PROJECT_URL_PREFIX = "https://www.pik.ru/"  # для формирования url-адреса проекта

SCRAPPER_DEBUG = True  # если True, то собирает данные НЕ полностью для экономии времени при отладке


class PIKScrapper(BaseScrapper, RequestsMixin):
    def __init__(self):
        """
        Собирает информация по ЖК и квартирам с сайта pik.ru в Москве и Области.

        """
        RequestsMixin.__init__(self)

        self.__projects: list[Project] = []     # хранит собранную информацию о ЖК
        self.__flats: list[Flat] = []           # хранит собранную информацию о квартирах
        self.__prices: list[Price] = []         # хранит собранную информацию о ценах на квартиры

    def __get_projects(self, html: str, current_data: str) -> None:
        """
        Собирает информацию о ЖК с главной страницы.
        """
        soup = BeautifulSoup(html, 'lxml')
        all_info = soup.find("script", id="__NEXT_DATA__").text

        all_info_json = json.loads(all_info)
        # props.pageProps.initialState.searchService.filteredProjects.data.projects
        projects_info = all_info_json["props"]["pageProps"]["initialState"]["searchService"]
        projects_info = projects_info["filteredProjects"]["data"]["projects"]

        for project in projects_info:
            self.__projects.append(Project(
                project_id=get_value_from_json(project, ['id']),
                city=get_value_from_json(project, ['locations', 'parent', 'name']),
                name=get_value_from_json(project, ['name']),
                url=PROJECT_URL_PREFIX + str(get_value_from_json(project, ['url'])),
                metro=get_value_from_json(project, ['metro']),
                time_to_metro=get_value_from_json(project, ['timeOnFoot']),
                longitude=get_value_from_json(project, ['longitude']),
                latitude=get_value_from_json(project, ['latitude']),
                address=get_value_from_json(project, ['surveillance', 'list', 0, 'name']),
                data_created=current_data)
            )

        logger.debug(f"Найдено {len(self.__projects)} ЖК.")

    def __get_flats_from_all_projects(self, data: str, all_projects: list[Project]) -> None:
        """
        Собирает информацию о квартирах во всех найденных на главной странице ЖК.

        :param data: Текущая дата в формате '%Y-%m-%d'.
        :param all_projects: Список найденных ЖК.
        """
        current_project_number = 1
        total_projects = len(all_projects)

        for project in all_projects:
            logger.debug(f"[{current_project_number}|{total_projects}] ЖК.")
            self.__get_flats_from_one_project(data, project)
            current_project_number += 1
            if SCRAPPER_DEBUG:
                break

        logger.info(f"Собрана информация по {len(self.__projects)} ЖК, в которых найдено {len(self.__flats)} квартир.")
        logger.debug(f'Всего {getsizeof(self.__projects) + getsizeof(self.__flats) + getsizeof(self.__prices)} bytes.')

    def __get_flats_from_one_project(self, data: str, project: Project) -> None:
        """
        Собирает все квартиры одного ЖК.
        Проходит по всем страницам ЖК, и вызывает метод __get_flats_from_page()
        для сбора данных со страницы.

        :param data: Текущая дата в формате '%Y-%m-%d'.
        :param project: Данные о ЖК в формате датакласса Project.
        :return: Кортеж списков с информацией о ЖК, квартирах в нем и их цене.
        """
        flat_page = 1
        url_project_flats = "https://api.pik.ru/v2/filter?customSort=1&type=1,2&location=2,3&block=" \
                            + f"{project.project_id}&flatLimit=50&onlyFlats=1&flatPage="

        flats_info = json.loads(self.requests_get(url=url_project_flats + str(flat_page)))

        total_flats = flats_info.get('count', 0)
        total_pages = total_flats // 50
        if total_flats % 50 != 0:
            total_pages += 1

        logger.debug(f"ЖК '{project.name}' всего квартир {total_flats}.")
        logger.debug(f"На {total_pages} страницах.")

        full_address = get_value_from_json(flats_info, ['blocks', 0, "flats", 0, "address"])
        project_address = re.sub(r'[, (]*[Кк]орп[уса]*[\d\w ,./()№]*', '', full_address)  # убираем корпуса
        project_address = re.sub(r'[, ]*[Ээ]тап[ы]*[\d .,/]+', '', project_address)  # убираем этапы
        project.address = project_address  # уточняем информацию об адресе ЖК

        # собираем информацию о квартирах в этом ЖК
        flats_on_this_page = get_value_from_json(flats_info, ['blocks', 0, "flats"])
        self.__get_flats_from_page(data, project.project_id, flats_on_this_page)

        if not SCRAPPER_DEBUG:
            for flat_page in range(2, total_pages + 1):
                logger.debug(f"[{flat_page}/{total_pages}]")
                flats_info = json.loads(self.requests_get(url=url_project_flats + str(flat_page)))
                flats_on_this_page = get_value_from_json(flats_info, ['blocks', 0, "flats"])
                self.__get_flats_from_page(data, project.project_id, flats_on_this_page)

                sleep(randint(1, 3))

        logger.debug(f"Собрана информация по {len(self.__flats)} квартирам.")

    def __get_flats_from_page(self, data: str, project_id: int, flats_on_page: json) -> None:
        """
        Собирает информацию о квартирах и их цене на странице ЖК.

        :param data: Текущая дата в формате '%Y-%m-%d'.
        :param project_id: id ЖК для указания принадлежности найденных квартир к этому ЖК.
        :param flats_on_page: json с данными о квартирах.
        """
        for flat in flats_on_page:
            result_flat = Flat(
                flat_id=get_value_from_json(flat, ["id"]),
                project_id=project_id,
                address=get_value_from_json(flat, ["address"]),
                floor=get_value_from_json(flat, ["floor"]),
                rooms=get_value_from_json(flat, ["rooms"]),
                area=get_value_from_json(flat, ["area"]),
                finishing=get_value_from_json(flat, ["finish"]),
                bulk=get_value_from_json(flat, ["bulk", "name"]),
                settlement_date=get_value_from_json(flat, ["bulk", "settlementDate"]),
                url_suffix="/flats/" + str(get_value_from_json(flat, ["id"])),
                data_created=data
            )
            result_price = Price(
                flat_id=result_flat.flat_id,
                benefit_name=get_value_from_json(flat, ['mainBenefit', "name"]),
                benefit_description=get_value_from_json(flat, ['mainBenefit', "description"]),
                price=get_value_from_json(flat, ["price"]),
                meter_price=get_value_from_json(flat, ["meterPrice"]),
                booking_status=get_value_from_json(flat, ["bookingStatus"]),
                data_created=data
            )
            self.__flats.append(result_flat)
            self.__prices.append(result_price)

    def run(self):
        """
        Запускает сбор информации о ЖК, квартирах и ценах.
        """
        logger.info(f"Начало сбора информации.")
        current_data = datetime.now().strftime('%Y-%m-%d')

        html_text = self.requests_get(HOST)

        if html_text:
            self.__get_projects(html_text, current_data)
            self.__get_flats_from_all_projects(current_data, self.__projects)
        else:
            logger.error(f"Не удалось получить главную страницу {HOST}!")

    def get_projects(self) -> list[Project]:
        """ Возвращает результат сбора информации по проектам. """
        return self.__projects

    def get_flats(self) -> list[Flat]:
        """ Возвращает результат сбора информации по квартирам. """
        return self.__flats

    def get_prices(self) -> list[Price]:
        """ Возвращает результат сбора информации по ценам. """
        return self.__prices
