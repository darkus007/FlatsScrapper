from unittest import TestCase

from ..requests_mixin import RequestsMixin


class RequestsMixinTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.request = RequestsMixin()

    def test_requests_get_ok(self):
        res = self.request.requests_get('https://ya.ru/')
        self.assertTrue(res)

    def test_requests_get_bad_request(self):
        res = self.request.requests_get('https://yaya.ru/')
        self.assertEqual(res, '')
