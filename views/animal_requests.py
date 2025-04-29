import sqlite3
import json
# Import the Animal class from the models package
from models import Animal
from models import Location
from models import Customer

# Instead of using dictionaries, we now store Animal objects
# This provides better structure and easier refactoring later when we add databases

ANIMALS = [
    Animal(1, "Snickers", "Dog", "Admitted", 1, 4),
    Animal(2, "Roman", "Dog", "Admitted", 1, 2),
    Animal(3, "Blue", "Cat", "Admitted", 2, 1)
]

# Function with a single parameter
def get_single_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM animal a
        WHERE a.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        if data:
            animal = Animal(data['id'], data['name'], data['breed'],
                            data['status'], data['location_id'],
                            data['customer_id'])
            return animal.__dict__
        else:
            return {}  # optional: handle "not found" cases



def get_all_animals():
    # establishes connection to database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        # converts to dictionary
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id,
            l.id,
            l.name location_name,
            l.address location_address,
            c.id customer_id,
            c.name customer_name,
            c.address customer_address,
            c.email customer_email,
            c.password customer_password
        FROM Animal a
        JOIN Location l ON l.id = a.location_id
        JOIN Customer c ON c.id = a.customer_id
        """)

        animals = []
        dataset = db_cursor.fetchall()

    for row in dataset:

            # Create an animal instance from the current row
            animal = Animal(row['id'], row['name'], row['breed'], row['status'],
                            row['location_id'], row['customer_id'])

            # Create a Location instance from the current row
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            
            customer = Customer(row['customer_id'],row['customer_name'],row['customer_address'],row['customer_email'],row['customer_password'])

            # Add the dictionary representation of the location to the animal
            animal.location = location.__dict__
            animal.customer = customer.__dict__

            # Add the dictionary representation of the animal to the list
            animals.append(animal.__dict__)

    return animals



import sqlite3

def create_animal(new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        INSERT INTO Animal
            ( name, breed, status, location_id, customer_id )
        VALUES
            ( ?, ?, ?, ?, ? );
        """, (
            new_animal['name'],
            new_animal['breed'],
            new_animal['status'],
            new_animal['locationId'],
            new_animal['customerId'],
        ))

        id = db_cursor.lastrowid
        new_animal['id'] = id

    return new_animal



def delete_animal(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM animal
        WHERE id = ?
        """, (id, ))


def update_animal(id, new_animal):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        UPDATE Animal
            SET
                name = ?,
                breed = ?,
                status = ?,
                location_id = ?,
                customer_id = ?
        WHERE id = ?
        """, (new_animal['name'], new_animal['breed'],
              new_animal['status'], new_animal['locationId'],
              new_animal['customerId'], id))

        rows_affected = db_cursor.rowcount

    # Determine if the update actually happened
    if rows_affected == 0:
        return False  # This triggers a 404 response
    else:
        return True   # This triggers a 204 No Content response


def get_animal_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM Animal a
        WHERE a.location_id = ?                     
        """, (location_id,))
        
        animals = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
            
    return animals

def get_animal_by_status(status):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            a.id,
            a.name,
            a.breed,
            a.status,
            a.location_id,
            a.customer_id
        FROM Animal a
        WHERE a.status = ?                     
        """, (status,))
        
        animals = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'], row['status'], row['location_id'], row['customer_id'])
            animals.append(animal.__dict__)
            
    return animals