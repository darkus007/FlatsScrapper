# FlatsScrapper v.1.0
Сервис по сбору информации с сайтов застройщиков и наполнению базы данных. 
Часть проекта Flats, в который также входят [FlatsWebsite](https://github.com/darkus007/FlatsWebsite) - сайт по подбору квартир.
FlatsTelegramBot - позволяет получать информацию о квартирах в мессенджере Telegram.

Данный проект написан на Python c использованием библиотек requests, beautifulsoup4 и psycopg2. \
Полный список в фале `requirements.txt`.

База данных [PostgreSQL](https://www.postgresql.org/).

### Описание структуры базы данных
> Projects - таблица с информацией о жилых комплексах.
>> project_id - уникальный идентификатор, совпадает с id застройщика.\
>> city - город.\
>> name - название ЖК.\
>> url - URL адрес ЖК на сайте застройщика.\
>> metro - ближайшее метро.\
>> time_to_metro - расстояние пешком до метро.\
>> latitude - координаты ЖК, широта.\
>> longitude - координаты ЖК, долгота.\
>> address - адрес ЖК.\
>> data_created - дата добавления ЖК в базу данных.\
>> data_closed - дата снятия ЖК с продажи.

> Flats - таблица с информацией о Квартирах.
>> flat_id - уникальный идентификатор, совпадает с id застройщика.\
>> address - адрес квартиры.\
>> floor - этаж.\
>> rooms - количество комнат.\
>> area - площадь.\
>> finishing - с отделкой?.\
>> settlement_date - дата заселения.\
>> url_suffix - продолжение URL к адресу ЖК.\
>> data_created - дата добавления квартиры в базу данных.\
>> data_closed - дата снятия квартиры с продажи.
>> project - проект к которому принадлежит квартира, связь один со многими.

> Prices - таблица с информацией о ценах на Квартиру.
>> benefit_name - ценовое предложение.\
>> benefit_description - описание ценового предложения.\
>> price - цена.\
>> meter_price - цена за метр.\
>> booking_status - статус бронирования.\
>> data_created - дата добавления записи в базу данных.\
>> flat - проект к которому принадлежит квартира, связь один со многими.

## Установка и запуск
Приложение написано на [Python v.3.11](https://www.python.org). \
Скачайте FlatsScrapper на Ваше устройство любым удобным способом (например Code -> Download ZIP, распакуйте архив). \
Установите и настройте [PostgreSQL](https://www.postgresql.org/).

### Настройка приложения
Создайте файл `env.dev` и установите значения переменных окружения: \
`DB_NAME` - название базы данных; \
`DB_USER` - пользователь базы данных; \
`DB_PASS` - пароль пользователя базы данных; \
`DB_HOST` - адрес базы данных; \
`DB_PORT` - порт базы данных; \
`LOGGER_LEVEL` - уровень логирования, например 'INFO'.

#### Запуск
Установите необходимые для работы приложения модули. 
Для этого откройте терминал, перейдите в каталог с приложением (cd <путь к приложению>/FlatsScrapper),
выполните команду `pip3 install -r requirements.txt`.  \
Запустите приложение выполнив команду `python3 main.py`.