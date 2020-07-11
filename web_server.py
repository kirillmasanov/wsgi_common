import socket

HOST = 'localhost'  # or '' to listen on any interface
PORT = 8080  # listen on port 8080
MAX_SIZE = 1024


def process_request(data):
    print('Received data:\n', data.decode('UTF-8'), sep='')
    return 'Hello World!'


with socket.socket() as s:
    s.bind((HOST, PORT))
    s.listen(1)
    while True:
        sock, addr = s.accept()
        with sock:
            print('Address info:', addr)
            request = sock.recv(MAX_SIZE)
            response = process_request(request)
            sock.sendall(response.encode('utf-8'))
