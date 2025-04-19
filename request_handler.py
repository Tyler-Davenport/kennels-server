from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (
    get_all_animals, get_single_animal,
    get_all_locations, get_single_location,
    get_all_employees, get_single_employee,
    get_all_customers, get_single_customer,
    create_customer, create_animal,
    create_employee, create_location,
    delete_location, delete_animal,
    delete_customer, delete_employee,
    update_customer, update_animal,
    update_employee, update_location
)
import json

class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def parse_url(self, path):
        """Parses the URL into resource and optional ID"""
        path_params = path.split("/")
        resource = path_params[1]
        id = None

        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass

        return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin headers on the response"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers for pre-flight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handles GET requests to the server"""
        self._set_headers(200)
        response = {}

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            if id is not None:
                response = get_single_animal(id)
            else:
                response = get_all_animals()

        elif resource == "locations":
            if id is not None:
                response = get_single_location(id)
            else:
                response = get_all_locations()

        elif resource == "employees":
            if id is not None:
                response = get_single_employee(id)
            else:
                response = get_all_employees()

        elif resource == "customers":
            if id is not None:
                response = get_single_customer(id)
            else:
                response = get_all_customers()

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        new_item = None

        if resource == "animals":
            new_item = create_animal(post_body)
        elif resource == "locations":
            new_item = create_location(post_body)
        elif resource == "employees":
            new_item = create_employee(post_body)
        elif resource == "customers":
            new_item = create_customer(post_body)

        self.wfile.write(json.dumps(new_item).encode())

    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            update_animal(id, post_body)
        elif resource == "locations":
            update_location(id, post_body)
        elif resource == "employees":
            update_employee(id, post_body)
        elif resource == "customers":
            update_customer(id, post_body)

        self.wfile.write("".encode())

        
    def do_DELETE(self):
        """Handles DELETE requests to the server"""
        self._set_headers(204)  # 204 means success, but no content to return
        (resource, id) = self.parse_url(self.path)

        if resource == "animals":
            delete_animal(id)
        elif resource == "locations":
            delete_location(id)
        elif resource == "employees":
            delete_employee(id)
        elif resource == "customers":
            delete_customer(id)

        self.wfile.write("".encode())  # Send an empty response


def main():
    """Starts the server on port 8088 using the HandleRequests class"""
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
