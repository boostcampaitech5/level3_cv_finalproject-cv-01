import socket
import time
import json
IP = ''
PORT = 2278
ADDR = (IP,PORT)
sample_result = {'class': 'tacco',
                 'recipe': ['vegitable', 'meet','sc']}
sample_result = json.dumps(sample_result)
def connect(ADDR):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        print('start')
        server.bind(ADDR)
        print('bind')
        server.listen()
        print('listen')
        while True:
            client_sock, client_addr = server.accept()
            msg = client_sock.recv(1024)
            print(msg,client_addr)
            time.sleep(0.5)
            client_sock.sendall(sample_result.encode())
            client_sock.close()

connect(ADDR)