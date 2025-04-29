import sqlite3
import json
# views/employee_requests.py

# Import the Employee class from the models package
from models import Employee
from models import Location

# Replaced dictionaries with Employee objects for better structure and future scalability
EMPLOYEES = [
    Employee(1, "Jenna Solis", "7943 harrow drive", 2)
]

# Function to get all employees
def get_all_employees():
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id,
            l.id,
            l.name location_name,
            l.address location_address
        FROM employee e
             JOIN Location l ON l.id = e.location_id
        """)

        employees = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            
            location = Location(row['location_id'], row['location_name'], row['location_address'])
            
            employee.location = location.__dict__
            
            employees.append(employee.__dict__)
            
    return employees
        

# Function with a single parameter to get one employee
def get_single_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, ( id, ))

        data = db_cursor.fetchone()

        if data:
            employee = Employee(data['id'], data['name'], data['address'], data['location_id'])
            return employee.__dict__
        else:
            return {}

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
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
        DELETE FROM employee
        WHERE id = ?
        """, (id,))

# Function to update an employee's data
def update_employee(id, new_employee_data):
    for index, employee in enumerate(EMPLOYEES):
        if employee.id == id:
            # Replace the existing object with a new one
            EMPLOYEES[index] = Employee(id, new_employee_data["name"])
            break

def get_employee_by_location(location_id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()
        
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM Employee e
        WHERE e.location_id = ?                     
        """, (location_id,))
        
        employees = []
        dataset = db_cursor.fetchall()
        
        for row in dataset:
            employee = Employee(row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)
            
    return employees