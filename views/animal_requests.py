import sqlite3
import json
# Import the Animal class from the models package
from models import Animal

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
            a.customer_id
        FROM animal a
        """)

        animals = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            animal = Animal(row['id'], row['name'], row['breed'],
                            row['status'], row['location_id'],
                            row['customer_id'])
            animals.append(animal.__dict__)  # Converts object to dictionary

    return animals



def create_animal(animal_data):
    # Get the ID of the last animal in the list and increment it
    max_id = ANIMALS[-1].id
    new_id = max_id + 1

    # Create a new Animal instance from the dictionary data provided
    new_animal = Animal(
        new_id,
        animal_data["name"],
        animal_data["species"],
        animal_data["status"],
        animal_data["locationId"],
        animal_data["customerId"]
    )

    # Append the object to the list
    ANIMALS.append(new_animal)

    # Return a dictionary representation of the new object
    return new_animal.__dict__


def delete_animal(id):
    animal_index = -1

    # Iterate the list to find the index of the animal object with the matching ID
    for index, animal in enumerate(ANIMALS):
        if animal.id == id:
            animal_index = index

    # If the animal was found, remove it using pop
    if animal_index >= 0:
        ANIMALS.pop(animal_index)


def update_animal(id, new_animal_data):
    # Iterate the ANIMALS list, but use enumerate() so that
    # you can access the index value of each item.
    for index, animal in enumerate(ANIMALS):
        if animal.id == id:
            # Replace the existing animal with a new Animal object built from new data
            ANIMALS[index] = Animal(
                id,
                new_animal_data["name"],
                new_animal_data["species"],
                new_animal_data["status"],
                new_animal_data["locationId"],
                new_animal_data["customerId"]
            )
            break
