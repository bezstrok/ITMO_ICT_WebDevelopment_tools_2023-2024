import re

__all__ = ["Format"]

_camel_case_re = re.compile(r"(?<!^)(?=[A-Z])")


class Format:
    @classmethod
    def snake_case(cls, string: str) -> str:
        return _camel_case_re.sub("_", string).lower()
