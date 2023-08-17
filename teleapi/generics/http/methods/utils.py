import json
from typing import Any
from aiohttp import FormData


def prepare_field(value: Any) -> str:
    return value if isinstance(value, str) else json.dumps(value)


def prepare_data(data: dict) -> dict:
    return {key: prepare_field(value) for key, value in data.items()}


def make_data_form(data, form_data: FormData = None) -> FormData:
    if form_data is None:
        form_data = FormData()

    for name, value in data.items():
        form_data.add_field(name, prepare_field(value))

    return form_data
