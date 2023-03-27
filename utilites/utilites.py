import json
from typing import Any, Union

from scrapper.data_classes import JsonDataclassEncoder


def get_value_from_json(json_data: Union[list, dict], keys: list) -> Any:
    """
    Возвращает данные из json по переданным ключам.
    Обрабатывает отсутствие ключа в dict и IndexError для list, в этом случае возвращает None.

    :param json_data: Json из которого требуется получить значение.
    :param keys: Список ключей, по которым лежит значение.
    :return: Любые данные, обычно str, int, float, None, ...
    """
    if len(keys) == 1:
        if isinstance(json_data, dict):
            return json_data.get(keys[0], None)
        elif isinstance(json_data, list):
            try:
                return json_data[keys[0]]
            except IndexError:
                return None
            except TypeError:
                return None
    else:
        key = keys.pop(0)
        if isinstance(json_data, dict):
            return get_value_from_json(json_data.get(key, None), keys)
        elif isinstance(json_data, list):
            try:
                return get_value_from_json(json_data[key], keys)
            except IndexError:
                return None


def write_to_json_file(file_name: str, data: json) -> None:
    """
    Сохраняет в json файл.
    :param file_name: Название файла, расширение
                        ".json" будет добавлено
                        автоматически.
    :param data: Данные для записи в формате json.
    """
    with open(file_name + ".json", 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False, cls=JsonDataclassEncoder)
