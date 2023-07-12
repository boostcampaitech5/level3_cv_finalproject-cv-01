import socket
import json
import torch
import json
import cv2
import torch.nn.functional as F
import numpy as np
import albumentations as A

PATH = '/opt/ml/server/pthfile/ResNet18_best.pth'
HOST = ''
PORT = 30010
THRESHOLD = 0.3

def make_head(data):
	tem = 'len' + ' ' + str(len(data))
	return '%-16s' % tem

#모델 로드
model = torch.load(PATH).cuda()
model.eval()

#Resize, Normalize
transforms = A.Compose([
	A.Resize(224, 224),
	A.Normalize()
])

with open('/opt/ml/server/order/order.json') as file:
	classes = json.load(file)

with open('/opt/ml/server/DB/DB.json') as file:
	recipes = json.load(file)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))

server_socket.listen(1)
print("waiting...")

while True:
	client_socket, client_address = server_socket.accept()
	client_socket.settimeout(10)
	print("connected : ", client_address)
	
	head = client_socket.recv(32).decode().replace(':', ' ').split()
	length = int(head[1])
	command = head[3]
	
	data = b''
	limit = 0
	while length:
		tem = client_socket.recv(1024)
		data = data + tem
		length = length - len(tem)
		limit = limit + 1
		if limit == 1000:
			raise
	
	if command == 'image':
		data = np.frombuffer(data, dtype=np.uint8)#1차원 배열
		image = cv2.imdecode(data, cv2.IMREAD_COLOR)#2차원 배열
		
		#???
		inputs = {'image' : image}
		transformed = transforms(**inputs)
		image = transformed['image']
		
		#Resize, Normalize
		width = image.shape[0]
		height = image.shape[1]
		worh = min(width, height)
		transforms = A.Compose([
			A.CenterCrop(worh, worh),
			A.Resize(224, 224),
			A.Normalize()
		])
		
		#모델에 넣기 위해서 이미지를 처리한다.
		image = np.transpose(image, (2, 0, 1))
		image = np.expand_dims(image, axis=0)
		image = torch.tensor(image).cuda()
		
		output = model(image)
		output = F.softmax(output[0], dim=0)
		
		#출력을 정리해서 dict로 만든다.
		arr = [(value, index) for index, value in enumerate(output)]#가장 큰 3개의 인덱스를 얻기 위해서 arr를 만든다.
		arr.sort()
		arr.reverse()
		result = []
		for i in range(3):
			index = arr[i][1]
			dish = classes[str(index)]
			if arr[i][0] > THRESHOLD:
				valid = True
			else:
				valid = False
			dictionary = {'class' : dish, 'recipe' : recipes[dish], 'valid' : valid}
			result.append(dictionary)
	
	result = json.dumps(result)#dict to str
	
	client_socket.sendall((packet.make_head(result)+packet.make_head([0])+result).encode())
	
	client_socket.close()

server_socket.close()