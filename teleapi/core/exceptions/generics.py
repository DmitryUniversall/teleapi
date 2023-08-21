from .teleapi import TeleapiError


class FileTooLargeError(TeleapiError):
    pass


class ParameterConflict(TeleapiError):
    pass
