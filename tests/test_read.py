import os
import pytest
import xlsxio
import datetime
from . import test_read_data


TYPES = (int, str, str, datetime.datetime, int, float, datetime.datetime, bool)
MAIN_DIR = os.path.dirname(os.path.abspath(__name__))
CURRENT_DIR = os.path.join(MAIN_DIR, 'tests')
XLSX_DIR = os.path.join(CURRENT_DIR, 'xlsx')
XLSX_TEST_FILENAME = 'test_file_base.xlsx'
XLSX_TEST_FILE_PATH = os.path.join(XLSX_DIR, XLSX_TEST_FILENAME)


def test_get_xlsxioread_version_string():
    assert xlsxio.get_xlsxioread_version_string() == '0.2.30'


class TestReadXlsx:
    def get_reader(self, *, filename: str = XLSX_TEST_FILENAME) -> xlsxio.XlsxioReader:
        return xlsxio.XlsxioReader(os.path.join(XLSX_DIR, filename))

    def base_read(self, reader: xlsxio.XlsxioReader):
        for sheet_name in reader.get_sheet_names():
            with reader.get_sheet(sheet_name) as sheet:
                assert sheet_name in test_read_data.TEST_READ_DATA_STRINGS
                assert sheet.read_data() == test_read_data.TEST_READ_DATA_STRINGS[sheet_name]
            with reader.get_sheet(sheet_name, default_type=bytes) as sheet:
                assert sheet_name in test_read_data.TEST_READ_DATA_BYTES
                assert sheet.read_data() == test_read_data.TEST_READ_DATA_BYTES[sheet_name]
            with reader.get_sheet(sheet_name, types=TYPES) as sheet:
                assert sheet_name in test_read_data.TEST_READ_DATA_TYPES
                assert sheet.read_data() == test_read_data.TEST_READ_DATA_TYPES[sheet_name]

    def test_read_from_filename(self):
        reader = xlsxio.XlsxioReader(XLSX_TEST_FILE_PATH)
        self.base_read(reader)

    def test_read_from_bytes(self):
        with open(XLSX_TEST_FILE_PATH, 'rb') as f:
            reader = xlsxio.XlsxioReader(f.read())
        self.base_read(reader)

    def test_read_from_filename_not_existing(self):
        with pytest.raises(FileNotFoundError, match='No such file: notfound.xlsx'):
            xlsxio.XlsxioReader('notfound.xlsx')

    def test_read_from_incorrect_bytes(self):
        with pytest.raises(ValueError, match='Incorrect value of xlsx file data'):
            xlsxio.XlsxioReader(b'')

    def test_read_incorrect_type(self):
        with pytest.raises(TypeError, match='Expected string or bytes, received: int'):
            xlsxio.XlsxioReader(123)

    def test_get_sheet_names(self):
        with self.get_reader() as reader:
            assert reader.get_sheet_names() == ('Sheet1', 'Привет', 'test_empty')

    def test_get_sheet_names_reader_closed(self):
        with self.get_reader() as reader:
            pass
        with pytest.raises(RuntimeError, match='Reader is closed or not opened'):
            reader.get_sheet_names()

    def test_sheet_incorrect_flags_value(self):
        with self.get_reader() as reader:
            with pytest.raises(ValueError, match='Incorrect flags value'):
                reader.get_sheet(flags=16)

    def test_sheet_incorrect_default_type_value(self):
        with self.get_reader() as reader:
            with pytest.raises(ValueError, match='Incorrect default_type value'):
                reader.get_sheet(default_type=list)

    def test_sheet_incorrect_sheetname_value(self):
        with self.get_reader() as reader:
            with pytest.raises(TypeError, match='Value sheetname must be str or None'):
                reader.get_sheet(123)

    def test_sheet_sheetname_not_found(self):
        with self.get_reader() as reader:
            with pytest.raises(ValueError, match='No such sheet: test'):
                reader.get_sheet('test')

    def test_sheet_icorrect_types(self):
        with self.get_reader() as reader:
            with pytest.raises(ValueError, match='Incorrect types value'):
                reader.get_sheet(types=[type])

    def test_read_sheet_ignore_type(self):
        with self.get_reader() as reader:
            with reader.get_sheet('Sheet1', types=TYPES) as sheet:
                sheet.read_row(True) == test_read_data.TEST_READ_DATA_STRINGS['Sheet1'][0]
                sheet.read_row(False) == test_read_data.TEST_READ_DATA_TYPES['Sheet1'][1]
                sheet.read_row(True) == test_read_data.TEST_READ_DATA_STRINGS['Sheet1'][2]

    def test_sheet_empty_read_data(self):
        with self.get_reader(filename='test_empty.xlsx') as reader:
            assert reader.get_sheet_names() == ('Sheet', 'empty')
            with reader.get_sheet('empty') as sheet:
                assert sheet.read_data() == []

    def test_flags(self):
        flag_names = [name for name in vars(xlsxio.XlsxioReadFlag).keys() if not name.startswith('__')]

        assert len(flag_names) == 6
        assert xlsxio.XlsxioReadFlag.SKIP_NONE == 0
        assert xlsxio.XlsxioReadFlag.SKIP_EMPTY_ROWS == 1
        assert xlsxio.XlsxioReadFlag.SKIP_EMPTY_CELLS == 2
        assert xlsxio.XlsxioReadFlag.SKIP_ALL_EMPTY == 3
        assert xlsxio.XlsxioReadFlag.SKIP_EXTRA_CELLS == 4
        assert xlsxio.XlsxioReadFlag.SKIP_HIDDEN_ROWS == 8

    def test_get_flags(self):
        with self.get_reader() as reader:
            flags = xlsxio.XlsxioReadFlag.SKIP_EXTRA_CELLS | xlsxio.XlsxioReadFlag.SKIP_HIDDEN_ROWS
            with reader.get_sheet(flags=flags) as sheet:
                assert not sheet.get_flags() & xlsxio.XlsxioReadFlag.SKIP_EMPTY_ROWS
                assert not sheet.get_flags() & xlsxio.XlsxioReadFlag.SKIP_EMPTY_CELLS
                assert not sheet.get_flags() & xlsxio.XlsxioReadFlag.SKIP_ALL_EMPTY
                assert sheet.get_flags() & xlsxio.XlsxioReadFlag.SKIP_EXTRA_CELLS
                assert sheet.get_flags() & xlsxio.XlsxioReadFlag.SKIP_HIDDEN_ROWS

    def test_get_flags_sheet_closed(self):
        with self.get_reader() as reader:
           sheet = reader.get_sheet()
           sheet.close()
           with pytest.raises(RuntimeError, match='Sheet is closed or not opened'):
               sheet.get_flags()

    def test_get_last_row_index(self):
        with self.get_reader() as reader:
            with reader.get_sheet() as sheet:
                assert sheet.get_last_row_index() == 0
                sheet.read_row()
                assert sheet.get_last_row_index() == 1

    def test_test_get_last_row_index_sheet_closed(self):
        with self.get_reader() as reader:
           sheet = reader.get_sheet()
           sheet.close()
           with pytest.raises(RuntimeError, match='Sheet is closed or not opened'):
               sheet.get_last_row_index()
