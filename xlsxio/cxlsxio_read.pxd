from libc.stddef cimport size_t
from libc.stdint cimport uint64_t, int64_t
from libc.time cimport time_t


cdef extern from "xlsxio_read.h":
    cdef unsigned int XLSXIOREAD_SKIP_NONE
    cdef unsigned int XLSXIOREAD_SKIP_EMPTY_ROWS
    cdef unsigned int XLSXIOREAD_SKIP_EMPTY_CELLS
    cdef unsigned int XLSXIOREAD_SKIP_ALL_EMPTY
    cdef unsigned int XLSXIOREAD_SKIP_EXTRA_CELLS
    cdef unsigned int XLSXIOREAD_SKIP_HIDDEN_ROWS

    const char* xlsxioread_get_version_string()

    ctypedef struct xlsxio_read_struct:
        pass
    ctypedef xlsxio_read_struct* xlsxioreader
    xlsxioreader xlsxioread_open (const char* filename)
    xlsxioreader xlsxioread_open_filehandle (int filehandle)
    xlsxioreader xlsxioread_open_memory (void* data, uint64_t datalen, int freedata)
    void xlsxioread_close (xlsxioreader handle)

    ctypedef struct xlsxio_read_sheetlist_struct:
        pass
    ctypedef xlsxio_read_sheetlist_struct* xlsxioreadersheetlist
    xlsxioreadersheetlist xlsxioread_sheetlist_open (xlsxioreader handle)
    void xlsxioread_sheetlist_close (xlsxioreadersheetlist sheetlisthandle)
    const char* xlsxioread_sheetlist_next (xlsxioreadersheetlist sheetlisthandle)

    ctypedef struct xlsxio_read_sheet_struct:
        pass
    ctypedef xlsxio_read_sheet_struct* xlsxioreadersheet
    size_t xlsxioread_sheet_last_row_index (xlsxioreadersheet sheethandle)
    size_t xlsxioread_sheet_last_column_index (xlsxioreadersheet sheethandle)
    unsigned int xlsxioread_sheet_flags (xlsxioreadersheet sheethandle)
    xlsxioreadersheet xlsxioread_sheet_open (xlsxioreader handle, const char* sheetname, unsigned int flags)
    void xlsxioread_sheet_close (xlsxioreadersheet sheethandle)
    int xlsxioread_sheet_next_row (xlsxioreadersheet sheethandle)
    char* xlsxioread_sheet_next_cell (xlsxioreadersheet sheethandle)
    int xlsxioread_sheet_next_cell_string (xlsxioreadersheet sheethandle, char** pvalue)
    int xlsxioread_sheet_next_cell_int (xlsxioreadersheet sheethandle, int64_t* pvalue)
    int xlsxioread_sheet_next_cell_float (xlsxioreadersheet sheethandle, double* pvalue)
    int xlsxioread_sheet_next_cell_datetime (xlsxioreadersheet sheethandle, time_t* pvalue)

    void xlsxioread_free (char* data)
