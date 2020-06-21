# python-xlsxio

Обертка для сишной библиотеки [xlsxio](https://github.com/brechtsanders/xlsxio)

## Установка

Перед этим надо установить саму библиотеку

* Для ОС базирующихся на Arch linux: `yay xlsxio`

Также необходимо установить Cython: `pip install Cython`
Затем выполнить: `pip install python-xlsxio`

## Пример

```
import xlsxio
xlsxio_reader = xlsxio.XlsxioReader('file.xlsx')
sheet = xlsxio_reader.get_sheet()
data = sheet.read_data()
sheet.close()
xlsxio_reader.close()

print(data)
```
