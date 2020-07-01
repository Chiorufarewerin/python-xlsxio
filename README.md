# python-xlsxio

Wrapper for c library [xlsxio](https://github.com/brechtsanders/xlsxio)

Since the main library is written in c, and its wrapper is written in cython (which compiles in c), the read speed is much faster than libraries written in python (as can be seen in the benchmarks).

This library also has streaming reading and does not load memory.

Of the minuses, you should know in advance the data types of each column, or read everything as a string or bytes.

## Install

You need install some additional libraries:

* For **Debian**: `apt-get install expat libzip-dev`

* For **Arch**: `pacman -S expat libzip`

You need cython: `pip install Cython`

And run: `pip install python-xlsxio`

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

```
import xlsxio
xlsxio_reader = xlsxio.XlsxioReader('file.xlsx')
sheet = xlsxio_reader.get_sheet()
data = sheet.read_data()
sheet.close()
xlsxio_reader.close()

print(data)
```

Or simply:

```
import xlsxio
with xlsxio.XlsxioReader('file.xlsx') as reader: 
    with reader.get_sheet() as sheet: 
        data = sheet.read_data() 

print(data)
```