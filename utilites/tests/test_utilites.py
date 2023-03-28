import json
import os
from unittest import TestCase
from dataclasses import dataclass

from utilites import get_value_from_json, write_to_json_file


class GetValueFromJsonTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.json_data = [
            {'key1': 'value1'},
            {'key2': 'value2'},
            {'key3': 'value3'},
            [
                {'key4': 'value4'},
                {'key5': 'value5'}
            ]
        ]

    def test_ok(self):
        res = get_value_from_json(self.json_data, [3, 0, 'key4'])
        self.assertEqual(res, 'value4')

    def test_not_find(self):
        res = get_value_from_json(self.json_data, [0, 1, 'key4'])
        self.assertEqual(res, None)


class WriteToJsonFileTestCase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        @dataclass
        class DataClass:
            data1: str
            data2: int

        cls.dataclass_to_save = DataClass(data1='data1', data2=1234)

        cls.json_to_save = [
            {'data1': 'data1', 'data2': 1234},
            {'data3': 'data3', 'data4': 5678}
        ]

    @classmethod
    def tearDownClass(cls) -> None:
        os.remove('unittest_json_test_file.json')
        os.remove('unittest_dataclass_test_file.json')

    def test_dataclass_save(self):
        write_to_json_file('unittest_dataclass_test_file', self.dataclass_to_save)

        with open('unittest_dataclass_test_file.json', 'r') as file:
            readed_json = json.load(file)

        self.assertEqual(self.dataclass_to_save.data1, readed_json.get('data1', None))
        self.assertEqual(self.dataclass_to_save.data2, readed_json.get('data2', None))

    def test_json_save(self):
        write_to_json_file('unittest_json_test_file', self.json_to_save)

        with open('unittest_json_test_file.json', 'r') as file:
            readed_json = json.load(file)

        self.assertEqual(self.json_to_save[0]['data1'], readed_json[0].get('data1', None))
        self.assertEqual(self.json_to_save[0]['data2'], readed_json[0].get('data2', None))
