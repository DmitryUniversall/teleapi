from enum import Enum


class ParseMode(Enum):
    MARKDOWN: str = "markdown"
    HTML: str = "html"
    MARKDOWN_V2: str = "markdownv2"
    NONE: str = "none"
