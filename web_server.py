from http.server import BaseHTTPRequestHandler, HTTPServer
import os

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, Render!")

def run(server_class=HTTPServer, handler_class=SimpleHandler):
    port = int(os.environ.get('PORT', 10000))  # Renderが提供するポート番号を使用
    server_address = ('0.0.0.0', port)  # 0.0.0.0にバインド
    httpd = server_class(server_address, handler_class)
    print(f'Starting httpd server on port {port}')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
