import socket
import json
import cv2 
import numpy as np
# IP = '127.0.0.1'
# IP = '118.67.132.167'
# PORT = 30012
IP = '101.101.208.43'
PORT = 30010
ADDR = (IP,PORT)
def connect(ADDR):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        total_msg = ""
        client.connect(ADDR)
        
        client.send(json.dumps({'a':1}).encode())
        while True:
            msg = client.recv(1024)
            if not msg:
                break
            total_msg += msg.decode()        
    print(total_msg)
        

def get_client_socket():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return client

def len_packet(data):
    len_data = f'len:{len(data):<12}'.encode()
    return len_data

def img_encode_func(img_data):
    retval, encode_data = cv2.imencode('.webp', img_data, [cv2.IMWRITE_WEBP_QUALITY,100])
    encode_data = encode_data.tobytes()

    # print(retval,type(encode_data))
    return encode_data

def connect_with_server(data,data_encode_func=img_encode_func):
    client = get_client_socket()
    client.settimeout(10)
    client.connect(ADDR)
    if data_encode_func:
        data = data_encode_func(data)

    data = len_packet(data)+data

    # data = data

    client.sendall(data)
    total_msg = ''

    ## length packet이 있을 경우
    total_len = int(client.recv(16).decode()[4:])
    print('total_len:',total_len)
    while total_len>0:
        msg = client.recv(1024)
        total_len -= len(msg)
        total_msg += msg.decode()

    ## length packet이 없을 경우
    # while True:
    #     print(client,'f')
    #     msg = client.recv(1024)
    #     total_msg += msg.decode()
    #     print(len(msg))
        
    #     if not msg:
    #         print('break')
    #         break

    print('recieve_len:',len(total_msg))
    print(total_msg)
    client.close()
    return total_msg





# len_packet(img_encode_func(cv2.imread('./sample_img.jpg')))
# connect(ADDR)
if __name__ == '__main__':
    connect_with_server(cv2.imread('./sample_img.jpg',cv2.IMREAD_COLOR),img_encode_func)
