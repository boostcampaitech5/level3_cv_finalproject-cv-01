import socket
import time
import json
import numpy as np
import cv2
IP = ''
PORT = 30012
ADDR = (IP,PORT)
sample_result = [{'class': 'taco',
                 'recipe': ['crab', 'cheese','lemon']}]
sample_result = json.dumps(sample_result)
def connect(ADDR):  
    total_msg = b''
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        print('start')
        server.bind(ADDR)
        print('bind')
        server.listen()
        print('listen')
        
        while True:
            client_sock, client_addr = server.accept()
            
            msg = client_sock.recv(16).decode()
            client_sock.recv(16)
            print('total_len',int(msg[4:]))
            total_len = int(msg[4:])
            while total_len >0:
                msg = client_sock.recv(1024)
                
                total_msg += msg
                total_len -= len(msg)
            
            print('send_result')
            # decode_img = cv2.imdecode(np.frombuffer(total_msg,np.uint8),cv2.IMREAD_COLOR)
            # cv2.imwrite('./image2.jpg',decode_img) 
            client_sock.sendall(len_packet(sample_result)+'1111111111111111'.encode()+sample_result.encode())
            client_sock.close()

def len_packet(data):
    len_data = f'len:{len(data):<12}'.encode()
    return len_data


connect(ADDR)