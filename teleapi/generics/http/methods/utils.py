from aiohttp import FormData


def make_data_form(data, form_data: FormData = None) -> FormData:
    if form_data is None:
        form_data = FormData()

    for name, value in data.items():
        form_data.add_field(name, str(value))

    return form_data
