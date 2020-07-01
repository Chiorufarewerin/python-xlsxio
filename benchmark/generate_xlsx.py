import datetime
import random
from openpyxl import Workbook


first_names = [
    'Liam',
    'Noah',
    'William',
    'James',
    'Oliver',
    'Benjamin',
    'Elijah',
    'Lucas',
    'Mason',
    'Logan',
    'Alexander',
    'Ethan',
    'Jacob',
    'Michael',
    'Daniel',
    'Henry',
    'Jackson',
    'Sebastian',
    'Aiden',
    'Matthew',
    'Samuel',
    'David',
    'Joseph',
    'Carter',
    'Owen',
    'Wyatt',
    'John',
    'Jack',
    'Luke',
    'Jayden',
    'Dylan',
    'Grayson',
    'Levi',
    'Isaac',
    'Gabriel',
    'Julian',
    'Mateo',
    'Anthony',
    'Jaxon',
    'Lincoln',
    'Joshua',
    'Christopher',
    'Andrew',
    'Theodore',
    'Caleb',
    'Ryan',
    'Asher',
    'Nathan',
    'Thomas',
    'Leo',
    'Isaiah',
    'Charles',
    'Josiah',
    'Hudson',
    'Christian',
    'Hunter',
    'Connor',
    'Eli',
    'Ezra',
    'Aaron',
    'Landon',
    'Adrian',
    'Jonathan',
    'Nolan',
    'Jeremiah',
    'Easton',
    'Elias',
    'Colton',
    'Cameron',
    'Carson',
    'Robert',
    'Angel',
    'Maverick',
    'Nicholas',
    'Dominic',
    'Jaxson',
    'Greyson',
    'Adam',
    'Ian',
    'Austin',
    'Santiago',
    'Jordan',
    'Cooper',
    'Brayden',
    'Roman',
    'Evan',
    'Ezekiel',
    'Xavier',
    'Jose',
    'Jace',
    'Jameson',
    'Leonardo',
    'Bryson',
    'Axel',
    'Everett',
    'Parker',
    'Kayden',
    'Miles',
    'Sawyer',
    'Jason',
]

last_names = [
    'Smith',
    'Johnson',
    'Williams',
    'Brown',
    'Jones',
    'Garcia',
    'Miller',
    'Davis',
    'Rodriguez',
    'Martinez',
    'Hernandez',
    'Lopez',
    'Gonzalez',
    'Wilson',
    'Anderson',
    'Thomas',
    'Taylor',
    'Moore',
    'Jackson',
    'Martin',
    'Lee',
    'Perez',
    'Thompson',
    'White',
    'Harris',
    'Sanchez',
    'Clark',
    'Ramirez',
    'Lewis',
    'Robinson',
    'Walker',
    'Young',
    'Allen',
    'King',
    'Wright',
    'Scott',
    'Torres',
    'Nguyen',
    'Hill',
    'Flores',
    'Green',
    'Adams',
    'Nelson',
    'Baker',
    'Hall',
    'Rivera',
    'Campbell',
    'Mitchell',
    'Carter',
    'Roberts',
]

header = ('ID', 'First name', 'Last name', 'Date birth', 'Age', 'Salary', 'Last activity', 'Is Male')


def get_row(_id):
    date_birth = datetime.datetime(1950, 1, 1) + datetime.timedelta(seconds=random.randint(0, 2000000000))
    age = int((datetime.datetime.now() - date_birth).days / 365)
    date_birth = date_birth.date()
    return (
        _id,
        random.choice(first_names),
        random.choice(last_names),
        date_birth,
        age,
        round(random.random() * 100000 + 100.0, random.randint(-3, 2)),
        datetime.datetime(2017, 1, 1) + datetime.timedelta(seconds=random.randint(0, 100000000)),
        bool(random.randint(0, 1)),
    )


wb = Workbook(write_only=True)
ws = wb.create_sheet()

ws.append(header)
for i in range(1, 100000):
    ws.append(get_row(i))

ws.close()

wb.save('benchmark.xlsx')

wb.close()
