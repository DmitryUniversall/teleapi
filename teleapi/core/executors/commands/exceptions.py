from teleapi.core.exceptions import TeleapiError


class CommandError(TeleapiError):
    default_message = "Command error"


class ParameterParseError(CommandError):
    default_message = "Failed to parse parameter value"
