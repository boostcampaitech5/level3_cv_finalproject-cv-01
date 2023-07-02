import socket
import json
# IP = '127.0.0.1'
IP = '118.67.132.167'
PORT = 30012
ADDR = (IP,PORT)
def connect(ADDR):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        total_msg = ""
        client.connect(ADDR)
        
        client.send(json.dumps({'a':1}).encode())
        while True:
            msg = client.recv(1024)
            if len(msg) == 0:
                break
            total_msg += msg.decode()        
    print(total_msg)
        

def get_client_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def connect_with_server(client,data,data_encode_func=None):
    client.connect(ADDR)
    if data_encode_func:
        data = data_encode_func(data)
    data = len_packet(data)+data

    client.sendall(data)
    total_msg = ''
    

    total_len = int(client.recv(16).decode()[4:])
    print('total_len:',total_len)
    while total_len>0:
        msg = client.recv(1024)
        total_len -= len(msg)
        total_msg += msg.decode()
    print('recieve_len:',len(total_msg))
    print(total_msg)
    client.close()


import cv2 
import numpy as np
def img_encode_func(img_data):
    retval, encode_data = cv2.imencode('.webp', img_data, [cv2.IMWRITE_WEBP_QUALITY,100])
    encode_data = encode_data.tostring()
    print(retval,type(encode_data))
    return encode_data

def len_packet(data):
    len_data = f'len:{len(data):<12}'.encode()
    return len_data
# len_packet(img_encode_func(cv2.imread('./sample_img.jpg')))
# connect(ADDR)
connect_with_server(get_client_socket(),cv2.imread('./sample_img.jpg',cv2.IMREAD_COLOR),img_encode_func)
