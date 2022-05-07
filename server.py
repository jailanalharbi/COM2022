
import cv2, imutils, socket 
import numpy as np
import time
import base64
import threading

BUFF_SIZE = 65536

CLIENT = []

# User dictionary 
USERS = {
    'Jailan':'1234',
    'Noor': '1234',
    'Lily': '1234',
    'Faye': '1234',
}

# Server create 
server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 9995
socket_address = ('0.0.0.0',port)


# Bind server and Listen
server_socket.bind(socket_address)
print('Listening at:',socket_address)


# Video initialisation 
vid = cv2.VideoCapture("cats.mp4")  # 0 for camera, "cats.mp4" for video



# Handling client 
def recieveFunction():

    while True:
            msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
            print('GOT connection from ',client_addr)
            message = base64.b64decode(msg,' /').decode('ascii')

           
            message = message.split('::')

            if message[0] == 'LOGIN':
                print('LOGIN')

                if len(CLIENT) >= 4:
                    text = "MESSAGE::FULL"
                    server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                else:
                    
                    if message[1] in CLIENT:
                        text = "MESSAGE::EXIST"
                        server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                        print('Already logged in')

                    else:

                        if message[1] in USERS.keys() :

                            if message[2] == USERS[message[1]]:
                                text = "MESSAGE::AUTHORIZE"

                                server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                                print('password match')
                                CLIENT.append(message[1])
                                x = threading.Thread(target=streamFunction, args=(client_addr[0],client_addr[1],message[1]))
                                x.start()
                            else:
                                text = "MESSAGE::UNAUTHORIZE"

                                server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                            
                                print('pass no')
                        else:
                            text = "MESSAGE::UNAUTHORIZE"

                            server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                            
                            print('No')
            elif message[0] == 'QUIT':
                CLIENT.remove(message[1])
                print(f'{message[1]} quit the server')
            elif message[0] == 'RTT':
                pass
            else:
                print(f'Unrecognized format of packet recieved: ',client_addr )

# Stream video 
def streamFunction(client_addr1, e, username):
    try:
        client_addr= (client_addr1,e)
        username = username
        WIDTH=200
        fps,st,frames_to_count,cnt = (0,0,20,0)
        while(vid.isOpened()):

            while username in CLIENT:
                _,frame = vid.read()
                frame = imutils.resize(frame,width=WIDTH)
                encoded,buffer = cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,80])

                packet = 'VIDEO::'
                for i in buffer:
                    packet += f'{i} '
                    
                        

                message = base64.b64encode(packet.encode('ascii'))
                server_socket.sendto(message,client_addr)

            
            print(f'Stop broadcasting video to {username}')
            break
    except AttributeError :
        text = "FINISH::"
        server_socket.sendto(base64.b64encode(text.encode('ascii')),client_addr)
                            
        print('Video Finish')

recieveFunction()