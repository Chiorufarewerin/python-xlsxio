# python-xlsxio

Wrapper for c library [xlsxio](https://github.com/brechtsanders/xlsxio)

Since the main library is written in c, and its wrapper is written in cython (which compiles in c), the read speed is much faster than libraries written in python (as can be seen in the benchmarks).

This library also has streaming reading and does not load memory.

Of the minuses, you should know in advance the data types of each column, or read everything as a string or bytes.

## Install

Just: `pip install python-xlsxio`

If you want speed up about 5% you can build from source:

`pip install cython python-xlsxio --no-binary python-xlsxio`

## Benchmarks read xlsx

How is testing you can see in **benchmark/benchmark.py**

File xlsx generated with openpyxl and conteins mixed types, how is generated you can see in **benchmark/generate_xlsx.py**

Big file - file with 100000 rows

Small file - file with 100 rows

**Test machine**: Linux 5.4.44-1-MANJARO #1 SMP PREEMPT Wed Jun 3 14:48:07 UTC 2020 x86_64

| Title                                             | Min sec execution | Calls/sec |
|---------------------------------------------------|:-----------------:|:---------:|
| xlsxio read big file with types                   | 1.08584           | 0.92095   |
| xlsxio read big file without types                | 0.93787           | 1.06625   |
| xlsxio read big file without types all in bytes   | 0.88268           | 1.13292   |
| xlsxio read big file with types from memory       | 1.09569           | 0.91267   |
| xlsxio read small file with types                 | 0.00128           | 780.58583 |
| xlsxio read small file without types              | 0.00117           | 855.33007 |
| xlsxio read small file without types all in bytes | 0.0011            | 905.32902 |
| xlsxio read small file with types from memory     | 0.00129           | 776.06377 |
| openpyxl read big file                            | 6.34512           | 0.1576    |
| openpyxl read big file from memory                | 6.35287           | 0.15741   |
| openpyxl read small file                          | 0.01131           | 88.40829  |
| openpyxl read small file from memory              | 0.01134           | 88.19221  |
| xlrd read big file                                | 4.10823           | 0.24341   |
| xlrd read big file from memory                    | 4.0911            | 0.24443   |
| xlrd read small file                              | 0.00486           | 205.74491 |
| xlrd read small file from memory                  | 0.00503           | 198.75329 |
| sxl read big file                                 | 4.9788            | 0.20085   |
| sxl read big file from memory                     | 4.96794           | 0.20129   |
| sxl read small file                               | 0.00627           | 159.49498 |
| sxl read small file from memory                   | 0.00619           | 161.4445  |
| xlsx2csv read big file                            | 6.53466           | 0.15303   |
| xlsx2csv read big file from memory                | 6.56024           | 0.15243   |
| xlsx2csv read small file                          | 0.01157           | 86.4205   |
| xlsx2csv read small file from memory              | 0.01147           | 87.21896  |

## Fast start with read xlsx

```python
import xlsxio
xlsxio_reader = xlsxio.XlsxioReader('file.xlsx')
sheet = xlsxio_reader.get_sheet()
data = sheet.read_data()
sheet.close()
xlsxio_reader.close()

print(data)
```

Or simply:

```python
import xlsxio
with xlsxio.XlsxioReader('file.xlsx') as reader:
    with reader.get_sheet() as sheet:
        data = sheet.read_data()

print(data)
```

Full example for reading xlsx file in sheet `hello`, and not reading at all in memory (write only rows, which have True in 5 column):
```python
import xlsxio
import datetime

types = [str, str, float, int, bool, datetime.datetime]
with xlsxio.XlsxioReader('file.xlsx') as reader:
    with reader.get_sheet('hello', types=types) as sheet:
        header = sheet.read_header()
        only_active = []
        for row in sheet.iter_rows():
            if row[4]:
                only_active.append(row)
print(only_active)
```

## Usage read xlsx

### XlsxioReader
Object of xlsx

#### def \_\_init\_\_(self, filename, encoding: str = 'utf-8')
Inittializating XlsxioReader
* filename - str (path to filename), bytes (loaded in memory file) or file like object (not BytesIO)
* encoding - encoding of xlsx file

#### def get_sheet_names(self) -> tuple
Return tuple of sheet names in xlsx file

#### def get_sheet(self, sheetname: Optional[str] = None, flags: int = XlsxioReadFlag.SKIP_EMPTY_ROWS, types: Optional[Iterable[type]] = None, default_type: type = str) -> XlsxioReaderSheet
Return XlsxioReaderSheet object
* sheetname - name of sheet (if None, returns first sheet)
* flags - default is XlsxioReadFlag.SKIP_EMPTY_ROWS ([Read more about flags](https://github.com/brechtsanders/xlsxio/blob/master/include/xlsxio_read.h#L151-L161)). All possible flags:
  * XlsxioReadFlag.SKIP_NONE
  * XlsxioReadFlag.SKIP_EMPTY_ROWS
  * XlsxioReadFlag.SKIP_EMPTY_CELLS
  * XlsxioReadFlag.SKIP_ALL_EMPTY
  * XlsxioReadFlag.SKIP_EXTRA_CELLS
  * XlsxioReadFlag.SKIP_HIDDEN_ROWS
* types - list of types by columns. example, if first column is integer, second - str, end third - float, you can pass: `types=[int, str, float]`. if fourth column will be, then will it default_type.
Possible types:
  * bytes
  * str
  * int
  * float
  * datetime.datetime
  * bool
* default_type - default type of columns if types not passed, default str

#### def close(self)
Closes reader


### XlsxioReaderSheet
Object of sheet

#### def \_\_init\_\_(self, xlsxioreader: XlsxioReader, sheetname: Optional[str] = None, flags: int = XlsxioReadFlag.SKIP_EMPTY_ROWS, types: Optional[Iterable[type]] = None, default_type: type = str)
Initializet XlsxioReaderSheet object (it object initializes in xlsxioreader.get_sheet and about params you can read there)

#### def read_row(self, ignore_type: bool = False) -> Optional[list]
Reading next row in list. If rows does not exists return None
* ignore_type - if this true, return row in default_type (convenient for heading)

#### def read_header(self) -> Optional[list]
Alias for read_row(True)

#### def iter_rows(self) -> Iterable[list]
Iterate rows while rows exists

#### def get_last_row_index(self) -> int:
Getting last row index (returns 0 if not readed yet)

#### def get_flags(self) -> int:
Getting applied flags

#### def read_data(self) -> List[list]
Read all sheet rows, and first row in default_type. Method code:
```python
header = self.read_header()
if header is None:
    return []
rows = list(self.iter_rows())
rows.insert(0, header)
return rows
```

#### def close(self)
Closes sheet
