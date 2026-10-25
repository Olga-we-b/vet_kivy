import sqlite3


def get_connection():
    connection = sqlite3.connect("fidel_bajzel.db")
    connection.execute("PRAGMA foreign_keys = ON")
    return connection

def create_tables():
    connection = get_connection()

    connection.executescript("""
        CREATE TABLE IF NOT EXISTS owners (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT,
            phone_number TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            kind TEXT NOT NULL,
            breed TEXT,
            date_of_birth TEXT,
            gender TEXT,
            owner_id INTEGER NOT NULL,
            FOREIGN KEY (owner_id) REFERENCES owners(id)
        );

        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            pwz_number TEXT NOT NULL UNIQUE
        );

        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            price INTEGER NOT NULL CHECK (price >= 0)
        );

        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY,
            animal_id INTEGER NOT NULL,
            doctor_id INTEGER NOT NULL,
            date_time TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'zaplanowana'
                CHECK (status IN (
                    'zaplanowana', 'anulowana', 'zakonczona'
                )),
            diagnosis TEXT NOT NULL DEFAULT '',
            recommendations TEXT NOT NULL DEFAULT '',
            FOREIGN KEY (animal_id) REFERENCES animals(id),
            FOREIGN KEY (doctor_id) REFERENCES doctors(id)
        );

        CREATE TABLE IF NOT EXISTS visit_positions (
            id INTEGER PRIMARY KEY,
            visit_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            price INTEGER NOT NULL CHECK (price >= 0),
            FOREIGN KEY (visit_id) REFERENCES visits(id),
            FOREIGN KEY (service_id) REFERENCES services(id)
        );
    """)

def save_owner(owner):
    connection = get_connection()
    try:
        cursor = connection.execute("""
               INSERT INTO owners (name, surname, email, phone_number)
               VALUES (?, ?, ?, ?)
           """, (
            owner.name,
            owner.surname,
            owner.email,
            owner.phone_number
        ))

        connection.commit()
        owner.id = cursor.lastrowid
    finally:
        connection.close()

def get_owners():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, name, surname, email, phone_number
            FROM owners
            ORDER BY id
        """)
        return cursor.fetchall()
    finally:
        connection.close()

def save_animal(animal):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO animals (
                name, kind, breed, date_of_birth, gender, owner_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            animal.name,
            animal.kind,
            animal.breed,
            animal.date_of_birth,
            animal.gender,
            animal.owner_id
        ))

        connection.commit()
        animal.id = cursor.lastrowid
    finally:
        connection.close()

def get_animals():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, name, kind, breed, date_of_birth, gender, owner_id
            FROM animals
            ORDER BY id
        """)
        return cursor.fetchall()
    finally:
        connection.close()

def save_doctor(doctor):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO doctors (name, surname, pwz_number)
            VALUES (?, ?, ?)
        """, (
            doctor.name,
            doctor.surname,
            doctor.pwz_number
        ))

        connection.commit()
        doctor.id = cursor.lastrowid
    finally:
        connection.close()

def get_doctors():
    connection = get_connection()
    try:
        cursor = connection.execute("""
               SELECT id, name, surname, pwz_number
               FROM doctors
               ORDER BY id
                                       """)
        return cursor.fetchall()
    finally:
        connection.close()

def save_service(service):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO services (name, price)
            VALUES (?, ?)
        """, (service.name, service.price))

        connection.commit()
        service.id = cursor.lastrowid
    finally:
        connection.close()


def get_services():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, name, price
            FROM services
            ORDER BY id
        """)
        return cursor.fetchall()
    finally:
        connection.close()

def save_visit(visit):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            INSERT INTO visits (
                animal_id, doctor_id, date_time,
                status, diagnosis, recommendations
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            visit.animal_id,
            visit.doctor_id,
            visit.date_time.isoformat(sep=" "),
            visit.status,
            visit.diagnosis,
            visit.recommendations
        ))

        connection.commit()
        visit.id = cursor.lastrowid
    finally:
        connection.close()


def get_visits():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, animal_id, doctor_id, date_time,
                   status, diagnosis, recommendations
            FROM visits
            ORDER BY date_time
        """)
        return cursor.fetchall()
    finally:
        connection.close()