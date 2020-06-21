# cython: language_level=3

from typing import Iterable

import datetime

from cython cimport sizeof
from libc.stdlib cimport malloc, free
from libc.stdint cimport int64_t, uint64_t
from libc.time cimport time_t

from xlsxio cimport cxlsxio_read


# Flags
XLSXIOREAD_SKIP_NONE = 0
XLSXIOREAD_SKIP_EMPTY_ROWS = 1
XLSXIOREAD_SKIP_EMPTY_CELLS = 2
XLSXIOREAD_SKIP_ALL_EMPTY = XLSXIOREAD_SKIP_EMPTY_ROWS | XLSXIOREAD_SKIP_EMPTY_CELLS
XLSXIOREAD_SKIP_EXTRA_CELLS = 4

# Type casts
XLSXIOREAD_CELL_BYTES = 0
XLSXIOREAD_CELL_STRING = 1
XLSXIOREAD_CELL_INT = 2
XLSXIOREAD_CELL_FLOAT = 3
XLSXIOREAD_CELL_DATETIME = 4

XLSXIOREAD_CELL_TYPES = frozenset((
    XLSXIOREAD_CELL_BYTES,
    XLSXIOREAD_CELL_STRING,
    XLSXIOREAD_CELL_INT,
    XLSXIOREAD_CELL_FLOAT,
    XLSXIOREAD_CELL_DATETIME,
))


def get_xlsxioread_version_string() -> str:
    cdef const char* version_char = cxlsxio_read.xlsxioread_get_version_string()
    return version_char.decode('ascii')


cdef class XlsxioReaderSheet:
    cdef object xlsxioreader
    cdef str encoding
    cdef cxlsxio_read.xlsxioreadersheet _c_xlsxioreadersheet
    cdef int _c_default_type
    cdef int* _c_types
    cdef int _c_types_size

    def __cinit__(self, xlsxioreader, str encoding):
        self.xlsxioreader = xlsxioreader  # define here, cuz xlsxioreader on __delloc__ closes

        self.encoding = encoding
        self._c_xlsxioreadersheet = NULL
        self._c_default_type = 0
        self._c_types = NULL
        self._c_types_size = 0

    cdef char* read_cell_char(self):
        cdef char* value
        cdef int result = cxlsxio_read.xlsxioread_sheet_next_cell_string(self._c_xlsxioreadersheet, &value)
        if result == 1:
            return value
        return NULL

    cdef object read_cell_bytes(self):
        cdef char* value_char = self.read_cell_char()
        if value_char is NULL:
            return None
        try:
            return value_char
        finally:
            free(value_char)

    cdef object read_cell_string(self):
        cdef char* value_char = self.read_cell_char()
        if value_char is NULL:
            return None
        try:
            return value_char.decode(self.encoding)
        finally:
            free(value_char)

    cdef object read_cell_int(self):
        cdef int64_t value
        cdef int result = cxlsxio_read.xlsxioread_sheet_next_cell_int(self._c_xlsxioreadersheet, &value)
        if result != 1:
            return None
        return value

    cdef object read_cell_float(self):
        cdef double value
        cdef int result = cxlsxio_read.xlsxioread_sheet_next_cell_float(self._c_xlsxioreadersheet, &value)
        if result != 1:
            return None
        return value

    cdef object read_cell_datetime(self):
        cdef time_t value
        cdef int result = cxlsxio_read.xlsxioread_sheet_next_cell_datetime(self._c_xlsxioreadersheet, &value)
        if result != 1:
            return None
        return datetime.datetime.fromtimestamp(value)

    cdef object read_cell(self, int _type):
        if _type == 0:
            return self.read_cell_bytes()
        if _type == 1:
            return self.read_cell_string()
        if _type == 2:
            return self.read_cell_int()
        if _type == 3:
            return self.read_cell_float()
        if _type == 4:
            return self.read_cell_datetime()
        raise ValueError('Incorrect type value')

    cdef list _read_row(self, int ignore_type = 0):
        if self._c_xlsxioreadersheet is NULL:
            raise RuntimeError('Sheet is not open')

        if not cxlsxio_read.xlsxioread_sheet_next_row(self._c_xlsxioreadersheet):
            return None

        cdef int n = 0, _type = 0
        cdef list row_data = []
        cdef object value

        while True:
            _type = self._c_types[n] if ignore_type == 0 and n < self._c_types_size else self._c_default_type
            value = self.read_cell(_type)
            if value is None:
                return row_data
            row_data.append(value)
            n += 1
    
    def read_row(self, ignore_type: bool = False):
        return self._read_row(int(ignore_type))

    def read_header(self):
        return self._read_row(1)

    def iter_rows(self):
        while True:
            row = self._read_row()
            if row is None:
                break
            yield row

    def read_data(self):
        header = self.read_header()
        if header is None:
            return []
        rows = list(self.iter_rows())
        rows.insert(0, header)
        return rows

    def close(self):
        if self._c_xlsxioreadersheet is not NULL:
            cxlsxio_read.xlsxioread_sheet_close(self._c_xlsxioreadersheet)
            self._c_xlsxioreadersheet = NULL
        if self._c_types is not NULL:
            free(self._c_types)
            self._c_types = NULL

    def __dealloc__(self):
        self.close()


