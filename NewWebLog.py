import http.server
import socketserver
import cgi

users = {'user1': {'username': 'user1', 'password': 'password1'}}

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('login.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            form_data = cgi.parse_qs(post_data)

            username = form_data.get('username', [''])[0]
            password = form_data.get('password', [''])[0]

            user = users.get(username)

            if user and user['password'] == password:
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Login successful! Welcome to the Dashboard.')
            else:
                self.send_response(401)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'Login failed. Please check your username and password.')
        else:
            super().do_POST()

if __name__ == "__main__":
    PORT = 8000

    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Serving on port {PORT}")
        httpd.serve_forever()

print("hoppan")