# flake8: noqa

import datetime


TEST_READ_DATA_TYPES = {
    'Sheet1': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        [1, 'Jayden', 'Young', datetime.datetime(1956, 7, 4, 0, 0), 64, 85844.5, datetime.datetime(2017, 8, 3, 20, 7, 45), True],
        [2, 'Parker', 'Nguyen', datetime.datetime(2012, 4, 18, 0, 0), 8, 36100.0, datetime.datetime(2019, 12, 3, 9, 3, 22), False],
        [3, 'Robert', 'Sanchez', datetime.datetime(1950, 6, 26, 0, 0), 70, 38719.05, datetime.datetime(2017, 4, 14, 9, 58), False],
        [4, 'Isaac', 'Adams', datetime.datetime(1992, 12, 24, 0, 0), 27, 77000.0, datetime.datetime(2018, 9, 23, 15, 55, 15), True],
        [5, 'Landon', 'Lewis', datetime.datetime(1993, 8, 28, 0, 0), 26, 13000.0, datetime.datetime(2018, 1, 12, 2, 2, 2), False],
        [6, 'Greyson', 'Adams', datetime.datetime(1984, 10, 13, 0, 0), 35, 14000.0, datetime.datetime(2017, 9, 7, 6, 20, 19), False],
        [7, 'Evan', 'Flores', datetime.datetime(2003, 6, 21, 0, 0), 17, 18000.0, datetime.datetime(2020, 1, 14, 3, 18, 8), False],
        [8, 'Ian', 'Taylor', datetime.datetime(1966, 10, 10, 0, 0), 53, 59000.0, datetime.datetime(2018, 8, 19, 10, 5, 51), False],
        [9, 'Connor', 'Walker', datetime.datetime(1983, 2, 27, 0, 0), 37, 92551.0, datetime.datetime(2018, 1, 13, 21, 27, 13), False],
        []
    ],
    'Привет': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        [1, 'Jayden', 'Young', datetime.datetime(1956, 7, 4, 0, 0), 64, 85844.5, datetime.datetime(2017, 8, 3, 20, 7, 45), True],
        [2, 'Parker', 'Nguyen', datetime.datetime(2012, 4, 18, 0, 0), 8, 36100.0, datetime.datetime(2019, 12, 3, 9, 3, 22), False],
        [3, 'Robert', 'Sanchez', datetime.datetime(1950, 6, 26, 0, 0), 70, 38719.05, datetime.datetime(2017, 4, 14, 9, 58), False],
        [4, 'Isaac', 'Adams', datetime.datetime(1900, 12, 24, 0, 0), 120, 77000.0, datetime.datetime(2018, 9, 23, 15, 55, 15), True]
    ],
    'test_empty': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        [1, '', '', datetime.datetime(1998, 10, 19, 0, 0), 21],
        [2, '', '', datetime.datetime(1995, 5, 5, 0, 0), 24, 85844.5, datetime.datetime(2019, 10, 19, 21, 19)],
        [0, '', '', datetime.datetime(1970, 1, 1, 0, 0), 0, 0.0, datetime.datetime(1970, 1, 1, 0, 0), True],
        [4],
        [6, 'Greyson', 'Adams', datetime.datetime(1984, 10, 13, 0, 0), 35, 14000.0, datetime.datetime(2017, 9, 7, 6, 20, 19), False]
    ],
}