cdef class XlsxioReader:
    cdef object filename
    cdef cxlsxio_read.xlsxioreader _c_xlsxioreader

    cdef init_by_filename(self, str filename):
        cdef bytes filename_bytes = filename.encode('utf-8')
        cdef const char* c_filename = filename_bytes
        self._c_xlsxioreader = cxlsxio_read.xlsxioread_open(c_filename)
        if self._c_xlsxioreader is NULL:
            raise FileNotFoundError('No such file: %s' % (filename,))

    cdef init_by_bytes(self, bytes data_bytes):
        cdef char* data = data_bytes
        cdef uint64_t data_len = len(data_bytes)
        self._c_xlsxioreader = cxlsxio_read.xlsxioread_open_memory(data, data_len, 0)
        if self._c_xlsxioreader is NULL:
            raise ValueError('Incorrect value of xlsx file data')

    cdef init_by_file(self, int filehandle):
        self._c_xlsxioreader = cxlsxio_read.xlsxioread_open_filehandle(filehandle)
        if self._c_xlsxioreader is NULL:
            raise ValueError('Incorrect value of xlsx file data')

    def __cinit__(self, filename):
        self.filename = filename

        if isinstance(filename, str):
            self.init_by_filename(filename)
        elif isinstance(filename, bytes):
            self.init_by_bytes(filename)
        elif hasattr(filename, 'fileno') and callable(filename.fileno):
            self.init_by_file(filename.fileno())
        else:
            raise TypeError('Incorrect type of xlsx file data ')

    def get_sheet(self, sheetname: str = None, flags: int = XLSXIOREAD_SKIP_EMPTY_ROWS,
                  default_type: int = XLSXIOREAD_CELL_STRING, types: Iterable[int] = None,
                  encoding: str = 'utf-8'):
        if self._c_xlsxioreader is NULL:
            raise RuntimeError('Reader is closed or not opened')
        if type(flags) is not int:
            raise TypeError('Value flags must be an integer')
        if flags < 0 or flags > 7:
            raise ValueError('Incorrect flags value')

        sheet = XlsxioReaderSheet(xlsxioreader=self, encoding=encoding)

        if default_type not in XLSXIOREAD_CELL_TYPES:
            raise ValueError('Incorrect default_type value')
        sheet._c_default_type = default_type

        if types is not None:
            if not all(_type in XLSXIOREAD_CELL_TYPES for _type in types):
                raise ValueError('Incorrect types value')
            sheet._c_types = <int *> malloc(len(types) * sizeof(int))
            sheet._c_types_size = len(types)
            if sheet._c_types is NULL:
                raise MemoryError()
            for i in range(len(types)):
                sheet._c_types[i] = types[i]

        if sheetname is None:
            sheet._c_xlsxioreadersheet = cxlsxio_read.xlsxioread_sheet_open(self._c_xlsxioreader, NULL, flags)
            if sheet._c_xlsxioreadersheet is NULL:
                raise RuntimeError('First sheet cannot be opened. May incorrect xlsx file.')
            return sheet

        cdef bytes sheetname_bytes = sheetname.encode('utf-8')
        cdef char* c_sheetname = sheetname_bytes
        sheet._c_xlsxioreadersheet = cxlsxio_read.xlsxioread_sheet_open(self._c_xlsxioreader, c_sheetname, flags)

        if sheet._c_xlsxioreadersheet is NULL:
            raise RuntimeError('Sheet cannot be opened. May incorrect xlsx file.')

        return sheet

    def close(self):
        if self._c_xlsxioreader is not NULL:
            cxlsxio_read.xlsxioread_close(self._c_xlsxioreader)
            self._c_xlsxioreader = NULL

    def __dealloc__(self):
        self.close()
