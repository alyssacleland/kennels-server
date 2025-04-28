import sqlite3
import json
from models import Employee


EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]


def get_all_employees():

    #  open the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # ask for some rows
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        """)

        employees = []

        # actually retrieve data to python memory
        dataset = db_cursor.fetchall()

        # turn data into objects
        for row in dataset:
            employee = Employee(
                row['id'], row['name'], row['address'], row['location_id'])
            employees.append(employee.__dict__)

    return employees


def get_single_employee(id):
    # open database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # sql query
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.id = ?
        """, (id,))

        # fetch result into python memory
        data = db_cursor.fetchone()

        # build python obj
        employee = Employee(data['id'], data['name'],
                            data['address'], data['location_id'])
        return employee.__dict__


def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]  # get id of last employee in list
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee  # this, paired with "self.wfile.write(json.dumps(new_animal).encode())" in request handler, is what outputs the response body (the employee json!) in postman. creating still works without them. w/o this return employee line, it outputs null (bc json dumps in request handler would be receiving None from this by default!). without the line in request handler, postman output would be an empty response body!!!


def delete_employee(id):
    with sqlite3.connect("./kennel.sqlite3") as conn:
        db_cursor = conn.cursor()

        db_cursor.execute("""
                          DELETE FROM employee
                          WHERE id = ?
                          """, (id, ))


def update_employee(id, new_employee):
    for index, employee in enumerate(EMPLOYEES):
        if employee["id"] == id:
            EMPLOYEES[index] = new_employee
            break


def get_employee_by_location_id(location_id):
    # open database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # sql query
        db_cursor.execute("""
        SELECT
            e.id,
            e.name,
            e.address,
            e.location_id
        FROM employee e
        WHERE e.location_id = ?
        """, (location_id,))

        employees = []

        # fetch result into python memory
        data = db_cursor.fetchall()

        for row in data:
            employee = Employee(row['id'], row['name'],
                                row['address'], row['location_id'])
            employees.append(employee.__dict__)
    return employees
