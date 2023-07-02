import socket
import json
IP = '127.0.0.1'
PORT = 2278
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
        

connect(ADDR)