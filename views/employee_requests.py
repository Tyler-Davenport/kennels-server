# views/employee_requests.py

# Import the Employee class from the models package
from models import Employee

# Replaced dictionaries with Employee objects for better structure and future scalability
EMPLOYEES = [
    Employee(1, "Jenna Solis", 2)
]

# Function to get all employees
def get_all_employees():
    # Convert each Employee object to a dictionary before returning
    return [employee.__dict__ for employee in EMPLOYEES]

# Function with a single parameter to get one employee
def get_single_employee(id):
    requested_employee = None
    for employee in EMPLOYEES:
        # Use object property instead of dictionary key
        if employee.id == id:
            requested_employee = employee
    # Return dictionary version of the object
    return requested_employee.__dict__ if requested_employee else None

# Function to create a new employee
def create_employee(employee_data):
    # Get the last employee's ID and increment by 1
    max_id = EMPLOYEES[-1].id
    new_id = max_id + 1

    # Create a new Employee object from the incoming data
    new_employee = Employee(new_id, employee_data["name"])

    # Add the new object to the list
    EMPLOYEES.append(new_employee)

    # Return the object as a dictionary
    return new_employee.__dict__

# Function to delete an employee by ID
def delete_employee(id):
    employee_index = -1

    for index, employee in enumerate(EMPLOYEES):
        # Check ID using object property
        if employee.id == id:
            employee_index = index

    # If employee was found, remove from list
    if employee_index >= 0:
        EMPLOYEES.pop(employee_index)

# Function to update an employee's data
def update_employee(id, new_employee_data):
    for index, employee in enumerate(EMPLOYEES):
        if employee.id == id:
            # Replace the existing object with a new one
            EMPLOYEES[index] = Employee(id, new_employee_data["name"])
            break
