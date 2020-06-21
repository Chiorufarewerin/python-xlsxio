# python-xlsxio

Wrapper for c library [xlsxio](https://github.com/brechtsanders/xlsxio)

## Install

Before install python library you need to install c librarry

* For Arch linux bases OS: `yay xlsxio`

And run: `pip install python-xlsxio`

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
