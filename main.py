"""
Сбор информации по ЖК, квартирам и ценам.

"""

from scrapper import PIKScrapper
from database import save_to_database, save_prices_to_database, create_database_if_not_exist

if __name__ == '__main__':
    scrapper = PIKScrapper()
    scrapper.run()

    create_database_if_not_exist()
    save_to_database('project', scrapper.get_projects())
    save_to_database('flat', scrapper.get_flats())
    save_prices_to_database('price', scrapper.get_prices())
