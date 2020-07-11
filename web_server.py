import socket

with socket.socket() as s:
    s.bind(('localhost', 8080))
    s.listen(1)
    sock, addr = s.accept()
    with sock:
        print('Address info:', addr)
        data = sock.recv(1024)
        print('Received data:\n', data.decode('UTF-8'), sep='')
        sock.sendall(b'Hello World!')
