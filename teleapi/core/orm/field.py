class Field:
    def __init__(self) -> None:
        self.__attribute_name__ = None
        self.__owner__ = None

    def __str__(self) -> str:
        return f"<{self.__class__.__name__} [{self.__attribute_name__} of {self.__owner__.__name__}]>"

    def __set_name__(self, owner: type, name: str) -> None:
        self.__attribute_name__ = name
        self.__owner__ = owner
