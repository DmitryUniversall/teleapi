from typing import Optional, Any, Callable


class DotDict(dict):
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__

    def __getattr__(self, item):
        try:
            return super(DotDict, self).__getitem__(item)
        except KeyError as error:
            raise AttributeError(f"{self.__class__.__name__} has no attribute '{item}'") from error

    def __init__(self, init_data: dict = None) -> None:
        super(DotDict, self).__init__(**(init_data if init_data else {}))

        for key, value in self.items():
            if isinstance(value, dict):
                setattr(self, key, DotDict(value))


def find_in_list(array: list, check: Callable[[Any], bool]) -> Optional[Any]:
    result = list(filter(check, array))
    if len(result) != 0:
        return result[0]


def clear_none_values(dictionary: dict) -> dict:
    return {key: value for key, value in dictionary.items() if value is not None}


def replace_substring(original_string: str, start_index: int, end_index: int, replacement_substring: str) -> str:
    if (start_index < 0 or start_index >= len(original_string)) or (end_index < 0 or end_index > len(original_string)) or (start_index > end_index):
        raise IndexError("Invalid start or end index.")

    return original_string[:start_index] + replacement_substring + original_string[end_index:]


def exclude_from_dict(dict_: dict, *exclude) -> dict:
    return {key:value for key, value in dict_.items() if key not in exclude}
