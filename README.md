# python-xlsxio

Wrapper for c library [xlsxio](https://github.com/brechtsanders/xlsxio)

## Install

### You need install some additional libraries:

* For **Debian**: `apt-get install expat libzip-dev`

* For **Arch**: `pacman -S expat libzip`

### You need cython: `pip install Cython`

### And run: `pip install python-xlsxio`

## Example

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