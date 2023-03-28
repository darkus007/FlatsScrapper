from unittest import TestCase
from unittest.mock import patch

from scrapper import pik_scrapper


class PIKScrapperTestCase(TestCase):

    # @patch("scrapper.pik_scrapper.SCRAPPER_DEBUG", True)
    @classmethod
    def setUpClass(cls) -> None:
        with patch("scrapper.pik_scrapper.SCRAPPER_DEBUG", True):
            cls.scrapper = pik_scrapper.PIKScrapper()
            cls.scrapper.run()

    def test_projects_ok(self):
        self.assertTrue(bool(len(self.scrapper.get_projects()) > 0))

    def test_flats_ok(self):
        self.assertTrue(bool(len(self.scrapper.get_flats()) > 0))

    def test_prices_ok(self):
        self.assertTrue(bool(len(self.scrapper.get_prices()) > 0))
