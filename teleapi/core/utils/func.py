def pass_additional_kwargs(obj, **additional_kwargs):
    def wrapper(*args, **kwargs):
        return obj(*args, **kwargs, **additional_kwargs)

    return wrapper
