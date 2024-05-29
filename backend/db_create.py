import psycopg2
from configparser import ConfigParser

# Leer la configuración de la base de datos desde un archivo de configuración
def config(filename='db_config.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(f'Section {section} not found in the {filename} file')

    return db

# Crear la conexión y las tablas, e insertar datos ficticios
def create_and_populate_db():
    conn = None
    try:
        params = config()

        # Conectar a la base de datos
        conn = psycopg2.connect(**params)
        cursor = conn.cursor()

        # Crear tablas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS properties (
            property_id SERIAL PRIMARY KEY,
            property_name TEXT NOT NULL,
            description TEXT,
            location TEXT
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS airbnb_reservations (
            reservation_id SERIAL PRIMARY KEY,
            property_id INTEGER REFERENCES properties(property_id),
            guest_name TEXT,
            check_in_date DATE,
            check_out_date DATE,
            number_of_guests INTEGER,
            total_price DECIMAL(10, 2),
            status TEXT
        );
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS booking_reservations (
            reservation_id SERIAL PRIMARY KEY,
            property_id INTEGER REFERENCES properties(property_id),
            guest_name TEXT,
            check_in_date DATE,
            check_out_date DATE,
            number_of_guests INTEGER,
            total_price DECIMAL(10, 2),
            status TEXT
        );
        ''')

        # Insertar datos ficticios
        properties = [
            ('Habitación Mango', 'Cómoda y acogedora habitación', 'Ciudad A'),
            ('Habitación Coco', 'Espaciosa habitación con vista al mar', 'Ciudad B'),
            ('Habitación Papaya', 'Habitación moderna y luminosa', 'Ciudad C'),
            ('Dormitorio Compartido', 'Dormitorio compartido en un hostal', 'Ciudad D')
        ]

        cursor.executemany('''
        INSERT INTO properties (property_name, description, location)
        VALUES (%s, %s, %s)
        ''', properties)

        airbnb_reservations = [
            (1, 'John Doe', '2024-06-01', '2024-06-05', 2, 500.00, 'confirmed'),
            (2, 'Jane Smith', '2024-06-10', '2024-06-15', 4, 750.00, 'confirmed'),
            (3, 'Alice Johnson', '2024-07-01', '2024-07-03', 1, 200.00, 'cancelled'),
            (4, 'Bob Brown', '2024-07-15', '2024-07-20', 6, 1200.00, 'confirmed')
        ]

        cursor.executemany('''
        INSERT INTO airbnb_reservations (property_id, guest_name, check_in_date, check_out_date, number_of_guests, total_price, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', airbnb_reservations)

        booking_reservations = [
            (1, 'Carlos García', '2024-05-01', '2024-05-03', 1, 150.00, 'confirmed'),
            (2, 'Laura Martínez', '2024-06-05', '2024-06-07', 2, 300.00, 'confirmed'),
            (3, 'Elena López', '2024-07-10', '2024-07-15', 3, 450.00, 'cancelled'),
            (4, 'Pedro Sánchez', '2024-08-01', '2024-08-05', 2, 500.00, 'confirmed')
        ]

        cursor.executemany('''
        INSERT INTO booking_reservations (property_id, guest_name, check_in_date, check_out_date, number_of_guests, total_price, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ''', booking_reservations)

        # Guardar los cambios y cerrar la conexión
        conn.commit()
        print("Base de datos creada y poblada con datos ficticios.")

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    create_and_populate_db()