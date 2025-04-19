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
    # Variable to hold the found animal, if it exists
    requested_animal = None

    # Iterate the ANIMALS list above. Very similar to the
    # for..of loops you used in JavaScript.
    for animal in ANIMALS:
        # Now that animal is an object, we access attributes using dot notation
        if animal.id == id:
            requested_animal = animal

    # Convert the object to a dictionary before returning
    return requested_animal.__dict__ if requested_animal else None


def get_all_animals():
    # Return list of all animal objects converted to dictionaries
    return [animal.__dict__ for animal in ANIMALS]


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
