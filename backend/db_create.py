import psycopg2
import configparser

config = configparser.ConfigParser()
config.read('db_config.ini')

# Conexión a la base de datos
conn = psycopg2.connect(
    host=config['postgresql']['host'],
    database=config['postgresql']['database'],
    user=config['postgresql']['user'],
    password=config['postgresql']['password']
)

cursor = conn.cursor()

# Crear tabla reservations
cursor.execute('''
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id SERIAL PRIMARY KEY,
    guest_name TEXT,
    property_id INTEGER,
    property_name TEXT,
    check_in_date DATE,
    check_out_date DATE,
    number_of_guests INTEGER,
    total_price DECIMAL(10,2),
    status TEXT
)
''')

# Insertar datos ficticios en la tabla reservations

reservations = [
    ('John Doe', 1, 'Beautiful Apartment', '2024-06-01', '2024-06-05', 2, 500.00, 'confirmed'),
    ('Jane Smith', 2, 'Cozy Cottage', '2024-06-10', '2024-06-15', 4, 750.00, 'confirmed'),
    ('Alice Johnson', 3, 'Modern Studio', '2024-07-01', '2024-07-03', 1, 200.00, 'cancelled'),
    ('Bob Brown', 4, 'Spacious Villa', '2024-07-15', '2024-07-20', 6, 1200.00, 'confirmed'),
    ('Charlie White', 5, 'Luxury Condo', '2024-08-01', '2024-08-07', 3, 950.00, 'confirmed'),
    ('Diana Black', 6, 'Rustic Cabin', '2024-09-01', '2024-09-05', 5, 600.00, 'confirmed'),
    ('Eve Green', 7, 'Urban Loft', '2024-10-10', '2024-10-15', 2, 700.00, 'cancelled'),
    ('Frank Blue', 8, 'Beach House', '2024-11-01', '2024-11-10', 4, 1300.00, 'confirmed'),
    ('Grace Yellow', 9, 'Mountain Retreat', '2024-12-01', '2024-12-07', 7, 1600.00, 'confirmed'),
    ('Henry Purple', 10, 'Country Farmhouse', '2025-01-05', '2025-01-10', 6, 1100.00, 'confirmed')
]

cursor.executemany('''
INSERT INTO reservations (guest_name, property_id, property_name, check_in_date, check_out_date, number_of_guests, total_price, status)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
''', reservations
)

conn.commit()
conn.close()

print("Base de datos creada y poblada con datos ficticios")