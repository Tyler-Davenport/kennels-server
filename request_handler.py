import json
from urllib.parse import urlparse, parse_qs
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
    update_employee, update_location,
    get_customer_by_email, get_animal_by_location,
    get_animal_by_status, get_employee_by_location
)
import json

class HandleRequests(BaseHTTPRequestHandler):
    # Controls the functionality of any GET, PUT, POST, DELETE requests to the server

    def parse_url(self, path):
        # Parses the URL into resource and optional ID
        parsed_url = urlparse(path)
        path_parts = parsed_url.path.split('/')
        resource = path_parts[1]
        
        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)
        
        pk = None
        try:
            pk = int(path_parts[2])
        except (IndexError, ValueError):
            pass
        
        return (resource, pk)

    def _set_headers(self, status):
        # Sets the status code, Content-Type and Access-Control-Allow-Origin headers on the response
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        # Sets the options headers for pre-flight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        # Handles GET requests to the server
        self._set_headers(200)
        response = {}

        parsed = self.parse_url(self.path)

        # If there's NO query string, run the regular logic (your original code)
        if '?' not in self.path:
            (resource, id) = parsed

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

        # If there IS a query string (like ?email=...), handle that separately
        else:
            (resource, query) = parsed

            if resource == "customers":
                if query.get('email'):
                    response = get_customer_by_email(query['email'][0])
                    
            elif resource == "animals":
                if query.get('location_id'):
                    response = get_animal_by_location(int(query["location_id"][0]))
                elif query.get('status'):
                    response = get_animal_by_status(query["status"][0])

            elif resource == "employees":
                if query.get('location_id'):
                    response = get_employee_by_location(int(query["location_id"][0]))
            
            # You can add more query filters here later!
            # Like animals by status, employees by location, etc.

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
