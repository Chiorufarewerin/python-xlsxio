# cython: language_level=3

import datetime

from cython cimport sizeof
from libc.stddef cimport size_t
from libc.stdlib cimport malloc, free
from libc.stdint cimport int64_t, uint64_t
from libc.time cimport time_t

from xlsxio cimport cxlsxio_read


cdef class XlsxioReadFlag:
    SKIP_NONE = cxlsxio_read.XLSXIOREAD_SKIP_NONE
    SKIP_EMPTY_ROWS = cxlsxio_read.XLSXIOREAD_SKIP_EMPTY_ROWS
    SKIP_EMPTY_CELLS = cxlsxio_read.XLSXIOREAD_SKIP_EMPTY_CELLS
    SKIP_ALL_EMPTY = cxlsxio_read.XLSXIOREAD_SKIP_ALL_EMPTY
    SKIP_EXTRA_CELLS = cxlsxio_read.XLSXIOREAD_SKIP_EXTRA_CELLS
    SKIP_HIDDEN_ROWS = cxlsxio_read.XLSXIOREAD_SKIP_HIDDEN_ROWS


# Type casts
cdef int XLSXIOREAD_CELL_BYTES = 0
cdef int XLSXIOREAD_CELL_STRING = 1
cdef int XLSXIOREAD_CELL_INT = 2
cdef int XLSXIOREAD_CELL_FLOAT = 3
cdef int XLSXIOREAD_CELL_DATETIME = 4
cdef int XLSXIOREAD_CELL_BOOL = 5

cdef dict XLSXIOREAD_CELL_TYPES = {
    bytes: XLSXIOREAD_CELL_BYTES,
    str: XLSXIOREAD_CELL_STRING,
    int: XLSXIOREAD_CELL_INT,
    float: XLSXIOREAD_CELL_FLOAT,
    datetime.datetime: XLSXIOREAD_CELL_DATETIME,
    bool: XLSXIOREAD_CELL_BOOL,
}


def get_xlsxioread_version_string() -> str:
    cdef const char* version_char = cxlsxio_read.xlsxioread_get_version_string()
    return version_char.decode('ascii')


cdef class XlsxioReader:
    cdef object filename
    cdef str encoding
    cdef tuple _cached_sheet_names

    cdef cxlsxio_read.xlsxioreader _c_xlsxioreader

    cdef init_by_filename(self, str filename):
        cdef bytes filename_bytes = filename.encode(self.encoding)
        cdef const char* c_filename = filename_bytes
        self._c_xlsxioreader = cxlsxio_read.xlsxioread_open(c_filename)
        if self._c_xlsxioreader is NULL:
            raise FileNotFoundError(f'No such file: {filename}')

    cdef init_by_bytes(self, bytes data_bytes):
        cdef char* data = data_bytes
        cdef uint64_t data_len = len(data_bytes)
        self._c_xlsxioreader = cxlsxio_read.xlsxioread_open_memory(data, data_len, 0)
        if self._c_xlsxioreader is NULL:
            raise ValueError('Incorrect value of xlsx file data')

    def __cinit__(self, filename, str encoding = 'utf-8'):
        self.filename = filename
        self.encoding = encoding

        if isinstance(filename, str):
            self.init_by_filename(filename)
        elif isinstance(filename, bytes):
            self.init_by_bytes(filename)
        else:
            raise TypeError(f'Expected string or bytes, received: {type(filename).__name__}')

    cpdef tuple get_sheet_names(self):
        if self._cached_sheet_names is None:
            with XlsxioReaderSheetList(self) as sheetlist:
                sheet_names = sheetlist.get_names()
            self._cached_sheet_names = sheet_names
        return self._cached_sheet_names

    def get_sheet(self, sheetname = None, int flags = XlsxioReadFlag.SKIP_EMPTY_ROWS,
                  types = None, type default_type = str):
        return XlsxioReaderSheet(self, sheetname, flags, types, default_type)

    cpdef close(self):
        if self._c_xlsxioreader is not NULL:
            cxlsxio_read.xlsxioread_close(self._c_xlsxioreader)
            self._c_xlsxioreader = NULL

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __dealloc__(self):
        self.close()


cdef class XlsxioReaderSheetList:
    cdef XlsxioReader xlsxioreader
    cdef cxlsxio_read.xlsxioreadersheetlist _c_xlsxioreadersheetlist

    def __cinit__(self, XlsxioReader xlsxioreader):
        if xlsxioreader._c_xlsxioreader is NULL:
            raise RuntimeError('Reader is closed or not opened')
        self.xlsxioreader = xlsxioreader
        self._c_xlsxioreadersheetlist = NULL
        self._c_xlsxioreadersheetlist = cxlsxio_read.xlsxioread_sheetlist_open(self.xlsxioreader._c_xlsxioreader)
        if self._c_xlsxioreadersheetlist is NULL:
            raise RuntimeError('Sheet list cannot be opened')

    cdef object get_name(self):
        cdef const char* name_char = cxlsxio_read.xlsxioread_sheetlist_next(self._c_xlsxioreadersheetlist)
        if name_char is NULL:
            return None
        return name_char.decode(self.xlsxioreader.encoding)

    cpdef tuple get_names(self):
        if self._c_xlsxioreadersheetlist is NULL:
            raise RuntimeError('Sheet list is closed or not opened')

        cdef list names = []
        cdef object name
        while True:
            name = self.get_name()
            if name is None:
                return tuple(names)
            names.append(name)

    cpdef close(self):
        if self._c_xlsxioreadersheetlist is not NULL:
            cxlsxio_read.xlsxioread_sheetlist_close(self._c_xlsxioreadersheetlist)
            self._c_xlsxioreadersheetlist = NULL

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __dealloc__(self):
        self.close()


