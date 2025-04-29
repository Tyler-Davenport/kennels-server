import sqlite3
import json
# views/location_requests.py

# Import the Location class from the models package
from models import Location

# Replaced dictionaries with Location objects for better structure and future scalability
LOCATIONS = [
    Location(1, "Nashville North", "8422 Johnson Pike"),
    Location(2, "Nashville South", "209 Emory Drive")
]

# Function with a single parameter to get a single location
# Function with a single parameter to get a single location
def get_single_location(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # First, get the Location info
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id,))
        
        data = db_cursor.fetchone()

        if data:
            location = Location(data['id'], data['name'], data['address'])
            location_dict = location.__dict__

            # Now get all Employees at this Location
            db_cursor.execute("""
            SELECT
                e.id,
                e.name,
                e.address,
                e.location_id
            FROM employee e
            WHERE e.location_id = ?
            """, (id,))
            
            employees = []
            employee_dataset = db_cursor.fetchall()

            for row in employee_dataset:
                employees.append({
                    "id": row["id"],
                    "name": row["name"],
                    "address": row["address"],
                    "location_id": row["location_id"]
                })

            # Now get all Animals at this Location
            db_cursor.execute("""
            SELECT
                a.id,
                a.name,
                a.breed,
                a.status,
                a.location_id,
                a.customer_id
            FROM animal a
            WHERE a.location_id = ?
            """, (id,))
            
            animals = []
            animal_dataset = db_cursor.fetchall()

            for row in animal_dataset:
                animals.append({
                    "id": row["id"],
                    "name": row["name"],
                    "breed": row["breed"],
                    "status": row["status"],
                    "location_id": row["location_id"],
                    "customer_id": row["customer_id"]
                })

            # Attach employees and animals to the location dictionary
            location_dict["employees"] = employees
            location_dict["animals"] = animals

            return location_dict
        else:
            return {}


# Function to get all locations
def get_all_locations():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        locations = []
        dataset = db_cursor.fetchall()

        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__)

    return locations

# Function to create a new location
def create_location(location_data):
    # Get the last location's ID and increment by 1
    max_id = LOCATIONS[-1].id
    new_id = max_id + 1

    # Create a new Location object from the incoming data
    new_location = Location(new_id, location_data["name"], location_data["address"])

    # Add the new object to the list
    LOCATIONS.append(new_location)

    # Return the object as a dictionary
    return new_location.__dict__

# Function to delete a location by ID
def delete_location(id):
    location_index = -1

    for index, location in enumerate(LOCATIONS):
        # Check ID using object property
        if location.id == id:
            location_index = index

    # If location was found, remove from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)

# Function to update a location's data
def update_location(id, new_location_data):
    for index, location in enumerate(LOCATIONS):
        if location.id == id:
            # Replace the existing object with a new one
            LOCATIONS[index] = Location(id, new_location_data["name"], new_location_data["address"])
            break
