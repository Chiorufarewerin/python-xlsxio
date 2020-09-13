import os
import datetime
from unittest import TestCase
from tests.test_read_data import TEST_READ_DATA_TYPES, TEST_READ_DATA_WITHOUT_TYPES, TEST_READ_DATA_BYTES

from xlsxio import XlsxioReader, XlsxioReadFlag


TYPES = (int, str, str, datetime.datetime, int, float, datetime.datetime, bool)
XLSX_DIR = os.path.join(os.path.dirname(os.path.abspath(__name__)), 'tests', 'xlsx')
XLSX_TEST_FILE_BASE = os.path.join(XLSX_DIR, 'test_file_base.xlsx')


class TestReadXlsx(TestCase):
    reader: XlsxioReader

    def setUp(self):
        self.reader = XlsxioReader(XLSX_TEST_FILE_BASE)

    def tearDown(self):
        self.reader.close()

    def test_sheet_names(self):
        self.assertEqual(self.reader.get_sheet_names(), ('Sheet1', 'Привет', 'test_empty'))

    def test_first_sheet_data_without_types(self):
        with self.reader.get_sheet() as sheet:
            data = sheet.read_data()

        self.assertEqual(len(data), 100)
        self.assertListEqual(data, TEST_READ_DATA_WITHOUT_TYPES['Sheet1'])

    def test_data_without_types(self):
        for sheet_name in self.reader.get_sheet_names()[:-1]:
            with self.reader.get_sheet(sheet_name) as sheet:
                data = sheet.read_data()
            self.assertListEqual(data, TEST_READ_DATA_WITHOUT_TYPES[sheet_name])

    def test_data_types(self):
        for sheet_name in self.reader.get_sheet_names()[:-1]:
            with self.reader.get_sheet(sheet_name, types=TYPES) as sheet:
                data = sheet.read_data()
            self.assertListEqual(data, TEST_READ_DATA_TYPES[sheet_name])

    def test_data_bytes(self):
        for sheet_name in self.reader.get_sheet_names()[:-1]:
            with self.reader.get_sheet(sheet_name, default_type=bytes) as sheet:
                data = sheet.read_data()
            self.assertListEqual(data, TEST_READ_DATA_BYTES[sheet_name])

    def test_read_header(self):
        with self.reader.get_sheet(types=TYPES) as sheet:
            row = sheet.read_row(True)
        with self.reader.get_sheet(types=TYPES) as sheet:
            header = sheet.read_header()
        self.assertListEqual(row, header)

    def test_iter_first_rows(self):
        with self.reader.get_sheet(types=TYPES) as sheet:
            rows = [sheet.read_header()]
            for i, row in enumerate(sheet.iter_rows()):
                rows.append(row)
                if i == 5:
                    break
        self.assertListEqual(rows, TEST_READ_DATA_TYPES['Sheet1'][:7])

    # def test_flag_skip_empty_rows(self):
    #     with self.reader.get_sheet('test_empty', flags=XlsxioReadFlag.SKIP_EMPTY_ROWS) as sheet:
    #         data = sheet.read_data()
    #     self.assertEqual(len(data), 5)
    #     test_data = list(filter(lambda x: any(x), TEST_READ_DATA_WITHOUT_TYPES['test_empty']))
    #     self.assertListEqual(data, test_data)

    def test_flag_skip_empty_cells(self):
        with self.reader.get_sheet('test_empty', flags=XlsxioReadFlag.SKIP_EMPTY_CELLS) as sheet:
            data = sheet.read_data()

        test_data = TEST_READ_DATA_WITHOUT_TYPES['test_empty']
        self.assertEqual(len(data), 7)
        self.assertEqual(len(data[0]), 8)
        self.assertListEqual(data[0], test_data[0])
        self.assertEqual(len(data[1]), 3)
        self.assertListEqual(data[1], list(filter(None, test_data[1])))
        self.assertEqual(len(data[2]), 5)
        self.assertListEqual(data[2], list(filter(None, test_data[2])))
        self.assertListEqual(data[3], [])
        self.assertEqual(len(data[4]), 1)
        self.assertEqual(data[4][0], test_data[4][0])
        self.assertListEqual(data[5], [])
        self.assertEqual(len(data[6]), 8)
        self.assertListEqual(data[6], test_data[-1])

    def test_flag_skip_all_empty(self):
        with self.reader.get_sheet('test_empty', flags=XlsxioReadFlag.SKIP_ALL_EMPTY) as sheet:
            data = sheet.read_data()

        test_data = TEST_READ_DATA_WITHOUT_TYPES['test_empty']
        self.assertEqual(len(data), 5)
        self.assertEqual(len(data[0]), 8)
        self.assertListEqual(data[0], test_data[0])
        self.assertEqual(len(data[1]), 3)
        self.assertListEqual(data[1], list(filter(None, test_data[1])))
        self.assertEqual(len(data[2]), 5)
        self.assertListEqual(data[2], list(filter(None, test_data[2])))
        self.assertEqual(len(data[3]), 1)
        self.assertEqual(data[3][0], test_data[4][0])
        self.assertEqual(len(data[4]), 8)
        self.assertListEqual(data[4], test_data[-1])