cdef class XlsxioReaderSheet:
    cdef XlsxioReader xlsxioreader
    cdef object sheetname

    cdef char* _c_sheetname
    cdef int _c_default_type
    cdef int* _c_types
    cdef int _c_types_size
    cdef int _c_flags
    cdef cxlsxio_read.xlsxioreadersheet _c_xlsxioreadersheet

    def __cinit__(self, XlsxioReader xlsxioreader, sheetname = None, int flags = XlsxioReadFlag.SKIP_EMPTY_ROWS,
                  types = None, type default_type = str):
        if flags < XlsxioReadFlag.SKIP_NONE or flags > (
            XlsxioReadFlag.SKIP_NONE |
            XlsxioReadFlag.SKIP_EMPTY_ROWS |
            XlsxioReadFlag.SKIP_EMPTY_CELLS |
            XlsxioReadFlag.SKIP_ALL_EMPTY |
            XlsxioReadFlag.SKIP_EXTRA_CELLS |
            XlsxioReadFlag.SKIP_HIDDEN_ROWS
        ):
            raise ValueError('Incorrect flags value')
        if default_type not in XLSXIOREAD_CELL_TYPES:
            raise ValueError('Incorrect default_type value')
        if sheetname is not None and not isinstance(sheetname, str):
            raise TypeError('Value sheetname must be str or None')
        if types is not None:
            types = tuple(types)

        self.xlsxioreader = xlsxioreader
        self.sheetname = sheetname
        self._c_sheetname = NULL
        self._c_xlsxioreadersheet = NULL
        self._c_default_type = 0
        self._c_types = NULL
        self._c_types_size = 0
        self._c_default_type = XLSXIOREAD_CELL_TYPES[default_type]
        self._c_flags = flags

        cdef bytes temp_filename

        if sheetname is not None:
            if sheetname not in xlsxioreader.get_sheet_names():
                raise ValueError(f'No such sheet: {sheetname}')
            temp_filename = sheetname.encode(xlsxioreader.encoding)
            self._c_sheetname = temp_filename

        self._c_xlsxioreadersheet = cxlsxio_read.xlsxioread_sheet_open(xlsxioreader._c_xlsxioreader,
                                                                       self._c_sheetname, self._c_flags)
        if self._c_xlsxioreadersheet is NULL:
            raise RuntimeError('Sheet cannot be opened')

        if types is not None:
            if not all(_type in XLSXIOREAD_CELL_TYPES for _type in types):
                raise ValueError('Incorrect types value')
            self._c_types = <int *> malloc(len(types) * sizeof(int))
            self._c_types_size = len(types)
            if self._c_types is NULL:
                raise MemoryError()
            for i in range(len(types)):
                self._c_types[i] = XLSXIOREAD_CELL_TYPES[types[i]]

    cdef _raise_on_sheet_null(self):
        if self._c_xlsxioreadersheet is NULL:
            raise RuntimeError('Sheet is closed or not opened')

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
            cxlsxio_read.xlsxioread_free(value_char)

    cdef object read_cell_string(self):
        cdef char* value_char = self.read_cell_char()
        if value_char is NULL:
            return None
        try:
            return value_char.decode(self.xlsxioreader.encoding)
        finally:
            cxlsxio_read.xlsxioread_free(value_char)

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
        IF UNAME_SYSNAME == "Windows":
            return datetime.datetime(1970, 1, 1) + datetime.timedelta(seconds=value)
        ELSE:
            return datetime.datetime.utcfromtimestamp(value)

    cdef object read_cell_bool(self):
        cdef object value = self.read_cell_int()
        if value is None:
            return None
        return bool(value)

    cdef object read_cell(self, int _type):
        if _type == XLSXIOREAD_CELL_BYTES:
            return self.read_cell_bytes()
        if _type == XLSXIOREAD_CELL_STRING:
            return self.read_cell_string()
        if _type == XLSXIOREAD_CELL_INT:
            return self.read_cell_int()
        if _type == XLSXIOREAD_CELL_FLOAT:
            return self.read_cell_float()
        if _type == XLSXIOREAD_CELL_DATETIME:
            return self.read_cell_datetime()
        if _type == XLSXIOREAD_CELL_BOOL:
            return self.read_cell_bool()
        raise ValueError('Incorrect type value')

    cdef list _read_row(self, int ignore_type = 0):
        self._raise_on_sheet_null()

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

    cpdef get_last_row_index(self):
        self._raise_on_sheet_null()

        cdef size_t row_index = cxlsxio_read.xlsxioread_sheet_last_row_index(self._c_xlsxioreadersheet)
        return row_index

    cpdef get_flags(self):
        self._raise_on_sheet_null()

        cdef unsigned int flags = cxlsxio_read.xlsxioread_sheet_flags(self._c_xlsxioreadersheet)
        return flags

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

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def __dealloc__(self):
        self.close()
