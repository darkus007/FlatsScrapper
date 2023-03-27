"""
Сбор информации по ЖК, квартирам и ценам.

"""

from scrapper import PIKScrapper
from utilites.utilites import write_to_json_file

if __name__ == '__main__':
    scrapper = PIKScrapper()
    scrapper.run()

    write_to_json_file('temp/projects', scrapper.get_projects())
    write_to_json_file('temp/flats', scrapper.get_flats())
    write_to_json_file('temp/prices', scrapper.get_prices())
