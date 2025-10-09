import json
import socket
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)  # змінюємо робочу директорію на ту, де main.py
print("[DEBUG] Changed working directory to:", os.getcwd())

# --- Налаштування портів і шляхів ---
HOST = 'localhost'
HTTP_PORT = 3000
SOCKET_PORT = 5000
STORAGE_DIR = 'storage'
DATA_FILE = os.path.join(STORAGE_DIR, 'data.json')

# якщо немає папки storage — створюємо
os.makedirs(STORAGE_DIR, exist_ok=True)


# --- UDP Socket сервер ---
# приймає дані з веб-форми, зберігає в data.json
def socket_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((HOST, SOCKET_PORT))
    print(f"[OK] Socket сервер запущено на порту {SOCKET_PORT}")

    while True:
        data, addr = sock.recvfrom(1024)
        message = data.decode('utf-8')

        try:
            message_dict = json.loads(message)
        except json.JSONDecodeError:
            continue  # якщо прийшло щось не JSON — пропускаємо

        timestamp = str(datetime.now())

        # читаємо існуючий файл або створюємо новий
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                try:
                    all_data = json.load(f)
                except json.JSONDecodeError:
                    all_data = {}
        else:
            all_data = {}

        # додаємо новий запис
        all_data[timestamp] = message_dict

        # перезаписуємо файл
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_data, f, ensure_ascii=False, indent=2)


# --- HTTP сервер ---
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path).path

        # маршрути до сторінок
        routes = {
            '/': 'index.html',
            '/index.html': 'index.html',
            '/message.html': 'message.html'
        }

        if parsed_path in routes:
            self.send_html(routes[parsed_path])
        elif parsed_path == '/style.css':
            self.send_static('style.css', 'text/css')
        elif parsed_path == '/logo.png':
            self.send_static('logo.png', 'image/png')
        else:
            # якщо сторінки не існує → показуємо 404
            self.send_html('error.html', 404)

    def do_POST(self):
        # Лог для зручності
        print(f"[POST] Отримано запит на {self.path}")

        # Якщо форма відправлена з /message
        if self.path.startswith('/message'):
            try:
                # Зчитуємо дані з форми
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode('utf-8')

                # Парсимо дані
                params = parse_qs(post_data)
                username = params.get('username', [''])[0]
                message = params.get('message', [''])[0]

                print(f"[OK] Отримано від користувача: {username} -> {message}")

                # Відправляємо дані на socket сервер
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                data = json.dumps({'username': username, 'message': message})
                sock.sendto(data.encode('utf-8'), (HOST, SOCKET_PORT))
                sock.close()

                # Після відправлення — редіректимо на головну
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
            except Exception as e:
                print(f"[ERR] do_POST() помилка: {e}")
                self.send_html('error.html', 500)
        else:
            # Якщо POST не на /message — повертаємо 404
            self.send_html('error.html', 404)

    # відправляє html-файли
    def send_html(self, filename, status=200):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(status)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            # якщо html-файл не знайдено — 404
            if filename != 'error.html':
                self.send_html('error.html', 404)

    # відправляє css або зображення
    def send_static(self, filename, content_type):
        try:
            with open(filename, 'rb') as f:
                content = f.read()
            self.send_response(200)
            self.send_header('Content-type', content_type)
            self.end_headers()
            self.wfile.write(content)
        except FileNotFoundError:
            self.send_html('error.html', 404)


# --- Запуск HTTP сервера ---
def run_http_server():
    httpd = HTTPServer((HOST, HTTP_PORT), SimpleHTTPRequestHandler)
    print(f"[OK] HTTP сервер запущено на порту {HTTP_PORT}")
    httpd.serve_forever()


# --- Основна частина ---
if __name__ == '__main__':
    # якщо message.html немає — створюємо базову форму
    if not os.path.exists('message.html'):
        with open('message.html', 'w', encoding='utf-8') as f:
            f.write('''<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Send message</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="/style.css" />
  </head>
  <body class="container mt-5">
    <h2>Send a Message</h2>
    <form action="/submit" method="post">
      <div class="mb-3">
        <label for="username" class="form-label">Username:</label>
        <input type="text" class="form-control" name="username" required>
      </div>
      <div class="mb-3">
        <label for="message" class="form-label">Message:</label>
        <textarea class="form-control" name="message" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Send</button>
    </form>
  </body>
</html>''')

    # запускаємо socket сервер у фоновому потоці
    thread_socket = threading.Thread(target=socket_server, daemon=True)
    thread_socket.start()

    # запускаємо http сервер
    run_http_server()