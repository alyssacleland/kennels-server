from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_animals, get_single_animal, get_all_locations, get_single_location, get_all_employees, get_single_employee, get_single_customer, get_all_customers, create_animal, create_employee, create_customer, delete_animal, delete_location, delete_employee, delete_customer, update_animal, update_customer, update_employee, update_location, get_customer_by_email, get_animal_by_location_id, get_employee_by_location_id, get_animal_by_status
import json
from urllib.parse import urlparse, parse_qs


# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    """

    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        # check if ufrl has a query string
        if parsed_url.query:
            # parse the query string into a DICTIONARY where keys are parameter names and values are the property values (after the = sign). also, apparently....??values are always lists (bc a query param can appear more than once) idk about that
            query = parse_qs(parsed_url.query)
            # return the resource (we got above at start of this method) and the parsed query dictionary
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            (resource, id) = parsed

            # It's an if..else statement
            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)

                else:
                    response = get_all_animals()

            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)

                else:
                    response = get_all_locations()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)

                else:
                    response = get_all_employees()
            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)

                else:
                    response = get_all_customers()

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                # [0] bc email will be in list format (b/c parse_qs does it like that)
                response = get_customer_by_email(query['email'][0])

            # see if the query dictionary has a location key and resource is animals
            if query.get('location_id') and resource == 'animals':
                response = get_animal_by_location_id(query['location_id'][0])

            # if resource is employees and thye have a location_id
            if query.get('location_id') and resource == 'employees':
                response = get_employee_by_location_id(query['location_id'][0])

            # if resource is animals and they have a status
            if query.get('status') and resource == 'animals':
                response = get_animal_by_status(query['status'][0])

        # turn dict into json string to send
        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.

    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        # TODO: Understand this line better:
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        # unpack tuple. tuple is on the right. the parenthesis in the first part are kinda misleading.
        (resource, id) = self.parse_url(self.path)

    ####### ANIMAL! #######
        # Initialize new animal
        new_animal = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create_animal
        # function next.
        if resource == "animals":
            new_animal = create_animal(post_body)

            # Encode the new animal and send in response
            self.wfile.write(json.dumps(new_animal).encode())

    ####### EMPLOYEE! #######
        new_employee = None
        if resource == "employees":
            new_employee = create_employee(post_body)
            self.wfile.write(json.dumps(new_employee).encode())

    ####### CUSTOMER! #######
        new_customer = None
        if resource == "customers":
            new_customer = create_customer(post_body)
            self.wfile.write(json.dumps(new_customer).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any PUT request.

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # set default value of success
        success = False

        if resource == "animals":
            # will return either True or False from `update_animal`
            success = update_animal(id, post_body)
        # rest of the elif's TODO:

        # handle the value of success
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        if resource == "locations":
            delete_location(id)
        if resource == "employees":
            delete_employee(id)
        if resource == "customers":
            delete_customer(id)

        # Encode the new animal and send in response
        self.wfile.write("".encode())


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


# A: If this file is being run directly (not imported into another file), run the main() function.
if __name__ == "__main__":
    main()
