# views/location_requests.py

# Import the Location class from the models package
from models import Location

# Replaced dictionaries with Location objects for better structure and future scalability
LOCATIONS = [
    Location(1, "Nashville North", "8422 Johnson Pike"),
    Location(2, "Nashville South", "209 Emory Drive")
]

# Function with a single parameter to get a single location
def get_single_location(id):
    requested_location = None
    for location in LOCATIONS:
        # Use object property instead of dictionary key
        if location.id == id:
            requested_location = location
    # Return dictionary version of the object
    return requested_location.__dict__ if requested_location else None

# Function to get all locations
def get_all_locations():
    # Convert each Location object to a dictionary before returning
    return [location.__dict__ for location in LOCATIONS]

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