TEST_READ_DATA_STRINGS = {
    'Sheet1': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        ['1', 'Jayden', 'Young', '20640', '64', '85844.5', '42950.8387268518', '1'],
        ['2', 'Parker', 'Nguyen', '41017', '8', '36100', '43802.377349537', '0'],
        ['3', 'Robert', 'Sanchez', '18440', '70', '38719.05', '42839.4152777778', '0'],
        ['4', 'Isaac', 'Adams', '33962', '27', '77000', '43366.6633680556', '1'],
        ['5', 'Landon', 'Lewis', '34209', '26', '13000', '43112.0847453704', '0'],
        ['6', 'Greyson', 'Adams', '30968', '35', '14000', '42985.2641087963', '0'],
        ['7', 'Evan', 'Flores', '37793', '17', '18000', '43844.1375925926', '0'],
        ['8', 'Ian', 'Taylor', '24390', '53', '59000', '43331.4207291667', '0'],
        ['9', 'Connor', 'Walker', '30374', '37', '92551', '43113.893912037', '0'],
        []
    ],
    'Привет': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        ['1', 'Jayden', 'Young', '20640', '64', '85844.5', '42950.8387268518', '1'],
        ['2', 'Parker', 'Nguyen', '41017', '8', '36100', '43802.377349537', '0'],
        ['3', 'Robert', 'Sanchez', '18440', '70', '38719.05', '42839.4152777778', '0'],
        ['4', 'Isaac', 'Adams', '359', '120', '77000', '43366.6633680556', '1']
    ],
    'test_empty': [
        ['ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male'],
        ['1', '', '', '36087', '21'],
        ['2', '', '', '34824', '24', '85844.5', '43757.8881944445'],
        ['', '', '', '', '', '', '', '1'],
        ['4'],
        ['6', 'Greyson', 'Adams', '30968', '35', '14000', '42985.2641087963', '0']
    ],
}

TEST_READ_DATA_BYTES = {
    'Sheet1': [
        [b'ID', b'First name', b'Last name', b'Date birth', b'Age', b'Salary', b'Last activity', b'Is Male'],
        [b'1', b'Jayden', b'Young', b'20640', b'64', b'85844.5', b'42950.8387268518', b'1'],
        [b'2', b'Parker', b'Nguyen', b'41017', b'8', b'36100', b'43802.377349537', b'0'],
        [b'3', b'Robert', b'Sanchez', b'18440', b'70', b'38719.05', b'42839.4152777778', b'0'],
        [b'4', b'Isaac', b'Adams', b'33962', b'27', b'77000', b'43366.6633680556', b'1'],
        [b'5', b'Landon', b'Lewis', b'34209', b'26', b'13000', b'43112.0847453704', b'0'],
        [b'6', b'Greyson', b'Adams', b'30968', b'35', b'14000', b'42985.2641087963', b'0'],
        [b'7', b'Evan', b'Flores', b'37793', b'17', b'18000', b'43844.1375925926', b'0'],
        [b'8', b'Ian', b'Taylor', b'24390', b'53', b'59000', b'43331.4207291667', b'0'],
        [b'9', b'Connor', b'Walker', b'30374', b'37', b'92551', b'43113.893912037', b'0'],
        []
    ],
    'Привет': [
        [b'ID', b'First name', b'Last name', b'Date birth', b'Age', b'Salary', b'Last activity', b'Is Male'],
        [b'1', b'Jayden', b'Young', b'20640', b'64', b'85844.5', b'42950.8387268518', b'1'],
        [b'2', b'Parker', b'Nguyen', b'41017', b'8', b'36100', b'43802.377349537', b'0'],
        [b'3', b'Robert', b'Sanchez', b'18440', b'70', b'38719.05', b'42839.4152777778', b'0'],
        [b'4', b'Isaac', b'Adams', b'359', b'120', b'77000', b'43366.6633680556', b'1']
    ],
    'test_empty': [
        [b'ID', b'First name', b'Last name', b'Date birth', b'Age', b'Salary', b'Last activity', b'Is Male'],
        [b'1', b'', b'', b'36087', b'21'],
        [b'2', b'', b'', b'34824', b'24', b'85844.5', b'43757.8881944445'],
        [b'', b'', b'', b'', b'', b'', b'', b'1'],
        [b'4'],
        [b'6', b'Greyson', b'Adams', b'30968', b'35', b'14000', b'42985.2641087963', b'0']
    ],
}
