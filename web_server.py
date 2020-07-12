import socket

HOST = 'localhost'  # or '' to listen on any interface
PORT = 8080  # listen on port 8080
MAX_SIZE = 1024
CRLF = '\r\n'


def parse_header_line(line):
    key, value = line.split(':', maxsplit=1)
    return format_header_key(key), value.strip()


def format_header_key(key):
    return 'HTTP_' + key.upper().replace('-', '_').replace(' ', '_')


def parse_http(data):
    request_line, *header_lines = data.split(CRLF)
    method, path, protocol = request_line.split()
    headers = dict(
        parse_header_line(line)
        for line in header_lines
    )
    return {
        'PATH_INFO': path,
        'REQUEST_METHOD': method,
        'SERVER_PROTOCOL': protocol,
        **headers,
    }


def application(environ, start_response):
    path = environ['PATH_INFO']
    response = process_request(path)
    start_response('200 OK', [
        ('Content-Length', str(len(response))),
        ('Content-Type', 'text/html'),
    ])
    return [response.encode('utf-8')]


def process_request(path):
    return f'Hello {path}'


with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        sock, addr = s.accept()
        with sock:
            print('Address info:', addr)
            request_data = sock.recv(MAX_SIZE).decode('utf-8').strip()
            environ = parse_http(request_data)

            # Define a callback for beginning the response
            def start_response(status, headers):
                # Send the status
                sock.sendall(f'HTTP1.1 {status}{CRLF}'.encode('utf-8'))

                # Send each header
                for (key, value) in headers:
                    sock.sendall(f'{key}: {value}{CRLF}'.encode('utf-8'))

                # Send an extra blank line before the response body
                sock.sendall('\r\n'.encode('utf-8'))


            # Run the application code
            response_chunks = application(environ, start_response)

            # Send the response body
            for chunk in response_chunks:
                sock.sendall(chunk)
