"""
Модуль содержит дата-классы представления собранных данных
и класс для преобразования дата-класса в json объект.
"""

from dataclasses import dataclass, is_dataclass, asdict
from json import JSONEncoder


@dataclass
class Project:                  # Информация о ЖК
    project_id: int             # id ЖК
    city: str                   # Город в котором находится ЖК
    name: str                   # Название ЖК
    url: str                    # URL адрес ЖК
    metro: str                  # Название метро
    time_to_metro: int          # Расстояние до метро
    latitude: float             # Координаты ЖК
    longitude: float            # Координаты ЖК
    address: str                # Адрес ЖК
    data_created: str           # дата сбора данных о ЖК с сайта


@dataclass
class Flat:                     # Информация о квартире
    flat_id: int                # id квартиры
    project_id: int             # id ЖК, которому принадлежит квартира
    address: str                # Адрес квартиры
    floor: int                  # Этаж
    rooms: int                  # Количество комнат
    area: float                 # Площадь квартиры
    finishing: bool             # Отделка
    bulk: str                   # Корпус дома
    settlement_date: str        # Дата заселения
    url_suffix: str             # Приставка к url адресу квартиры, полный адрес будет Project.url + Flat.url_suffix
    data_created: str           # дата сбора данных о квартире с сайта


@dataclass
class Price:                    # Информация о цене
    price_id: int               # id квартиры, которой принадлежит данная цена
    benefit_name: str           # Название ценового предложения
    benefit_description: str    # Описание ценового предложения
    price: int                  # Цена
    meter_price: int            # Цена за метр
    booking_status: str         # Статус бронирования
    data_created: str           # дата сбора данных о цене с сайта


class JsonDataclassEncoder(JSONEncoder):
    """
    Используется для преобразования дата-класса в json объект.
    Пример json.dumps(dataclass, ensure_ascii=False, cls=JsonDataclassEncoder).
    """
    def default(self, obj):
        if is_dataclass(obj):
            return asdict(obj)
        return super().default(obj)
