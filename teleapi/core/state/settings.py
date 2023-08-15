import os
from typing import Any
from teleapi.core.utils.lazy_objects import LazyObject
from teleapi.core.utils.types import UNDEFINED
from teleapi.core.utils.imp import import_module


class Settings:
    """
    Класс, предоставляющий доступ к настройкам проекта.
    Имя файла с настройками должно находится в переменных окружения
    """

    environ_variable_name: str = 'SETTINGS_MODULE'

    def __init__(self, name: str = None) -> None:
        # Хранит дополнительную информацию, создаваемую в процессе
        self.__dict__['_Settings__module_info'] = {
            'SETTINGS_FILE_NAME': name,
        }

        name = name if name else os.environ.get(self.environ_variable_name)

        if not name:
            raise ValueError(f"Environ variable for settings module ('{self.environ_variable_name}') not specified")

        self.__module = import_module(name)

    def __getattr__(self, item: str) -> Any:
        """
        Берёт информацию из self.__module_info или из модуля

        :param item: Аттрибут, который нужно найти
        :return: Значение указанного аттрибута из __module_info
        :raises: AttributeError если аттрибут не найден
        """

        if (value := self.__module_info.get(item, UNDEFINED)) is not UNDEFINED:
            return value.obj if isinstance(value, LazyObject) else value
        elif (value := getattr(self.__module, item, UNDEFINED)) is not UNDEFINED:
            return value.obj if isinstance(value, LazyObject) else value

        raise AttributeError(f"Settings module has no attribute '{item}'")

    def __setattr__(self, key: str, value: Any) -> None:
        """
        Записывает все атрибуты в self.__module_info для дальнейшего использования
        """

        self.__module_info[key] = value

    def get(self, item: str, default: Any = None) -> Any:
        """
        :param item: Атрибут, который надо взять
        :param default: Значение по умолчанию, вернётся если атрибут будет не найден
        :return: Значение атрибута / Значение по умолчанию
        """

        try:
            return getattr(self, item)
        except AttributeError:
            return default


project_settings = Settings()
