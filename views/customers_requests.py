# views/customer_requests.py

# Import the Customer class from the models package
from models import Customer

# Replaced dictionaries with Customer objects for stronger data structure
CUSTOMERS = [
    Customer(1, "Ryan Tanay")
]

# Function to get all customer objects, returned as dictionaries
def get_all_customers():
    return [customer.__dict__ for customer in CUSTOMERS]

# Function to get a single customer by ID
def get_single_customer(id):
    requested_customer = None
    for customer in CUSTOMERS:
        # Use dot notation to compare object property
        if customer.id == id:
            requested_customer = customer
    # Convert object to dictionary before returning
    return requested_customer.__dict__ if requested_customer else None

# Function to create a new customer
def create_customer(customer_data):
    # Find the last ID and add 1 to assign to the new customer
    max_id = CUSTOMERS[-1].id
    new_id = max_id + 1

    # Create a Customer instance from the incoming dictionary data
    new_customer = Customer(new_id, customer_data["name"])

    # Append new object to the list
    CUSTOMERS.append(new_customer)

    # Return dictionary representation of the object
    return new_customer.__dict__

# Function to delete a customer from the list by ID
def delete_customer(id):
    customer_index = -1

    for index, customer in enumerate(CUSTOMERS):
        # Compare using object property
        if customer.id == id:
            customer_index = index

    # Remove customer by index if found
    if customer_index >= 0:
        CUSTOMERS.pop(customer_index)

# Function to update an existing customer by ID
def update_customer(id, new_customer_data):
    for index, customer in enumerate(CUSTOMERS):
        if customer.id == id:
            # Replace the object with a new one using incoming data
            CUSTOMERS[index] = Customer(id, new_customer_data["name"])
            break
