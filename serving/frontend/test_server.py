import socket
import time
import json
IP = ''
PORT = 30012
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
            
            msg = client_sock.recv(16).decode()
            print('total_len',int(msg[4:]))
            total_len = int(msg[4:])
            while total_len >0:
                msg = client_sock.recv(1024)
                total_len -= len(msg)

            print('send_result')    
            client_sock.sendall(len_packet(sample_result)+sample_result.encode())
            client_sock.close()
            

def len_packet(data):
    len_data = f'len:{len(data):<12}'.encode()
    return len_data


connect(ADDR)