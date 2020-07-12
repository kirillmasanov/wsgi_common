import json
import socket

HOST = 'localhost'  # or '' to listen on any interface
PORT = 8080  # listen on port 8080
MAX_SIZE = 1024


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    return key, value


def parse_http(data):
    request_line, *header_lines = data.split('\r\n')
    method, path, protocol = request_line.split()
    headers = dict(
        parse_header_line(line)
        for line in header_lines
    )
    return {
        'method': method,
        'path': path,
        'protocol': protocol,
        'headers': headers,
    }


def process_request(data):
    # print(json.dumps(request, indent=4))
    return f'Hello {request["path"]}'


def prepare_response(response):
    content_length = len(response)
    response_headers = '\r\n'.join([
        'HTTP/1.1 200 OK',
        f'Content-Length: {content_length}',
        'Content-Type: text/html',
        ])
    return response_headers


with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        sock, addr = s.accept()
        with sock:
            # print('Address info:', addr)
            request_data = sock.recv(MAX_SIZE).decode('utf-8').strip()
            request = parse_http(request_data)
            response = process_request(request)
            http_response = prepare_response(response)
            print(http_response)
            sock.sendall(http_response.encode('utf-8'))
            sock.sendall('\r\n\n'.encode('utf-8'))
            sock.sendall(response.encode('utf-8'))
