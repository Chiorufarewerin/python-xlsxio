from typing import Any, Iterable, Iterator, List, Optional, Tuple, Union


def get_xlsxioread_version_string() -> str:
    ...


class XlsxioReadFlag:
    SKIP_NONE: int
    SKIP_EMPTY_ROWS: int
    SKIP_EMPTY_CELLS: int
    SKIP_ALL_EMPTY: int
    SKIP_EXTRA_CELLS: int
    SKIP_HIDDEN_ROWS: int


class XlsxioReader:
    def __init__(self, filename: Union[str, bytes], encoding: str = 'utf-8'):
        ...

    def get_sheet_names(self) -> Tuple[str, ...]:
        ...

    def get_sheet(self, sheetname: Optional[str] = None,
                  flags: int = XlsxioReadFlag.SKIP_EMPTY_ROWS,
                  types: Optional[Iterable[type]] = None, default_type: type = str) -> 'XlsxioReaderSheet':
        ...

    def close(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, traceback):
        ...

    def __dealloc__(self):
        ...


class XlsxioReaderSheetList:
    def __init__(self, xlsxioreader: XlsxioReader):
        ...

    def get_names(self) -> Tuple[str, ...]:
        ...

    def close(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, traceback):
        ...

    def __dealloc__(self):
        ...


class XlsxioReaderSheet:
    def __init__(self, xlsxioreader: XlsxioReader, sheetname: Optional[str] = None,
                 flags: int = XlsxioReadFlag.SKIP_EMPTY_ROWS,
                 types: Optional[Iterable[type]] = None, default_type: type = str):
        ...

    def get_last_row_index(self) -> int:
        ...

    def get_flags(self) -> int:
        ...

    def read_row(self, ignore_type: bool = False) -> Optional[List[Any]]:
        ...

    def read_header(self) -> Optional[List[Any]]:
        ...

    def iter_rows(self) -> Iterator[List[Any]]:
        ...

    def read_data(self) -> List[List[Any]]:
        ...

    def close(self):
        ...

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_value, traceback):
        ...

    def __dealloc__(self):
        ...
