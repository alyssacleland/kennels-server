import json
import sqlite3
from models import Location, Employee


LOCATIONS = [
    {
        "id": 1,
        "name": "Nashville North",
        "address": "8422 Johnson Pike"
    },
    {
        "id": 2,
        "name": "Nashville South",
        "address": "209 Emory Drive"
    }
]


def get_all_locations():

    #  open the database
    with sqlite3.connect("./kennel.sqlite3") as conn:

        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # ask for some rows
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        """)

        locations = []

        # actually retrieve data to python memory
        dataset = db_cursor.fetchall()

        # turn data into objects
        for row in dataset:
            location = Location(row['id'], row['name'], row['address'])
            locations.append(location.__dict__)

    return locations


def get_single_location(id):
    # open database
    with sqlite3.connect("./kennel.sqlite3") as conn:
        conn.row_factory = sqlite3.Row
        db_cursor = conn.cursor()

        # sql query
        db_cursor.execute("""
        SELECT
            l.id,
            l.name,
            l.address
        FROM location l
        WHERE l.id = ?
        """, (id,))

        data = db_cursor.fetchone()

        if data is None:
            return None  # or raise an error, or return {}

        # build location obj
        location = Location(data["id"], data["name"], data["address"])

        # Get employees at this location
        db_cursor.execute("""
            SELECT 
                e.id employee_id, 
                e.name employee_name, 
                e.location_id 
            FROM Employee e
            WHERE location_id = ?
        """, (id,))

        employees = [
            {
                "id": row["employee_id"],
                "name": row["employee_name"],
                "location_id": row["location_id"]
            }
            for row in db_cursor.fetchall()
        ]
        # make a dict
        location_dict = location.__dict__
        # convert each employee into a dict too
        location_dict["employees"] = employees

        # TODO: add animals too

        return location_dict


def delete_location(id):
    # Initial -1 value for location index, in case one isn't found
    location_index = -1

    # Iterate the LOCATIONS list, but use enumerate() so that you
    # can access the index value of each item
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            # Found the location. Store the current index.
            location_index = index

    # If the location was found, use pop(int) to remove it from list
    if location_index >= 0:
        LOCATIONS.pop(location_index)


def update_location(id, new_location):
    for index, location in enumerate(LOCATIONS):
        if location["id"] == id:
            LOCATIONS[index] = new_location
            break
