import json
from typing import Any
from aiohttp import FormData


def prepare_field(value: Any) -> str:
    return value if isinstance(value, (str, bytes)) else json.dumps(value)


def prepare_data(data: dict) -> dict:
    return {key: prepare_field(value) for key, value in data.items()}


def make_data_form(data, data_form: FormData = None) -> FormData:
    if data_form is None:
        data_form = FormData()

    for name, value in data.items():
        data_form.add_field(name, prepare_field(value))

    return data_form
