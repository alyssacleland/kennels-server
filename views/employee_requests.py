EMPLOYEES = [
    {
        "id": 1,
        "name": "Jenna Solis"
    }
]


def get_all_employees():
    return EMPLOYEES


def get_single_employee(id):
    requested_employee = None
    for employee in EMPLOYEES:
        if employee["id"] == id:
            requested_employee = employee
    return requested_employee


def create_employee(employee):
    max_id = EMPLOYEES[-1]["id"]  # get id of last employee in list
    new_id = max_id + 1
    employee["id"] = new_id
    EMPLOYEES.append(employee)
    return employee  # this, paired with "self.wfile.write(json.dumps(new_animal).encode())" in request handler, is what outputs the response body (the employee json!) in postman. creating still works without them. w/o this return employee line, it outputs null (bc json dumps in request handler would be receiving None from this by default!). without the line in request handler, postman output would be an empty response body!!!
