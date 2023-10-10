from _typeshed import StrPath
from logging import FileHandler
from .cache import get_current_schema_name


class TenantFileHandler(FileHandler):
    
    def __init__(self, filename: StrPath, mode: str = "a", encoding: str | None = None, delay: bool = False, errors: str | None = None) -> None:
        filename = get_current_schema_name()
        super().__init__(filename, mode, encoding, delay, errors)